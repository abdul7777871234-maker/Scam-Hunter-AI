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

DARK = {
    "BG": "#050811", "PANEL": "#0B1120", "PANEL2": "#111827",
    "INPUT": "#0F172A", "TEXT": "#F8FAFC", "MUTED": "#94A3B8",
    "SELECT_BG": "#1E293B", "SELECT_TEXT": "#F1F5F9", "SELECT_ARROW": "#CBD5E1", "SELECT_BORDER": "#334155",
    "BORDER": "rgba(148,163,184,0.20)", "HOVER": "#172033",
    "MENU": "#0B1120", "MENUHOVER": "#172033", "SCHEME": "dark",
}
LIGHT = {
    "BG": "#F8FAFC", "PANEL": "#FFFFFF", "PANEL2": "#F1F5F9",
    "INPUT": "#FFFFFF", "TEXT": "#0F172A", "MUTED": "#64748B",
    "SELECT_BG": "#FFFFFF", "SELECT_TEXT": "#0F172A", "SELECT_ARROW": "#334155", "SELECT_BORDER": "#CBD5E1",
    "BORDER": "rgba(15,23,42,0.14)", "HOVER": "#E8EEF7",
    "MENU": "#FFFFFF", "MENUHOVER": "#EEF4FA", "SCHEME": "light",
}

