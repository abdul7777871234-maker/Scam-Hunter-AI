from __future__ import annotations
from datetime import datetime, timezone

def build_report(question, answer, verdict=None, scan=None, sources=None, mode="Quick Check"):
    lines=["# ScamHunter AI Investigation Report","",f"Generated: {datetime.now(timezone.utc).isoformat()}",f"Mode: {mode}","","## User Content","",question or "(No text provided.)","","## Instant Scan",""]
    if scan:
        lines += [f"- Level: {scan.get('level','none')}",f"- Signal score: {scan.get('score',0)}/100",f"- Summary: {scan.get('headline','')}",""]
        lines += [f"- {f.get('label','Signal')}: {f.get('advice','')}" for f in scan.get("flags",[])]
        lines.append("")
    lines += ["## AI Investigation","",answer or "(No answer generated.)",""]
    if verdict:
        lines += ["## Verdict","",f"- Level: {verdict.get('level','')}",f"- Category: {verdict.get('category','') or 'Not specified'}",f"- Source: {verdict.get('source','')}",""]
    if sources:
        lines += ["## Sources",""]
        for i,s in enumerate(sources,1):
            if not isinstance(s,dict): lines.append(f"{i}. {s}"); continue
            st=s.get("source_type","unknown")
            if st=="knowledge_base": lines.append(f"{i}. Knowledge Base: {s.get('filename') or 'Document'} — Page {s.get('page') or 'not specified'}")
            elif st=="web": lines.append(f"{i}. Web: {s.get('title') or 'Source'}"+(f" — {s.get('url')}" if s.get('url') else ""))
            else: lines.append(f"{i}. {s.get('title') or s.get('filename') or st}")
        lines.append("")
    lines += ["---","", "ScamHunter AI provides investigation support. Heuristic signals and AI analysis do not independently establish that a person, organization, website, or message is fraudulent."]
    return "\n".join(lines)
