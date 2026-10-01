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
    accent_color = ACCENTS.get(
        accent,
        ACCENTS["Cyan"],
    )

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
        scheme = "dark"

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
        scheme = "light"

    css = """
    <style>

    :root {
        --sh-accent: ACCENT;
        --sh-bg: BG;
        --sh-panel: PANEL;
        --sh-panel2: PANEL2;
        --sh-input: INPUT;
        --sh-text: TEXT;
        --sh-muted: MUTED;
        --sh-border: BORDER;
        --sh-hover: HOVER;
        --sh-menu: MENU;
        --sh-menu-hover: MENUHOVER;
        color-scheme: SCHEME;
    }

    /* ==============================
       GLOBAL
    ============================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--sh-bg) !important;
        color: var(--sh-text) !important;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                ACCENT18 0,
                transparent 32%
            ),
            var(--sh-bg) !important;
    }

    .block-container {
        max-width: 1320px !important;
        padding-top: 4.5rem !important;
        padding-bottom: 8rem !important;
    }

    * {
        box-sizing: border-box;
    }

    /* ==============================
       HEADER
    ============================== */

    header,
    [data-testid="stHeader"] {
        background: var(--sh-bg) !important;
        background-color: var(--sh-bg) !important;
        border-bottom: 1px solid var(--sh-border) !important;
        box-shadow: none !important;
    }

    [data-testid="stHeader"] *,
    [data-testid="stToolbar"] * {
        color: var(--sh-text) !important;
    }

    [data-testid="stHeader"] button,
    [data-testid="stToolbar"] button,
    [data-testid="stMainMenu"] button {
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: var(--sh-text) !important;
    }

    [data-testid="stHeader"] button:hover,
    [data-testid="stToolbar"] button:hover {
        background: var(--sh-hover) !important;
        color: var(--sh-accent) !important;
        border-radius: 10px !important;
    }

    [data-testid="stHeader"] svg,
    [data-testid="stToolbar"] svg {
        color: var(--sh-text) !important;
        fill: currentColor !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div {
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid var(--sh-border) !important;
    }

    section[data-testid="stSidebar"] * {
        color: var(--sh-text);
    }

    section[data-testid="stSidebar"] hr {
        border-color: var(--sh-border) !important;
    }

    section[data-testid="stSidebar"] small,
    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] * {
        color: var(--sh-muted) !important;
    }

    /* ==============================
       SIDEBAR BRANDING
    ============================== */

    .sidebar-brand {
        width: 100%;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 2px 14px;
    }

    .sidebar-brand-logo {
        width: 48px;
        height: 48px;
        min-width: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background: ACCENT18;
        border: 1px solid ACCENT66;

        color: var(--sh-accent) !important;
        font-size: 23px;
        line-height: 1;

        box-shadow: 0 0 24px ACCENT20;
    }

    .sidebar-brand-text {
        min-width: 0;
        flex: 1;
    }

    .sidebar-brand-name {
        color: var(--sh-text) !important;
        font-size: 18px;
        line-height: 1.1;
        font-weight: 800;
        white-space: nowrap;
    }

    .sidebar-brand-name span {
        color: var(--sh-accent) !important;
    }

    .sidebar-brand-subtitle {
        margin-top: 4px;
        color: var(--sh-muted) !important;
        font-size: 10px;
        white-space: nowrap;
    }

    .sidebar-section-title {
        color: var(--sh-muted) !important;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 8px 0;
    }

    /* ==============================
       SIDEBAR COLLAPSE
    ============================== */

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;
        color: var(--sh-text) !important;
        border: 1px solid var(--sh-border) !important;
        box-shadow: none !important;
        border-radius: 10px !important;
    }

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        color: var(--sh-text) !important;
        fill: currentColor !important;
    }

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: var(--sh-hover) !important;
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
    }

    /* ==============================
       SELECTBOX
    ============================== */

    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] label p {
        color: var(--sh-text) !important;
        font-weight: 700 !important;
    }

    [data-baseweb="select"] {
        background: transparent !important;
        color: var(--sh-text) !important;
    }

    [data-baseweb="select"] > div {
        min-height: 42px !important;

        background: var(--sh-input) !important;
        background-color: var(--sh-input) !important;
        background-image: none !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 12px !important;

        box-shadow: none !important;
    }

    [data-baseweb="select"] > div:hover {
        background: var(--sh-hover) !important;
        background-color: var(--sh-hover) !important;
        border-color: var(--sh-accent) !important;
    }

    [data-baseweb="select"] * {
        color: var(--sh-text) !important;
        -webkit-text-fill-color: var(--sh-text) !important;
    }

    [data-baseweb="select"] svg {
        color: var(--sh-muted) !important;
        fill: currentColor !important;
    }

    /* ==============================
       DROPDOWN MENU
    ============================== */

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {
        background: var(--sh-menu) !important;
        background-color: var(--sh-menu) !important;
        color: var(--sh-text) !important;
        border-color: var(--sh-border) !important;
    }

    [data-baseweb="menu"] {
        padding: 6px !important;
        border-radius: 14px !important;
    }

    [role="option"],
    li[role="option"],
    div[role="option"] {
        background: var(--sh-menu) !important;
        background-color: var(--sh-menu) !important;
        color: var(--sh-text) !important;
        border-radius: 9px !important;
    }

    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background: var(--sh-menu-hover) !important;
        background-color: var(--sh-menu-hover) !important;
        color: var(--sh-accent) !important;
    }

    /* ==============================
       BUTTONS
    ============================== */

    div.stButton > button {
        min-height: 40px;

        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 11px !important;

        box-shadow: none !important;
    }

    div.stButton > button:hover {
        background: var(--sh-hover) !important;
        background-color: var(--sh-hover) !important;

        color: var(--sh-accent) !important;

        border-color: var(--sh-accent) !important;
    }

    /* ==============================
       POPOVERS
    ============================== */

    [data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"] {
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;
        color: var(--sh-text) !important;
        border: 1px solid var(--sh-border) !important;
        border-radius: 11px !important;
        box-shadow: none !important;
    }

    [data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: var(--sh-hover) !important;
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
    }

    /* ==============================
       CHAT INPUT
    ============================== */

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: var(--sh-bg) !important;
        background-color: var(--sh-bg) !important;
    }

    [data-testid="stChatInput"] > div {
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 18px !important;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--sh-text) !important;
        -webkit-text-fill-color: var(--sh-text) !important;
        caret-color: var(--sh-accent) !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--sh-muted) !important;
        -webkit-text-fill-color: var(--sh-muted) !important;
    }

    [data-testid="stChatInput"] button {
        background: var(--sh-panel2) !important;
        color: var(--sh-muted) !important;
        border: 0 !important;
    }

    [data-testid="stChatInput"] button:hover {
        color: var(--sh-accent) !important;
    }

    /* ==============================
       HERO
    ============================== */

    .hero {
        border: 1px solid var(--sh-border);
        border-radius: 24px;

        padding: 42px 30px;

        text-align: center;

        background:
            linear-gradient(
                145deg,
                var(--sh-panel),
                ACCENT0D
            );

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.08);
    }

    .hero-logo {
        width: 66px;
        height: 66px;

        margin: 0 auto;

        display: flex;
        align-items: center;
        justify-content: center;

        border: 1px solid var(--sh-accent);
        border-radius: 20px;

        font-size: 30px;
        line-height: 1;

        box-shadow:
            0 0 28px ACCENT44;
    }

    .hero-title {
        margin-top: 18px;

        font-size: 44px;
        line-height: 1.02;

        font-weight: 800;
        letter-spacing: -2px;

        color: var(--sh-text) !important;
    }

    .hero-title span {
        color: var(--sh-accent) !important;
    }

    .hero-description {
        max-width: 760px;
        margin: 12px auto 0;

        color: var(--sh-muted) !important;

        font-size: 16px;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        margin-top: 16px;
        padding: 8px 14px;

        border: 1px solid var(--sh-accent);
        border-radius: 999px;

        color: var(--sh-accent) !important;

        font-size: 12px;
        font-weight: 700;

        background: ACCENT0F;
    }

    /* ==============================
       SOURCE CARDS
    ============================== */

    .source-card,
    .source {
        border: 1px solid var(--sh-border);
        border-left: 3px solid var(--sh-accent);

        border-radius: 12px;

        padding: 15px;
        margin: 10px 0;

        background: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }

    .source-header {
        display: flex;
        align-items: flex-start;
        gap: 11px;
    }

    .source-icon {
        width: 34px;
        height: 34px;
        min-width: 34px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: ACCENT12;

        color: var(--sh-accent) !important;
    }

    .source-title {
        color: var(--sh-text) !important;
        font-weight: 750;
        font-size: 14px;
    }

    .source-meta {
        margin-top: 3px;
        color: var(--sh-muted) !important;
        font-size: 11px;
    }

    .source-excerpt {
        margin-top: 12px;
        padding-top: 11px;

        border-top: 1px solid var(--sh-border);

        color: var(--sh-muted) !important;

        font-size: 13px;
        line-height: 1.65;
    }

    /* ==============================
       PIPELINE
    ============================== */

    .pipeline-card {
        padding: 16px;
        margin: 8px 0;

        border: 1px solid var(--sh-border);
        border-radius: 16px;

        background: var(--sh-panel);
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 12px;

        padding: 10px 12px;
        margin: 6px 0;

        border: 1px solid var(--sh-border);
        border-radius: 12px;

        background: var(--sh-panel2);
    }

    .pipeline-icon {
        width: 30px;
        height: 30px;
        min-width: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: ACCENT18;
        border: 1px solid ACCENT44;

        color: var(--sh-accent) !important;
    }

    .pipeline-text {
        flex: 1;
    }

    .pipeline-name {
        color: var(--sh-text) !important;
        font-weight: 700;
        font-size: 13px;
    }

    .pipeline-status {
        color: var(--sh-muted) !important;
        font-size: 11px;
    }

    .pipeline-arrow {
        text-align: center;
        color: var(--sh-muted) !important;
    }

    /* ==============================
       VERDICT
    ============================== */

    .verdict-card {
        display: flex;
        align-items: center;
        gap: 14px;

        padding: 14px 16px;
        margin-bottom: 12px;

        border: 1px solid var(--verdict-color);
        border-left: 4px solid var(--verdict-color);

        border-radius: 14px;

        background: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }

    .verdict-dot {
        width: 15px;
        height: 15px;
        min-width: 15px;

        border-radius: 50%;

        background: var(--verdict-color);

        box-shadow:
            0 0 14px var(--verdict-color);
    }

    .verdict-title {
        color: var(--sh-text) !important;
        font-weight: 700;
    }

    .verdict-note {
        margin-top: 3px;
        color: var(--sh-muted) !important;
        font-size: 13px;
    }

    /* ==============================
       MUTED
    ============================== */

    .muted {
        color: var(--sh-muted) !important;
    }

    /* ==============================
       FOOTER
    ============================== */

    .footer-card {
        width: 100%;

        margin-top: 28px;
        padding: 18px 20px;

        text-align: center;

        border: 1px solid var(--sh-border);
        border-radius: 16px;

        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-muted) !important;
    }

    .footer-card * {
        color: var(--sh-muted) !important;
    }

    .footer-title {
        color: var(--sh-text) !important;
        font-size: 12px;
        font-weight: 700;
    }

    .footer-description {
        margin-top: 6px;
        color: var(--sh-muted) !important;
        font-size: 11px;
        line-height: 1.55;
    }

    /* ==============================
       STATUS CARD
    ============================== */

    .sidebar-status-card {
        display: flex;
        align-items: center;
        gap: 8px;

        padding: 9px 10px;

        border: 1px solid var(--sh-border);
        border-radius: 10px;

        background: var(--sh-panel2);

        color: var(--sh-muted) !important;

        font-size: 11px;
    }

    .sidebar-status-dot {
        width: 7px;
        height: 7px;
        min-width: 7px;

        border-radius: 50%;

        background: var(--sh-accent);
        box-shadow: 0 0 10px var(--sh-accent);
    }

    /* ==============================
       EXPANDERS
    ============================== */

    [data-testid="stExpander"] {
        background: var(--sh-panel) !important;
        border: 1px solid var(--sh-border) !important;
        border-radius: 14px !important;
    }

    [data-testid="stExpander"] summary {
        background: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }

    /* ==============================
       FILE UPLOADER
    ============================== */

    section[data-testid="stFileUploaderDropzone"] {
        background: var(--sh-input) !important;
        border: 1px dashed var(--sh-border) !important;
        border-radius: 14px !important;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: var(--sh-text) !important;
    }

    /* ==============================
       SCROLLBAR
    ============================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--sh-bg);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--sh-border);
        border-radius: 999px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--sh-accent);
    }

    </style>
    """

    css = (
        css
        .replace("ACCENT", accent_color)
        .replace("BG", bg)
        .replace("PANEL2", panel2)
        .replace("PANEL", panel)
        .replace("INPUT", input_bg)
        .replace("TEXT", text)
        .replace("MUTED", muted)
        .replace("BORDER", border)
        .replace("HOVER", hover)
        .replace("MENUHOVER", menu_hover)
        .replace("MENU", menu)
        .replace("SCHEME", scheme)
    )

    st.markdown(
        css,
        unsafe_allow_html=True,
    )
