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
    source_type = (
        item.get("source_type")
        or item.get("type")
        or ""
    ).lower()

    # -----------------------------
    # Knowledge Base source
    # -----------------------------
    if source_type == "knowledge_base":
        title = (
            item.get("filename")
            or item.get("title")
            or "Knowledge Base Document"
        )

        page = item.get("page")
        section = item.get("section") or "General"
        chunk_id = item.get("chunk_id") or ""

        detail_parts = []

        if page:
            detail_parts.append(f"Page {page}")

        if section:
            detail_parts.append(section)

        if chunk_id:
            detail_parts.append(chunk_id)

        detail = " · ".join(detail_parts)

        excerpt = (
            item.get("excerpt")
            or item.get("text")
            or ""
        )

        st.markdown(
            f"""
            <div class="source">
              <b>📄 {title}</b><br>
              <span class="muted">{detail}</span>
              <br><br>
              {excerpt}
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # -----------------------------
    # Web source
    # -----------------------------
    title = (
        item.get("title")
        or item.get("url")
        or "Web source"
    )

    detail = item.get("url", "")

    excerpt = (
        item.get("snippet")
        or item.get("excerpt")
        or ""
    )

    st.markdown(
        f"""
        <div class="source">
          <b>🌐 {title}</b><br>
          <span class="muted">{detail}</span>
          <br><br>
          {excerpt}
        </div>
        """,
        unsafe_allow_html=True,
    )
