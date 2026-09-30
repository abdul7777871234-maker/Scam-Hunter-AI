from pathlib import Path
import re

ALLOWED = {".pdf", ".docx", ".txt", ".md", ".png", ".jpg", ".jpeg", ".webp"}

def validate_upload(path: str | Path, max_mb: int = 10):
    p = Path(path)
    if p.suffix.lower() not in ALLOWED:
        raise ValueError("Unsupported file type.")
    if p.stat().st_size > max_mb * 1024 * 1024:
        raise ValueError(f"File exceeds the {max_mb} MB limit.")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", p.name)
    return safe
