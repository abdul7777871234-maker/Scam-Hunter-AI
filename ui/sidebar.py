import streamlit as st

from ui.theme import ACCENTS
from ui.history_store import load_chats, new_id, delete_all
from ui.verdict import LEVELS


def render():
    """Top part of the sidebar (controls). Returns (mode, style, accent)."""

    st.session_state.setdefault("dark", True)
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

        st.caption(
            f"Active: {'Dark' if st.session_state.dark else 'Light'} · {accent}"
        )

    return mode, style, accent


def _last_dot(chat: dict) -> str:
    for m in reversed(chat.get("messages", [])):
        level = (m.get("verdict") or {}).get("level")
        if level in LEVELS:
            return LEVELS[level]["emoji"]
    return "⚪"


def render_footer(uid: str, kb_status: str):
    """Bottom part of the sidebar. Call at the END of app.py so the saved
    chat list is always up to date."""

    with st.sidebar:
        st.divider()
        st.markdown("**KNOWLEDGE BASE**")
        st.caption(kb_status)
        st.divider()

        st.markdown("**RECENT INVESTIGATIONS**")
        chats = load_chats(uid)

        if chats:
            current = st.session_state.get("chat_id")
            for chat in chats[:10]:
                title = chat.get("title", "Chat")
                label = f"{_last_dot(chat)} {title}"
                if chat.get("id") == current:
                    label = "▸ " + label
                if st.button(
                    label,
                    key=f"open_{chat['id']}",
                    use_container_width=True,
                ):
                    st.session_state.load_chat_id = chat["id"]
                    st.rerun()
            st.caption("Bookmark this page to get your saved chats back later.")
        else:
            st.caption("No investigations yet.")

        if st.button("Clear Chat", use_container_width=True, key="btn_clear"):
            # Clears the screen only. Saved chats stay in the list above.
            st.session_state.messages = []
            st.session_state.chat_id = new_id()
            st.rerun()

        with st.popover("Delete saved history", use_container_width=True):
            st.caption("This permanently deletes all saved chats for this browser link.")
            if st.button("Yes, delete everything", key="btn_delete_all"):
                delete_all(uid)
                st.session_state.messages = []
                st.session_state.chat_id = new_id()
                st.rerun()
