import streamlit as st

PAGE_CONFIG = {
    "page_title": "Blue Switch | Data Center Orchestrator",
    "page_icon": "⚡",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

ROLES = {
    "ejecutivo": "Panel Ejecutivo Global",
    "operaciones": "Sala de Control (Simulador 24h)",
    "telemetria": "Telemetría en Vivo (Horizonte Deslizante)",
    "auditor": "Auditoría y Compliance ESG",
}

# Extraemos las URLs de la bóveda de secretos de Streamlit
try:
    CLOUD_RUN_URL = st.secrets["CLOUD_RUN_URL"]
    CLOUD_RUN_HEALTH_URL = st.secrets["CLOUD_RUN_HEALTH_URL"]
    CLOUD_RUN_EJECUTIVO_URL = st.secrets["CLOUD_RUN_EJECUTIVO_URL"]
    
except KeyError as e:
    # Error de seguridad controlado en caso de que alguien clone el repo y no configure los secretos
    st.error(f"⚠️ Error Crítico de FinOps: Falta la credencial o URL {e} en los secretos del sistema.")
    
    # URLs de respaldo (mock) para evitar que la aplicación haga un crash total
    CLOUD_RUN_URL = "http://localhost:8080/optimizar"
    CLOUD_RUN_HEALTH_URL = "http://localhost:8080/health"
    CLOUD_RUN_EJECUTIVO_URL = "http://localhost:8080/ejecutivo"

COLORS = {
    "bg": "#0B1820",
    "surface": "#13262F",
    "surface_2": "#18323D",
    "surface_3": "#21424F",
    "primary": "#2C8C95",
    "accent_blue": "#4B8FC2",
    "success": "#92B468",
    "warning": "#D9A24F",
    "danger": "#C95A67",
    "text": "#F4F8FA",
    "muted": "#C3D0D5",
    "border": "rgba(196, 209, 214, 0.22)",
}