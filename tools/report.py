from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO


def _esc(text):
    return str(text or "").replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_report(question, answer, verdict=None, scan=None, sources=None, mode="Quick Check", language="English"):
    lines = [
        "ScamHunter AI Investigation Report",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Mode: {mode}",
        f"Language: {language}",
        "",
        "USER CONTENT",
        str(question or "(No text provided.)"),
        "",
        "AI INVESTIGATION",
        str(answer or "(No answer generated.)"),
        "",
        "INSTANT SCAN",
    ]
    if scan:
        lines += [
            f"Level: {scan.get('level', 'none')}",
            f"Signal score: {scan.get('score', 0)}/100",
            f"Summary: {scan.get('headline', '')}",
        ]
    if verdict:
        lines += [
            "",
            "VERDICT",
            f"Level: {verdict.get('level', '')}",
            f"Category: {verdict.get('category', '') or 'Not specified'}",
        ]
    if sources:
        lines += ["", "SOURCES"]
        for i, source in enumerate(sources, 1):
            if isinstance(source, dict):
                lines.append(f"{i}. {source.get('title') or source.get('filename') or 'Source'}")
                if source.get("url"):
                    lines.append(f"   {source['url']}")
            else:
                lines.append(f"{i}. {source}")
    lines += [
        "",
        "ScamHunter AI provides investigation support. AI analysis and heuristic signals do not independently establish fraud.",
    ]

    wrapped = []
    for raw in lines:
        text = raw.replace("\r", "").replace("\t", "    ")
        if not text:
            wrapped.append("")
            continue
        while len(text) > 90:
            wrapped.append(text[:90])
            text = text[90:]
        wrapped.append(text)

    pages = [wrapped[i:i + 48] for i in range(0, len(wrapped), 48)] or [["ScamHunter AI Investigation Report"]]
    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    objects = []
    for page in pages:
        content = ["BT", "/F1 10 Tf", "42 750 Td"]
        for index, line in enumerate(page):
            if index:
                content.append("0 -14 Td")
            content.append(f"({_esc(line)}) Tj")
        content.append("ET")
        stream = "\n".join(content).encode("latin-1", "replace")
        objects.append(
            b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" +
            stream + b"\nendstream"
        )

    offsets = [0]
    for obj in objects:
        offsets.append(pdf.tell())
        pdf.write(str(len(offsets)).encode() + b" 0 obj\n")
        pdf.write(obj)
        pdf.write(b"\nendobj\n")

    # Minimal single-font PDF objects.
    font_id = len(objects) + 1
    pdf.write(f"{font_id} 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n".encode())
    pages_id = font_id + 1
    page_ids = []
    for i, _ in enumerate(objects, 1):
        page_ids.append(i)
    pdf.seek(0)
    # Rebuild with correct object graph.
    out = bytearray(b"%PDF-1.4\n")
    all_objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"",
    ]
    page_start = 3
    content_start = page_start + len(pages)
    all_objects[1] = f"<< /Type /Pages /Kids [{' '.join(f'{page_start + i} 0 R' for i in range(len(pages)))}] /Count {len(pages)} >>".encode()
    for i in range(len(pages)):
        all_objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 {content_start + len(pages)} 0 R >> >> /Contents {3 + len(pages) + i} 0 R >>".encode())
    for obj in objects:
        all_objects.append(obj)
    all_objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    xref = [0]
    for n, obj in enumerate(all_objects, 1):
        xref.append(len(out))
        out.extend(f"{n} 0 obj\n".encode())
        out.extend(obj)
        out.extend(b"\nendobj\n")
    start = len(out)
    out.extend(f"xref\n0 {len(all_objects)+1}\n0000000000 65535 f \n".encode())
    for off in xref[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(f"trailer\n<< /Size {len(all_objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF".encode())
    return bytes(out)
