import streamlit as st


def apply_theme() -> None:
    """Inyecta una capa visual sobria sin alterar la lógica existente."""
    st.markdown(
        """
        <style>
        :root {
            --bs-bg: #F4F8F8;
            --bs-surface: #FFFFFF;
            --bs-surface-2: #EDF4F5;
            --bs-surface-3: #E3EEF0;
            --bs-primary: #00AFA3;
            --bs-blue: #1493D1;
            --bs-success: #2E9E5B;
            --bs-warning: #C69236;
            --bs-danger: #C95A67;
            --bs-text: #12313A;
            --bs-muted: #5F7A83;
            --bs-border: rgba(18, 49, 58, 0.12);
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(0, 175, 163, 0.10), transparent 24%),
                radial-gradient(circle at left top, rgba(20, 147, 209, 0.07), transparent 22%),
                linear-gradient(180deg, #F4F8F8 0%, #EEF5F6 100%);
            color: var(--bs-text);
        }

        [data-testid="stHeader"] {
            background: rgba(244, 248, 248, 0.88);
            backdrop-filter: blur(6px);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #EEF5F6 0%, #E8F1F3 100%);
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
            background: rgba(255, 255, 255, 0.92);
            border-radius: 14px;
            margin-bottom: 0.65rem;
            box-shadow: 0 6px 18px rgba(18, 49, 58, 0.06);
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
            background: rgba(237, 244, 245, 0.95);
        }

        .bs-pill.ok {
            color: #2E9E5B;
        }

        .bs-pill.muted {
            color: var(--bs-muted);
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(237, 244, 245, 0.98));
            border: 1px solid var(--bs-border);
            border-radius: 16px;
            padding: 0.75rem 0.85rem;
            min-height: 130px;
            box-shadow: 0 8px 24px rgba(18, 49, 58, 0.06);
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
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 6px 18px rgba(0, 143, 132, 0.18);
            text-shadow: none !important;
        }

        .stButton > button *,
        .stDownloadButton > button * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: linear-gradient(180deg, #14BDB1 0%, #00978E 100%);
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.96);
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
            background: rgba(255, 255, 255, 0.94);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--bs-border);
            border-radius: 14px;
            overflow: hidden;
            background: #FFFFFF;
        }

        hr {
            border-color: var(--bs-border);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
