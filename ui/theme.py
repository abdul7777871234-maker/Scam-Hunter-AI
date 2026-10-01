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


def apply_theme(
    dark: bool,
    accent: str,
):
    """Apply the complete ScamHunter AI theme."""

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

        menu_bg = "#0B1120"
        menu_hover = "#172033"

        color_scheme = "dark"

    else:

        bg = "#F8FAFC"
        panel = "#FFFFFF"
        panel2 = "#F1F5F9"
        input_bg = "#FFFFFF"

        text = "#0F172A"
        muted = "#64748B"

        border = "rgba(15,23,42,0.14)"
        hover = "#E8EEF7"

        menu_bg = "#FFFFFF"
        menu_hover = "#EEF4FA"

        color_scheme = "light"

    css = f"""
    <style>

    /* =========================================================
       ROOT VARIABLES
    ========================================================= */

    :root {{
        --sh-accent: {accent_color};

        --sh-bg: {bg};
        --sh-panel: {panel};
        --sh-panel2: {panel2};
        --sh-input: {input_bg};

        --sh-text: {text};
        --sh-muted: {muted};

        --sh-border: {border};
        --sh-hover: {hover};

        --sh-menu: {menu_bg};
        --sh-menu-hover: {menu_hover};

        --sh-surface-shadow:
            0 12px 40px rgba(0, 0, 0, 0.08);

        color-scheme: {color_scheme};
    }}


    /* =========================================================
       GLOBAL APP
    ========================================================= */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background: var(--sh-bg) !important;
        color: var(--sh-text) !important;
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at 50% -10%,
                {accent_color}18 0%,
                transparent 34%
            ),
            var(--sh-bg) !important;
    }}

    .block-container {{
        max-width: 1320px !important;
        padding-top: 4.5rem !important;
        padding-bottom: 8rem !important;
    }}

    *,
    *::before,
    *::after {{
        box-sizing: border-box;
    }}

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    span,
    label,
    li,
    div {{
        color: inherit;
    }}


    /* =========================================================
       STREAMLIT HEADER
       Prevent black header blocks / black icon backgrounds
    ========================================================= */

    header,
    header[data-testid="stHeader"],
    [data-testid="stHeader"] {{
        background: var(--sh-bg) !important;
        background-color: var(--sh-bg) !important;
        border-bottom: 1px solid var(--sh-border) !important;
        box-shadow: none !important;
    }}

    header *,
    [data-testid="stHeader"] * {{
        color: var(--sh-text) !important;
    }}

    [data-testid="stToolbar"],
    [data-testid="stToolbar"] > div {{
        background: transparent !important;
        box-shadow: none !important;
    }}

    [data-testid="stHeader"] button,
    [data-testid="stToolbar"] button,
    [data-testid="stMainMenu"] button {{
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: var(--sh-text) !important;
    }}

    [data-testid="stHeader"] button:hover,
    [data-testid="stToolbar"] button:hover,
    [data-testid="stMainMenu"] button:hover {{
        background: var(--sh-hover) !important;
        color: var(--sh-accent) !important;
        border-radius: 10px !important;
    }}

    [data-testid="stHeader"] svg,
    [data-testid="stToolbar"] svg,
    [data-testid="stMainMenu"] svg {{
        color: var(--sh-text) !important;
        fill: currentColor !important;
    }}

    [data-testid="stHeader"] button:hover svg,
    [data-testid="stToolbar"] button:hover svg {{
        color: var(--sh-accent) !important;
    }}

    [data-testid="stDecoration"] {{
        display: none !important;
    }}


    /* =========================================================
       SIDEBAR BASE
    ========================================================= */

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] > div > div {{
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }}

    section[data-testid="stSidebar"] {{
        border-right: 1px solid var(--sh-border) !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--sh-text);
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: var(--sh-border) !important;
        opacity: 1 !important;
    }}

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
    section[data-testid="stSidebar"] small {{
        color: var(--sh-muted) !important;
    }}


    /* =========================================================
       SIDEBAR BRANDING
    ========================================================= */

    .sidebar-brand {{
        width: 100%;
        display: flex;
        align-items: center;
        gap: 12px;

        padding: 8px 2px 14px;
    }}

    .sidebar-brand-logo {{
        width: 48px;
        height: 48px;
        min-width: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background:
            linear-gradient(
                145deg,
                {accent_color}20,
                var(--sh-panel2)
            );

        border: 1px solid {accent_color}66;

        color: var(--sh-accent) !important;

        font-size: 23px;
        line-height: 1;

        box-shadow:
            0 0 24px {accent_color}20;
    }}

    .sidebar-brand-text {{
        min-width: 0;
        flex: 1;
    }}

    .sidebar-brand-name {{
        color: var(--sh-text) !important;
        font-size: 18px;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: -0.5px;
        white-space: nowrap;
    }}

    .sidebar-brand-name span {{
        color: var(--sh-accent) !important;
    }}

    .sidebar-brand-subtitle {{
        margin-top: 4px;
        color: var(--sh-muted) !important;
        font-size: 10px;
        line-height: 1.3;
        white-space: nowrap;
    }}

    .sidebar-section-title {{
        color: var(--sh-muted) !important;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
        margin: 8px 0 8px;
    }}

    .sidebar-active-theme {{
        color: var(--sh-muted) !important;
        font-size: 11px;
        text-align: center;
        margin: 8px 0 4px;
    }}

    .sidebar-active-theme strong {{
        color: var(--sh-text) !important;
    }}

    .sidebar-active-theme span {{
        color: var(--sh-muted) !important;
        margin: 0 3px;
    }}


    /* =========================================================
       SIDEBAR COLLAPSE / EXPAND BUTTON
    ========================================================= */

    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {{
        background: transparent !important;
    }}

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {{
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        box-shadow: none !important;

        border-radius: 10px !important;
    }}

    [data-testid="stSidebarCollapseButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {{
        color: var(--sh-text) !important;
        fill: currentColor !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {{
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
        background: var(--sh-hover) !important;
    }}


    /* =========================================================
       SELECTBOX
       Fixes box, arrow, nested BaseWeb layers and popup
    ========================================================= */

    [data-testid="stSelectbox"] {{
        color: var(--sh-text) !important;
    }}

    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] label p {{
        color: var(--sh-text) !important;
        font-weight: 700 !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"],
    section[data-testid="stSidebar"] [data-baseweb="select"] {{
        width: 100% !important;
        background: transparent !important;
        color: var(--sh-text) !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        min-height: 42px !important;

        background: var(--sh-input) !important;
        background-color: var(--sh-input) !important;
        background-image: none !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 12px !important;

        box-shadow: none !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
    section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {{
        background: var(--sh-hover) !important;
        background-color: var(--sh-hover) !important;
        border-color: var(--sh-accent) !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {{
        border-color: var(--sh-accent) !important;
        box-shadow: 0 0 0 1px var(--sh-accent) !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [data-baseweb="select"] input {{
        color: var(--sh-text) !important;
        -webkit-text-fill-color: var(--sh-text) !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"] svg {{
        color: var(--sh-muted) !important;
        fill: currentColor !important;
    }}

    [data-testid="stSelectbox"] [data-baseweb="select"]:hover svg {{
        color: var(--sh-accent) !important;
    }}


    /* =========================================================
       SELECTBOX DROPDOWN POPUP
       Streamlit/BaseWeb popup is rendered outside sidebar,
       therefore global selectors are required.
    ========================================================= */

    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"] {{
        background: var(--sh-menu) !important;
        background-color: var(--sh-menu) !important;

        color: var(--sh-text) !important;

        border-color: var(--sh-border) !important;

        box-shadow:
            0 18px 50px rgba(0, 0, 0, 0.18) !important;
    }}

    [data-baseweb="popover"] {{
        border-radius: 14px !important;
        overflow: hidden !important;
    }}

    [data-baseweb="menu"] {{
        padding: 6px !important;
        border-radius: 14px !important;
    }}

    [data-baseweb="menu"] *,
    [role="listbox"] * {{
        color: var(--sh-text) !important;
    }}

    [role="option"],
    li[role="option"],
    div[role="option"] {{
        background: var(--sh-menu) !important;
        background-color: var(--sh-menu) !important;

        color: var(--sh-text) !important;

        border-radius: 9px !important;
        margin: 2px 0 !important;
    }}

    [role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    [role="option"][aria-selected="true"] {{
        background: var(--sh-menu-hover) !important;
        background-color: var(--sh-menu-hover) !important;

        color: var(--sh-accent) !important;
    }}

    [role="option"] *,
    li[role="option"] *,
    div[role="option"] * {{
        color: inherit !important;
    }}


    /* =========================================================
       BUTTONS
    ========================================================= */

    div.stButton > button {{
        min-height: 40px;

        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 11px !important;

        box-shadow: none !important;
    }}

    div.stButton > button p,
    div.stButton > button span {{
        color: inherit !important;
    }}

    div.stButton > button:hover {{
        background: var(--sh-hover) !important;
        background-color: var(--sh-hover) !important;

        color: var(--sh-accent) !important;

        border-color: var(--sh-accent) !important;
    }}

    div.stButton > button:focus,
    div.stButton > button:focus-visible {{
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
        box-shadow: 0 0 0 1px var(--sh-accent) !important;
    }}


    /* =========================================================
       POPOVER BUTTON
    ========================================================= */

    [data-testid="stPopover"] button,
    button[data-testid="stPopoverButton"] {{
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-text) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 11px !important;

        box-shadow: none !important;
    }}

    [data-testid="stPopover"] button:hover,
    button[data-testid="stPopoverButton"]:hover {{
        background: var(--sh-hover) !important;
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
    }}


    /* =========================================================
       CHAT INPUT
    ========================================================= */

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {{
        background: var(--sh-bg) !important;
        background-color: var(--sh-bg) !important;
    }}

    [data-testid="stChatInput"] {{
        background: transparent !important;
    }}

    [data-testid="stChatInput"] > div {{
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 18px !important;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.06) !important;
    }}

    [data-testid="stChatInput"] > div:focus-within {{
        border-color: var(--sh-accent) !important;
        box-shadow:
            0 0 0 1px var(--sh-accent),
            0 8px 30px rgba(0, 0, 0, 0.08) !important;
    }}

    [data-testid="stChatInput"] textarea {{
        background: transparent !important;
        color: var(--sh-text) !important;
        -webkit-text-fill-color: var(--sh-text) !important;
        caret-color: var(--sh-accent) !important;
    }}

    [data-testid="stChatInput"] textarea::placeholder {{
        color: var(--sh-muted) !important;
        -webkit-text-fill-color: var(--sh-muted) !important;
    }}

    [data-testid="stChatInput"] button {{
        background: var(--sh-panel2) !important;
        background-color: var(--sh-panel2) !important;

        color: var(--sh-muted) !important;

        border: 1px solid transparent !important;
        border-radius: 10px !important;
    }}

    [data-testid="stChatInput"] button:hover {{
        color: var(--sh-accent) !important;
        border-color: var(--sh-accent) !important;
    }}

    [data-testid="stChatInput"] svg {{
        color: currentColor !important;
        fill: currentColor !important;
    }}


    /* =========================================================
       CHAT MESSAGES
    ========================================================= */

    [data-testid="stChatMessage"] {{
        background: transparent !important;
        color: var(--sh-text) !important;
    }}

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {{
        color: var(--sh-text) !important;
    }}


    /* =========================================================
       EXPANDERS
    ========================================================= */

    [data-testid="stExpander"] {{
        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        border: 1px solid var(--sh-border) !important;
        border-radius: 14px !important;

        overflow: hidden;
    }}

    [data-testid="stExpander"] summary {{
        background: var(--sh-panel) !important;
        color: var(--sh-text) !important;
    }}

    [data-testid="stExpander"] summary:hover {{
        background: var(--sh-hover) !important;
    }}

    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] p {{
        color: var(--sh-text) !important;
    }}


    /* =========================================================
       FILE UPLOADER
    ========================================================= */

    section[data-testid="stFileUploaderDropzone"] {{
        background: var(--sh-input) !important;
        background-color: var(--sh-input) !important;

        border: 1px dashed var(--sh-border) !important;
        border-radius: 14px !important;
    }}

    section[data-testid="stFileUploaderDropzone"]:hover {{
        border-color: var(--sh-accent) !important;
    }}

    section[data-testid="stFileUploaderDropzone"] * {{
        color: var(--sh-text) !important;
    }}


    /* =========================================================
       HERO
    ========================================================= */

    .hero {{
        border: 1px solid var(--sh-border);
        border-radius: 24px;

        padding: 42px 30px;

        text-align: center;

        background:
            linear-gradient(
                145deg,
                var(--sh-panel),
                {accent_color}0D
            );

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.08);
    }}

    .hero-logo {{
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
            0 0 28px {accent_color}44;
    }}

    .hero-title {{
        margin-top: 18px;

        font-size: 44px;
        line-height: 1.02;

        font-weight: 800;
        letter-spacing: -2px;

        color: var(--sh-text) !important;
    }}

    .hero-title span {{
        color: var(--sh-accent) !important;
    }}

    .hero-description {{
        max-width: 760px;

        margin: 12px auto 0;

        color: var(--sh-muted) !important;

        font-size: 16px;
        line-height: 1.6;
    }}

    .hero-badge {{
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

        background: {accent_color}0F;
    }}

    .hero-badge-dot {{
        color: var(--sh-accent) !important;
    }}


    /* =========================================================
       SECTION LABELS
    ========================================================= */

    .section-label {{
        color: var(--sh-accent) !important;

        font-size: 11px;
        font-weight: 800;

        letter-spacing: 1.6px;
        text-transform: uppercase;

        margin: 28px 0 12px;
    }}


    /* =========================================================
       INFO CARD
    ========================================================= */

    .info-card {{
        padding: 18px;

        border:
            1px solid var(--sh-border);

        border-radius: 16px;

        background: var(--sh-panel);
        color: var(--sh-text) !important;
    }}

    .info-card-title {{
        display: flex;
        align-items: center;
        gap: 8px;

        font-weight: 800;

        color: var(--sh-text) !important;
    }}

    .info-card-icon {{
        color: var(--sh-accent) !important;
    }}

    .info-card-body {{
        margin-top: 8px;

        color: var(--sh-muted) !important;

        line-height: 1.6;
    }}


    /* =========================================================
       SOURCE / EVIDENCE CARDS
    ========================================================= */

    .source-card {{
        padding: 15px;

        margin: 10px 0;

        border: 1px solid var(--sh-border);
        border-left: 3px solid var(--sh-accent);

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                var(--sh-panel),
                {accent_color}08
            );

        color: var(--sh-text) !important;
    }}

    .source-header {{
        display: flex;
        align-items: flex-start;
        gap: 11px;
    }}

    .source-icon {{
        width: 34px;
        height: 34px;
        min-width: 34px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: {accent_color}12;

        color: var(--sh-accent) !important;
    }}

    .source-heading {{
        min-width: 0;
        flex: 1;
    }}

    .source-title {{
        color: var(--sh-text) !important;

        font-weight: 750;
        font-size: 14px;

        overflow-wrap: anywhere;
    }}

    .source-meta {{
        margin-top: 3px;

        color: var(--sh-muted) !important;

        font-size: 11px;

        overflow-wrap: anywhere;
    }}

    .source-excerpt {{
        margin-top: 12px;

        padding-top: 11px;

        border-top: 1px solid var(--sh-border);

        color: var(--sh-muted) !important;

        font-size: 13px;
        line-height: 1.65;
    }}


    /* =========================================================
       PIPELINE
    ========================================================= */

    .pipeline-card {{
        padding: 16px;
        margin: 8px 0;

        border: 1px solid var(--sh-border);
        border-radius: 16px;

        background:
            linear-gradient(
                135deg,
                var(--sh-panel),
                {accent_color}08
            );
    }}

    .pipeline-step {{
        display: flex;
        align-items: center;

        gap: 12px;

        padding: 10px 12px;
        margin: 6px 0;

        border: 1px solid var(--sh-border);
        border-radius: 12px;

        background: var(--sh-panel2);
    }}

    .pipeline-icon {{
        width: 30px;
        height: 30px;
        min-width: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 9px;

        background: {accent_color}18;
        border: 1px solid {accent_color}44;

        color: var(--sh-accent) !important;

        font-size: 14px;
    }}

    .pipeline-text {{
        flex: 1;
        min-width: 0;
    }}

    .pipeline-name {{
        color: var(--sh-text) !important;

        font-weight: 700;
        font-size: 13px;
    }}

    .pipeline-status {{
        color: var(--sh-muted) !important;

        font-size: 11px;
        margin-top: 2px;
    }}

    .pipeline-arrow {{
        text-align: center;

        color: var(--sh-muted) !important;

        font-size: 13px;

        margin: -2px 0;
    }}


    /* =========================================================
       GENERIC CARD
    ========================================================= */

    .card {{
        border: 1px solid var(--sh-border);
        border-radius: 18px;

        padding: 18px;

        background: var(--sh-panel);
        color: var(--sh-text) !important;
    }}


    /* =========================================================
       MUTED TEXT
    ========================================================= */

    .muted {{
        color: var(--sh-muted) !important;
    }}


    /* =========================================================
       FOOTER
    ========================================================= */

    .footer-card {{
        width: 100%;

        margin-top: 28px;
        padding: 18px 20px;

        text-align: center;

        border: 1px solid var(--sh-border);
        border-radius: 16px;

        background: var(--sh-panel) !important;
        background-color: var(--sh-panel) !important;

        color: var(--sh-muted) !important;

        box-shadow: none;
    }}

    .footer-card *,
    .footer-card span,
    .footer-card p,
    .footer-card div {{
        color: var(--sh-muted) !important;
    }}

    .footer-title {{
        color: var(--sh-text) !important;

        font-size: 12px;
        font-weight: 700;
    }}

    .footer-description {{
        margin-top: 6px;

        color: var(--sh-muted) !important;

        font-size: 11px;
        line-height: 1.55;
    }}


    /* =========================================================
       SIDEBAR KNOWLEDGE STATUS
    ========================================================= */

    .sidebar-status-card {{
        display: flex;
        align-items: center;
        gap: 8px;

        padding: 9px 10px;

        border: 1px solid var(--sh-border);
        border-radius: 10px;

        background: var(--sh-panel2);

        color: var(--sh-muted) !important;

        font-size: 11px;
    }}

    .sidebar-status-dot {{
        width: 7px;
        height: 7px;
        min-width: 7px;

        border-radius: 50%;

        background: var(--sh-accent);

        box-shadow:
            0 0 10px var(--sh-accent);
    }}


    /* =========================================================
       SCROLLBAR
    ========================================================= */

    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: var(--sh-bg);
    }}

    ::-webkit-scrollbar-thumb {{
        background: var(--sh-border);
        border-radius: 999px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: var(--sh-accent);
    }}


    /* =========================================================
       MOBILE
    ========================================================= */

    @media (max-width: 768px) {{

        .block-container {{
            padding-top: 3.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        .hero {{
            padding: 30px 18px;
            border-radius: 20px;
        }}

        .hero-title {{
            font-size: 34px;
        }}

        .hero-description {{
            font-size: 14px;
        }}

        .sidebar-brand-name {{
            font-size: 16px;
        }}

        .sidebar-brand-logo {{
            width: 44px;
            height: 44px;
            min-width: 44px;
        }}
    }}

    </style>
    """

    st.markdown(
        css,
        unsafe_allow_html=True,
    )
