from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO


PAGE_W = 612
PAGE_H = 792
MARGIN = 42

NAVY = (0.035, 0.055, 0.10)
PANEL = (0.075, 0.095, 0.16)
PANEL_2 = (0.055, 0.072, 0.13)
TEXT = (0.94, 0.96, 0.99)
MUTED = (0.58, 0.64, 0.73)
CYAN = (0.10, 0.78, 0.96)
BLUE = (0.20, 0.42, 1.00)
GREEN = (0.20, 0.78, 0.45)
YELLOW = (0.95, 0.68, 0.16)
RED = (0.95, 0.25, 0.30)
WHITE = (1.0, 1.0, 1.0)


def _esc(text):
    return (
        str(text or "")
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
        .replace("\r", "")
        .replace("\n", " ")
    )


def _rgb(color):
    return " ".join(f"{value:.3f}" for value in color)


def _text(cmd, x, y, value, size=10, color=TEXT, font="F1"):
    return (
        f"BT /{font} {size} Tf {_rgb(color)} rg "
        f"{x:.1f} {y:.1f} Td ({_esc(value)}) Tj ET"
    )


def _line(cmd, x1, y1, x2, y2, color=MUTED, width=0.7):
    cmd.append(
        f"{_rgb(color)} RG {width:.2f} w "
        f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"
    )


def _rect(cmd, x, y, w, h, fill, stroke=None, width=0.7, radius=False):
    # Rounded rectangles are intentionally avoided so the PDF stays dependency-free.
    cmd.append(f"{_rgb(fill)} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")
    if stroke:
        cmd.append(
            f"{_rgb(stroke)} RG {width:.2f} w "
            f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re S"
        )


def _wrap(text, width=92):
    words = str(text or "").replace("\r", "").split()
    if not words:
        return [""]
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            while len(word) > width:
                lines.append(word[:width])
                word = word[width:]
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _source_lines(source):
    if not isinstance(source, dict):
        return [str(source or "Source")]
    title = source.get("title") or source.get("filename") or "Source"
    source_type = source.get("source_type", "")
    meta = []
    if source_type == "knowledge_base":
        if source.get("page"):
            meta.append(f"Page {source['page']}")
        meta.append("Knowledge Base")
    elif source_type == "web":
        meta.append("Web Evidence")
    if source.get("url"):
        meta.append(source["url"])
    return [str(title)] + meta


def _risk_color(verdict=None, scan=None):
    level = str((verdict or {}).get("level") or (scan or {}).get("level") or "").lower()
    if level in {"red", "high", "critical"}:
        return RED
    if level in {"yellow", "medium", "elevated", "low"}:
        return YELLOW
    if level in {"green", "safe", "none"}:
        return GREEN
    return CYAN


def _risk_label(verdict=None, scan=None):
    level = str((verdict or {}).get("level") or (scan or {}).get("level") or "").strip()
    return level.replace("_", " ").upper() if level else "REVIEW"


def _draw_watermark(cmd):
    # Large, low-opacity-style vector/text watermark behind the report content.
    cmd.append("q")
    cmd.append("0.11 0.14 0.22 rg")
    cmd.append("BT /F2 54 Tf 0.35 Tc 0 1 -1 0 250 300 Tm (SCAMHUNTER AI) Tj ET")
    cmd.append("Q")


def _draw_header(cmd, generated, mode, language):
    _rect(cmd, 0, PAGE_H - 94, PAGE_W, 94, NAVY)
    # Shield-style brand mark drawn with simple vector geometry.
    cmd.append(
        f"{_rgb(CYAN)} rg "
        "58 733 m 58 760 l 74 769 l 90 760 l 90 733 "
        "c 0 -14 -12 -25 -16 -28 c -4 3 -16 14 -16 28 h 0 f"
    )
    cmd.append(f"{_rgb(NAVY)} rg 70 735 m 70 752 l 78 757 l 78 735 l 74 729 l 70 735 f")
    cmd.append(_text(cmd, 106, 748, "SCAMHUNTER AI", 20, WHITE, "F2"))
    cmd.append(_text(cmd, 106, 730, "AI-POWERED SCAM INVESTIGATION REPORT", 8.5, CYAN, "F2"))
    cmd.append(_text(cmd, 430, 750, "CONFIDENTIAL", 8, MUTED, "F2"))
    cmd.append(_text(cmd, 430, 734, generated, 7.5, MUTED, "F1"))
    cmd.append(_text(cmd, 430, 720, f"{mode} • {language}", 7.5, MUTED, "F1"))


