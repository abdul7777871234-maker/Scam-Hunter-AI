from __future__ import annotations

import inspect
import tempfile
import time
from html import escape
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
from ui.sidebar import render as render_sidebar, render_footer
from ui.components import hero, source_card
from ui.verdict import extract_verdict, badge_html
from ui.history_store import new_id, valid_uid, load_chats, save_chat


# -------------------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------------------

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
S.setdefault("kb_status", "Knowledge base not initialized")
S.setdefault("chat_id", new_id())
S.setdefault("answer_cache", {})


# -------------------------------------------------------------------
# BROWSER ID
# -------------------------------------------------------------------

if not valid_uid(S.get("uid")):
    url_uid = st.query_params.get("u")
    S.uid = url_uid if valid_uid(url_uid) else new_id()

if st.query_params.get("u") != S.uid:
    st.query_params["u"] = S.uid

uid = S.uid


# -------------------------------------------------------------------
# OPEN A SAVED CHAT
# -------------------------------------------------------------------

pending_chat = S.pop("load_chat_id", None)

if pending_chat:
    for saved in load_chats(uid):
        if saved.get("id") == pending_chat:
            S.messages = saved.get("messages", [])
            S.chat_id = saved["id"]
            break


# -------------------------------------------------------------------
# SIDEBAR + THEME
# -------------------------------------------------------------------

mode, style, accent = render_sidebar()

apply_theme(S.dark, accent)


# -------------------------------------------------------------------
# RUNTIME
# -------------------------------------------------------------------

@st.cache_resource(show_spinner="Loading models and knowledge base…")
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


# -------------------------------------------------------------------
# KNOWLEDGE BASE STATUS
# -------------------------------------------------------------------

if kb.store.count:
    S.kb_status = f"{kb.store.count:,} chunks indexed"
else:
    S.kb_status = "Knowledge base ready for document indexing."


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

PIPELINE_ICONS = (
    ("knowledge", "📚"),
    ("web", "🌐"),
    ("evidence", "🔬"),
    ("pattern", "🧩"),
    ("contradiction", "⚖️"),
    ("review", "🧑‍⚖️"),
    ("response", "✍️"),
    ("quality", "🛡️"),
)


def pipeline_icon(event: str) -> str:
    low = event.lower()
    for key, icon in PIPELINE_ICONS:
        if key in low:
            return icon
    return "✓"


