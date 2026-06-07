from typing import Iterable, Optional

import plotly.graph_objects as go

from utils.config import COLORS


def apply_chart_style(fig: go.Figure, *, height: int = 320, legend: bool = True) -> go.Figure:
    """Aplica una estética coherente de producto a un gráfico Plotly."""
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], family="Inter, Segoe UI, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) if legend else dict(),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(gridcolor="rgba(190,205,214,0.20)", zeroline=False),
    )
    return fig


def add_now_marker(fig: go.Figure, x_value, text: str = "AHORA") -> go.Figure:
    fig.add_vline(x=x_value, line_width=2, line_dash="dash", line_color=COLORS["danger"])
    fig.add_annotation(x=x_value, y=1.05, yref="paper", text=text, showarrow=False, font=dict(size=12, color=COLORS["danger"]))
    return fig


def get_sequence(names: Optional[Iterable[str]] = None) -> list[str]:
    base = [COLORS["primary"], COLORS["success"], COLORS["warning"], COLORS["danger"], COLORS["accent_blue"]]
    return base if names is None else base[: len(list(names))]