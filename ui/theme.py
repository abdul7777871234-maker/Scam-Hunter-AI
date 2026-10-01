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

    a = ACCENTS.get(accent, ACCENTS["Cyan"])

    if dark:
        bg = "#050811"
        panel = "#0B1120"
        panel2 = "#111827"
        text = "#F8FAFC"
        muted = "#94A3B8"
        border = "rgba(148,163,184,.18)"
        input_bg = "#0F172A"
        hover = "#172033"
    else:
        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15,23,42,.10)"
        input_bg = "#FFFFFF"
        hover = "#F1F5F9"

    st.markdown(
        f"""
        <style>

        /* =========================================================
           GLOBAL
           ========================================================= */

        :root {{
            --accent: {a};
            --bg: {bg};
            --panel: {panel};
            --panel2: {panel2};
            --text: {text};
            --muted: {muted};
            --border: {border};
            --input-bg: {input_bg};
            --hover: {hover};
        }}

        .stApp {{
            background:
                radial-gradient(
                    circle at 50% -10%,
                    {a}18 0,
                    transparent 32%
                ),
                var(--bg);

            color: var(--text);
        }}

        .block-container {{
            max-width: 1320px;
            padding-top: 2rem;
            padding-bottom: 7rem;
        }}


        /* =========================================================
           SIDEBAR
           ========================================================= */

        section[data-testid="stSidebar"] {{
            background: var(--panel) !important;
            border-right: 1px solid var(--border);
        }}

        section[data-testid="stSidebar"] * {{
            color: var(--text);
        }}

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {{
            color: var(--muted) !important;
        }}


        /* =========================================================
           SELECTBOX
           ========================================================= */

        div[data-baseweb="select"] > div {{
            background: var(--input-bg) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
        }}

        div[data-baseweb="select"] * {{
            color: var(--text) !important;
        }}

        div[data-baseweb="popover"] {{
            background: var(--panel) !important;
        }}

        div[role="listbox"] {{
            background: var(--panel) !important;
            border: 1px solid var(--border) !important;
        }}

        div[role="option"] {{
            background: var(--panel) !important;
            color: var(--text) !important;
        }}

        div[role="option"]:hover {{
            background: var(--hover) !important;
            color: var(--text) !important;
        }}


        /* =========================================================
           BUTTONS
           ========================================================= */

        div.stButton > button {{
            background: var(--panel) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }}

        div.stButton > button:hover {{
            background: var(--hover) !important;
            color: var(--accent) !important;
            border-color: var(--accent) !important;
        }}


        /* =========================================================
           CHAT INPUT
           ========================================================= */

        div[data-testid="stChatInput"] {{
            background: transparent !important;
        }}

        div[data-testid="stChatInput"] > div {{
            background: var(--panel) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            background: var(--panel) !important;
            color: var(--text) !important;
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: var(--muted) !important;
        }}

        div[data-testid="stChatInput"] button {{
            color: var(--text) !important;
        }}

        div[data-testid="stChatInput"] button:hover {{
            color: var(--accent) !important;
        }}


        /* =========================================================
           CHAT MESSAGES
           ========================================================= */

        div[data-testid="stChatMessage"] {{
            color: var(--text);
        }}

        div[data-testid="stChatMessage"] p,
        div[data-testid="stChatMessage"] li {{
            color: var(--text);
        }}


        /* =========================================================
           HERO
           ========================================================= */

        .hero {{
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 42px 30px;
            text-align: center;
            background:
                linear-gradient(
                    145deg,
                    var(--panel),
                    {a}0D
                );
            box-shadow:
                0 20px 60px rgba(0,0,0,.10);
        }}

        .logo {{
            width: 66px;
            height: 66px;
            border: 1px solid {a};
            border-radius: 20px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            color: {a};
            box-shadow: 0 0 28px {a}44;
        }}

        .hero h1 {{
            font-size: 44px;
            line-height: 1.02;
            margin: 18px 0 10px;
            letter-spacing: -2px;
            color: var(--text);
        }}

        .hero h1 span {{
            color: {a};
        }}

        .hero p {{
            color: var(--muted);
            font-size: 16px;
        }}

        .badge {{
            display: inline-block;
            margin-top: 12px;
            padding: 8px 14px;
            border: 1px solid {a};
            border-radius: 999px;
            color: {a};
            font-size: 12px;
            background: {a}0F;
        }}


        /* =========================================================
           GENERAL CARDS
           ========================================================= */

        .section-label {{
            color: {a};
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.6px;
            text-transform: uppercase;
            margin: 28px 0 12px;
        }}

        .card {{
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px;
            background: var(--panel);
        }}

        .source {{
            border-left: 3px solid {a};
            padding: 12px 15px;
            margin: 9px 0;
            background: {a}09;
            border-radius: 10px;
            color: var(--text);
        }}

        .muted {{
            color: var(--muted) !important;
        }}

        .footer-card {{
            margin-top: 24px;
            text-align: center;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
