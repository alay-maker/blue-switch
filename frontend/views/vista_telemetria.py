import time
import uuid

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

from components.kpis import render_kpi_row
from utils.config import CLOUD_RUN_URL, COLORS


@st.cache_data
def cargar_telemetria(nodo: str) -> pd.DataFrame:
    ruta = f"frontend/artefactos/telemetria_{nodo.lower()}.csv"
    try:
        df = pd.read_csv(ruta)
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d %H:%M")
        return df
    except Exception as exc:
        st.error(f"Error cargando telemetría local: {exc}")
        return pd.DataFrame()


def _inicializar_estado() -> None:
    defaults = {
        "indice_t": 0,
        "run_id_vivo": f"live_demo_{uuid.uuid4().hex[:6]}",
        "acumulado_ahorro": 0.0,
        "acumulado_co2": 0.0,
        "historial_ejecutado": [],
        "plan_futuro": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _crear_figura_radar(df_plot: pd.DataFrame, hora_ahora) -> go.Figure:
    fig_radar = go.Figure()

    fig_radar.add_trace(
        go.Bar(
            x=df_plot["time"],
            y=df_plot.get("carga_sincrona_efectiva", [0] * len(df_plot)),
            name="Carga síncrona base",
            marker_color=COLORS["accent_blue"],
        )
    )
    fig_radar.add_trace(
        go.Bar(
            x=df_plot["time"],
            y=df_plot.get("nueva_async_kw", [0] * len(df_plot)),
            name="Carga asíncrona (MPC)",
            marker_color=COLORS["warning"],
        )
    )

    fig_radar.add_vline(
        x=hora_ahora,
        line_width=3,
        line_dash="dash",
        line_color=COLORS["danger"],
    )

    fig_radar.add_annotation(
        x=hora_ahora,
        y=1.05,
        yref="paper",
        text="PASADO | FUTURO",
        showarrow=False,
        font=dict(size=12, color="#F4F8FA"),
    )

    fig_radar.update_layout(
        barmode="stack",
        height=350,
        margin=dict(l=0, r=0, t=34, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F4F8FA", family="Inter, Segoe UI, sans-serif"),
        xaxis=dict(
            title=None,
            showgrid=False,
            zeroline=False,
            tickfont=dict(color="#C3D0D5"),
            title_font=dict(color="#F4F8FA"),
        ),
        yaxis=dict(
            title="Potencia asignada (kW)",
            gridcolor="rgba(196, 209, 214, 0.22)",
            tickfont=dict(color="#C3D0D5"),
            title_font=dict(color="#F4F8FA"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#F4F8FA", size=12),
            title_font=dict(color="#F4F8FA"),
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(
            bgcolor="#16303A",
            bordercolor="rgba(196, 209, 214, 0.22)",
            font=dict(color="#F4F8FA"),
        ),
    )

    return fig_radar


def mostrar_panel_vivo() -> None:
    st.title("Radar Predictivo · Horizonte Deslizante")
    st.markdown(
        "Visualización en tiempo real del orquestador."
    )

    _inicializar_estado()

    nodo = st.selectbox("Seleccionar Data Center:", ["VALENCIA", "SANTIAGO"])
    df_full = cargar_telemetria(nodo)

    if df_full.empty:
        return

    col_ctrl1, col_ctrl2 = st.columns([2, 1])

    with col_ctrl1:
        estrategia = st.radio(
            "Directriz de optimización (cambia en vivo):",
            [
                "Balanceada (ESG)",
                "Agresiva (Costes)",
                "Sostenible (CO2)",
                "Conservación (Agua)",
            ],
            horizontal=True,
        )

    with col_ctrl2:
        auto_play = st.toggle("Auto-Pilot")

    pesos = {
        "Balanceada (ESG)": (0.33, 0.33, 0.34),
        "Agresiva (Costes)": (0.80, 0.10, 0.10),
        "Sostenible (CO2)": (0.10, 0.80, 0.10),
        "Conservación (Agua)": (0.10, 0.10, 0.80),
    }
    alpha, beta, gamma = pesos[estrategia]

    if auto_play:
        st.caption(
            "Auto-Pilot activado."
        )

    tick_pulsado = st.button("Procesar siguiente tick", type="primary", use_container_width=True)

    if (tick_pulsado or auto_play) and st.session_state.indice_t + 24 <= len(df_full):
        df_ventana = df_full.iloc[
            st.session_state.indice_t : st.session_state.indice_t + 24
        ].copy()
        df_ventana["d_async_kw"] = df_ventana["it_load_kw"] * 0.20
        capacidad_max_kw = float(df_ventana["it_load_kw"].max() * 1.20)

        payload = {
            "nodo": nodo,
            "is_simulation": False,
            "run_id": st.session_state.run_id_vivo,
            "alpha_fin": alpha,
            "beta_eco": beta,
            "gamma_h2o": gamma,
            "capacidad_max_kw": capacidad_max_kw,
            "telemetria": df_ventana.to_dict(orient="records"),
        }

        try:
            respuesta_http = requests.post(CLOUD_RUN_URL, json=payload, timeout=20.0)
            respuesta_http.raise_for_status()
            respuesta = respuesta_http.json()
        except requests.exceptions.RequestException as exc:
            st.error(f"Fallo de conexión con la API: {exc}")
            respuesta = {}

        if "kpis" in respuesta:
            grafica = respuesta["grafica_horaria"]
            hora_actual = grafica[0]

            st.session_state.historial_ejecutado.append(hora_actual)
            if len(st.session_state.historial_ejecutado) > 6:
                st.session_state.historial_ejecutado.pop(0)

            st.session_state.plan_futuro = grafica[1:]
            st.session_state.acumulado_ahorro += (
                hora_actual["coste_naive_eur"] - hora_actual["coste_opt_eur"]
            )
            st.session_state.acumulado_co2 += (
                hora_actual["carbono_naive_kg"] - hora_actual["carbono_opt_kg"]
            )
            st.session_state.indice_t += 1

    st.divider()
    st.markdown("### Visión del orquestador")

    contenedor_grafica = st.empty()

    if st.session_state.historial_ejecutado or st.session_state.plan_futuro:
        df_pasado = pd.DataFrame(st.session_state.historial_ejecutado)
        df_futuro = pd.DataFrame(st.session_state.plan_futuro)
        df_plot = pd.concat([df_pasado, df_futuro], ignore_index=True)
        df_plot["time"] = pd.to_datetime(df_plot["time"])

        indice_ahora = len(df_pasado) - 1 if not df_pasado.empty else 0
        hora_ahora = df_plot.iloc[indice_ahora]["time"]

        fig_radar = _crear_figura_radar(df_plot, hora_ahora)
        contenedor_grafica.plotly_chart(fig_radar, use_container_width=True)
    else:
        contenedor_grafica.info(
            "Aún no hay ticks procesados. Activa Auto-Pilot o ejecuta el siguiente tick para iniciar el radar."
        )

    st.markdown("### Impacto consolidado de la sesión")
    render_kpi_row(
        [
            {
                "label": "Hora actual ejecutada",
                "value": f"Tick {st.session_state.indice_t}",
            },
            {
                "label": "Ahorro acumulado BQ",
                "value": f"€ {st.session_state.acumulado_ahorro:.2f}",
            },
            {
                "label": "CO2 evitado acumulado",
                "value": f"{st.session_state.acumulado_co2:.2f} kg",
            },
        ]
    )

    if st.button("Reiniciar sesión"):
        for key in [
            "indice_t",
            "run_id_vivo",
            "acumulado_ahorro",
            "acumulado_co2",
            "historial_ejecutado",
            "plan_futuro",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    if auto_play and st.session_state.indice_t + 24 <= len(df_full):
        time.sleep(2.5)
        st.rerun()