# Tokens are written @@NAME@@ so one token can never be a substring of another
# (the old .replace("HOVER") also rewrote the inside of "MENUHOVER").
CSS = """
<style>
:root{
  --sh-accent:@@ACCENT@@; --sh-bg:@@BG@@; --sh-panel:@@PANEL@@; --sh-panel2:@@PANEL2@@;
  --sh-input:@@INPUT@@; --sh-text:@@TEXT@@; --sh-muted:@@MUTED@@; --sh-border:@@BORDER@@;
  --sh-hover:@@HOVER@@; --sh-menu:@@MENU@@; --sh-menu-hover:@@MENUHOVER@@;
  --sh-input-bg:@@INPUT@@; --sh-input-text:@@TEXT@@; --sh-input-arrow:@@MUTED@@;
  --sh-select-bg:@@SELECT_BG@@; --sh-select-text:@@SELECT_TEXT@@; --sh-select-arrow:@@SELECT_ARROW@@; --sh-select-border:@@SELECT_BORDER@@;
  --sh-scheme:@@SCHEME@@;\n  color-scheme:var(--sh-scheme);
}

/* GLOBAL */
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--sh-bg)!important; color:var(--sh-text)!important; color-scheme:var(--sh-scheme)!important;}
.stApp{background:radial-gradient(circle at 50% -10%,@@ACCENT@@18 0,transparent 32%),var(--sh-bg)!important;}
.block-container{max-width:1320px!important;padding-top:4.5rem!important;padding-bottom:8rem!important;}
* {box-sizing:border-box;}

/* HEADER */
header,[data-testid="stHeader"]{background:var(--sh-bg)!important;background-color:var(--sh-bg)!important;
  border-bottom:1px solid var(--sh-border)!important;box-shadow:none!important;}
[data-testid="stHeader"] *,[data-testid="stToolbar"] *{color:var(--sh-text)!important;}
[data-testid="stHeader"] button,[data-testid="stToolbar"] button,[data-testid="stMainMenu"] button{
  background:transparent!important;border:0!important;box-shadow:none!important;color:var(--sh-text)!important;}
[data-testid="stHeader"] button:hover,[data-testid="stToolbar"] button:hover{
  background:var(--sh-hover)!important;color:var(--sh-accent)!important;border-radius:10px!important;}
[data-testid="stHeader"] svg,[data-testid="stToolbar"] svg{color:var(--sh-text)!important;fill:currentColor!important;}
[data-testid="stDecoration"]{display:none!important;}

/* SIDEBAR */
section[data-testid="stSidebar"],section[data-testid="stSidebar"]>div,section[data-testid="stSidebar"]>div>div{
  background:var(--sh-panel)!important;color:var(--sh-text)!important;}
section[data-testid="stSidebar"]{border-right:1px solid var(--sh-border)!important;}
section[data-testid="stSidebar"] *{color:var(--sh-text);}
section[data-testid="stSidebar"] hr{border-color:var(--sh-border)!important;}
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *{color:var(--sh-muted)!important;}

.sidebar-brand{width:100%;display:flex;align-items:center;gap:12px;padding:8px 2px 14px;}
.sidebar-brand-logo{width:48px;height:48px;min-width:48px;display:flex;align-items:center;justify-content:center;
  border-radius:14px;background:@@ACCENT@@18;border:1px solid @@ACCENT@@66;color:var(--sh-accent)!important;
  font-size:23px;line-height:1;box-shadow:0 0 24px @@ACCENT@@20;}
.sidebar-brand-text{min-width:0;flex:1;}
.sidebar-brand-name{color:var(--sh-text)!important;font-size:18px;line-height:1.1;font-weight:800;white-space:nowrap;}
.sidebar-brand-name span{color:var(--sh-accent)!important;}
.sidebar-brand-subtitle{margin-top:4px;color:var(--sh-muted)!important;font-size:10px;white-space:nowrap;}
.sidebar-section-title{color:var(--sh-muted)!important;font-size:10px;font-weight:800;letter-spacing:1.4px;
  text-transform:uppercase;margin:8px 0;}

[data-testid="stSidebarCollapseButton"] button,[data-testid="stSidebarCollapsedControl"] button{
  background:var(--sh-panel)!important;color:var(--sh-text)!important;border:1px solid var(--sh-border)!important;
  box-shadow:none!important;border-radius:10px!important;}
[data-testid="stSidebarCollapseButton"] svg,[data-testid="stSidebarCollapsedControl"] svg{
  color:var(--sh-text)!important;fill:currentColor!important;}
[data-testid="stSidebarCollapseButton"] button:hover,[data-testid="stSidebarCollapsedControl"] button:hover{
  background:var(--sh-hover)!important;color:var(--sh-accent)!important;border-color:var(--sh-accent)!important;}

/* SELECTBOX */
[data-testid="stSelectbox"] label,[data-testid="stSelectbox"] label p{color:var(--sh-text)!important;font-weight:700!important;}
[data-baseweb="select"]{background:transparent!important;color:var(--sh-text)!important;}
[data-baseweb="select"]>div{min-height:42px!important;background:var(--sh-input)!important;background-image:none!important;
  color:var(--sh-text)!important;border:1px solid var(--sh-border)!important;border-radius:12px!important;box-shadow:none!important;}
[data-baseweb="select"]>div:hover{background:var(--sh-hover)!important;border-color:var(--sh-accent)!important;}
[data-baseweb="select"] *{color:var(--sh-text)!important;-webkit-text-fill-color:var(--sh-text)!important;}
[data-baseweb="select"] svg{color:var(--sh-muted)!important;fill:currentColor!important;}

/* DROPDOWN MENU */
[data-baseweb="popover"],[data-baseweb="popover"]>div,[data-baseweb="menu"],[role="listbox"]{
  background:var(--sh-menu)!important;color:var(--sh-text)!important;border-color:var(--sh-border)!important;}
[data-baseweb="menu"]{padding:6px!important;border-radius:14px!important;}
[role="option"],li[role="option"],div[role="option"]{background:var(--sh-menu)!important;color:var(--sh-text)!important;border-radius:9px!important;}
[role="option"]:hover,li[role="option"]:hover,div[role="option"]:hover,[role="option"][aria-selected="true"]{
  background:var(--sh-menu-hover)!important;color:var(--sh-accent)!important;}

/* BUTTONS + POPOVERS */
div.stButton>button,[data-testid="stPopover"] button,button[data-testid="stPopoverButton"]{
  min-height:40px;background:var(--sh-panel)!important;color:var(--sh-text)!important;
  border:1px solid var(--sh-border)!important;border-radius:11px!important;box-shadow:none!important;}
div.stButton>button:hover,[data-testid="stPopover"] button:hover,button[data-testid="stPopoverButton"]:hover{
  background:var(--sh-hover)!important;color:var(--sh-accent)!important;border-color:var(--sh-accent)!important;}
div.stButton>button p{color:inherit!important;}

/* CHAT INPUT */
[data-testid="stBottom"],[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"]{background:var(--sh-bg)!important;}
[data-testid="stChatInput"]>div{background:var(--sh-panel)!important;border:1px solid var(--sh-border)!important;border-radius:18px!important;}
[data-testid="stChatInput"] textarea{background:transparent!important;color:var(--sh-text)!important;
  -webkit-text-fill-color:var(--sh-text)!important;caret-color:var(--sh-accent)!important;}
[data-testid="stChatInput"] textarea::placeholder{color:var(--sh-muted)!important;-webkit-text-fill-color:var(--sh-muted)!important;}
[data-testid="stChatInput"] button{background:var(--sh-panel2)!important;color:var(--sh-muted)!important;border:0!important;}
[data-testid="stChatInput"] svg{color:inherit!important;fill:currentColor!important;}
[data-testid="stChatInput"] button:hover{color:var(--sh-accent)!important;}

/* CHAT MESSAGES */
[data-testid="stChatMessage"]{background:transparent!important;}
[data-testid="stChatMessage"] p,[data-testid="stChatMessage"] li{color:var(--sh-text)!important;}

/* HERO */
.hero{border:1px solid var(--sh-border);border-radius:24px;padding:28px 24px;text-align:center;
  background:linear-gradient(145deg,var(--sh-panel),@@ACCENT@@0D);box-shadow:0 20px 60px rgba(0,0,0,.08);}
.hero-logo{width:54px;height:54px;margin:0 auto;display:flex;align-items:center;justify-content:center;
  border:1px solid var(--sh-accent);border-radius:20px;font-size:25px;line-height:1;box-shadow:0 0 28px @@ACCENT@@44;}
.hero-title{margin-top:12px;font-size:38px;line-height:1.02;font-weight:800;letter-spacing:-2px;color:var(--sh-text)!important;}
.hero-title span{color:var(--sh-accent)!important;}
.hero-description{max-width:760px;margin:9px auto 0;color:var(--sh-muted)!important;font-size:14px;line-height:1.45;}
.hero-badge{display:inline-flex;align-items:center;gap:7px;margin-top:11px;padding:6px 12px;border:1px solid var(--sh-accent);
  border-radius:999px;color:var(--sh-accent)!important;font-size:11px;font-weight:700;background:@@ACCENT@@0F;}

/* SOURCE CARDS */
.source-card,.source{border:1px solid var(--sh-border);border-left:3px solid var(--sh-accent);border-radius:12px;
  padding:15px;margin:10px 0;background:var(--sh-panel)!important;color:var(--sh-text)!important;}
.source-header{display:flex;align-items:flex-start;gap:11px;}
.source-icon{width:34px;height:34px;min-width:34px;display:flex;align-items:center;justify-content:center;
  border-radius:9px;background:@@ACCENT@@12;color:var(--sh-accent)!important;}
.source-title{color:var(--sh-text)!important;font-weight:750;font-size:14px;}
.source-meta{margin-top:3px;color:var(--sh-muted)!important;font-size:11px;}
.source-excerpt{margin-top:12px;padding-top:11px;border-top:1px solid var(--sh-border);
  color:var(--sh-muted)!important;font-size:13px;line-height:1.65;}

/* PIPELINE */
.pipeline-card{padding:16px;margin:8px 0;border:1px solid var(--sh-border);border-radius:16px;background:var(--sh-panel);}
.pipeline-step{display:flex;align-items:center;gap:12px;padding:10px 12px;margin:6px 0;border:1px solid var(--sh-border);
  border-radius:12px;background:var(--sh-panel2);}
.pipeline-icon{width:30px;height:30px;min-width:30px;display:flex;align-items:center;justify-content:center;border-radius:9px;
  background:@@ACCENT@@18;border:1px solid @@ACCENT@@44;color:var(--sh-accent)!important;}
.pipeline-text{flex:1;}
.pipeline-name{color:var(--sh-text)!important;font-weight:700;font-size:13px;}
.pipeline-status{color:var(--sh-muted)!important;font-size:11px;}
.pipeline-arrow{text-align:center;color:var(--sh-muted)!important;}

/* VERDICT */
.verdict-card{display:flex;align-items:center;gap:14px;padding:14px 16px;margin-bottom:12px;
  border:1px solid var(--verdict-color);border-left:4px solid var(--verdict-color);border-radius:14px;
  background:var(--sh-panel)!important;color:var(--sh-text)!important;}
.verdict-dot{width:15px;height:15px;min-width:15px;border-radius:50%;background:var(--verdict-color);box-shadow:0 0 14px var(--verdict-color);}
.verdict-title{color:var(--sh-text)!important;font-weight:700;}
.verdict-note{margin-top:3px;color:var(--sh-muted)!important;font-size:13px;}

/* MISC */
.muted{color:var(--sh-muted)!important;}
.footer-card,.card{width:100%;margin-top:28px;padding:18px 20px;text-align:center;border:1px solid var(--sh-border);
  border-radius:16px;background:var(--sh-panel)!important;color:var(--sh-muted)!important;}
.footer-card *{color:var(--sh-muted)!important;}
.footer-title{color:var(--sh-text)!important;font-size:12px;font-weight:700;}
.footer-description{margin-top:6px;color:var(--sh-muted)!important;font-size:11px;line-height:1.55;}
.sidebar-status-card{display:flex;align-items:center;gap:8px;padding:9px 10px;border:1px solid var(--sh-border);
  border-radius:10px;background:var(--sh-panel2);color:var(--sh-muted)!important;font-size:11px;}
.sidebar-status-dot{width:7px;height:7px;min-width:7px;border-radius:50%;background:var(--sh-accent);box-shadow:0 0 10px var(--sh-accent);}

[data-testid="stExpander"]{background:var(--sh-panel)!important;border:1px solid var(--sh-border)!important;border-radius:14px!important;}
[data-testid="stExpander"] summary{background:var(--sh-panel)!important;color:var(--sh-text)!important;}
[data-testid="stExpander"] summary *{color:var(--sh-text)!important;}
section[data-testid="stFileUploaderDropzone"]{background:var(--sh-input)!important;border:1px dashed var(--sh-border)!important;border-radius:14px!important;}
section[data-testid="stFileUploaderDropzone"] *{color:var(--sh-text)!important;}

::-webkit-scrollbar{width:8px;height:8px;}
::-webkit-scrollbar-track{background:var(--sh-bg);}
::-webkit-scrollbar-thumb{background:var(--sh-border);border-radius:999px;}
::-webkit-scrollbar-thumb:hover{background:var(--sh-accent);}

/* =====================================================================
   HARD OVERRIDES: literal colors (no var()), extra specificity.
   These win even if Streamlit's native dark theme or another stylesheet
   fights the rules above. This is what removes the black spots.
===================================================================== */
html body .stApp [data-testid="stHeader"],
html body .stApp header{background:@@BG@@!important;background-color:@@BG@@!important;}
html body .stApp [data-testid="stHeader"] *{color:@@TEXT@@!important;}
html body .stApp [data-testid="stHeader"] svg{color:@@TEXT@@!important;fill:currentColor!important;}

html body .stApp [data-testid="stBottom"],
html body .stApp [data-testid="stBottom"]>div,
html body .stApp [data-testid="stBottomBlockContainer"]{background:@@BG@@!important;background-color:@@BG@@!important;}
html body .stApp [data-testid="stChatInput"],
html body .stApp [data-testid="stChatInput"]>div,
html body .stApp [data-testid="stChatInput"] [data-baseweb="textarea"],
html body .stApp [data-testid="stChatInput"] [data-baseweb="base-input"]{background:@@PANEL@@!important;background-color:@@PANEL@@!important;}
html body .stApp [data-testid="stChatInput"] textarea{color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;}
html body .stApp [data-testid="stChatInput"] button{background:@@PANEL2@@!important;color:@@MUTED@@!important;}
html body .stApp [data-testid="stChatInput"] svg{color:@@MUTED@@!important;fill:currentColor!important;}

html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"],
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] div,
html body .stApp [data-baseweb="select"]>div{background:@@INPUT@@!important;background-color:@@INPUT@@!important;background-image:none!important;}
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] *{color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;}
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] svg{color:@@MUTED@@!important;fill:currentColor!important;}

html body div[data-baseweb="popover"],
html body div[data-baseweb="popover"] *:not(svg):not(path),
html body ul[role="listbox"],
html body ul[role="listbox"] li{background:@@MENU@@!important;background-color:@@MENU@@!important;color:@@TEXT@@!important;}
html body ul[role="listbox"] li:hover,
html body ul[role="listbox"] li[aria-selected="true"]{background:@@MENUHOVER@@!important;color:@@ACCENT@@!important;}

html body .stApp [data-testid="stSidebar"] button,
html body .stApp [data-testid="stSidebar"] [data-testid="stExpander"],
html body .stApp [data-testid="stSidebar"] [data-testid="stExpander"] summary{background:@@PANEL@@!important;background-color:@@PANEL@@!important;color:@@TEXT@@!important;}
html body .stApp [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg{color:@@TEXT@@!important;fill:currentColor!important;}

/* ---- round 2: sidebar labels, bottom bar, select arrow ---- */
html body .stApp section[data-testid="stSidebar"] label,
html body .stApp section[data-testid="stSidebar"] label p,
html body .stApp section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
html body .stApp section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
html body .stApp section[data-testid="stSidebar"] h1,
html body .stApp section[data-testid="stSidebar"] h2,
html body .stApp section[data-testid="stSidebar"] h3{color:@@TEXT@@!important;opacity:1!important;}
html body .stApp section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *{color:@@MUTED@@!important;opacity:1!important;}

html body .stApp [data-testid*="Bottom"],
html body .stApp [class*="stBottom"],
html body .stApp [class*="ChatFloating"],
html body .stApp [data-testid="stBottom"] > div > div,
html body .stApp [data-testid="stBottomBlockContainer"] > div{background:@@BG@@!important;background-color:@@BG@@!important;}
html body .stApp [data-testid="stChatInput"] > div,
html body .stApp [data-testid="stChatInput"] > div > div{background:@@PANEL@@!important;background-color:@@PANEL@@!important;}
html body .stApp [data-testid="stChatInput"] textarea,
html body .stApp [data-testid="stChatInputTextArea"]{background:@@PANEL@@!important;background-color:@@PANEL@@!important;color:@@TEXT@@!important;}

html body .stApp [data-baseweb="select"] *:not(svg):not(path){background-color:@@INPUT@@!important;background-image:none!important;}
html body .stApp [data-baseweb="select"] svg{background:transparent!important;fill:@@MUTED@@!important;color:@@MUTED@@!important;}

/* ---- round 3: selectbox black value area ---- */
html body .stApp [data-baseweb="select"],
html body .stApp [data-baseweb="select"] *{color-scheme:@@SCHEME@@!important;}
html body .stApp [data-baseweb="select"] > div,
html body .stApp [data-baseweb="select"] > div > div,
html body .stApp [data-baseweb="select"] > div > div > div,
html body .stApp [data-baseweb="select"] input,
html body .stApp [data-baseweb="select"] [value]{
  background:@@INPUT@@!important;background-color:@@INPUT@@!important;background-image:none!important;
  box-shadow:inset 0 0 0 100px @@INPUT@@!important;
  color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;opacity:1!important;filter:none!important;}
html body .stApp [data-baseweb="select"] > div::before,
html body .stApp [data-baseweb="select"] > div::after{background:transparent!important;display:none!important;}
html body .stApp [data-baseweb="select"] > div{border:1px solid @@BORDER@@!important;border-radius:12px!important;overflow:hidden;}
html body .stApp [data-baseweb="select"] svg{color:@@MUTED@@!important;fill:@@MUTED@@!important;}

/* ---- FINAL THEME LOCK: sidebar select controls + dropdown menus ---- */
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div {
  background:@@INPUT@@!important;background-color:@@INPUT@@!important;background-image:none!important;
  color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;border-color:@@BORDER@@!important;
  box-shadow:none!important;opacity:1!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
  color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;fill:@@MUTED@@!important;
}
html body div[data-baseweb="popover"],
html body div[data-baseweb="popover"] > div,
html body div[data-baseweb="popover"] [data-baseweb="menu"],
html body div[data-baseweb="popover"] ul[role="listbox"] {
  background:@@MENU@@!important;background-color:@@MENU@@!important;color:@@TEXT@@!important;
  border-color:@@BORDER@@!important;box-shadow:0 18px 50px rgba(0,0,0,.16)!important;
}
html body div[data-baseweb="popover"] [role="option"],
html body div[data-baseweb="popover"] li[role="option"],
html body div[data-baseweb="popover"] [role="option"] * {
  background:@@MENU@@!important;background-color:@@MENU@@!important;color:@@TEXT@@!important;
  -webkit-text-fill-color:@@TEXT@@!important;
}
html body div[data-baseweb="popover"] [role="option"]:hover,
html body div[data-baseweb="popover"] [role="option"][aria-selected="true"],
html body div[data-baseweb="popover"] li[role="option"]:hover {
  background:@@MENUHOVER@@!important;background-color:@@MENUHOVER@@!important;color:@@ACCENT@@!important;
  -webkit-text-fill-color:@@ACCENT@@!important;
}
.sidebar-provider-card {
  display:flex;align-items:center;gap:10px;padding:10px 11px;margin:7px 0 4px;
  border:1px solid var(--sh-border);border-radius:11px;background:var(--sh-panel2);color:var(--sh-text)!important;
}
.sidebar-provider-dot {width:8px;height:8px;min-width:8px;border-radius:50%;background:var(--sh-accent);box-shadow:0 0 10px var(--sh-accent);}
.sidebar-provider-title {color:var(--sh-text)!important;font-size:11px;font-weight:800;}
.sidebar-provider-list {margin-top:2px;color:var(--sh-muted)!important;font-size:10px;}
.sidebar-provider-offline .sidebar-provider-dot {background:var(--sh-muted);box-shadow:none;}
/* ---- FINAL BASEWEB PORTAL OVERRIDE: light/dark dropdowns ---- */
body > div [data-baseweb="popover"],
body > div [data-baseweb="popover"] > div,
body > div [data-baseweb="popover"] [data-baseweb="menu"],
body > div [data-baseweb="popover"] ul[role="listbox"],
body > div [data-baseweb="popover"] li[role="option"] {
  background:@@MENU@@ !important;
  background-color:@@MENU@@ !important;
  color:@@TEXT@@ !important;
  color-scheme:@@SCHEME@@ !important;
  border-color:@@BORDER@@ !important;
}
body > div [data-baseweb="popover"] [role="option"],
body > div [data-baseweb="popover"] [role="option"] span,
body > div [data-baseweb="popover"] [role="option"] div,
body > div [data-baseweb="popover"] li[role="option"] * {
  background:transparent !important;
  background-color:transparent !important;
  color:@@TEXT@@ !important;
  -webkit-text-fill-color:@@TEXT@@ !important;
}
body > div [data-baseweb="popover"] [role="option"]:hover,
body > div [data-baseweb="popover"] [role="option"][aria-selected="true"],
body > div [data-baseweb="popover"] li[role="option"]:hover {
  background:@@MENUHOVER@@ !important;
  background-color:@@MENUHOVER@@ !important;
  color:@@ACCENT@@ !important;
}
body > div [data-baseweb="popover"] [role="option"]:hover *,
body > div [data-baseweb="popover"] [role="option"][aria-selected="true"] * {
  background:transparent !important;
  color:@@ACCENT@@ !important;
  -webkit-text-fill-color:@@ACCENT@@ !important;
}
/* The trigger itself must follow the active palette, including nested BaseWeb wrappers. */
html body .stApp section[data-testid="stSidebar"] [data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-baseweb="select"] > div > div > div {
  background:@@INPUT@@ !important;
  background-color:@@INPUT@@ !important;
  box-shadow:none !important;
  color:@@TEXT@@ !important;
  -webkit-text-fill-color:@@TEXT@@ !important;
  color-scheme:@@SCHEME@@ !important;
}

/* ---- DASHBOARD SPACING + RESPONSIVE SAMPLE QUERIES ---- */
.stat-card{min-height:82px;width:100%;padding:14px 12px;border:1px solid var(--sh-border);border-radius:14px;background:var(--sh-panel)!important;overflow:hidden;}
.stat-label{color:var(--sh-muted)!important;font-size:10px;font-weight:800;letter-spacing:.7px;text-transform:uppercase;line-height:1.25;white-space:normal;overflow-wrap:anywhere;}
.stat-value{color:var(--sh-text)!important;font-size:19px;font-weight:800;line-height:1.25;margin-top:6px;white-space:normal;overflow-wrap:anywhere;}
.sample-query-title{margin:22px 0 8px;color:var(--sh-muted)!important;font-size:10px;font-weight:800;letter-spacing:1.3px;text-transform:uppercase;}
div.stButton>button{white-space:normal!important;overflow-wrap:anywhere!important;line-height:1.25!important;min-height:44px!important;height:auto!important;padding:9px 12px!important;}
div.stButton>button p{white-space:normal!important;overflow-wrap:anywhere!important;line-height:1.25!important;margin:0!important;}
/* ---- SIDEBAR BASEWEB SELECT ---- */
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"],
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] [aria-haspopup="listbox"]{
  background:@@INPUT@@!important;background-color:@@INPUT@@!important;background-image:none!important;
  color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;color-scheme:@@SCHEME@@!important;
  border-color:@@BORDER@@!important;box-shadow:none!important;opacity:1!important;filter:none!important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] div{
  color:@@TEXT@@!important;-webkit-text-fill-color:@@TEXT@@!important;
}
section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg{
  background:transparent!important;color:@@MUTED@@!important;fill:@@MUTED@@!important;
}
/* Dropdowns render in a portal outside the sidebar DOM. */
div[data-baseweb="popover"],div[data-baseweb="popover"] > div,div[data-baseweb="popover"] [role="listbox"]{
  background:@@MENU@@!important;background-color:@@MENU@@!important;color:@@TEXT@@!important;
  color-scheme:@@SCHEME@@!important;border:1px solid @@BORDER@@!important;
}
div[data-baseweb="popover"] [role="option"],div[data-baseweb="popover"] [role="option"] > div,
div[data-baseweb="popover"] [role="option"] span{
  background:transparent!important;background-color:transparent!important;color:@@TEXT@@!important;
  -webkit-text-fill-color:@@TEXT@@!important;
}
div[data-baseweb="popover"] [role="option"]:hover,div[data-baseweb="popover"] [role="option"][aria-selected="true"]{
  background:@@MENUHOVER@@!important;background-color:@@MENUHOVER@@!important;color:@@ACCENT@@!important;
}
@media (max-width:900px){
  .stat-value{font-size:16px;}
  .stat-card{min-height:76px;padding:12px 10px;}
  .sample-query-title{margin-top:18px;}
}

/* ================================================================
   INSTANT SCAN METER
================================================================ */
.risk-meter-card{
  margin:12px 0 10px;padding:15px 16px;border:1px solid var(--sh-border);
  border-radius:16px;background:var(--sh-panel)!important;
}
.risk-meter-top{display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--sh-text)!important;}
.risk-meter-top strong{font-size:18px;color:var(--sh-accent)!important;}
.risk-meter-title{font-size:13px;font-weight:800;color:var(--sh-text)!important;}
.risk-meter-level{margin-left:8px;font-size:11px;color:var(--sh-muted)!important;}
.risk-meter-track{height:9px;margin-top:11px;border-radius:999px;overflow:hidden;background:var(--sh-panel2)!important;border:1px solid var(--sh-border);}
.risk-meter-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,var(--sh-accent),#ef4444)!important;transition:width .25s ease;}
.risk-meter-scale{display:flex;justify-content:space-between;margin-top:4px;font-size:9px;color:var(--sh-muted)!important;}
.risk-meter-note{margin-top:9px;font-size:10px;line-height:1.45;color:var(--sh-muted)!important;}

/* ================================================================
   FINAL UI-ONLY PATCH
   Theme-aware sidebar selects + safe hero/stat-card spacing.
================================================================ */
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div {
  background:var(--sh-input-bg)!important;
  background-color:var(--sh-input-bg)!important;
  background-image:none!important;
  color:var(--sh-input-text)!important;
  -webkit-text-fill-color:var(--sh-input-text)!important;
  border:1px solid var(--sh-border)!important;
  border-radius:12px!important;
  box-shadow:none!important;
  opacity:1!important;
  color-scheme:@@SCHEME@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] input {
  background:transparent!important;
  background-color:transparent!important;
  color:var(--sh-input-text)!important;
  -webkit-text-fill-color:var(--sh-input-text)!important;
  opacity:1!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg {
  background:transparent!important;
  color:var(--sh-input-arrow)!important;
  fill:var(--sh-input-arrow)!important;
  opacity:1!important;
}

/* BaseWeb renders the opened menu in a portal, outside the sidebar. */
body > div[data-baseweb="popover"],
body > div[data-baseweb="popover"] > div,
body > div[data-baseweb="popover"] [data-baseweb="menu"],
body > div[data-baseweb="popover"] ul[role="listbox"],
body > div[data-baseweb="popover"] li[role="option"] {
  background:var(--sh-menu)!important;
  background-color:var(--sh-menu)!important;
  color:var(--sh-text)!important;
  border-color:var(--sh-border)!important;
}
body > div[data-baseweb="popover"] [role="option"],
body > div[data-baseweb="popover"] [role="option"] > div,
body > div[data-baseweb="popover"] [role="option"] span {
  background:transparent!important;
  background-color:transparent!important;
  color:var(--sh-text)!important;
  -webkit-text-fill-color:var(--sh-text)!important;
}
body > div[data-baseweb="popover"] [role="option"]:hover,
body > div[data-baseweb="popover"] [role="option"][aria-selected="true"],
body > div[data-baseweb="popover"] li[role="option"]:hover {
  background:var(--sh-menu-hover)!important;
  background-color:var(--sh-menu-hover)!important;
  color:var(--sh-accent)!important;
  -webkit-text-fill-color:var(--sh-accent)!important;
}

/* FINAL SELECTBOX CALIBRATION: keep sidebar BaseWeb select surfaces locked to the active theme. */
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div > div {
  background:var(--sh-select-bg)!important;
  background-color:var(--sh-select-bg)!important;
  background-image:none!important;
  color:var(--sh-select-text)!important;
  -webkit-text-fill-color:var(--sh-select-text)!important;
  border:1px solid var(--sh-select-border)!important;
  border-radius:12px!important;
  box-shadow:none!important;
  opacity:1!important;
  color-scheme:@@SCHEME@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] input {
  background:transparent!important;
  background-color:transparent!important;
  color:var(--sh-select-text)!important;
  -webkit-text-fill-color:var(--sh-select-text)!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg {
  background:transparent!important;
  color:var(--sh-select-arrow)!important;
  fill:var(--sh-select-arrow)!important;
  opacity:1!important;
}

/* BaseWeb renders the opened menu in a portal outside the sidebar. */
html body div[data-baseweb="popover"],
html body div[data-baseweb="popover"] > div,
html body div[data-baseweb="popover"] [data-baseweb="menu"],
html body div[data-baseweb="popover"] ul[role="listbox"],
html body div[data-baseweb="popover"] li[role="option"] {
  background:var(--sh-menu)!important;
  background-color:var(--sh-menu)!important;
  color:var(--sh-text)!important;
  border-color:var(--sh-border)!important;
  color-scheme:@@SCHEME@@!important;
}
html body div[data-baseweb="popover"] [role="option"],
html body div[data-baseweb="popover"] [role="option"] > div,
html body div[data-baseweb="popover"] [role="option"] span {
  background:transparent!important;
  background-color:transparent!important;
  color:var(--sh-text)!important;
  -webkit-text-fill-color:var(--sh-text)!important;
}
html body div[data-baseweb="popover"] [role="option"]:hover,
html body div[data-baseweb="popover"] [role="option"][aria-selected="true"],
html body div[data-baseweb="popover"] li[role="option"]:hover {
  background:var(--sh-menu-hover)!important;
  background-color:var(--sh-menu-hover)!important;
  color:var(--sh-accent)!important;
  -webkit-text-fill-color:var(--sh-accent)!important;
}
html body div[data-baseweb="popover"] [role="option"]:hover *,
html body div[data-baseweb="popover"] [role="option"][aria-selected="true"] * {
  background:transparent!important;
  color:var(--sh-accent)!important;
  -webkit-text-fill-color:var(--sh-accent)!important;
}

/* Give the hero its own layout space; no transforms/negative margins. */
.hero {
  position:relative!important;
  height:auto!important;
  min-height:0!important;
  margin-top:0!important;
  margin-bottom:1.5rem!important;
  padding-bottom:42px!important;
  overflow:visible!important;
  transform:none!important;
}
.hero + div {
  margin-top:0!important;
}
.stat-card {
  position:relative!important;
  transform:none!important;
  margin-top:0!important;
  overflow:hidden!important;
}
@media (max-width:900px) {
  .hero {
    margin-bottom:1.25rem!important;
    padding:30px 20px!important;
  }
  .hero-title {font-size:36px!important;letter-spacing:-1.5px!important;}
}

/* =====================================================================
   FINAL SIDEBAR DROPDOWN COLOR LOCK
   Applies to all three sidebar selectboxes in both Light and Dark themes.
   Streamlit/BaseWeb may render the open menu in a portal outside the sidebar,
   so both in-sidebar and portal surfaces are explicitly theme-locked.
===================================================================== */
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div {
  background:@@INPUT@@!important;
  background-color:@@INPUT@@!important;
  color:@@TEXT@@!important;
  -webkit-text-fill-color:@@TEXT@@!important;
  border:1px solid @@BORDER@@!important;
  border-radius:12px!important;
  box-shadow:none!important;
  opacity:1!important;
  color-scheme:@@SCHEME@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input {
  background:transparent!important;
  background-color:transparent!important;
  color:@@TEXT@@!important;
  -webkit-text-fill-color:@@TEXT@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
  background:transparent!important;
  color:@@MUTED@@!important;
  fill:@@MUTED@@!important;
}

/* Open dropdown: BaseWeb portal can live directly under body or inside
   another portal wrapper, so cover both structures. */
html body div[data-baseweb="popover"],
html body div[data-baseweb="popover"] > div,
html body div[data-baseweb="popover"] [data-baseweb="menu"],
html body div[data-baseweb="popover"] ul[role="listbox"],
html body div[data-baseweb="popover"] li[role="option"] {
  background:@@MENU@@!important;
  background-color:@@MENU@@!important;
  color:@@TEXT@@!important;
  border-color:@@BORDER@@!important;
  color-scheme:@@SCHEME@@!important;
}
html body div[data-baseweb="popover"] [role="option"],
html body div[data-baseweb="popover"] [role="option"] > div,
html body div[data-baseweb="popover"] [role="option"] span {
  background:transparent!important;
  background-color:transparent!important;
  color:@@TEXT@@!important;
  -webkit-text-fill-color:@@TEXT@@!important;
}
html body div[data-baseweb="popover"] [role="option"]:hover,
html body div[data-baseweb="popover"] [role="option"][aria-selected="true"],
html body div[data-baseweb="popover"] li[role="option"]:hover {
  background:@@MENUHOVER@@!important;
  background-color:@@MENUHOVER@@!important;
  color:@@ACCENT@@!important;
  -webkit-text-fill-color:@@ACCENT@@!important;
}
html body div[data-baseweb="popover"] [role="option"]:hover *,
html body div[data-baseweb="popover"] [role="option"][aria-selected="true"] * {
  background:transparent!important;
  color:@@ACCENT@@!important;
  -webkit-text-fill-color:@@ACCENT@@!important;
}

/* FINAL SIDEBAR SELECT CALIBRATION */
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"],
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] [role="button"] {
  background:@@SELECT_BG@@!important;
  background-color:@@SELECT_BG@@!important;
  background-image:none!important;
  color:@@SELECT_TEXT@@!important;
  -webkit-text-fill-color:@@SELECT_TEXT@@!important;
  border-color:@@SELECT_BORDER@@!important;
  box-shadow:none!important;
  color-scheme:@@SCHEME@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] [role="button"] * {
  background:transparent!important;
  background-color:transparent!important;
  color:@@SELECT_TEXT@@!important;
  -webkit-text-fill-color:@@SELECT_TEXT@@!important;
}
html body .stApp section[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg {
  background:transparent!important;
  color:@@SELECT_ARROW@@!important;
  fill:@@SELECT_ARROW@@!important;
}
</style>
"""


