import streamlit as st


def apply_theme() -> None:
    """Inyecta una capa visual sobria y legible sin alterar la lógica existente."""
    st.markdown(
        """
        <style>
        :root {
            --bs-bg: #08161C;
            --bs-surface: #10242C;
            --bs-surface-2: #16313B;
            --bs-surface-3: #1D3E49;
            --bs-primary: #00C7B7;
            --bs-blue: #0099E5;
            --bs-success: #27AE60;
            --bs-warning: #D6A23D;
            --bs-danger: #D95C68;
            --bs-text: #F7FBFC;
            --bs-muted: #D3E0E5;
            --bs-border: rgba(179, 205, 214, 0.24);
            --bs-button-text: #061115;
        }

        .stApp {
            background:
                radial-gradient(circle at top right, rgba(0, 199, 183, 0.10), transparent 26%),
                radial-gradient(circle at left center, rgba(0, 153, 229, 0.08), transparent 22%),
                linear-gradient(180deg, #08161C 0%, #0D1F26 100%);
            color: var(--bs-text);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stHeader"] {
            background: rgba(8, 22, 28, 0.78);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0E2027 0%, #112730 100%);
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
            opacity: 0.98;
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
            background: rgba(22, 49, 59, 0.82);
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
            background: rgba(22, 49, 59, 0.62);
        }

        .bs-pill.ok {
            color: #DDF7E8;
        }

        .bs-pill.muted {
            color: var(--bs-text);
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(22, 49, 59, 0.94), rgba(16, 36, 44, 0.96));
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
            background: linear-gradient(180deg, #D6A23D 0%, #BE8D2E 100%) !important;
            color: var(--bs-button-text) !important;
            -webkit-text-fill-color: var(--bs-button-text) !important;
            border: 1px solid rgba(255, 226, 163, 0.30) !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            text-shadow: none !important;
            box-shadow: 0 6px 18px rgba(190, 141, 46, 0.24) !important;
        }

        .stButton > button *,
        .stDownloadButton > button *,
        div[data-testid="stButton"] > button *,
        div[data-testid="stDownloadButton"] > button *,
        button[kind="primary"] * {
            color: var(--bs-button-text) !important;
            fill: var(--bs-button-text) !important;
            stroke: var(--bs-button-text) !important;
            -webkit-text-fill-color: var(--bs-button-text) !important;
            opacity: 1 !important;
            text-shadow: none !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        div[data-testid="stButton"] > button:hover,
        div[data-testid="stDownloadButton"] > button:hover,
        button[kind="primary"]:hover {
            background: linear-gradient(180deg, #E0AD4A 0%, #C69331 100%) !important;
            color: var(--bs-button-text) !important;
            -webkit-text-fill-color: var(--bs-button-text) !important;
            box-shadow: 0 8px 22px rgba(198, 147, 49, 0.30) !important;
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
            color: var(--bs-button-text) !important;
            -webkit-text-fill-color: var(--bs-button-text) !important;
            outline: none !important;
        }

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stTextArea textarea {
            background: rgba(22, 49, 59, 0.82);
            color: var(--bs-text);
            border: 1px solid var(--bs-border);
            border-radius: 12px;
        }

        
