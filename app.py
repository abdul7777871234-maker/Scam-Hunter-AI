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

st.set_page_config(page_title="ScamHunter AI", page_icon="🛡️", layout="wide")

S = st.session_state
S.setdefault("dark", False)
S.setdefault("messages", [])
S.setdefault("history", [])
S.setdefault("kb_ready", False)

settings = Settings.from_runtime()
mode, style, accent = render_sidebar()
apply_theme(S.dark, accent)

# Cache expensive resources.
@st.cache_resource
def get_runtime():
    settings = Settings.from_runtime()
    kb = KnowledgeBase(settings)
    router = ModelRouter(settings)
    retriever = Retriever(kb, settings)
    web = WebSearch(settings)
    orchestrator = InvestigationOrchestrator(router, retriever, web, settings)
    return settings, kb, router, retriever, web, orchestrator

settings, kb, router, retriever, web, orchestrator = get_runtime()

if kb.store.count:
    S.kb_status = f"{kb.store.count:,} chunks indexed"
else:
    S.kb_status = "Knowledge base empty — use the setup script or upload documents."

hero()

st.markdown('<div class="section-label">Suggested Investigations</div>', unsafe_allow_html=True)
cols = st.columns(2)
suggestions = [
    "Analyze this suspicious job offer for scam signals.",
    "Analyze these payment instructions for suspicious patterns.",
    "Check this investment message for red flags and evidence.",
    "Analyze this phishing-style account verification message.",
]
for i, text in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(text, use_container_width=True, key=f"s{i}"):
            S["pending_prompt"] = text

st.markdown('<div class="section-label">Investigation Workspace</div>', unsafe_allow_html=True)

upload = st.file_uploader(
    "Attach evidence",
    type=["pdf","docx","txt","md","png","jpg","jpeg","webp"],
    help="Maximum 10 MB per file.",
)
if upload:
    try:
        safe_name = validate_upload(upload.name, settings.max_upload_mb)
        tmp = Path(tempfile.gettempdir()) / safe_name
        tmp.write_bytes(upload.getbuffer())
        if tmp.suffix.lower() in {".pdf",".docx",".txt",".md"}:
            kb.add_upload(tmp)
            S.kb_status = "New document copied. Run the knowledge-base build script to embed it."
        st.success(f"Attached: {safe_name}")
    except Exception as exc:
        st.error(str(exc))

default_prompt = S.pop("pending_prompt", "")
prompt = st.chat_input("Paste a suspicious message, offer, URL, or question…")
if not prompt and default_prompt:
    prompt = default_prompt

if prompt:
    S.messages.append({"role":"user","content":prompt})
    S.history.append(prompt)
    with st.spinner("Running evidence-first investigation…"):
        try:
            result = orchestrator.run(prompt)
            answer = result["answer"]
            S.messages.append({"role":"assistant","content":answer})
        except Exception as exc:
            answer = f"Investigation could not be completed: {exc}"
            S.messages.append({"role":"assistant","content":answer})
            result = {"events": [], "rag": {"evidence":[]}, "web":{"items":[]}}

for m in S.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if S.messages and S.messages[-1]["role"] == "assistant" and "result" in locals():
    st.divider()
    with st.expander("Investigation Pipeline", expanded=False):
        for event in result.get("events", []):
            st.write("✓ " + event)

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

st.markdown("""
<div class="card" style="margin-top:24px;text-align:center">
<span class="muted">🔒 Evidence is treated as untrusted data. ScamHunter AI provides investigation support and does not guarantee the authenticity or safety of any person, site, message, or offer.</span>
</div>
""", unsafe_allow_html=True)
