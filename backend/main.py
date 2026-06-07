import functions_framework
from flask import jsonify
import pandas as pd
import numpy as np
import joblib
import os
from scipy.optimize import linprog
from google.cloud import bigquery, storage

# =============================================================================
# 1. CONFIGURACIÓN Y CLIENTES CLOUD (Seguridad mediante Variables de Entorno)
# =============================================================================
# Protegemos la topología en el repositorio público usando variables de entorno
TABLA_AUDITORIA = os.getenv("TABLA_AUDITORIA", "tu-proyecto.blue_switch.dataset_semilla")
BUCKET_MODELOS = os.getenv("BUCKET_MODELOS", "tu-bucket-de-modelos")

try:
    bq_client = bigquery.Client()
except Exception as e:
    print(f"⚠️ Aviso: Cliente BQ no inicializado. {e}")
    bq_client = None

# =============================================================================
# 2. CARGA GLOBAL DINÁMICA DE MODELOS
# =============================================================================
cache_modelos = {}

def descargar_modelo_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    ruta_local = os.path.join('/tmp', destination_file_name)
    if not os.path.exists(ruta_local):
        blob.download_to_filename(ruta_local)
    return joblib.load(ruta_local)

def obtener_modelos_nodo(nodo):
    nodo_str = nodo.lower()
    if nodo_str not in cache_modelos:
        cache_modelos[nodo_str] = {
            'ridge': descargar_modelo_gcs(BUCKET_MODELOS, f'{nodo_str}/sinc_kw_ridge_{nodo_str}.joblib', f'ridge_{nodo_str}.joblib'),
            'scaler_ridge': descargar_modelo_gcs(BUCKET_MODELOS, f'{nodo_str}/scaler_ridge_{nodo_str}.joblib', f'scaler_ridge_{nodo_str}.joblib'),
            'gx': descargar_modelo_gcs(BUCKET_MODELOS, f'{nodo_str}/gx_{nodo_str}.joblib', f'gx_{nodo_str}.joblib'),
            'scaler_gx': descargar_modelo_gcs(BUCKET_MODELOS, f'{nodo_str}/scaler_gx_{nodo_str}.joblib', f'scaler_gx_{nodo_str}.joblib')
        }
    return cache_modelos[nodo_str]

