from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from config.settings import Settings
from providers.model_router import ModelRouter
from rag.ingestion import KnowledgeBase
from rag.retriever import Retriever
from tools.web_search import WebSearch
from tools.document_tools import validate_upload
from agents.orchestrator import InvestigationOrchestrator
from ui.theme import apply_theme
from ui.sidebar import render as render_sidebar
from ui.components import hero, source_card


st.set_page_config(
    page_title="ScamHunter AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------------------

S = st.session_state

S.setdefault("dark", False)
S.setdefault("messages", [])
S.setdefault("history", [])
S.setdefault("kb_status", "Knowledge base not initialized")


# -------------------------------------------------------------------
# SETTINGS
# -------------------------------------------------------------------

settings = Settings.from_runtime()

mode, style, accent = render_sidebar()
apply_theme(S.dark, accent)


# -------------------------------------------------------------------
# RUNTIME
# -------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_runtime():
    runtime_settings = Settings.from_runtime()

    kb = KnowledgeBase(runtime_settings)
    router = ModelRouter(runtime_settings)
    retriever = Retriever(kb, runtime_settings)
    web = WebSearch(runtime_settings)

    orchestrator = InvestigationOrchestrator(
        router,
        retriever,
        web,
        runtime_settings,
    )

    return runtime_settings, kb, router, retriever, web, orchestrator


settings, kb, router, retriever, web, orchestrator = get_runtime()


if kb.store.count:
    S.kb_status = f"{kb.store.count:,} chunks indexed"
else:
    S.kb_status = "Knowledge base ready for document indexing."


# -------------------------------------------------------------------
# HERO
# -------------------------------------------------------------------

hero()


# -------------------------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------------------------

for message in S.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------------------------------------------------
# CHAT INPUT + ATTACHMENT
# -------------------------------------------------------------------

submission = st.chat_input(
    "Investigate a suspicious message, offer, link, or document…",
    accept_file=True,
    file_type=[
        "pdf",
        "docx",
        "txt",
        "md",
        "png",
        "jpg",
        "jpeg",
        "webp",
    ],
    max_upload_size=settings.max_upload_mb,
    key="scamhunter_chat",
)


# -------------------------------------------------------------------
# PROCESS SUBMISSION
# -------------------------------------------------------------------

if submission:

    prompt = submission.text.strip()

    uploaded_files = list(submission.files or [])

    attachment_context = []

    for uploaded in uploaded_files:
        try:
            safe_name = validate_upload(
                uploaded.name,
                settings.max_upload_mb,
            )

            temp_path = Path(tempfile.gettempdir()) / safe_name
            temp_path.write_bytes(uploaded.getbuffer())

            suffix = temp_path.suffix.lower()

            if suffix in {".pdf", ".docx", ".txt", ".md"}:
                kb.add_upload(temp_path)
                attachment_context.append(
                    f"Attached document: {safe_name}"
                )

            elif suffix in {
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
            }:
                attachment_context.append(
                    f"Attached image: {safe_name}"
                )

        except Exception as exc:
            st.error(f"Attachment error: {exc}")

    if attachment_context:
        S.history.extend(attachment_context)

    if prompt or attachment_context:

        if prompt:
            display_prompt = prompt
        else:
            display_prompt = "\n".join(attachment_context)

        S.messages.append(
            {
                "role": "user",
                "content": display_prompt,
            }
        )

        S.history.append(display_prompt)

        with st.chat_message("user"):
            st.markdown(display_prompt)

        # -----------------------------------------------------------
        # INVESTIGATION
        # -----------------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner("Investigating evidence…"):

                try:

                    result = orchestrator.run(display_prompt)

                    answer = result.get(
                        "answer",
                        "No investigation result was returned.",
                    )

                    st.markdown(answer)

                    S.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except Exception as exc:

                    answer = (
                        "Investigation could not be completed.\n\n"
                        f"`{exc}`"
                    )

                    st.error(answer)

                    S.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                    result = {
                        "events": [],
                        "rag": {"evidence": []},
                        "web": {"items": []},
                    }


        # -----------------------------------------------------------
        # EVIDENCE
        # -----------------------------------------------------------

        st.divider()

        with st.expander(
            "Investigation Pipeline",
            expanded=False,
        ):
            for event in result.get("events", []):
                st.write("✓ " + event)

        with st.expander(
            "Knowledge Base Evidence",
            expanded=False,
        ):
            items = result.get("rag", {}).get("evidence", [])

            if items:
                for item in items:
                    source_card(item)
            else:
                st.caption(
                    "No matching internal evidence was retrieved."
                )

        with st.expander(
            "Web Evidence",
            expanded=False,
        ):
            items = result.get("web", {}).get("items", [])

            if items:
                for item in items:
                    source_card(item)
            else:
                st.caption(
                    "No web evidence was retrieved."
                )


# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------

st.markdown(
    """
    <div class="card footer-card">
        <span class="muted">
            🔒 Evidence is treated as untrusted data.
            ScamHunter AI provides investigation support and does not
            guarantee the authenticity or safety of any person, site,
            message, or offer.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
