import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from api.cloud_service import obtener_dia_base, simular_escenario_mpc
from components.kpis import render_kpi_row
from utils.config import COLORS


def mostrar() -> None:
    st.title("Sala de Control de Operaciones")
    st.markdown("Orquestación termodinámica, simulación MPC y lectura táctica para decidir bajo presión operativa.")
    st.divider()
    col_controles, col_resultados = st.columns([1, 2], gap="large")
    with col_controles:
        st.subheader("Configuración del escenario")
        nodo = st.selectbox("Seleccionar Data Center:", ["VALENCIA", "SANTIAGO"])
        st.markdown("**Impacto meteorológico y mercado**")
        temp_offset = st.slider("Ola de calor (Offset ºC)", min_value=0.0, max_value=15.0, value=0.0, step=0.5, help="Simula un aumento de temperatura sobre la base real de este día.")
        precio_offset = st.slider("Crisis energética (+ €/MWh)", min_value=0.0, max_value=200.0, value=0.0, step=10.0, help="Añade sobrecoste al precio del mercado spot.")
        st.markdown("**Estrategia corporativa (pesos del algoritmo)**")
        estrategia = st.radio("Prioridad de optimización:", ["Balanceada (ESG)", "Agresiva (Costes)", "Sostenible (CO2)", "Conservación (Agua)"])
        if estrategia == "Balanceada (ESG)":
            alpha, beta, gamma = 0.33, 0.33, 0.34
        elif estrategia == "Agresiva (Costes)":
            alpha, beta, gamma = 0.80, 0.10, 0.10
        elif estrategia == "Sostenible (CO2)":
            alpha, beta, gamma = 0.10, 0.80, 0.10
        else:
            alpha, beta, gamma = 0.10, 0.10, 0.80
        ejecutar = st.button("Ejecutar IA de orquestación", type="primary", use_container_width=True)
    with col_resultados:
        st.subheader("Resultados de producción")
        if ejecutar:
            with st.spinner("Conectando con Google Cloud y resolviendo tensores..."):
                modificadores = {"temp_offset": temp_offset, "precio_offset": precio_offset, "alpha": alpha, "beta": beta, "gamma": gamma}
                resultado = simular_escenario_mpc(modificadores, nodo=nodo)
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                kpis = resultado.get("kpis", {})
                st.success(f"Simulación resuelta exitosamente para **{nodo}**")
                render_kpi_row([{"label": "Ahorro diario", "value": f"€ {kpis.get('ahorro_diario_eur', 0):.2f}"}, {"label": "CO2 mitigado", "value": f"{kpis.get('co2_mitigado_kg', 0):.1f} kg"}, {"label": "Agua ahorrada", "value": f"{kpis.get('agua_ahorrada_litros', 0):.1f} L"}])
                consumo_agua_final = kpis.get("consumo_base_litros", 0) - kpis.get("agua_ahorrada_litros", 0)
                render_kpi_row([{"label": "PUE medio proyectado", "value": f"{kpis.get('pue_medio_proyectado', 1.0):.3f}"}, {"label": "Gasto final estimado", "value": f"€ {kpis.get('gasto_base_eur', 0) - kpis.get('ahorro_diario_eur', 0):.2f}"}, {"label": "Consumo final agua", "value": f"{consumo_agua_final:.1f} L"}])
                carga_pospuesta = kpis.get("carga_pospuesta_kw", 0)
                if carga_pospuesta > 0:
                    st.warning(f"⚠️ Alerta de capacidad (SLA Backlog): {carga_pospuesta} kW de tareas asíncronas han sido pospuestas para el día siguiente debido a que se alcanzó el límite físico del servidor.")
                else:
                    st.success("✅ SLA cumplido: toda la carga asíncrona fue procesada dentro de las 24 horas (0 kW pospuestos).")
                st.divider()
                df_graf = pd.DataFrame(resultado.get("grafica_horaria", []))
                df_base = obtener_dia_base(nodo)
                if not df_graf.empty and not df_base.empty:
                    df_graf["Hora"] = pd.to_datetime(df_base["time"]).dt.strftime("%H:%M")
                    st.markdown("### Distribución dinámica de cargas")
                    fig_cargas = go.Figure()
                    fig_cargas.add_trace(go.Bar(x=df_graf["Hora"], y=df_base["d_sync_kw"], name="Carga síncrona base", marker_color=COLORS["accent_blue"]))
                    fig_cargas.add_trace(go.Bar(x=df_graf["Hora"], y=df_graf["nueva_async_kw"], name="Carga flexible IA", marker_color=COLORS["warning"]))
                    fig_cargas.update_layout(barmode="stack", height=300, margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]), yaxis=dict(title="Potencia asignada (kW)", gridcolor="rgba(148,163,184,0.14)"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_cargas, use_container_width=True)
                    st.markdown("### Impacto térmico y coste horario")
                    fig_coste = go.Figure()
                    fig_coste.add_trace(go.Scatter(x=df_graf["Hora"], y=df_graf["coste_opt_eur"], name="Coste optimizado (€)", line=dict(color=COLORS["warning"], width=3)))
                    fig_coste.add_trace(go.Scatter(x=df_graf["Hora"], y=df_graf["pue_predicho"], name="PUE predictivo", line=dict(color=COLORS["danger"], dash="dot"), yaxis="y2"))
                    fig_coste.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]), yaxis=dict(title="Coste horario (€)", gridcolor="rgba(148,163,184,0.14)"), yaxis2=dict(title="PUE", overlaying="y", side="right", range=[1.0, 1.8]), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                    st.plotly_chart(fig_coste, use_container_width=True)
                    st.info("El gráfico apilado mantiene la funcionalidad original y refuerza la lectura táctica de cómo el orquestador desplaza carga flexible hacia ventanas más rentables.")
        else:
            st.info("Configura los parámetros del escenario y pulsa Ejecutar para simular cómo reaccionaría la inteligencia artificial a lo largo de un día completo.")