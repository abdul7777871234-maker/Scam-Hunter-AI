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
        background = "#050811"
        panel = "#0B1120"
        panel_alt = "#111827"
        input_background = "#0F172A"
        text = "#F8FAFC"
        muted = "#94A3B8"
        border = "rgba(148, 163, 184, 0.20)"
        hover = "#172033"
    else:
        background = "#F8FAFC"
        panel = "#FFFFFF"
        panel_alt = "#F1F5F9"
        input_background = "#FFFFFF"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15, 23, 42, 0.14)"
        hover = "#E8EEF7"

    css = """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    html,
    body,
    [data-testid="stAppViewContainer"] {
        background: __BACKGROUND__ !important;
        color: __TEXT__ !important;
    }

    [data-testid="stApp"] {
        background: __BACKGROUND__ !important;
    }

    [data-testid="stHeader"] {
        background: __BACKGROUND__ !important;
        border-bottom: 1px solid __BORDER__ !important;
    }

    .main {
        background: transparent !important;
    }

    .block-container {
        background: transparent !important;
        color: __TEXT__ !important;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* =========================
       TEXT
       ========================= */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: __TEXT__ !important;
    }

    p,
    label,
    span {
        color: inherit;
    }

    .muted {
        color: __MUTED__ !important;
    }

    /* =========================
       HERO
       ========================= */

    .hero {
        background: linear-gradient(
            135deg,
            __PANEL__,
            __PANEL_ALT__
        ) !important;

        border: 1px solid __BORDER__ !important;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }

    .hero .logo {
        font-size: 42px;
        line-height: 1;
        margin-bottom: 10px;
    }

    .hero h1 {
        color: __TEXT__ !important;
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }

    .hero p {
        color: __MUTED__ !important;
        font-size: 16px;
        line-height: 1.6;
        margin-top: 10px;
    }

    .badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: __ACCENT_ALPHA__ !important;
        border: 1px solid __ACCENT_BORDER__ !important;
        color: __ACCENT__ !important;
        font-size: 13px;
        font-weight: 700;
    }

    /* =========================
       CARDS
       ========================= */

    .card,
    .source,
    .source-card,
    .footer-card,
    .verdict-card {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 18px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }

    .source,
    .source-card {
        padding: 18px;
        margin: 10px 0;
    }

    .footer-card {
        padding: 20px;
        margin-top: 28px;
    }

    /* =========================
       SIDEBAR
       ========================= */

    [data-testid="stSidebar"] {
        background: __PANEL__ !important;
        border-right: 1px solid __BORDER__ !important;
    }

    [data-testid="stSidebar"] > div {
        background: __PANEL__ !important;
    }

    .sidebar-brand {
        padding: 18px 8px 24px 8px;
        text-align: center;
    }

    .sidebar-brand-icon {
        font-size: 40px;
        line-height: 1;
        margin-bottom: 8px;
    }

    .sidebar-brand-title {
        color: __TEXT__ !important;
        font-size: 23px;
        font-weight: 800;
    }

    .sidebar-brand-subtitle {
        color: __MUTED__ !important;
        font-size: 12px;
        margin-top: 5px;
    }

    /* =========================
       SELECTBOX
       ========================= */

    [data-baseweb="select"] > div {
        background: __PANEL_ALT__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 10px !important;
    }

    [data-baseweb="select"] input {
        color: __TEXT__ !important;
    }

    [data-baseweb="select"] span {
        color: __TEXT__ !important;
    }

    [role="listbox"] {
        background: __PANEL__ !important;
        border: 1px solid __BORDER__ !important;
        color: __TEXT__ !important;
    }

    [role="option"] {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
    }

    [role="option"]:hover {
        background: __HOVER__ !important;
    }

    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {
        background: __PANEL_ALT__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 12px !important;
        min-height: 42px;
    }

    .stButton > button:hover {
        background: __HOVER__ !important;
        border-color: __ACCENT__ !important;
        color: __ACCENT__ !important;
    }

    /* =========================
       INPUTS
       ========================= */

    textarea,
    input {
        background: __INPUT__ !important;
        color: __TEXT__ !important;
        border-color: __BORDER__ !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: __MUTED__ !important;
    }

    [data-testid="stChatInput"] {
        background: __PANEL__ !important;
        border-color: __BORDER__ !important;
    }

    [data-testid="stChatInput"] textarea {
        background: __INPUT__ !important;
        color: __TEXT__ !important;
    }

    /* =========================
       FILE UPLOADER
       ========================= */

    [data-testid="stFileUploader"] {
        background: __PANEL__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 16px !important;
        padding: 10px;
    }

    [data-testid="stFileUploader"] section {
        background: __PANEL__ !important;
        border-color: __BORDER__ !important;
    }

    [data-testid="stFileUploader"] * {
        color: __TEXT__ !important;
    }

    /* =========================
       EXPANDERS
       ========================= */

    [data-testid="stExpander"] {
        background: __PANEL__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 14px !important;
    }

    [data-testid="stExpander"] * {
        color: __TEXT__ !important;
    }

    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color: __BORDER__ !important;
    }

    /* =========================
       FOOTER
       ========================= */

    .footer-card,
    .footer-card span,
    .footer-card p {
        color: __MUTED__ !important;
    }

    /* =========================
       SCROLLBAR
       ========================= */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: __BACKGROUND__;
    }

    ::-webkit-scrollbar-thumb {
        background: __PANEL_ALT__;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: __ACCENT__;
    }

    </style>
    """

    css = css.replace("__BACKGROUND__", background)
    css = css.replace("__PANEL__", panel)
    css = css.replace("__PANEL_ALT__", panel_alt)
    css = css.replace("__INPUT__", input_background)
    css = css.replace("__TEXT__", text)
    css = css.replace("__MUTED__", muted)
    css = css.replace("__BORDER__", border)
    css = css.replace("__HOVER__", hover)
    css = css.replace("__ACCENT__", accent_color)
    css = css.replace(
        "__ACCENT_ALPHA__",
        accent_color + "22",
    )
    css = css.replace(
        "__ACCENT_BORDER__",
        accent_color + "66",
    )

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
