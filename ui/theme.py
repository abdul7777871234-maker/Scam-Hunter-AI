
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
    accent_color = ACCENTS.get(
        accent,
        ACCENTS["Cyan"],
    )

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
        background: var(--bg) !important;
        color: var(--text);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -10%,
                __ACCENT__18 0,
                transparent 32%
            ),
            var(--bg) !important;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 4.5rem;
        padding-bottom: 8rem;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    label,
    p,
    span,
    li {
        color: inherit;
    }


    /* =========================================================
       HEADER
    ========================================================= */

    header[data-testid="stHeader"],
    [data-testid="stHeader"] {
        background: var(--bg) !important;
        border-bottom: 1px solid var(--border);
    }

    [data-testid="stToolbar"],
    [data-testid="stToolbar"] *,
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] a {
        color: var(--text) !important;
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

    [data-testid="stToolbar"] svg,
    [data-testid="stMainMenu"] svg {
        fill: currentColor !important;
    }

    [data-testid="stHeader"] button:hover {
        color: var(--accent) !important;
        background: var(--hover) !important;
    }

    [data-testid="stDecoration"] {
        display: none;
    }


    /* =========================================================
       SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background: var(--panel) !important;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] label p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"]
    [data-testid="stMarkdownContainer"] p {
        color: var(--text) !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] *,
    section[data-testid="stSidebar"] small {
        color: var(--muted) !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: var(--border) !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarCollapsedControl"] * {
        color: var(--text) !important;
    }


    /* =========================================================
       SELECTBOX
    ========================================================= */

    div[data-baseweb="select"] > div {
        background: var(--input-bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: var(--accent) !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    div[data-baseweb="select"] *,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span {
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
    }

    div[data-baseweb="select"] svg {
        fill: var(--muted) !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: var(--panel) !important;
        color: var(--text) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="popover"] {
        border: 1px solid var(--border);
    }

    li[role="option"],
    div[role="option"] {
        background: var(--panel) !important;
        color: var(--text) !important;
    }

    li[role="option"]:hover,
    div[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {
        background: var(--hover) !important;
        color: var(--accent) !important;
    }


    /* =========================================================
       BUTTONS
    ========================================================= */

    div.stButton > button {
        background: var(--panel) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div.stButton > button p {
        color: inherit !important;
    }

    div.stButton > button:hover,
    div.stButton > button:focus-visible {
        background: var(--hover) !important;
        color: var(--accent) !important;
        border-color: var(--accent) !important;
    }


    /* =========================================================
       POPOVER
    ========================================================= */

    div[data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"] {
        background: var(--panel) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    div[data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {
        background: var(--hover) !important;
        border-color: var(--accent) !important;
    }


    /* =========================================================
       CHAT INPUT
    ========================================================= */

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background: var(--bg) !important;
    }

    div[data-testid="stChatInput"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] > div {
        background: var(--panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: none !important;
    }

    div[data-testid="stChatInput"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    div[data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        caret-color: var(--accent);
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
    }


    /* =========================================================
       CHAT MESSAGES
    ========================================================= */

    div[data-testid="stChatMessage"],
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li {
        color: var(--text) !important;
    }

    div[data-testid="stChatMessage"] {
        background: transparent !important;
    }


    /* =========================================================
       EXPANDERS
    ========================================================= */

    div[data-testid="stExpander"] {
        background: var(--panel) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary * {
        color: var(--text) !important;
    }


    /* =========================================================
       FILE UPLOADER
    ========================================================= */

    section[data-testid="stFileUploaderDropzone"] {
        background: var(--input-bg) !important;
        border: 1px dashed var(--border) !important;
        border-radius: 14px !important;
    }

    section[data-testid="stFileUploaderDropzone"] * {
        color: var(--text) !important;
    }


    /* =========================================================
       HERO
    ========================================================= */

    .hero {
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 42px 30px;
        text-align: center;
        background: linear-gradient(
            145deg,
            var(--panel),
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
        color: var(--text) !important;
    }

    .hero h1 span {
        color: __ACCENT__ !important;
    }

    .hero p {
        color: var(--muted) !important;
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
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 16px;
        margin: 8px 0;
        background: linear-gradient(
            135deg,
            var(--panel),
            __ACCENT__08
        );
    }

    .pipeline-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        margin: 6px 0;
        border: 1px solid var(--border);
        border-radius: 12px;
        background: var(--panel2);
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
        color: var(--text) !important;
        font-weight: 700;
        font-size: 13px;
    }

    .pipeline-status {
        color: var(--muted) !important;
        font-size: 11px;
        margin-top: 2px;
    }

    .pipeline-arrow {
        text-align: center;
        color: var(--muted) !important;
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
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        background: var(--panel);
        color: var(--text);
    }

    .source {
        border-left: 3px solid __ACCENT__;
        padding: 12px 15px;
        margin: 9px 0;
        background: __ACCENT__12;
        border-radius: 10px;
        color: var(--text);
    }

    .muted {
        color: var(--muted) !important;
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
        background: var(--border);
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

    st.markdown(
        css,
        unsafe_allow_html=True,
    )