# =============================================================================
# 3. MOTOR DE ORQUESTACIÓN (MPC)
# =============================================================================
class BlueSwitchOrchestrator:
    def __init__(self, models_dict, config):
        self.modelo_sinc = models_dict['ridge']
        self.scaler_sinc = models_dict['scaler_ridge']
        self.modelo_pue = models_dict['gx']
        self.scaler_pue = models_dict['scaler_gx']
        self.config = config

    def _scale_and_predict_pue(self, X_gx_base, it_load_series):
        """Helper: construye el input completo del scaler_gx, escala y predice PUE."""
        cols_gx_full = list(self.scaler_pue.feature_names_in_)
        X = X_gx_base.copy().reset_index(drop=True)
        X['it_load_kw'] = it_load_series.values
        X = X[cols_gx_full]
        X_scaled = pd.DataFrame(
            self.scaler_pue.transform(X),
            columns=cols_gx_full
        )
        return self.modelo_pue.predict(X_scaled)

    def procesar_lote_diario(self, df_dia, X_ridge_dia, X_gx_dia):
        df_dia = df_dia.reset_index(drop=True)
        X_ridge_dia = X_ridge_dia.reset_index(drop=True)
        X_gx_dia = X_gx_dia.reset_index(drop=True)
        N = len(df_dia)

        # 1. Predicción Síncrona y PUE Inicial
        X_ridge_scaled = pd.DataFrame(
            self.scaler_sinc.transform(X_ridge_dia),
            columns=X_ridge_dia.columns
        )
        df_dia['pred_dsync_kw'] = self.modelo_sinc.predict(X_ridge_scaled)
        df_dia['pue_predicho'] = self._scale_and_predict_pue(X_gx_dia, df_dia['pred_dsync_kw'])

        # 2. Downclocking de seguridad
        mask_crisis = df_dia['pue_predicho'] > self.config['LIMITE_PUE']
        df_dia['carga_sincrona_efectiva'] = np.where(
            mask_crisis,
            df_dia['pred_dsync_kw'] * (1.0 - self.config['MAX_DOWNCLOCK_SINK']),
            df_dia['pred_dsync_kw']
        )

        # --- CÁLCULO DEL WUE ---
        temp_array = df_dia['ambient_temperature'].values
        nodo_actual = self.config.get('NODO', 'VALENCIA')

        if nodo_actual == 'VALENCIA':
            df_dia['wue_calculado'] = np.where(temp_array > 15.0, 0.35 + 0.04 * (temp_array - 15.0), 0.35)
        elif nodo_actual == 'SANTIAGO':
            df_dia['wue_calculado'] = np.where(temp_array > 25.0, 0.02 + 0.005 * (temp_array - 25.0), 0.02)
        else:
            df_dia['wue_calculado'] = np.full(N, 0.35)

        # 3. OPTIMIZACIÓN MATEMÁTICA (Load Shifting)
        presupuesto_async_total = df_dia['d_async_kw'].sum()
        df_dia['nueva_async_kw'] = 0.0

        capacidad_servidor = self.config['CAPACIDAD_FISICA_MAX_KW']

        if presupuesto_async_total > 0:
            espacio_fisico_libre = np.maximum(0, capacidad_servidor - df_dia['carga_sincrona_efectiva'].values)
            limites_superiores = espacio_fisico_libre
            capacidad_total_disp = np.sum(limites_superiores)

            if capacidad_total_disp > 0:
                pue_array = df_dia['pue_predicho'].values
                precio_array = (df_dia['energy_spot_price_eur'] / 1000.0).values
                carbono_array = (df_dia['grid_carbon_intensity'] / 1000.0).values
                wue_array = df_dia['wue_calculado'].values

                coste_fin = pue_array * precio_array
                coste_eco = pue_array * carbono_array
                coste_h2o = wue_array * 1.0

                epsilon = 1e-9
                c_fin_norm = (coste_fin - np.min(coste_fin)) / (np.max(coste_fin) - np.min(coste_fin) + epsilon)
                c_eco_norm = (coste_eco - np.min(coste_eco)) / (np.max(coste_eco) - np.min(coste_eco) + epsilon)
                c_h2o_norm = (coste_h2o - np.min(coste_h2o)) / (np.max(coste_h2o) - np.min(coste_h2o) + epsilon)

                a = self.config.get('ALPHA_FIN', 0.33)
                b = self.config.get('BETA_ECO', 0.33)
                g = self.config.get('GAMMA_H2O', 0.34)

                suma = a + b + g
                a, b, g = a / suma, b / suma, g / suma

                c = (a * c_fin_norm) + (b * c_eco_norm) + (g * c_h2o_norm)
                c = np.nan_to_num(c, nan=0.0)

                A_eq = np.ones((1, N))
                b_eq = np.array([min(presupuesto_async_total, capacidad_total_disp)])
                bounds = [(0, float(lim_sup)) for lim_sup in limites_superiores]

                res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

                if res.success:
                    df_dia['nueva_async_kw'] = res.x
                else:
                    print("⚠️ Aviso MPC: No se pudo optimizar la curva. Aplicando naive limitando a la física.")
                    df_dia['nueva_async_kw'] = np.minimum(df_dia['d_async_kw'], limites_superiores)

        # 4. Auditoría y KPIs Finales (Modo Optimizado)
        carga_total_opt = df_dia['carga_sincrona_efectiva'] + df_dia['nueva_async_kw']
        df_dia['pue_opt_final'] = self._scale_and_predict_pue(X_gx_dia, carga_total_opt)

        df_dia['coste_opt_eur'] = (carga_total_opt * df_dia['pue_opt_final']) * (df_dia['energy_spot_price_eur'] / 1000.0)
        df_dia['carbono_opt_kg'] = (carga_total_opt * df_dia['pue_opt_final']) * (df_dia['grid_carbon_intensity'] / 1000.0)
        df_dia['agua_opt_litros'] = carga_total_opt * df_dia['wue_calculado']

        df_dia['pue_predicho'] = df_dia['pue_opt_final']

        # 5. Auditoría Naive (Sin optimizar)
        carga_total_naive = df_dia['pred_dsync_kw'] + df_dia['d_async_kw']
        df_dia['pue_naive'] = self._scale_and_predict_pue(X_gx_dia, carga_total_naive)

        df_dia['coste_naive_eur'] = (carga_total_naive * df_dia['pue_naive']) * (df_dia['energy_spot_price_eur'] / 1000.0)
        df_dia['carbono_naive_kg'] = (carga_total_naive * df_dia['pue_naive']) * (df_dia['grid_carbon_intensity'] / 1000.0)
        df_dia['agua_naive_litros'] = carga_total_naive * df_dia['wue_calculado']

        return df_dia

