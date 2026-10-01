import streamlit as st


def hero():
    st.markdown(
        """
        <div class="hero">
          <div class="logo">🛡️</div>
          <h1>ScamHunter <span>AI</span></h1>
          <p>
            Investigate suspicious messages, offers, links and online claims
            with AI-powered evidence analysis.
          </p>
          <div class="badge">● Evidence-first AI investigation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_card(item):
    """
    Render a citation card for either Knowledge Base or Web evidence.

    Supports both:
    - flat evidence dictionaries
    - evidence dictionaries containing a nested `source` object
    """

    if not isinstance(item, dict):
        item = {"text": str(item)}

    source = item.get("source")

    # Some pipeline stages wrap the original source inside
    # item["source"]. Merge both levels so metadata is preserved.
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

    # ---------------------------------------------------------------
    # KNOWLEDGE BASE
    # ---------------------------------------------------------------

    if source_type == "knowledge_base":
        filename = (
            item.get("filename")
            or item.get("title")
            or "Knowledge Base Document"
        )

        page = item.get("page")
        section = item.get("section") or "General"
        chunk_id = item.get("chunk_id")

        detail_parts = []

        if page is not None:
            detail_parts.append(f"Page {page}")

        if section:
            detail_parts.append(section)

        if chunk_id:
            detail_parts.append(chunk_id)

        detail = " · ".join(detail_parts)

        excerpt = (
            item.get("excerpt")
            or item.get("text")
            or item.get("content")
            or ""
        )

        st.markdown(
            f"""
            <div class="source">
              <b>📄 {filename}</b><br>
              <span class="muted">{detail}</span>
              <br><br>
              {excerpt}
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # ---------------------------------------------------------------
    # WEB SOURCE
    # ---------------------------------------------------------------

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

    st.markdown(
        f"""
        <div class="source">
          <b>🌐 {title}</b><br>
          <span class="muted">{url}</span>
          <br><br>
          {excerpt}
        </div>
        """,
        unsafe_allow_html=True,
    )
