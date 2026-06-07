import pandas as pd
import plotly.express as px
import streamlit as st
import requests

from components.kpis import render_kpi_row, render_section_title
# Importamos la nueva URL centralizada y los colores
from utils.config import COLORS, CLOUD_RUN_EJECUTIVO_URL 

@st.cache_data(ttl=60, show_spinner="Consultando inteligencia de negocio a través del API...")
def obtener_datos_ejecutivos() -> pd.DataFrame:
    try:
        # 1. Llamada segura al backend (Cloud Run se encarga de consultar a BigQuery)
        respuesta = requests.get(CLOUD_RUN_EJECUTIVO_URL)
        
        # Si el servidor devuelve un error (ej. 500), forzamos a que salte al except
        respuesta.raise_for_status() 
        
        # Convertimos la respuesta JSON en un DataFrame
        df = pd.DataFrame(respuesta.json())
        
        # Aseguramos el formato de fecha para los gráficos
        if not df.empty:
            df['fecha'] = pd.to_datetime(df['fecha']).dt.date
            
        return df

    except Exception as exc:
        # 2. FAIL-SAFE: Si el API falla, cargamos los datos locales para salvar la demo
        st.warning("⚠️ Modo Demostración: Conexión con el orquestador interrumpida. Cargando auditoría local.")
        try:
            df_fallback = pd.read_csv("data/dataset_semilla_fallback.csv")
            df_fallback['fecha'] = pd.to_datetime(df_fallback['fecha']).dt.date
            return df_fallback
        except Exception as csv_exc:
            st.error("Error crítico: Sistema de respaldo inaccesible.")
            return pd.DataFrame()


def mostrar() -> None:
    st.title("Panel Ejecutivo Global")
    st.markdown("Orquestación financiera, impacto ESG verificable y trazabilidad histórica consolidada desde BigQuery.")
    st.divider()
    
    df_hist = obtener_datos_ejecutivos()
    
    if df_hist.empty:
        st.info("Aún no hay datos históricos registrados o no se ha podido conectar al Data Warehouse.")
        return
        
    ahorro_total = df_hist["ahorro_eur"].sum()
    co2_total = df_hist["co2_evitado_kg"].sum()
    agua_total = df_hist["agua_ahorrada_litros"].sum()
    pue_global = df_hist["pue_medio"].mean()
    
    render_section_title("Impacto acumulado", "Lectura ejecutiva en primer nivel: coste, carbono, agua y eficiencia térmica.")
    render_kpi_row([
        {"label": "Ahorro financiero", "value": f"€ {ahorro_total:,.2f}"},
        {"label": "CO2 evitado", "value": f"{co2_total:,.0f} kg"},
        {"label": "Agua conservada", "value": f"{agua_total:,.0f} L"},
        {"label": "PUE medio flota", "value": f"{pue_global:.3f}"},
    ])
    
    col_mapa, col_grafico = st.columns([1.15, 1], gap="large")
    
    with col_mapa:
        st.markdown("### Huella geográfica del ahorro")
        df_mapa = df_hist.groupby("nodo_id", as_index=False).sum(numeric_only=True)
        coordenadas = {"VALENCIA": {"lat": 39.4699, "lon": -0.3774}, "SANTIAGO": {"lat": -33.4489, "lon": -70.6693}}
        df_mapa["lat"] = df_mapa["nodo_id"].map(lambda x: coordenadas.get(x, {}).get("lat", 0))
        df_mapa["lon"] = df_mapa["nodo_id"].map(lambda x: coordenadas.get(x, {}).get("lon", 0))
        fig_mapa = px.scatter_geo(df_mapa, lat="lat", lon="lon", size="ahorro_eur", color="nodo_id", hover_name="nodo_id", color_discrete_sequence=[COLORS["primary"], COLORS["warning"]], projection="natural earth", size_max=28)
        fig_mapa.update_layout(margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]), geo=dict(bgcolor="rgba(0,0,0,0)", showcoastlines=True, coastlinecolor="rgba(232,240,242,0.18)", showland=True, landcolor="rgba(16,39,48,0.45)", showocean=True, oceancolor="rgba(7,20,26,0.35)"))
        st.plotly_chart(fig_mapa, use_container_width=True)
        
    with col_grafico:
        st.markdown("### Evolución del PUE")
        fig_pue = px.line(df_hist, x="fecha", y="pue_medio", color="nodo_id", markers=True, color_discrete_sequence=[COLORS["primary"], COLORS["warning"]])
        fig_pue.update_layout(yaxis=dict(range=[1.0, 1.5], gridcolor="rgba(148,163,184,0.14)"), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=10, r=10), font=dict(color=COLORS["text"]), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_pue, use_container_width=True)
        
    st.info("La vista ejecutiva procesa la auditoría B2B mediante arquitectura Serverless sin exposición de credenciales.")