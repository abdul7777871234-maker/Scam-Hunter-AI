
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


def apply_theme(dark=False, accent="Cyan"):

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
        border = "rgba(148,163,184,0.22)"
        hover = "#172033"
    else:
        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15,23,42,0.14)"
        hover = "#E2E8F0"

    css = """
<style>

:root {
    --accent: ACCENT;
    --bg: BG;
    --panel: PANEL;
    --panel2: PANEL2;
    --text: TEXT;
    --muted: MUTED;
    --border: BORDER;
    --hover: HOVER;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    max-width: 1320px;
    padding-top: 4rem;
    padding-bottom: 8rem;
}


/* Sidebar */

section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div {
    background: var(--panel) !important;
}

section[data-testid="stSidebar"] {
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--text) !important;
}


/* Buttons */

div.stButton > button {
    background: var(--panel) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

div.stButton > button:hover {
    background: var(--hover) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}


/* Select boxes */

div[data-baseweb="select"] > div {
    background: var(--panel) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] * {
    color: var(--text) !important;
}


/* Chat input */

div[data-testid="stChatInput"] > div {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
}

div[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}


/* Expanders */

div[data-testid="stExpander"] {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}

div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary * {
    color: var(--text) !important;
}


/* Hero */

.hero {
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 42px 30px;
    text-align: center;
    background: var(--panel);
}

.logo {
    width: 66px;
    height: 66px;
    border: 1px solid ACCENT;
    border-radius: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    color: ACCENT;
}

.hero h1 {
    font-size: 44px;
    line-height: 1.02;
    margin: 18px 0 10px;
    color: var(--text) !important;
}

.hero h1 span {
    color: ACCENT !important;
}

.hero p {
    color: var(--muted) !important;
    font-size: 16px;
}

.badge {
    display: inline-block;
    margin-top: 12px;
    padding: 8px 14px;
    border: 1px solid ACCENT;
    border-radius: 999px;
    color: ACCENT !important;
    font-size: 12px;
}


/* Investigation Pipeline */

.pipeline-card {
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px;
    margin: 8px 0;
    background: var(--panel);
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
    background: ACCENT;
    color: white !important;
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


/* Source cards */

.source {
    border-left: 3px solid ACCENT;
    padding: 12px 15px;
    margin: 9px 0;
    background: var(--panel2);
    border-radius: 10px;
    color: var(--text);
}

.muted {
    color: var(--muted) !important;
}

.card {
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    background: var(--panel);
    color: var(--text);
}

.footer-card {
    margin-top: 24px;
    text-align: center;
}

</style>
"""

    css = css.replace(
        "ACCENT",
        accent_color,
    )

    css = css.replace(
        "BG",
        bg,
    )

    css = css.replace(
        "PANEL2",
        panel2,
    )

    css = css.replace(
        "PANEL",
        panel,
    )

    css = css.replace(
        "TEXT",
        text,
    )

    css = css.replace(
        "MUTED",
        muted,
    )

    css = css.replace(
        "BORDER",
        border,
    )

    css = css.replace(
        "HOVER",
        hover,
    )

    st.markdown(
        css,
        unsafe_allow_html=True,
    )

