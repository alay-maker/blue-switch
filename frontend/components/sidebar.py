import time
from typing import Dict, Union

import requests
import streamlit as st

from utils.config import CLOUD_RUN_HEALTH_URL, ROLES


@st.cache_data(ttl=300)
def despertar_backend() -> Dict[str, Union[str, int, None]]:
    """Lanza un ping silencioso a Cloud Run para reducir el cold start."""
    inicio = time.time()
    try:
        respuesta = requests.get(CLOUD_RUN_HEALTH_URL, timeout=5.0)
        latencia = int((time.time() - inicio) * 1000)
        if respuesta.status_code == 200:
            return {"estado": "Operativo", "color": "🟢", "latencia": latencia}
        return {"estado": "Error de API", "color": "🔴", "latencia": None}
    except requests.exceptions.Timeout:
        return {"estado": "Despertando...", "color": "🟡", "latencia": ">5000"}
    except requests.exceptions.RequestException:
        return {"estado": "Desconectado", "color": "🔴", "latencia": None}


def renderizar_menu_lateral() -> str:
    """Dibuja el menú lateral interactivo y devuelve el rol seleccionado."""
    with st.sidebar:
        st.markdown('<div class="bs-sidebar-brand">BLUE SWITCH</div>', unsafe_allow_html=True)
        st.markdown('<div class="bs-sidebar-caption">Infraestructura inteligente. Impacto verificable.</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown("### Navegación")
        rol_seleccionado = st.selectbox(
            "Selecciona tu vista operativa:",
            options=list(ROLES.values()),
            index=1,
        )
        st.divider()
        st.markdown("### Diagnóstico")
        estado_api = despertar_backend()
        card_html = f"""<div class='bs-status-card'>
            <div class='bs-status-dot'>{estado_api['color']}</div>
            <div>
                <div class='bs-status-label'>API Cloud Run</div>
                <div class='bs-status-value'>{estado_api['estado']}</div>
            </div>
        </div>"""
        st.markdown(card_html, unsafe_allow_html=True)
        if estado_api["latencia"]:
            st.caption(f"Latencia: {estado_api['latencia']} ms")
        st.markdown('<div class="bs-pill ok">BigQuery · Modo Append</div>', unsafe_allow_html=True)
        st.markdown('<div class="bs-pill muted">Data Lake · Activo</div>', unsafe_allow_html=True)
        return rol_seleccionado