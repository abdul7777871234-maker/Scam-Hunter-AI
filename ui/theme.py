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
    bg = "#050811" if dark else "#F8FAFC"
    panel = "#0B1120" if dark else "#FFFFFF"
    text = "#E2E8F0" if dark else "#0F172A"
    muted = "#94A3B8" if dark else "#64748B"
    border = "rgba(148,163,184,.18)" if dark else "rgba(15,23,42,.10)"
    shadow = "0 20px 60px rgba(0,0,0,.18)" if dark else "0 20px 60px rgba(15,23,42,.08)"
    st.markdown(f"""
    <style>
    :root {{ --accent:{a}; --bg:{bg}; --panel:{panel}; --text:{text}; --muted:{muted}; --border:{border}; }}
    .stApp {{ background: radial-gradient(circle at 50% -10%, {a}18 0, transparent 32%), var(--bg); color:var(--text); }}
    section[data-testid="stSidebar"] {{ background:linear-gradient(180deg,{panel},var(--bg)); border-right:1px solid var(--border); }}
    .block-container {{ max-width:1320px; padding-top:2rem; padding-bottom:7rem; }}
    .hero {{ border:1px solid var(--border); border-radius:24px; padding:42px 30px; text-align:center;
             background:linear-gradient(145deg,{panel},{a}0D); box-shadow:{shadow}; }}
    .logo {{ width:66px;height:66px;border:1px solid {a};border-radius:20px;display:inline-flex;
             align-items:center;justify-content:center;font-size:30px;color:{a};
             box-shadow:0 0 28px {a}44; }}
    .hero h1 {{ font-size:44px; line-height:1.02; margin:18px 0 10px; letter-spacing:-2px; color:var(--text); }}
    .hero h1 span {{ color:{a}; }}
    .hero p {{ color:var(--muted); font-size:16px; }}
    .badge {{ display:inline-block; margin-top:12px; padding:8px 14px; border:1px solid {a};
              border-radius:999px; color:{a}; font-size:12px; background:{a}0F; }}
    .section-label {{ color:{a}; font-size:11px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; margin:28px 0 12px; }}
    .card {{ border:1px solid var(--border); border-radius:18px; padding:18px; background:var(--panel); }}
    .source {{ border-left:3px solid {a}; padding:12px 15px; margin:9px 0; background:{a}09; border-radius:10px; }}
    .muted {{ color:var(--muted); }}
    div.stButton > button {{ border-radius:12px; border:1px solid var(--border); background:var(--panel); color:var(--text); }}
    div.stButton > button:hover {{ border-color:{a}; color:{a}; }}
    .stTextArea textarea, .stTextInput input {{ border-radius:14px !important; }}
    </style>
    """, unsafe_allow_html=True)
