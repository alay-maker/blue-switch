from utils.config import PAGE_CONFIG, ROLES
from utils.theme import apply_theme
from components.sidebar import renderizar_menu_lateral
from views import vista_auditoria, vista_ejecutiva, vista_operaciones, vista_telemetria
import streamlit as st

st.set_page_config(**PAGE_CONFIG)
apply_theme()


def main() -> None:
    rol_actual = renderizar_menu_lateral()

    if rol_actual == ROLES["ejecutivo"]:
        vista_ejecutiva.mostrar()
    elif rol_actual == ROLES["operaciones"]:
        vista_operaciones.mostrar()
    elif rol_actual == ROLES["telemetria"]:
        vista_telemetria.mostrar_panel_vivo()
    elif rol_actual == ROLES["auditor"]:
        vista_auditoria.mostrar()
    else:
        st.error("No se ha podido resolver la vista solicitada.")


if __name__ == "__main__":
    main()
