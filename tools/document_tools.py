from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Union


# -------------------------------------------------------------
# FILE TYPES
# -------------------------------------------------------------

TEXT_TYPES = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
}

IMAGE_TYPES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

ALLOWED_EXTENSIONS = (
    TEXT_TYPES
    | IMAGE_TYPES
)

IMAGE_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


# -------------------------------------------------------------
# UPLOAD VALIDATION
# -------------------------------------------------------------

def validate_upload(
    path: Union[str, Path],
    max_mb: int = 10,
    size_bytes: int | None = None,
) -> str:
    """
    Validate an uploaded file and return a safe filename.

    Supports both:
        validate_upload("file.pdf")
        validate_upload("file.pdf", size_bytes=12345)

    The explicit size_bytes argument is important for Streamlit's
    UploadedFile objects because their temporary filesystem path
    may not exist.
    """

    p = Path(path)

    suffix = p.suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type: "
            f"{suffix or 'unknown'}"
        )

    # ---------------------------------------------------------
    # Determine file size
    # ---------------------------------------------------------

    actual_size = size_bytes

    if actual_size is None:
        if p.exists() and p.is_file():
            actual_size = p.stat().st_size

    if actual_size is not None:
        max_bytes = (
            max(1, int(max_mb))
            * 1024
            * 1024
        )

        if actual_size > max_bytes:
            raise ValueError(
                f"File exceeds the {max_mb} MB limit."
            )

        if actual_size < 0:
            raise ValueError(
                "Invalid file size."
            )

    # ---------------------------------------------------------
    # Sanitize filename
    # ---------------------------------------------------------

    safe_name = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        p.name,
    )

    safe_name = safe_name.strip(
        "._"
    )

    if not safe_name:
        raise ValueError(
            "Invalid filename."
        )

    # Keep extension after sanitization.
    if "." not in safe_name:
        raise ValueError(
            "Filename must include a supported extension."
        )

    return safe_name


# -------------------------------------------------------------
# TEXT EXTRACTION
# -------------------------------------------------------------

def extract_upload_text(
    filename: Union[str, Path],
    data: bytes,
) -> str:
    """
    Extract text from an uploaded PDF, DOCX, TXT, or Markdown file.

    Returns plain text suitable for adding to the investigation
    prompt.
    """

    if not data:
        return ""

    path = Path(filename)
    suffix = path.suffix.lower()

    if suffix == ".txt" or suffix == ".md":
        return data.decode(
            "utf-8",
            errors="ignore",
        ).strip()

    if suffix == ".pdf":
        return _extract_pdf_bytes(
            data
        ).strip()

    if suffix == ".docx":
        return _extract_docx_bytes(
            data
        ).strip()

    raise ValueError(
        f"Text extraction is not supported "
        f"for {suffix or 'unknown'} files."
    )


# -------------------------------------------------------------
# PDF
# -------------------------------------------------------------

def _extract_pdf_bytes(
    data: bytes,
) -> str:

    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires the 'pypdf' package."
        ) from exc

    try:
        reader = PdfReader(
            io.BytesIO(data)
        )

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = (
                page.extract_text()
                or ""
            ).strip()

            if text:
                pages.append(
                    f"[Page {page_number}]\n{text}"
                )

        return "\n\n".join(
            pages
        )

    except Exception as exc:
        raise ValueError(
            f"Could not read PDF: {exc}"
        ) from exc


# -------------------------------------------------------------
# DOCX
# -------------------------------------------------------------

def _extract_docx_bytes(
    data: bytes,
) -> str:

    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError(
            "DOCX support requires the 'python-docx' package."
        ) from exc

    try:
        document = Document(
            io.BytesIO(data)
        )

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n\n".join(
            paragraphs
        )

    except Exception as exc:
        raise ValueError(
            f"Could not read DOCX: {exc}"
        ) from exc


# -------------------------------------------------------------
# OPTIONAL HELPERS
# -------------------------------------------------------------

def is_supported_file(
    filename: Union[str, Path],
) -> bool:
    return (
        Path(filename)
        .suffix
        .lower()
        in ALLOWED_EXTENSIONS
    )


def is_image_file(
    filename: Union[str, Path],
) -> bool:
    return (
        Path(filename)
        .suffix
        .lower()
        in IMAGE_TYPES
    )


def is_text_file(
    filename: Union[str, Path],
) -> bool:
    return (
        Path(filename)
        .suffix
        .lower()
        in TEXT_TYPES
    )


def get_image_mime(
    filename: Union[str, Path],
) -> str:
    suffix = (
        Path(filename)
        .suffix
        .lower()
    )

    mime = IMAGE_MIME.get(
        suffix
    )

    if not mime:
        raise ValueError(
            f"Unsupported image type: "
            f"{suffix or 'unknown'}"
        )

    return mime
