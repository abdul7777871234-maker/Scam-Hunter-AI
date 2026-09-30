import streamlit as st

def hero():
    st.markdown("""
    <div class="hero">
      <div class="logo">🛡️</div>
      <h1>ScamHunter <span>AI</span></h1>
      <p>Investigate suspicious messages, offers, links and online claims with AI-powered evidence analysis.</p>
      <div class="badge">● Evidence-first AI investigation</div>
    </div>
    """, unsafe_allow_html=True)

def source_card(item):
    if item.get("type") == "knowledge_base":
        title = item.get("title", "Knowledge Base")
        detail = f"Page {item.get('page')} · {item.get('section') or 'General'} · {item.get('chunk_id')}"
        excerpt = item.get("excerpt","")
    else:
        title = item.get("title") or item.get("url") or "Web source"
        detail = item.get("url","")
        excerpt = item.get("snippet","")
    st.markdown(f'<div class="source"><b>{title}</b><br><span class="muted">{detail}</span><br><br>{excerpt}</div>', unsafe_allow_html=True)
