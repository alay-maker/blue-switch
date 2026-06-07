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
    "bg": "#F4F8F8",
    "surface": "#FFFFFF",
    "surface_2": "#EDF4F5",
    "surface_3": "#E3EEF0",
    "primary": "#00AFA3",
    "accent_blue": "#1493D1",
    "success": "#2E9E5B",
    "warning": "#C69236",
    "danger": "#C95A67",
    "text": "#12313A",
    "muted": "#5F7A83",
    "border": "rgba(18, 49, 58, 0.12)",
}
