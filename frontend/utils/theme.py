import streamlit as st


def apply_theme() -> None:
    """Inyecta una capa visual sobria y legible sin alterar la lógica existente."""
    st.markdown(
        """
        <style>
        :root {
            --bs-bg: #0B1820;
            --bs-surface: #13262F;
            --bs-surface-2: #18323D;
            --bs-surface-3: #21424F;
            --bs-primary: #2C8C95;
            --bs-blue: #4B8FC2;
            --bs-success: #92B468;
            --bs-warning: #D9A24F;
            --bs-danger: #C95A67;
            --bs-text: #F4F8FA;
            --bs-muted: #C3D0D5;
            --bs-border: rgba(196, 209, 214, 0.22);
            --bs-button-text: #081218;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(44,140,149,0.11), transparent 24%),
                linear-gradient(180deg, #0B1820 0%, #0E1D25 100%);
            color: var(--bs-text);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(11, 24, 32, 0.78);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #102029 0%, #12232B 100%);
            border-right: 1px solid var(--bs-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--bs-text);
        }

        [data-testid="stSidebarNav"] {
            display: none;
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, h4, h5, h6 {
            letter-spacing: -0.02em;
            font-weight: 700;
            color: var(--bs-text);
        }

        p,
        li,
        label,
        .stMarkdown,
        .stCaption,
        .stText,
        div[data-testid="stMarkdownContainer"] p {
            color: var(--bs-muted);
        }

        strong,
        b {
            color: var(--bs-text);
        }

        .bs-sidebar-brand {
            font-size: 1.2rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            color: var(--bs-text);
        }

        .bs-sidebar-caption {
            color: var(--bs-muted);
            font-size: 0.9rem;
            margin-top: 0.25rem;
            margin-bottom: 0.2rem;
        }

        .bs-status-card {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0.85rem 0.9rem;
            border: 1px solid var(--bs-border);
            background: rgba(24, 50, 61, 0.82);
            border-radius: 14px;
            margin-bottom: 0.65rem;
        }

        .bs-status-dot {
            font-size: 1.1rem;
        }

        .bs-status-label {
            font-size: 0.78rem;
            color: var(--bs-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .bs-status-value {
            color: var(--bs-text);
            font-weight: 600;
        }

        .bs-pill {
            display: inline-block;
            margin-top: 0.35rem;
            padding: 0.38rem 0.7rem;
            border-radius: 999px;
            border: 1px solid var(--bs-border);
            font-size: 0.78rem;
            font-weight: 600;
            background: rgba(24, 50, 61, 0.62);
        }

        .bs-pill.ok {
            color: #E5F1D6;
        }

        .bs-pill.muted {
            color: var(--bs-text);
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(24,50,61,0.92), rgba(19,38,47,0.92));
            border: 1px solid var(--bs-border);
            border-radius: 16px;
            padding: 0.75rem 0.85rem;
            min-height: 130px;
        }

        [data-testid="stMetricLabel"] {
            color: var(--bs-muted);
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: var(--bs-text);
            font-weight: 700;
            letter-spacing: -0.03em;
        }

        [data-testid="stMetricDelta"] {
            color: var(--bs-text);
        }

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stButton"] > button,
        div[data-testid="stDownloadButton"] > button,
        button[kind="primary"] {
            background: linear-gradient(180deg, #D9A24F 0%, #C98933 100%) !important;
            color: #081218 !important;
            -webkit-text-fill-color: #081218 !important;
            border: 1px solid rgba(255, 225, 170, 0.28) !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            text-shadow: none !important;
            box-shadow: 0 6px 18px rgba(201, 137, 51, 0.24) !important;
        }

        .stButton > button *,
        .stDownloadButton > button *,
        div[data-testid="stButton"] > button *,
        div[data-testid="stDownloadButton"] > button *,
        button[kind="primary"] * {
            color: #081218 !important;
            fill: #081218 !important;
            stroke: #081218 !important;
            -webkit-text-fill-color: #081218 !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover,
        button[kind="primary"]:hover {
            background: linear-gradient(180deg, #E3AE5C 0%, #D39340 100%) !important;
            color: #081218 !important;
            -webkit-text-fill-color: #081218 !important;
            box-shadow: 0 8px 22px rgba(211, 147, 64, 0.30) !important;
            transform: translateY(-1px);
        }

        .stButton > button:focus,
        .stDownloadButton > button:focus,
        .stButton > button:active,
        .stDownloadButton > button:active,
        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:active,
        button[kind="primary"]:focus,
        button[kind="primary"]:active {
            color: #081218 !important;
            -webkit-text-fill-color: #081218 !important;
            outline: none !important;
        }

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stTextArea textarea {
            background: rgba(24, 50, 61, 0.82);
            color: var(--bs-text);
            border: 1px solid var(--bs-border);
            border-radius: 12px;
        }

        .stSelectbox label,
        .stMultiSelect label,
        .stTextInput label,
        .stNumberInput label,
        .stTextArea label,
        .stSlider label,
        .stRadio label,
        .stCheckbox label,
        .stToggle label {
            color: var(--bs-text) !important;
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background: var(--bs-primary);
        }

        .stSlider [data-baseweb="slider"] [role="slider"] {
            background: #F7FAFB !important;
            border: 2px solid var(--bs-primary) !important;
            box-shadow: 0 0 0 3px rgba(44, 140, 149, 0.18);
        }

        .stSlider [data-baseweb="slider"] [data-testid="stTickBarMin"],
        .stSlider [data-baseweb="slider"] [data-testid="stTickBarMax"],
        .stSlider [data-baseweb="slider"] div[aria-hidden="true"] {
            color: var(--bs-text) !important;
            opacity: 0.95 !important;
        }

        .stSlider p {
            color: var(--bs-text) !important;
        }

        [data-testid="stToggle"] label {
            color: var(--bs-text) !important;
            font-weight: 600;
        }

        [data-testid="stToggle"] [data-baseweb="checkbox"] > div {
            background-color: rgba(195, 208, 213, 0.26) !important;
            border: 1px solid rgba(195, 208, 213, 0.34) !important;
        }

        [data-testid="stToggle"] input:checked + div,
        [data-testid="stToggle"] [aria-checked="true"] {
            background-color: var(--bs-warning) !important;
            border-color: rgba(255, 225, 170, 0.28) !important;
        }

        [data-testid="stToggle"] [data-baseweb="checkbox"] div div {
            background: #0A1419 !important;
        }

        /* Spinner y overlays más discretos */
        [data-testid="stSpinner"] {
            border-radius: 14px;
            border: 1px solid var(--bs-border);
            background: rgba(24, 50, 61, 0.90) !important;
            color: var(--bs-text) !important;
        }

        .stSpinner > div {
            background: transparent !important;
        }

        /* Evita el lavado visual del chart durante reruns */
        .stPlotlyChart,
        .stPlotlyChart > div,
        .stPlotlyChart iframe,
        .js-plotly-plot,
        .plot-container,
        .plotly,
        .main-svg {
            opacity: 1 !important;
            filter: none !important;
        }

        .stPlotlyChart {
            background: linear-gradient(180deg, rgba(28,58,70,0.94), rgba(20,40,49,0.94));
            border: 1px solid var(--bs-border);
            border-radius: 18px;
            padding: 0.4rem 0.4rem 0.1rem 0.4rem;
            position: relative;
            isolation: isolate;
        }

        .stPlotlyChart::before,
        .stPlotlyChart::after {
            display: none !important;
            content: none !important;
        }

        div[data-testid="stEmpty"] {
            background: transparent !important;
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
            border: 1px solid var(--bs-border);
            background: rgba(24, 50, 61, 0.78);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--bs-border);
            border-radius: 14px;
            overflow: hidden;
        }

        hr {
            border-color: var(--bs-border);
        }

                /* Evitar opacidad durante el Auto-Pilot (stale state de Streamlit) */
        [data-testid="stStaleNode"],
        [data-stale="true"],
        .st-emotion-cache-1cvow4s {
            opacity: 1 !important;
            transition: none !important;
            filter: none !important;
        }

        /* Refuerzo extra para que Plotly no se vea lavado durante el rerun */
        .stPlotlyChart,
        .stPlotlyChart > div,
        .js-plotly-plot,
        .plot-container,
        .plotly,
        .main-svg {
            opacity: 1 !important;
            filter: none !important;
            transition: none !important;
        }

        /* Leyenda y texto SVG del gráfico siempre claros */
        .stPlotlyChart text,
        .stPlotlyChart tspan {
            fill: #F4F8FA !important;
            color: #F4F8FA !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )