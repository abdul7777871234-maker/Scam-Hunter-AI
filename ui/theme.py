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
        border = "rgba(148,163,184,.22)"
        input_bg = "#0F172A"
        hover = "#172033"
        scheme = "dark"
    else:
        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        text = "#0F172A"
        muted = "#64748B"
        border = "rgba(15,23,42,.14)"
        input_bg = "#FFFFFF"
        hover = "#F1F5F9"
        scheme = "light"

    st.markdown(
        f"""
        <style>

        /* ================= GLOBAL ================= */

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
            --primary-color: {a};
            color-scheme: {scheme};
        }}

        html, body, .stApp, [data-testid="stAppViewContainer"] {{
            background: var(--bg) !important;
            color: var(--text);
        }}

        .stApp {{
            background:
                radial-gradient(circle at 50% -10%, {a}18 0, transparent 32%),
                var(--bg) !important;
        }}

        .block-container {{
            max-width: 1320px;
            padding-top: 4.5rem;      /* keeps hero clear of the header */
            padding-bottom: 8rem;
        }}

        h1, h2, h3, h4, h5, h6, label, p, span, li {{
            color: inherit;
        }}


        /* ================= TOP HEADER / TOOLBAR ================= */

        header[data-testid="stHeader"],
        [data-testid="stHeader"] {{
            background: var(--bg) !important;
            border-bottom: 1px solid var(--border);
        }}

        [data-testid="stToolbar"],
        [data-testid="stToolbar"] *,
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] a,
        [data-testid="stHeader"] svg {{
            color: var(--text) !important;
            fill: var(--text) !important;
        }}

        [data-testid="stHeader"] button:hover {{
            color: var(--accent) !important;
            background: var(--hover) !important;
        }}

        [data-testid="stDecoration"] {{
            display: none;
        }}


        /* ================= SIDEBAR ================= */

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div {{
            background: var(--panel) !important;
        }}

        section[data-testid="stSidebar"] {{
            border-right: 1px solid var(--border);
        }}

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] strong,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: var(--text) !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
        section[data-testid="stSidebar"] small {{
            color: var(--muted) !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: var(--border) !important;
        }}

        [data-testid="stSidebarCollapseButton"] *,
        [data-testid="stSidebarCollapsedControl"] * {{
            color: var(--text) !important;
            fill: var(--text) !important;
        }}


        /* ================= SELECTBOX ================= */

        div[data-baseweb="select"] > div {{
            background: var(--input-bg) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }}

        div[data-baseweb="select"] > div:hover {{
            border-color: var(--accent) !important;
        }}

        div[data-baseweb="select"] > div:focus-within {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }}

        div[data-baseweb="select"] *,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] span {{
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
        }}

        div[data-baseweb="select"] svg {{
            fill: var(--muted) !important;
            color: var(--muted) !important;
        }}

        /* dropdown menu */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        ul[role="listbox"] {{
            background: var(--panel) !important;
            color: var(--text) !important;
            border-radius: 12px !important;
        }}

        div[data-baseweb="popover"] {{
            border: 1px solid var(--border);
        }}

        li[role="option"],
        div[role="option"] {{
            background: var(--panel) !important;
            color: var(--text) !important;
        }}

        li[role="option"] *,
        div[role="option"] * {{
            color: var(--text) !important;
        }}

        li[role="option"]:hover,
        div[role="option"]:hover,
        li[role="option"][aria-selected="true"],
        div[role="option"][aria-selected="true"] {{
            background: var(--hover) !important;
            color: var(--accent) !important;
        }}


        /* ================= BUTTONS ================= */

        div.stButton > button {{
            background: var(--panel) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }}

        div.stButton > button p {{
            color: inherit !important;
        }}

        div.stButton > button:hover,
        div.stButton > button:focus-visible {{
            background: var(--hover) !important;
            color: var(--accent) !important;
            border-color: var(--accent) !important;
        }}

        div.stButton > button:active {{
            background: {a}22 !important;
            color: var(--accent) !important;
        }}


        /* ================= CHAT INPUT + BOTTOM BAR ================= */

        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] {{
            background: var(--bg) !important;
        }}

        div[data-testid="stChatInput"] {{
            background: transparent !important;
        }}

        div[data-testid="stChatInput"] > div {{
            background: var(--panel) !important;
            border: 1px solid var(--border) !important;
            border-radius: 18px !important;
            box-shadow: none !important;
        }}

        div[data-testid="stChatInput"] > div:focus-within {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }}

        div[data-testid="stChatInput"] textarea {{
            background: transparent !important;
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            caret-color: var(--accent);
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: var(--muted) !important;
            -webkit-text-fill-color: var(--muted) !important;
        }}

        div[data-testid="stChatInput"] button {{
            color: var(--text) !important;
            background: var(--panel2) !important;
        }}

        div[data-testid="stChatInput"] button:hover {{
            color: var(--accent) !important;
        }}

        div[data-testid="stChatInput"] svg {{
            fill: currentColor !important;
        }}


        /* ================= CHAT MESSAGES ================= */

        div[data-testid="stChatMessage"],
        div[data-testid="stChatMessage"] p,
        div[data-testid="stChatMessage"] li {{
            color: var(--text) !important;
        }}

        div[data-testid="stChatMessage"] {{
            background: transparent !important;
        }}

        code, pre {{
            background: var(--panel2) !important;
            color: var(--text) !important;
        }}


        /* ================= EXPANDER / ALERTS / UPLOADER ================= */

        div[data-testid="stExpander"] {{
            background: var(--panel) !important;
            border: 1px solid var(--border) !important;
            border-radius: 14px !important;
        }}

        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary * {{
            color: var(--text) !important;
        }}

        section[data-testid="stFileUploaderDropzone"] {{
            background: var(--input-bg) !important;
            border: 1px dashed var(--border) !important;
            border-radius: 14px !important;
        }}

        section[data-testid="stFileUploaderDropzone"] * {{
            color: var(--text) !important;
        }}


        /* ================= HERO ================= */

        .hero {{
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 42px 30px;
            text-align: center;
            background: linear-gradient(145deg, var(--panel), {a}0D);
            box-shadow: 0 20px 60px rgba(0,0,0,.10);
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
            color: var(--text) !important;
        }}

        .hero h1 span {{
            color: {a} !important;
        }}

        .hero p {{
            color: var(--muted) !important;
            font-size: 16px;
        }}

        .badge {{
            display: inline-block;
            margin-top: 12px;
            padding: 8px 14px;
            border: 1px solid {a};
            border-radius: 999px;
            color: {a} !important;
            font-size: 12px;
            background: {a}0F;
        }}


        /* ================= GENERAL CARDS ================= */

        .section-label {{
            color: {a} !important;
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
            color: var(--text);
        }}

        .source {{
            border-left: 3px solid {a};
            padding: 12px 15px;
            margin: 9px 0;
            background: {a}12;
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


        /* ================= SCROLLBARS ================= */

        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 8px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
