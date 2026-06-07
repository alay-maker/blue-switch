from typing import Iterable, Optional

import streamlit as st


def render_kpi_row(items: Iterable[dict]) -> None:
    """Renderiza una fila de KPIs homogénea sin alterar la lógica funcional."""
    items = list(items)
    if not items:
        return
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            st.metric(
                label=item.get("label", ""),
                value=item.get("value", "—"),
                delta=item.get("delta"),
                help=item.get("help"),
            )


def render_section_title(title: str, caption: Optional[str] = None) -> None:
    st.markdown(f"### {title}")
    if caption:
        st.caption(caption)