def _draw_footer(cmd, page_no, page_count):
    _line(cmd, 42, 34, 570, 34, (0.15, 0.19, 0.27), 0.6)
    cmd.append(_text(cmd, 42, 21, "SCAMHUNTER AI  •  Investigation support, not a fraud determination", 7, MUTED))
    cmd.append(_text(cmd, 520, 21, f"{page_no}/{page_count}", 7, MUTED, "F2"))


def _build_page(commands, page_no, page_count, generated, mode, language):
    _draw_watermark(commands)
    _draw_header(commands, generated, mode, language)
    _draw_footer(commands, page_no, page_count)


def build_report(
    question,
    answer,
    verdict=None,
    scan=None,
    sources=None,
    mode="Quick Check",
    language="English",
):
    generated_dt = datetime.now(timezone.utc)
    generated = generated_dt.strftime("%Y-%m-%d %H:%M UTC")
    risk = _risk_color(verdict, scan)
    risk_label = _risk_label(verdict, scan)

    content = []
    pages = []
    page = []

    # Page 1: executive report.
    page.append(_text(page, 42, 680, "INVESTIGATION SUMMARY", 9, CYAN, "F2"))
    page.append(_text(page, 42, 650, "ScamHunter AI Investigation Report", 24, TEXT, "F2"))
    page.append(_text(page, 42, 628, "A structured snapshot of the investigation performed by the application.", 9, MUTED))

    # Metadata strip.
    _rect(page, 42, 575, 528, 38, PANEL, (0.13, 0.18, 0.28))
    page.append(_text(page, 56, 590, "GENERATED", 7, MUTED, "F2"))
    page.append(_text(page, 126, 590, generated, 8.5, TEXT))
    page.append(_text(page, 310, 590, "MODE", 7, MUTED, "F2"))
    page.append(_text(page, 348, 590, mode, 8.5, TEXT))
    page.append(_text(page, 455, 590, "LANGUAGE", 7, MUTED, "F2"))
    page.append(_text(page, 505, 590, language, 8.5, TEXT))

    # Risk card.
    _rect(page, 42, 485, 528, 68, PANEL_2, risk)
    page.append(_text(page, 58, 529, "ASSESSMENT SIGNAL", 7.5, MUTED, "F2"))
    page.append(_text(page, 58, 506, risk_label, 20, risk, "F2"))
    if scan:
        score = scan.get("score", 0)
        page.append(_text(page, 220, 512, f"Signal score: {score}/100", 10, TEXT, "F2"))
        headline = scan.get("headline", "")
        if headline:
            wrapped = _wrap(headline, 56)
            page.append(_text(page, 220, 496, wrapped[0], 8.5, MUTED))
            if len(wrapped) > 1:
                page.append(_text(page, 220, 484, wrapped[1], 8.5, MUTED))
    elif verdict:
        category = verdict.get("category") or "Not specified"
        page.append(_text(page, 220, 512, f"Category: {category}", 10, TEXT, "F2"))

    # User content.
    page.append(_text(page, 42, 456, "USER CONTENT", 9, CYAN, "F2"))
    y = 436
    for line in _wrap(question or "(No text provided.)", 91):
        if y < 125:
            break
        page.append(_text(page, 42, y, line, 9, TEXT))
        y -= 14

    # AI response.
    y -= 12
    page.append(_text(page, 42, y, "AI INVESTIGATION", 9, CYAN, "F2"))
    y -= 22
    for paragraph in str(answer or "(No answer generated.)").replace("\r", "").split("\n"):
        for line in _wrap(paragraph, 91):
            if y < 66:
                pages.append(page)
                page = []
                y = 680
                _build_page(page, len(pages) + 1, 0, generated, mode, language)
            page.append(_text(page, 42, y, line, 8.8, TEXT))
            y -= 13
        y -= 4

    # Sources always get their own continuation area so the report remains readable.
    if sources:
        if y < 190:
            pages.append(page)
            page = []
            y = 680
            _build_page(page, len(pages) + 1, 0, generated, mode, language)
        page.append(_text(page, 42, y, "EVIDENCE & SOURCES", 9, CYAN, "F2"))
        y -= 20
        for index, source in enumerate(sources, 1):
            source_lines = _source_lines(source)
            title = source_lines[0]
            if y < 90:
                pages.append(page)
                page = []
                y = 680
                _build_page(page, len(pages) + 1, 0, generated, mode, language)
            page.append(_text(page, 42, y, f"{index:02d}", 8, CYAN, "F2"))
            page.append(_text(page, 70, y, title[:78], 8.5, TEXT, "F2"))
            y -= 13
            for detail in source_lines[1:]:
                for line in _wrap(detail, 83):
                    if y < 60:
                        pages.append(page)
                        page = []
                        y = 680
                        _build_page(page, len(pages) + 1, 0, generated, mode, language)
                    page.append(_text(page, 70, y, line, 7.3, MUTED))
                    y -= 11
            y -= 7

    pages.append(page)

    # Instant scan details get a compact final block when space permits.
    if scan and scan.get("flags"):
        page = []
        _build_page(page, len(pages) + 1, 0, generated, mode, language)
        page.append(_text(page, 42, 680, "INSTANT SCAN DETAILS", 9, CYAN, "F2"))
        page.append(_text(page, 42, 650, "Detected signals", 18, TEXT, "F2"))
        y = 620
        for flag in scan.get("flags", [])[:10]:
            label = flag.get("label", "Signal")
            advice = flag.get("advice", "")
            page.append(_text(page, 42, y, f"• {label}", 9, TEXT, "F2"))
            y -= 14
            for line in _wrap(advice, 86):
                page.append(_text(page, 56, y, line, 8, MUTED))
                y -= 12
            y -= 5
            if y < 75:
                pages.append(page)
                page = []
                _build_page(page, len(pages) + 1, 0, generated, mode, language)
                y = 680
        pages.append(page)

    # Rebuild page headers/footers now that the final page count is known.
    final_pages = []
    for page_commands in pages:
        final = []
        _build_page(final, len(final_pages) + 1, len(pages), generated, mode, language)
        final.extend(page_commands)
        final_pages.append(final)

    return _make_pdf(final_pages)


def _make_pdf(pages):
    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")

    objects = []

    # Object 1: catalog, object 2: page tree.
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"")  # Filled after page count is known.

    page_start = 3
    content_start = page_start + len(pages)
    font_regular = content_start + len(pages)
    font_bold = font_regular + 1

    objects[1] = (
        f"<< /Type /Pages /Kids [{' '.join(f'{page_start + i} 0 R' for i in range(len(pages)))}] "
        f"/Count {len(pages)} >>"
    ).encode()

    streams = []
    for commands in pages:
        stream = "\n".join(commands).encode("latin-1", "replace")
        streams.append(
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
            + stream
            + b"\nendstream"
        )

    for i in range(len(pages)):
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
            f"/Resources << /Font << /F1 {font_regular} 0 R /F2 {font_bold} 0 R >> >> "
            f"/Contents {content_start + i} 0 R >>"
        .encode()
        )

    objects.extend(streams)
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(pdf.getvalue()))
        pdf.write(f"{number} 0 obj\n".encode())
        pdf.write(obj)
        pdf.write(b"\nendobj\n")

    xref_start = len(pdf.getvalue())
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode())

    pdf.write(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_start}\n%%EOF".encode()
    )
    return pdf.getvalue()
