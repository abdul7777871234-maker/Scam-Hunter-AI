import streamlit as st
from ui.theme import ACCENTS


def render():
    # Initialise state first so every widget below can rely on it
    st.session_state.setdefault("dark", True)
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("messages", [])

    with st.sidebar:
        st.markdown("### 🛡️ SCAMHUNTER AI")
        st.caption("AI-powered scam investigation assistant")
        st.divider()

        mode = st.selectbox(
            "INVESTIGATION MODE",
            ["Quick Check", "Deep Investigation"],
            index=0,
            key="mode",
        )
        style = st.selectbox(
            "RESPONSE STYLE",
            ["Concise", "Balanced", "Detailed"],
            index=1,
            key="style",
        )
        accent = st.selectbox(
            "ACCENT COLOR",
            list(ACCENTS),
            index=list(ACCENTS).index("Amber"),
            key="accent",
        )

        st.markdown("**THEME**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "☀ Light",
                use_container_width=True,
                key="btn_light",
                type="primary" if not st.session_state.dark else "secondary",
            ):
                st.session_state.dark = False
                st.rerun()
        with c2:
            if st.button(
                "🌙 Dark",
                use_container_width=True,
                key="btn_dark",
                type="primary" if st.session_state.dark else "secondary",
            ):
                st.session_state.dark = True
                st.rerun()

        st.caption(f"Active: {'Dark' if st.session_state.dark else 'Light'} · {accent}")
        st.divider()

        st.markdown("**KNOWLEDGE BASE**")
        st.caption(st.session_state.get("kb_status", "Not initialized"))
        st.divider()

        st.markdown("**RECENT INVESTIGATIONS**")
        history = st.session_state.history
        if history:
            for h in history[-5:][::-1]:
                st.caption(h[:65] + ("…" if len(h) > 65 else ""))
        else:
            st.caption("No investigations yet.")

        if st.button("Clear Chat History", use_container_width=True, key="btn_clear"):
            st.session_state.history = []
            st.session_state.messages = []
            st.rerun()

    return mode, style, accent
