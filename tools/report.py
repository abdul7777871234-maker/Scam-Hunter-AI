from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def _paragraph(text, style):
    return Paragraph(escape(str(text or "")).replace("\n", "<br/>"), style)


def build_report(
    question,
    answer,
    verdict=None,
    scan=None,
    sources=None,
    mode="Quick Check",
    language="English",
):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="ScamHunter AI Investigation Report",
        author="ScamHunter AI",
    )

    styles = getSampleStyleSheet()
    title = styles["Title"]
    heading = styles["Heading2"]
    body = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        leading=14,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "ReportSmall",
        parent=body,
        fontSize=8.5,
        leading=11,
    )

    story = [
        _paragraph("ScamHunter AI Investigation Report", title),
        Spacer(1, 6),
        _paragraph(
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            small,
        ),
        _paragraph(f"Mode: {mode}", small),
        _paragraph(f"Response language: {language}", small),
        Spacer(1, 12),
        _paragraph("User Content", heading),
        _paragraph(question or "(No text provided.)", body),
        _paragraph("Instant Scan", heading),
    ]

    if scan:
        story.extend(
            [
                _paragraph(f"Level: {scan.get('level', 'none')}", body),
                _paragraph(
                    f"Signal score: {scan.get('score', 0)}/100",
                    body,
                ),
                _paragraph(f"Summary: {scan.get('headline', '')}", body),
            ]
        )
        for flag in scan.get("flags", []):
            story.append(
                _paragraph(
                    f"{flag.get('label', 'Signal')}: {flag.get('advice', '')}",
                    body,
                )
            )
    else:
        story.append(_paragraph("No instant scan data was available.", body))

    story.extend(
        [
            _paragraph("AI Investigation", heading),
            _paragraph(answer or "(No answer generated.)", body),
            _paragraph("Evidence Note", heading),
            _paragraph(
                "The Instant Scan score is heuristic and should be treated as a warning signal, not proof of fraud.",
                body,
            ),
        ]
    )

    if verdict:
        story.extend(
            [
                _paragraph("Verdict", heading),
                _paragraph(f"Level: {verdict.get('level', '')}", body),
                _paragraph(
                    f"Category: {verdict.get('category', '') or 'Not specified'}",
                    body,
                ),
                _paragraph(f"Source: {verdict.get('source', '')}", body),
            ]
        )

    if sources:
        story.append(_paragraph("Sources", heading))
        for i, source in enumerate(sources, 1):
            if not isinstance(source, dict):
                story.append(_paragraph(f"{i}. {source}", body))
                continue

            source_type = source.get("source_type", "unknown")
            if source_type == "knowledge_base":
                text = (
                    f"{i}. Knowledge Base: {source.get('filename') or 'Document'}"
                    f" — Page {source.get('page') or 'not specified'}"
                )
            elif source_type == "web":
                text = f"{i}. Web: {source.get('title') or 'Source'}"
                if source.get("url"):
                    text += f" — {source['url']}"
            else:
                text = (
                    f"{i}. "
                    f"{source.get('title') or source.get('filename') or source_type}"
                )
            story.append(_paragraph(text, small))

    story.extend(
        [
            Spacer(1, 10),
            _paragraph(
                "ScamHunter AI provides investigation support. Heuristic signals and AI analysis do not independently establish that a person, organization, website, or message is fraudulent.",
                small,
            ),
        ]
    )

    doc.build(story)
    return buffer.getvalue()