def render_pipeline(events: list) -> None:
    """
    Render the whole pipeline as ONE html string.

    No indentation and no blank lines: Markdown treats an indented
    line or a blank line inside HTML as a code block, which was
    the cause of the raw-code display.
    """
    if not events:
        st.caption("No pipeline events were recorded.")
        return

    steps = []

    for event in events:
        name = escape(str(event))
        steps.append(
            '<div class="pipeline-step">'
            f'<div class="pipeline-icon">{pipeline_icon(str(event))}</div>'
            '<div class="pipeline-text">'
            f'<div class="pipeline-name">{name}</div>'
            '<div class="pipeline-status">Completed</div>'
            "</div></div>"
        )

    html = (
        '<div class="pipeline-card">'
        + '<div class="pipeline-arrow">↓</div>'.join(steps)
        + "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)


def render_disclaimer() -> None:
    st.markdown(
        '<div class="footer-card"><span class="muted">'
        "🔒 Evidence is treated as untrusted data.<br>"
        "ScamHunter AI provides investigation support and does not "
        "guarantee the authenticity or safety of any person, site, "
        "message, or offer."
        "</span></div>",
        unsafe_allow_html=True,
    )


# -------------------------------------------------------------------
# INVESTIGATION ROUTER
# -------------------------------------------------------------------

def run_investigation(text: str) -> dict:
    """
    Quick Check:
        FAISS/RAG -> Evidence Agent -> Response Agent

    Deep Investigation:
        Full multi-agent investigation pipeline.
    """

    if mode == "Quick Check":
        quick_method = getattr(orchestrator, "run_quick", None)

        if quick_method is None:
            raise RuntimeError(
                "Quick Check is not available. "
                "Please make sure agents/orchestrator.py "
                "contains run_quick()."
            )

        return quick_method(text)

    params = inspect.signature(orchestrator.run).parameters

    kwargs = {}

    if "mode" in params:
        kwargs["mode"] = mode

    if "style" in params:
        kwargs["style"] = style

    return orchestrator.run(text, **kwargs)


# -------------------------------------------------------------------
# HERO
# -------------------------------------------------------------------

hero()


# -------------------------------------------------------------------
# CHAT HISTORY
# -------------------------------------------------------------------

for message in S.messages:
    with st.chat_message(message["role"]):
        if message.get("verdict"):
            st.markdown(
                badge_html(message["verdict"]),
                unsafe_allow_html=True,
            )

        st.markdown(message["content"])


# -------------------------------------------------------------------
# CHAT INPUT + ATTACHMENT
# -------------------------------------------------------------------

submission = st.chat_input(
    "Investigate a suspicious message, offer, link, or document…",
    accept_file=True,
    file_type=["pdf", "docx", "txt", "md", "png", "jpg", "jpeg", "webp"],
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

    # ---------------------------------------------------------------
    # PROCESS ATTACHMENTS
    # ---------------------------------------------------------------

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
                attachment_context.append(f"Attached document: {safe_name}")

            elif suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                attachment_context.append(f"Attached image: {safe_name}")

        except Exception as exc:
            st.error(f"Attachment error: {exc}")

    # ---------------------------------------------------------------
    # ONLY CONTINUE IF THERE IS CONTENT
    # ---------------------------------------------------------------

    if prompt or attachment_context:

        display_prompt = prompt if prompt else "\n".join(attachment_context)

        S.messages.append({"role": "user", "content": display_prompt})
        save_chat(uid, S.chat_id, S.messages)

        with st.chat_message("user"):
            st.markdown(display_prompt)

        cache_key = (mode, style, display_prompt)

        # Uploaded files should not use the normal text-answer cache.
        use_cache = not uploaded_files

        empty_result = {
            "answer": "",
            "events": [],
            "rag": {"items": [], "evidence": []},
            "web": {"items": [], "cached": False},
        }

        # -----------------------------------------------------------
        # INVESTIGATION
        # -----------------------------------------------------------

        with st.chat_message("assistant"):

            result = empty_result
            verdict = None

            cached = S.answer_cache.get(cache_key) if use_cache else None

            # ---- cached response ----
            if cached:
                result = cached

                parsed = extract_verdict(result, result.get("answer", ""))
                answer = parsed["answer"]
                verdict = parsed["verdict"]

                if verdict:
                    st.markdown(badge_html(verdict), unsafe_allow_html=True)

                st.markdown(answer)
                st.caption("⚡ Instant (cached)")

            # ---- new investigation ----
            else:
                label = (
                    "⚡ Quick check…"
                    if mode == "Quick Check"
                    else "🔎 Deep investigation…"
                )

                started = time.perf_counter()

                with st.spinner(label):
                    try:
                        result = run_investigation(display_prompt)

                        raw_answer = result.get(
                            "answer",
                            "No investigation result was returned.",
                        )

                        if use_cache and result.get("answer"):
                            S.answer_cache[cache_key] = result

                        parsed = extract_verdict(result, raw_answer)
                        answer = parsed["answer"]
                        verdict = parsed["verdict"]

                    except Exception as exc:
                        answer = (
                            "Investigation could not be completed.\n\n"
                            f"`{exc}`"
                        )
                        result = empty_result
                        verdict = None

                elapsed = time.perf_counter() - started

                if verdict:
                    st.markdown(badge_html(verdict), unsafe_allow_html=True)

                st.markdown(answer)
                st.caption(f"⏱ {elapsed:.1f}s · {mode}")

            # ---- save assistant message ----
            assistant_message = {"role": "assistant", "content": answer}

            if verdict:
                assistant_message["verdict"] = verdict

            S.messages.append(assistant_message)
            save_chat(uid, S.chat_id, S.messages)

        # ===========================================================
        # EVIDENCE SECTION
        # ===========================================================

        st.divider()

        with st.expander("🧠 Investigation Pipeline", expanded=False):
            render_pipeline(result.get("events", []))

        with st.expander("Knowledge Base Evidence", expanded=False):
            items = result.get("rag", {}).get("evidence", [])

            if items:
                for item in items:
                    source_card(item)
            else:
                st.caption("No matching internal evidence was retrieved.")

        with st.expander("Web Evidence", expanded=False):
            items = result.get("web", {}).get("items", [])

            if items:
                for item in items:
                    source_card(item)
            else:
                st.caption("No web evidence was retrieved.")


# -------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------

render_disclaimer()

render_footer(uid, S.kb_status)
