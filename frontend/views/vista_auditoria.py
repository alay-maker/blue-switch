import json
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.config import COLORS


def mostrar() -> None:
    st.title("Auditoría de IA y explicabilidad")
    st.markdown("Transparencia algorítmica, pesos de modelo y salud operativa del sistema de decisión térmica.")
    st.divider()
    nodo_seleccionado = st.radio("Seleccionar infraestructura a auditar:", ["Valencia", "Santiago"], horizontal=True)
    nodo_str = nodo_seleccionado.lower()
    ruta_json = f"frontend/artefactos/pesos_modelo_{nodo_str}.json"
    col_grafico, col_texto = st.columns([2, 1], gap="large")
    if os.path.exists(ruta_json):
        with open(ruta_json, "r", encoding="utf-8") as file:
            pesos = json.load(file)
        nombres_legibles = {
            "inercia_termica_ext_3h": "Inercia térmica exterior (3h)",
            "ambient_temperature": "Temperatura ambiente",
            "it_load_kw": "Carga síncrona servidores (kW)",
            "relative_humidity": "Humedad relativa (%)",
            "delta_temp_1h": "Variación térmica (1h)",
        }
        df_pesos = pd.DataFrame({"Variable": [nombres_legibles.get(key, key) for key in pesos.keys()], "Importancia (%)": [value * 100 for value in pesos.values()]})
        with col_grafico:
            st.subheader(f"Matriz de decisión XGBoost · {nodo_seleccionado}")
            fig = px.bar(df_pesos, x="Importancia (%)", y="Variable", orientation="h", color="Importancia (%)", color_continuous_scale=["rgba(44,110,159,0.18)", COLORS["primary"]])
            fig.update_layout(yaxis={"categoryorder": "total ascending"}, xaxis_title="Peso en la predicción del PUE (%)", yaxis_title="", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]), margin=dict(l=0, r=0, t=30, b=0), height=350)
            st.plotly_chart(fig, use_container_width=True)
        with col_texto:
            st.subheader("Ficha técnica")
            st.info(f"**Modelo activo:** `gx_{nodo_str}.joblib`\n\n**Framework:** XGBoost Regressor\n\n**Métrica principal:** RMSE < 0.02")
            if nodo_seleccionado == "Valencia":
                st.write("La IA prioriza inercia térmica y humedad relativa, coherente con una infraestructura evaporativa sensible al estrés térmico prolongado.")
            else:
                st.write("El sistema Dry Cooling responde casi exclusivamente a la temperatura, lo que refuerza la consistencia termodinámica del modelo.")
    else:
        st.error(f"No se encontró el archivo de pesos: `{ruta_json}`. Ejecuta la fábrica de modelos primero.")
    st.divider()
    st.subheader("Monitor de salud del modelo")
    col_drift1, col_drift2 = st.columns([2, 1])
    with col_drift1:
        st.warning("[WIP] Módulo de reentrenamiento automático")
        st.markdown("""Actualmente en desarrollo para producción. El orquestador evaluará en tiempo real si la distribución térmica del clima difiere de los datos de entrenamiento.
Si la desviación matemática supera el **5%**, se encolará un trabajo para reentrenar los pesos sin intervención humana.""")
    with col_drift2:
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=1.2, title={"text": "Desviación (Drift) %"}, gauge={"axis": {"range": [None, 10]}, "bar": {"color": COLORS["primary"]}, "steps": [{"range": [0, 5], "color": "rgba(138,154,91,0.12)"}, {"range": [5, 10], "color": "rgba(158,67,80,0.12)"}], "threshold": {"line": {"color": COLORS["danger"], "width": 4}, "thickness": 0.75, "value": 5}}))
        fig_gauge.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]))
        st.plotly_chart(fig_gauge, use_container_width=True)