# =============================================================================
# 4. ENDPOINTS DE LA API CLOUD RUN
# =============================================================================
@functions_framework.http
def optimizar_nodo(request):
    # --- RUTA 1: HEALTH CHECK ---
    if request.path == '/health':
        return jsonify({"status": "online", "message": "Blue Switch API operativa", "version": "2.1"}), 200

    # --- RUTA 2: PROXY DE BIGQUERY (PANEL EJECUTIVO) ---
    if request.path == '/ejecutivo':
        if not bq_client:
            return jsonify({"error": "Cliente de BigQuery no inicializado en el servidor."}), 500
        
        try:
            # Uso de f-string para inyectar la variable de entorno de forma segura
            query = f"""
            SELECT
                DATE(time) AS fecha,
                nodo_id,
                SUM(coste_naive_eur - coste_opt_eur) AS ahorro_eur,
                SUM(carbono_naive_kg - carbono_opt_kg) AS co2_evitado_kg,
                SUM(agua_naive_litros - agua_opt_litros) AS agua_ahorrada_litros,
                AVG(pue_predicho) AS pue_medio,
                SUM(carga_sincrona_efectiva + nueva_async_kw) AS carga_total_kw
            FROM `{TABLA_AUDITORIA}`
            WHERE run_id LIKE 'live_demo_%'
            GROUP BY fecha, nodo_id
            ORDER BY fecha ASC
            """
            df_ejecutivo = bq_client.query(query).to_dataframe()
            
            if not df_ejecutivo.empty:
                df_ejecutivo['fecha'] = df_ejecutivo['fecha'].astype(str)
                
            return jsonify(df_ejecutivo.to_dict(orient="records")), 200
            
        except Exception as exc:
            print(f"❌ Error en la ruta ejecutiva de BQ: {str(exc)}")
            return jsonify({"error": str(exc)}), 500

    # --- RUTA 3: ORQUESTADOR PRINCIPAL (LOAD SHIFTING) ---
    request_json = request.get_json(silent=True)
    if not request_json:
        return jsonify({"error": "No se recibió payload JSON válido"}), 400

    try:
        is_simulation = request_json.get('is_simulation', False)
        nodo = request_json.get('nodo', 'VALENCIA').upper()
        run_id = request_json.get('run_id', 'simulacion_huerfana')

        modelos_activos = obtener_modelos_nodo(nodo)

        datos_telemetria = request_json.get('telemetria', [])
        if not datos_telemetria:
            return jsonify({"error": "El array de telemetría está vacío"}), 400

        df_operativo = pd.DataFrame(datos_telemetria).reset_index(drop=True)

        columnas_ridge = list(modelos_activos['ridge'].feature_names_in_)
        cols_gx_full = list(modelos_activos['scaler_gx'].feature_names_in_)
        columnas_gx = [c for c in cols_gx_full if c != 'it_load_kw']

        X_ridge = df_operativo[columnas_ridge]
        X_gx = df_operativo[columnas_gx]

        config_cliente = {
            'NODO': nodo,
            'LIMITE_PUE': 1.20,
            'MAX_DOWNCLOCK_SINK': 0.10,
            'CAPACIDAD_FISICA_MAX_KW': request_json.get('capacidad_max_kw', df_operativo['it_load_kw'].max() * 1.20),
            'ALPHA_FIN': request_json.get('alpha_fin', 0.33),
            'BETA_ECO': request_json.get('beta_eco', 0.33),
            'GAMMA_H2O': request_json.get('gamma_h2o', 0.34)
        }

        orquestador = BlueSwitchOrchestrator(modelos_activos, config_cliente)
        df_resultado = orquestador.procesar_lote_diario(df_operativo, X_ridge, X_gx)

        ahorro_eur = float(df_resultado['coste_naive_eur'].sum() - df_resultado['coste_opt_eur'].sum())
        co2_evitado = float(df_resultado['carbono_naive_kg'].sum() - df_resultado['carbono_opt_kg'].sum())
        agua_evitada_litros = float(df_resultado['agua_naive_litros'].sum() - df_resultado['agua_opt_litros'].sum())
        pue_medio = float(df_resultado['pue_predicho'].mean())
        wue_medio = float(df_resultado['wue_calculado'].mean())

        carga_inicial = float(df_operativo['d_async_kw'].sum())
        carga_procesada = float(df_resultado['nueva_async_kw'].sum())
        carga_pospuesta_kw = max(0.0, carga_inicial - carga_procesada)

        respuesta = {
            "estado": "Exito",
            "nodo": nodo,
            "kpis": {
                "ahorro_diario_eur": round(ahorro_eur, 2),
                "co2_mitigado_kg": round(co2_evitado, 2),
                "agua_ahorrada_litros": round(agua_evitada_litros, 2),
                "gasto_base_eur": round(float(df_resultado['coste_naive_eur'].sum()), 2),
                "emisiones_base_kg": round(float(df_resultado['carbono_naive_kg'].sum()), 2),
                "consumo_base_litros": round(float(df_resultado['agua_naive_litros'].sum()), 2),
                "pue_medio_proyectado": round(pue_medio, 3),
                "wue_medio_proyectado": round(wue_medio, 3),
                "carga_pospuesta_kw": round(carga_pospuesta_kw, 2)
            },
            "grafica_horaria": df_resultado[[
                'time', 'nueva_async_kw', 'coste_opt_eur', 'coste_naive_eur', 
                'carbono_opt_kg', 'carbono_naive_kg', 'pue_predicho', 'wue_calculado',
                'carga_sincrona_efectiva'
            ]].to_dict(orient='records')
        }

        if bq_client and not is_simulation:
            try:
                df_auditoria = df_resultado[[
                    'time', 'ambient_temperature', 'it_load_kw', 'energy_spot_price_eur',
                    'grid_carbon_intensity', 'pue_naive', 'pue_predicho',
                    'wue_calculado', 'coste_naive_eur', 'coste_opt_eur',
                    'carbono_naive_kg', 'carbono_opt_kg', 'agua_naive_litros', 'agua_opt_litros',
                    'carga_sincrona_efectiva', 'nueva_async_kw'
                ]].copy()

                df_auditoria_tick = df_auditoria.iloc[[0]].copy()
                df_auditoria_tick['nodo_id'] = nodo
                df_auditoria_tick['run_id'] = run_id
                df_auditoria_tick['estrategia_alpha'] = float(config_cliente['ALPHA_FIN'])
                df_auditoria_tick['estrategia_beta'] = float(config_cliente['BETA_ECO'])
                df_auditoria_tick['estrategia_gamma'] = float(config_cliente['GAMMA_H2O'])
                df_auditoria_tick['timestamp_ejecucion'] = pd.Timestamp.utcnow()
                df_auditoria_tick['time'] = pd.to_datetime(df_auditoria_tick['time'])

                job_config = bigquery.LoadJobConfig(
                    write_disposition="WRITE_APPEND",
                    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
                )
                job = bq_client.load_table_from_dataframe(df_auditoria_tick, TABLA_AUDITORIA, job_config=job_config)
                job.result()
                print(f"✅ Auditoría BQ: {job.output_rows} filas insertadas ({nodo} - Tick Horizonte Deslizante)")

            except Exception as e:
                print(f"❌ Error guardando en BigQuery: {str(e)}")

        elif is_simulation:
            print(f"🛡️ Modo Simulación activo, ignorando escritura en BQ.")

        return jsonify(respuesta), 200

    except Exception as e:
        print(f"❌ Error interno de la API: {str(e)}")
        return jsonify({"error": str(e)}), 500
