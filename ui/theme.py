import streamlit as st


ACCENTS = {
    "Cyan": "#22D3EE",
    "Electric Blue": "#3B82F6",
    "Emerald": "#10B981",
    "Violet": "#8B5CF6",
    "Rose": "#F43F5E",
    "Amber": "#F59E0B",
    "Sunset": "#F97316",
}


def apply_theme(dark: bool, accent: str):
    accent_color = ACCENTS.get(accent, ACCENTS["Cyan"])

    if dark:
        bg = "#050811"
        panel = "#0B1120"
        panel2 = "#111827"
        input_bg = "#0F172A"
        text = "#F8FAFC"
        muted = "#94A3B8"
        border = "rgba(148,163,184,0.20)"
        hover = "#172033"
        menu = "#0B1120"
        menu_hover = "#172033"
    else:
        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        input_bg = "#FFFFFF"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15,23,42,0.14)"
        hover = "#E8EEF7"
        menu = "#FFFFFF"
        menu_hover = "#EEF4FA"

    css = f"""
    <style>

    html, body, [data-testid="stAppViewContainer"] {{
        background: {bg} !important;
        color: {text} !important;
    }}

    [data-testid="stHeader"] {{
        background: {bg} !important;
        border-bottom: 1px solid {border};
    }}

    [data-testid="stSidebar"] {{
        background: {panel} !important;
        border-right: 1px solid {border};
    }}

    [data-testid="stSidebar"] > div {{
        background: {panel} !important;
    }}

    .block-container {{
        background: transparent !important;
        color: {text} !important;
    }}

    h1, h2, h3, h4, h5, h6,
    p, span, label, div {{
        color: inherit;
    }}

    .hero {{
        background: linear-gradient(
            135deg,
            {panel},
            {panel2}
        ) !important;
        border: 1px solid {border};
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
    }}

    .hero h1 {{
        margin: 0;
        color: {text} !important;
        font-size: 42px;
        font-weight: 800;
    }}

    .hero p {{
        color: {muted} !important;
        font-size: 16px;
    }}

    .logo {{
        font-size: 42px;
        margin-bottom: 8px;
    }}

    .badge {{
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: {accent_color}22;
        border: 1px solid {accent_color}66;
        color: {accent_color} !important;
        font-weight: 700;
        font-size: 13px;
    }}

    .card,
    .source,
    .source-card,
    .footer-card,
    .verdict-card {{
        background: {panel} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    }}

    .source,
    .source-card {{
        padding: 18px;
        margin: 10px 0;
    }}

    .footer-card {{
        padding: 18px;
        margin-top: 25px;
    }}

    .muted {{
        color: {muted} !important;
    }}

    textarea,
    input {{
        background: {input_bg} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}

    textarea::placeholder,
    input::placeholder {{
        color: {muted} !important;
    }}

    [data-baseweb="select"] > div {{
        background: {menu} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}

    [data-baseweb="select"] * {{
        color: {text} !important;
    }}

    [role="listbox"] {{
        background: {menu} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
    }}

    [role="option"] {{
        background: {menu} !important;
        color: {text} !important;
    }}

    [role="option"]:hover {{
        background: {menu_hover} !important;
    }}

    button {{
        border-radius: 12px !important;
    }}

    .stButton > button {{
        background: {panel2} !important;
        color: {text} !important;
        border: 1px solid {border} !important;
    }}

    .stButton > button:hover {{
        border-color: {accent_color} !important;
        color: {accent_color} !important;
    }}

    [data-testid="stFileUploader"] {{
        background: {panel} !important;
        border: 1px solid {border} !important;
        border-radius: 16px;
        padding: 10px;
    }}

    [data-testid="stFileUploader"] section {{
        background: {panel} !important;
        border-color: {border} !important;
    }}

    [data-testid="stFileUploader"] * {{
        color: {text} !important;
    }}

    [data-testid="stChatInput"] {{
        background: {panel} !important;
        border-color: {border} !important;
    }}

    [data-testid="stChatInput"] textarea {{
        background: {input_bg} !important;
        color: {text} !important;
    }}

    [data-testid="stExpander"] {{
        background: {panel} !important;
        border: 1px solid {border} !important;
        border-radius: 14px;
    }}

    [data-testid="stExpander"] * {{
        color: {text} !important;
    }}

    .sidebar-brand {{
        padding: 18px 8px 24px 8px;
        text-align: center;
    }}

    .sidebar-brand-icon {{
        font-size: 38px;
        margin-bottom: 5px;
    }}

    .sidebar-brand-title {{
        font-size: 22px;
        font-weight: 800;
        color: {text} !important;
    }}

    .sidebar-brand-subtitle {{
        font-size: 12px;
        color: {muted} !important;
        margin-top: 4px;
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def render_footer():
    st.markdown(
        """
        <div class="card footer-card">
            <span class="muted">
                🔒 Evidence is treated as untrusted data.
                <br><br>
                ScamHunter AI provides investigation support
                and does not guarantee the authenticity or safety
                of any person, site, message, or offer.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
