import streamlit as st


def apply_theme() -> None:
    """Inyecta una capa visual sobria sin alterar la lógica existente."""
    st.markdown(
        """
        <style>
        :root {
            --bs-bg: #07141A;
            --bs-surface: #0D1B22;
            --bs-surface-2: #102730;
            --bs-surface-3: #14343E;
            --bs-primary: #00AFA3;
            --bs-blue: #2C6E9F;
            --bs-success: #8A9A5B;
            --bs-warning: #B88746;
            --bs-danger: #9E4350;
            --bs-text: #E8F0F2;
            --bs-muted: #92A7AF;
            --bs-border: rgba(154, 169, 176, 0.18);
        }

        .stApp {
            background: radial-gradient(circle at top right, rgba(0,175,163,0.12), transparent 22%), linear-gradient(180deg, #07141A 0%, #08171D 100%);
            color: var(--bs-text);
        }

        [data-testid="stHeader"] {
            background: rgba(7,20,26,0.72);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0A171D 0%, #0C1A21 100%);
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

        h1, h2, h3 {
            letter-spacing: -0.02em;
            font-weight: 700;
            color: var(--bs-text);
        }

        p, li, .stMarkdown, label, .stCaption {
            color: var(--bs-muted);
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
            background: rgba(16,39,48,0.72);
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
            background: rgba(16,39,48,0.55);
        }

        .bs-pill.ok {
            color: #D8E4D1;
        }

        .bs-pill.muted {
            color: var(--bs-muted);
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(16,39,48,0.88), rgba(13,27,34,0.88));
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
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            color: var(--bs-text);
            font-weight: 700;
            letter-spacing: -0.03em;
        }

        .stButton > button,
        .stDownloadButton > button {
            background: linear-gradient(180deg, #00AFA3 0%, #008E84 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 6px 18px rgba(0, 143, 132, 0.20);
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: linear-gradient(180deg, #14BDB1 0%, #00978E 100%);
            color: #FFFFFF;
        }

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stTextArea textarea {
            background: rgba(16,39,48,0.7);
            color: var(--bs-text);
            border: 1px solid var(--bs-border);
            border-radius: 12px;
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background: var(--bs-primary);
        }

        .stRadio label,
        .stCheckbox label,
        .stToggle label {
            color: var(--bs-text) !important;
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
            border: 1px solid var(--bs-border);
            background: rgba(16,39,48,0.68);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--bs-border);
            border-radius: 14px;
            overflow: hidden;
        }

        .stPlotlyChart {
            background: linear-gradient(180deg, rgba(16,39,48,0.82), rgba(13,27,34,0.82));
            border: 1px solid var(--bs-border);
            border-radius: 18px;
            padding: 0.4rem 0.4rem 0.1rem 0.4rem;
        }

        hr {
            border-color: var(--bs-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
