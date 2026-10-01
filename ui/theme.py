from __future__ import annotations

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
        text = "#F8FAFC"
        muted = "#94A3B8"
        border = "rgba(148,163,184,.22)"
        input_bg = "#0F172A"
        hover = "#172033"
        color_scheme = "dark"
    else:
        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15,23,42,.14)"
        input_bg = "#FFFFFF"
        hover = "#F1F5F9"
        color_scheme = "light"

    css = """
    <style>

    /* =========================================================
       GLOBAL
    ========================================================= */

    :root {
        --accent: __ACCENT__;
        --bg: __BG__;
        --panel: __PANEL__;
        --panel2: __PANEL2__;
        --text: __TEXT__;
        --muted: __MUTED__;
        --border: __BORDER__;
        --input-bg: __INPUT_BG__;
        --hover: __HOVER__;
        --primary-color: __ACCENT__;
        color-scheme: __COLOR_SCHEME__;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"] {
        background: __BG__ !important;
        color: __TEXT__;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                __ACCENT__18 0,
                transparent 32%
            ),
            __BG__ !important;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 4.5rem;
        padding-bottom: 8rem;
    }

    h1, h2, h3, h4, h5, h6,
    label, p, span, li {
        color: inherit;
    }


    /* =========================================================
       HEADER
    ========================================================= */

    header[data-testid="stHeader"],
    [data-testid="stHeader"] {
        background: __BG__ !important;
        border-bottom: 1px solid __BORDER__;
    }

    [data-testid="stToolbar"],
    [data-testid="stToolbar"] *,
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a {
        color: __TEXT__ !important;
    }

    [data-testid="stToolbar"] {
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
        right: 1rem !important;
    }

    [data-testid="stToolbar"] button,
    [data-testid="stMainMenu"] button,
    [data-testid="stHeader"] button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Header icons: color only, never fill child shapes */
    [data-testid="stHeader"] svg,
    [data-testid="stToolbar"] svg,
    [data-testid="stMainMenu"] svg {
        fill: currentColor !important;
        color: __TEXT__ !important;
    }

    [data-testid="stHeader"] button:hover {
        color: __ACCENT__ !important;
        background: __HOVER__ !important;
    }

    [data-testid="stHeader"] button:hover svg {
        color: __ACCENT__ !important;
    }

    [data-testid="stDecoration"] {
        display: none;
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: __PANEL__ !important;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid __BORDER__;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"]
    [data-testid="stMarkdownContainer"] p {
        color: __TEXT__ !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] *,
    section[data-testid="stSidebar"] small {
        color: __MUTED__ !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: __BORDER__ !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarCollapsedControl"] * {
        color: __TEXT__ !important;
    }


    /* =========================================================
       SELECTBOX (forces every nested BaseWeb layer)
    ========================================================= */

    [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] div,
    div[data-baseweb="select"] > div {
        background-color: __INPUT_BG__ !important;
        color: __TEXT__ !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        border: 1px solid __BORDER__ !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: __ACCENT__ !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: __ACCENT__ !important;
        box-shadow: 0 0 0 1px __ACCENT__ !important;
    }

    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {
        color: __TEXT__ !important;
        -webkit-text-fill-color: __TEXT__ !important;
    }

    div[data-baseweb="select"] svg {
        fill: __MUTED__ !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="popover"] {
        border: 1px solid __BORDER__;
    }

    li[role="option"],
    div[role="option"] {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
    }

    li[role="option"]:hover,
    div[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: __HOVER__ !important;
        color: __ACCENT__ !important;
    }


    /* Selectbox: maximum specificity so nothing can override it */
    html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"],
    html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
    html body .stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: __INPUT_BG__ !important;
        background-color: __INPUT_BG__ !important;
        background-image: none !important;
        color: __TEXT__ !important;
        border-color: __BORDER__ !important;
    }


    /* =========================================================
       BUTTONS
    ========================================================= */

    div.stButton > button {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div.stButton > button p {
        color: inherit !important;
    }

    div.stButton > button:hover,
    div.stButton > button:focus-visible {
        background: __HOVER__ !important;
        color: __ACCENT__ !important;
        border-color: __ACCENT__ !important;
    }


    /* =========================================================
       POPOVER
    ========================================================= */

    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"] {
        background: __PANEL__ !important;
        color: __TEXT__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: __HOVER__ !important;
        border-color: __ACCENT__ !important;
    }


    /* =========================================================
       CHAT INPUT
    ========================================================= */

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: __BG__ !important;
    }

    div[data-testid="stChatInput"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] > div {
        background: __PANEL__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 18px !important;
        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] > div:focus-within {
        border-color: __ACCENT__ !important;
        box-shadow: 0 0 0 1px __ACCENT__ !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: __TEXT__ !important;
        -webkit-text-fill-color: __TEXT__ !important;
        caret-color: __ACCENT__;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: __MUTED__ !important;
        -webkit-text-fill-color: __MUTED__ !important;
    }

    /* "+" attach icon and send arrow */
    div[data-testid="stChatInput"] button {
        background: __PANEL2__ !important;
        color: __MUTED__ !important;
        border-radius: 10px !important;
    }

    div[data-testid="stChatInput"] svg {
        fill: currentColor !important;
        color: inherit !important;
    }

    div[data-testid="stChatInput"] button:hover {
        color: __ACCENT__ !important;
    }


    /* =========================================================
       CHAT MESSAGES
    ========================================================= */

    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li {
        color: __TEXT__ !important;
    }

    div[data-testid="stChatMessage"] {
        background: transparent !important;
    }


    /* =========================================================
       EXPANDERS
    ========================================================= */

    div[data-testid="stExpander"] {
        background: __PANEL__ !important;
        border: 1px solid __BORDER__ !important;
        border-radius: 14px !important;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary * {
        color: __TEXT__ !important;
    }


    /* =========================================================
       FILE UPLOADER
    ========================================================= */

    section[data-testid="stFileUploaderDropzone"] {
        background: __INPUT_BG__ !important;
        border: 1px dashed __BORDER__ !important;
        border-radius: 14px !important;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: __TEXT__ !important;
    }


    /* =========================================================
       HERO
    ========================================================= */

    .hero {
        border: 1px solid __BORDER__;
        border-radius: 24px;
        padding: 42px 30px;
        text-align: center;
        background: linear-gradient(
            145deg,
            __PANEL__,
            __ACCENT__0D
        );
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.10);
    }

    .logo {
        width: 66px;
        height: 66px;
        border: 1px solid __ACCENT__;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: __ACCENT__;
        box-shadow: 0 0 28px __ACCENT__44;
    }

    .hero h1 {
        font-size: 44px;
        line-height: 1.02;
        margin: 18px 0 10px;
        letter-spacing: -2px;
        color: __TEXT__ !important;
    }

    .hero h1 span {
        color: __ACCENT__ !important;
    }

    .hero p {
        color: __MUTED__ !important;
        font-size: 16px;
    }

    .badge {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 14px;
        border: 1px solid __ACCENT__;
        border-radius: 999px;
        color: __ACCENT__ !important;
        font-size: 12px;
        background: __ACCENT__0F;
    }


    /* =========================================================
       INVESTIGATION PIPELINE
    ========================================================= */

    .pipeline-card {
        border: 1px solid __BORDER__;
        border-radius: 16px;
        padding: 16px;
        margin: 8px 0;
        background: linear-gradient(
            135deg,
            __PANEL__,
            __ACCENT__08
        );
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        margin: 6px 0;
        border: 1px solid __BORDER__;
        border-radius: 12px;
        background: __PANEL2__;
    }

    .pipeline-icon {
        width: 30px;
        height: 30px;
        min-width: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: __ACCENT__18;
        border: 1px solid __ACCENT__44;
        color: __ACCENT__ !important;
        font-size: 14px;
    }

    .pipeline-text {
        flex: 1;
    }

    .pipeline-name {
        color: __TEXT__ !important;
        font-weight: 700;
        font-size: 13px;
    }

    .pipeline-status {
        color: __MUTED__ !important;
        font-size: 11px;
        margin-top: 2px;
    }

    .pipeline-arrow {
        text-align: center;
        color: __MUTED__ !important;
        font-size: 13px;
        margin: -2px 0;
    }


    /* =========================================================
       GENERAL CARDS
    ========================================================= */

    .section-label {
        color: __ACCENT__ !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.6px;
        text-transform: uppercase;
        margin: 28px 0 12px;
    }

    .card {
        border: 1px solid __BORDER__;
        border-radius: 18px;
        padding: 18px;
        background: __PANEL__;
        color: __TEXT__;
    }

    .source {
        border-left: 3px solid __ACCENT__;
        padding: 12px 15px;
        margin: 9px 0;
        background: __ACCENT__12;
        border-radius: 10px;
        color: __TEXT__;
    }

    .muted {
        color: __MUTED__ !important;
    }

    .footer-card {
        margin-top: 24px;
        text-align: center;
    }


    /* =========================================================
       SCROLLBAR
    ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: __BORDER__;
        border-radius: 8px;
    }

    </style>
    """

    css = (
        css
        .replace("__ACCENT__", accent_color)
        .replace("__BG__", bg)
        .replace("__PANEL__", panel)
        .replace("__PANEL2__", panel2)
        .replace("__TEXT__", text)
        .replace("__MUTED__", muted)
        .replace("__BORDER__", border)
        .replace("__INPUT_BG__", input_bg)
        .replace("__HOVER__", hover)
        .replace("__COLOR_SCHEME__", color_scheme)
    )

    st.markdown(css, unsafe_allow_html=True)


def render_footer():
    """Footer HTML on a single unindented string, so Markdown never treats it as a code block."""
    html = (
        '<div class="card footer-card"><span class="muted">'
        '\U0001F512 Evidence is treated as untrusted data.<br><br>'
        'ScamHunter AI provides investigation support and does not guarantee '
        'the authenticity or safety of any person, site, message, or offer.'
        '</span></div>'
    )
    st.markdown(html, unsafe_allow_html=True)
