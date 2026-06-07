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
    "bg": "#08161C",
    "surface": "#10242C",
    "surface_2": "#16313B",
    "surface_3": "#1D3E49",
    "primary": "#00C7B7",
    "accent_blue": "#0099E5",
    "success": "#27AE60",
    "warning": "#D6A23D",
    "danger": "#D95C68",
    "text": "#F7FBFC",
    "muted": "#D3E0E5",
    "border": "rgba(179, 205, 214, 0.24)",
}
