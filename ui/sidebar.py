import streamlit as st
from ui.theme import ACCENTS


def render():
    # Keep theme state available before rendering controls
    if "dark" not in st.session_state:
        st.session_state.dark = False

    with st.sidebar:

        # ---------------------------------------------------------
        # BRAND
        # ---------------------------------------------------------
        st.markdown(
            """
            <div style="
                font-weight:800;
                font-size:18px;
                letter-spacing:.4px;
                margin-bottom:4px;
            ">
                🛡️ SCAMHUNTER AI
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("AI-powered scam investigation assistant")
        st.divider()

        # ---------------------------------------------------------
        # INVESTIGATION SETTINGS
        # ---------------------------------------------------------
        mode = st.selectbox(
            "INVESTIGATION MODE",
            ["Quick Check", "Deep Investigation"],
            index=0,
            key="investigation_mode",
        )

        style = st.selectbox(
            "RESPONSE STYLE",
            ["Concise", "Balanced", "Detailed"],
            index=1,
            key="response_style",
        )

        accent = st.selectbox(
            "ACCENT COLOR",
            list(ACCENTS.keys()),
            index=0,
            key="accent_color",
        )

        # ---------------------------------------------------------
        # THEME
        # ---------------------------------------------------------
        st.markdown("**THEME**")

        c1, c2 = st.columns(2)

        with c1:
            if st.button(
                "☀ Light",
                use_container_width=True,
                key="theme_light",
            ):
                st.session_state.dark = False
                st.rerun()

        with c2:
            if st.button(
                "🌙 Dark",
                use_container_width=True,
                key="theme_dark",
            ):
                st.session_state.dark = True
                st.rerun()

        current_theme = "Dark" if st.session_state.dark else "Light"

        st.caption(
            f"Active: {current_theme} · {accent}"
        )

        st.divider()

        # ---------------------------------------------------------
        # KNOWLEDGE BASE
        # ---------------------------------------------------------
        st.markdown("**KNOWLEDGE BASE**")

        kb_status = st.session_state.get(
            "kb_status",
            "Not initialized",
        )

        st.caption(kb_status)

        st.divider()

        # ---------------------------------------------------------
        # RECENT INVESTIGATIONS
        # ---------------------------------------------------------
        st.markdown("**RECENT INVESTIGATIONS**")

        history = st.session_state.get(
            "history",
            [],
        )

        if history:
            for index, item in enumerate(
                history[-5:][::-1]
            ):
                text = str(item)

                if len(text) > 65:
                    text = text[:65] + "…"

                st.caption(
                    f"{index + 1}. {text}"
                )
        else:
            st.caption(
                "No investigations yet."
            )

        st.divider()

        # ---------------------------------------------------------
        # CLEAR HISTORY
        # ---------------------------------------------------------
        if st.button(
            "Clear Chat History",
            use_container_width=True,
            key="clear_history",
        ):
            st.session_state.history = []
            st.session_state.messages = []
            st.rerun()

        return mode, style, accent