# ---------------------------------------------------------------------------
# HTML safety net
# Markdown turns indented lines / blank lines inside HTML into a code block,
# which is why raw <div ...> text appeared in the hero and sidebar. Any
# st.markdown(..., unsafe_allow_html=True) whose content starts with "<" is
# flattened (indentation + blank lines removed) before rendering.
# ---------------------------------------------------------------------------
def _flatten_html(body):
    if isinstance(body, str) and body.lstrip().startswith("<"):
        return "\n".join(line.strip() for line in body.splitlines() if line.strip())
    return body


def _install_html_fix():
    from streamlit.delta_generator import DeltaGenerator

    if getattr(DeltaGenerator.markdown, "_sh_patched", False):
        return

    original = DeltaGenerator.markdown

    def markdown(self, body, *args, **kwargs):
        unsafe = kwargs.get("unsafe_allow_html", args[0] if args else False)
        if unsafe:
            body = _flatten_html(body)
        return original(self, body, *args, **kwargs)

    markdown._sh_patched = True
    DeltaGenerator.markdown = markdown

    original_top = st.markdown

    def top_markdown(body, *args, **kwargs):
        unsafe = kwargs.get("unsafe_allow_html", args[0] if args else False)
        if unsafe:
            body = _flatten_html(body)
        return original_top(body, *args, **kwargs)

    st.markdown = top_markdown


_install_html_fix()


def apply_theme(dark: bool, accent: str):
    palette = dict(DARK if dark else LIGHT)
    palette["ACCENT"] = ACCENTS.get(accent, ACCENTS["Cyan"])

    css = CSS
    for key, value in palette.items():
        css = css.replace(f"@@{key}@@", value)

    st.markdown(css, unsafe_allow_html=True)
