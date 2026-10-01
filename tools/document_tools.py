from __future__ import annotations

import re
from pathlib import Path
from typing import Union


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}


def validate_upload(
    path: Union[str, Path],
    max_mb: int = 10,
) -> str:
    """
    Validate an uploaded file and return a safe filename.

    The function accepts either:
        - a filesystem path
        - a filename

    It validates the extension and file size when the
    supplied path exists.
    """

    p = Path(path)

    suffix = p.suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {suffix or 'unknown'}"
        )

    # Only check physical file size if the file actually exists.
    # This makes the function safe for Streamlit UploadedFile names.
    if p.exists() and p.is_file():
        max_bytes = max_mb * 1024 * 1024

        if p.stat().st_size > max_bytes:
            raise ValueError(
                f"File exceeds the {max_mb} MB limit."
            )

    safe_name = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        p.name,
    ).strip("._")

    if not safe_name:
        raise ValueError(
            "Invalid filename."
        )

    return safe_name
