# Blue Switch

**Blue Switch** es una plataforma de optimización inteligente para centros de datos que reduce costes energéticos, emisiones de CO₂ y consumo de agua mediante la planificación dinámica de cargas computacionales.

El sistema predice el comportamiento térmico y energético de un nodo, evalúa el impacto de mover cargas asíncronas a las horas más favorables y calcula una estrategia óptima que equilibra coste económico, huella de carbono y consumo hídrico.

## Descripción

Blue Switch utiliza un enfoque de **Model Predictive Control (MPC)** para redistribuir cargas asíncronas a lo largo del día. A partir de telemetría operativa, precios de electricidad, intensidad de carbono de la red y condiciones ambientales, el motor calcula cuándo conviene ejecutar o posponer trabajo no crítico.

La solución compara una estrategia de referencia (*naive*) con la estrategia optimizada y genera indicadores de ahorro económico, CO₂ evitado, agua ahorrada, PUE y WUE.

## Características

- Predicción de carga síncrona mediante modelos Ridge entrenados por nodo.
- Estimación del PUE con modelos de machine learning.
- Cálculo dinámico del WUE según la temperatura ambiente y la ubicación del nodo.
- Optimización de *load shifting* mediante programación lineal.
- Protección operativa mediante límites de PUE y capacidad física del servidor.
- Downclocking de seguridad cuando se detectan condiciones térmicas adversas.
- Comparación entre escenario optimizado y escenario de referencia.
- Registro de auditoría en Google BigQuery.
- API HTTP preparada para despliegue en Google Cloud Functions o Cloud Run.
- Panel ejecutivo para consultar KPIs agregados por fecha y nodo.

## Arquitectura

```text
Frontend
   │
   ▼
Blue Switch API (Cloud Functions / Cloud Run)
   │
   ├── Modelos ML almacenados en Google Cloud Storage
   ├── Optimizador de programación lineal (SciPy)
   └── Google BigQuery
         └── Auditoría y KPIs ejecutivos
```

## Tecnologías

- Python
- Flask y Google Functions Framework
- pandas y NumPy
- scikit-learn / joblib
- SciPy
- Google Cloud BigQuery
- Google Cloud Storage
- Frontend web para visualización de resultados

## Funcionamiento

1. El frontend envía telemetría horaria del nodo, parámetros de capacidad y pesos de optimización.
2. La API descarga o recupera de caché los modelos correspondientes al nodo.
3. El sistema predice la carga síncrona y el PUE esperado.
4. Si el PUE supera el límite configurado, aplica una reducción segura de carga síncrona.
5. Calcula el WUE estimado según la temperatura y el nodo.
6. Resuelve un problema de programación lineal para distribuir la carga asíncrona en las franjas horarias más eficientes.
7. Compara el resultado optimizado con la estrategia de referencia.
8. Devuelve KPIs y datos horarios para su visualización.
9. Si la ejecución no es una simulación, almacena la auditoría en BigQuery.

## API

### Health check

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "online",
  "message": "Blue Switch API operativa",
  "version": "2.1"
}
```

### Optimización de nodo

```http
POST /
Content-Type: application/json
```

Ejemplo de cuerpo de solicitud:

```json
{
  "nodo": "VALENCIA",
  "run_id": "live_demo_001",
  "is_simulation": true,
  "capacidad_max_kw": 500,
  "alpha_fin": 0.33,
  "beta_eco": 0.33,
  "gamma_h2o": 0.34,
  "telemetria": [
    {
      "time": "2026-01-01T00:00:00Z",
      "ambient_temperature": 18.5,
      "it_load_kw": 320,
      "d_async_kw": 80,
      "energy_spot_price_eur": 95,
      "grid_carbon_intensity": 180
    }
  ]
}
```

La respuesta incluye KPIs agregados y una serie horaria con la carga asignada, costes, emisiones, consumo de agua, PUE y WUE.

### Panel ejecutivo

```http
GET /ejecutivo
```

Devuelve los KPIs agregados desde BigQuery para las ejecuciones identificadas como `live_demo_%`, incluyendo ahorro económico, CO₂ evitado, agua ahorrada, PUE medio y carga total.

## Parámetros de optimización

| Parámetro | Descripción | Valor por defecto |
|---|---|---:|
| `alpha_fin` | Peso del coste económico | `0.33` |
| `beta_eco` | Peso de las emisiones de CO₂ | `0.33` |
| `gamma_h2o` | Peso del consumo de agua | `0.34` |
| `capacidad_max_kw` | Capacidad física máxima del nodo | Calculada a partir de la telemetría |
| `LIMITE_PUE` | Umbral de PUE que activa medidas de seguridad | `1.20` |
| `MAX_DOWNCLOCK_SINK` | Reducción máxima de carga síncrona en condiciones críticas | `0.10` |

Los pesos se normalizan internamente, por lo que pueden expresarse en cualquier escala relativa.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `TABLA_AUDITORIA` | Tabla de BigQuery utilizada para almacenar la auditoría |
| `BUCKET_MODELOS` | Bucket de Google Cloud Storage que contiene los modelos por nodo |

Ejemplo:

```bash
export TABLA_AUDITORIA="tu-proyecto.blue_switch.dataset_semilla"
export BUCKET_MODELOS="tu-bucket-de-modelos"
```

## Estructura de modelos

Los modelos deben estar organizados en Google Cloud Storage por nodo:

```text
gs://<BUCKET_MODELOS>/<nodo>/
├── sinc_kw_ridge_<nodo>.joblib
├── scaler_ridge_<nodo>.joblib
├── gx_<nodo>.joblib
└── scaler_gx_<nodo>.joblib
```

Actualmente, el sistema contempla nodos como `VALENCIA` y `SANTIAGO`, con reglas específicas de cálculo de WUE para cada ubicación.

## Ejecución local

```bash
cd backend
pip install -r requirements.txt
functions-framework --target=optimizar_nodo --debug
```

La API quedará disponible de forma local y podrá probarse mediante peticiones HTTP con un cliente como `curl`, Postman o el frontend incluido en el repositorio.

## Estructura del repositorio

```text
blue-switch/
├── backend/
│   └── main.py
├── frontend/
├── README.md
└── LICENSE
```

## Licencia

Este proyecto se distribuye bajo los términos de la licencia incluida en el archivo [`LICENSE`](./LICENSE).
