import streamlit as st
from ui.theme import ACCENTS

def render():
    with st.sidebar:
        st.markdown("### 🛡️ SCAMHUNTER AI")
        st.caption("AI-powered scam investigation assistant")
        st.divider()

        mode = st.selectbox("INVESTIGATION MODE", ["Quick Check", "Deep Investigation"], index=0)
        style = st.selectbox("RESPONSE STYLE", ["Concise", "Balanced", "Detailed"], index=1)
        accent = st.selectbox("ACCENT COLOR", list(ACCENTS), index=0)

        c1, c2 = st.columns(2)
        with c1:
            light = st.button("☀ Light", use_container_width=True)
        with c2:
            dark = st.button("🌙 Dark", use_container_width=True)

        if "dark" not in st.session_state:
            st.session_state.dark = False
        if light:
            st.session_state.dark = False
        if dark:
            st.session_state.dark = True

        st.caption(f"Theme: {'Dark' if st.session_state.dark else 'Light'} · {accent}")
        st.divider()

        st.markdown("**KNOWLEDGE BASE**")
        st.caption(st.session_state.get("kb_status", "Not initialized"))

        st.markdown("**RECENT INVESTIGATIONS**")
        history = st.session_state.get("history", [])
        if history:
            for h in history[-5:][::-1]:
                st.caption(h[:65] + ("…" if len(h) > 65 else ""))
        else:
            st.caption("No investigations yet.")

        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.history = []
            st.session_state.messages = []
            st.rerun()

        return mode, style, accent
