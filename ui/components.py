from __future__ import annotations

import html

import streamlit as st


def hero():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-logo">🛡️</div>

            <div class="hero-title">
                ScamHunter <span>AI</span>
            </div>

            <div class="hero-description">
                Investigate suspicious messages, offers, links and online
                claims with AI-powered evidence analysis.
            </div>

            <div class="hero-badge">
                <span class="hero-badge-dot">●</span>
                Evidence-first AI investigation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_card(item):
    """
    Render a safe, theme-aware evidence citation card.

    Supports:
    - Knowledge Base evidence
    - Web evidence
    - Flat evidence dictionaries
    - Nested source dictionaries
    """

    if not isinstance(item, dict):
        item = {"text": str(item)}

    source = item.get("source")

    if isinstance(source, dict):
        merged = dict(source)

        for key, value in item.items():
            if key != "source" and value not in (None, ""):
                merged[key] = value

        item = merged

    source_type = (
        item.get("source_type")
        or item.get("type")
        or ""
    ).lower()

    # ---------------------------------------------------------
    # KNOWLEDGE BASE SOURCE
    # ---------------------------------------------------------

    if source_type == "knowledge_base":
        filename = (
            item.get("filename")
            or item.get("title")
            or "Knowledge Base Document"
        )

        page = item.get("page")
        section = item.get("section") or "General"
        chunk_id = item.get("chunk_id")

        details = []

        if page is not None:
            details.append(f"Page {page}")

        if section:
            details.append(section)

        if chunk_id:
            details.append(chunk_id)

        detail_text = " · ".join(details)

        excerpt = (
            item.get("excerpt")
            or item.get("text")
            or item.get("content")
            or ""
        )

        filename = html.escape(str(filename))
        detail_text = html.escape(str(detail_text))
        excerpt = html.escape(str(excerpt)).replace("\n", "<br>")

        st.markdown(
            f"""
            <div class="source-card source-card-kb">

                <div class="source-header">
                    <div class="source-icon">📄</div>

                    <div class="source-heading">
                        <div class="source-title">
                            {filename}
                        </div>

                        <div class="source-meta">
                            {detail_text}
                        </div>
                    </div>
                </div>

                <div class="source-excerpt">
                    {excerpt}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # ---------------------------------------------------------
    # WEB SOURCE
    # ---------------------------------------------------------

    title = (
        item.get("title")
        or item.get("url")
        or "Web source"
    )

    url = item.get("url", "")

    excerpt = (
        item.get("snippet")
        or item.get("excerpt")
        or item.get("text")
        or item.get("content")
        or ""
    )

    title = html.escape(str(title))
    url = html.escape(str(url))
    excerpt = html.escape(str(excerpt)).replace("\n", "<br>")

    st.markdown(
        f"""
        <div class="source-card source-card-web">

            <div class="source-header">
                <div class="source-icon">🌐</div>

                <div class="source-heading">
                    <div class="source-title">
                        {title}
                    </div>

                    <div class="source-meta">
                        {url}
                    </div>
                </div>
            </div>

            <div class="source-excerpt">
                {excerpt}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def section_label(text: str):
    """Render a small uppercase section label."""

    safe_text = html.escape(str(text))

    st.markdown(
        f'<div class="section-label">{safe_text}</div>',
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str, icon: str = "ℹ️"):
    """Render a generic theme-aware information card."""

    safe_title = html.escape(str(title))
    safe_body = html.escape(str(body)).replace("\n", "<br>")
    safe_icon = html.escape(str(icon))

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-card-title">
                <span class="info-card-icon">{safe_icon}</span>
                <span>{safe_title}</span>
            </div>

            <div class="info-card-body">
                {safe_body}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )
