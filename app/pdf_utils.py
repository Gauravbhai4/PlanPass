"""Permit Setu: PDF utilities — text extraction AND vision for Azure OpenAI.

Two capabilities are exposed here:

1. Text extraction (pypdf): cheap, fast, works on PDFs that contain real text
   layers. Useful for typed corrections letters.

2. Vision-mode rendering (PyMuPDF + Pillow): renders each PDF page to JPEG and
   base64-encodes it for Azure OpenAI vision-capable deployments.
"""
from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import List, Union

from pypdf import PdfReader

PathLike = Union[str, Path]


def extract_text_from_pdf(pdf_path: PathLike) -> str:
    """Extract all text from a PDF file using pypdf."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PdfReader(str(pdf_path))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"[Could not extract text from page {i}: {e}]"
        parts.append(f"--- Page {i} ---\n{text.strip()}\n")
    return "\n".join(parts)


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extract text from in-memory PDF bytes."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as e:
            text = f"[Could not extract text from page {i}: {e}]"
        parts.append(f"--- Page {i} ---\n{text.strip()}\n")
    return "\n".join(parts)


def _open_doc(pdf_input: Union[PathLike, bytes]):
    """Open a PyMuPDF document from a path or in-memory bytes."""
    import fitz
    if isinstance(pdf_input, (bytes, bytearray)):
        return fitz.open(stream=bytes(pdf_input), filetype="pdf")
    return fitz.open(str(pdf_input))


def pdf_to_images(
    pdf_input: Union[PathLike, bytes],
    dpi: int = 150,
    max_pages: int = 10,
    max_dimension: int = 2048,
):
    """Render PDF pages to PIL.Image objects."""
    from PIL import Image
    import fitz
    doc = _open_doc(pdf_input)
    try:
        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)
        images = []
        total = min(len(doc), max_pages)
        for page_num in range(total):
            page = doc[page_num]
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            mode = "RGB" if pixmap.alpha == 0 else "RGBA"
            img = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples)
            longest = max(img.size)
            if longest > max_dimension:
                ratio = max_dimension / longest
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            images.append(img)
        return images
    finally:
        doc.close()


def image_to_base64_data_url(img, fmt: str = "JPEG", jpeg_quality: int = 85) -> str:
    """Convert a PIL.Image to a base64 data-URL for the OpenAI vision API."""
    buf = io.BytesIO()
    if fmt.upper() == "JPEG":
        img.convert("RGB").save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
        mime = "image/jpeg"
    else:
        img.save(buf, format="PNG", optimize=True)
        mime = "image/png"
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def pdf_to_base64_images(
    pdf_input: Union[PathLike, bytes],
    dpi: int = 150,
    max_pages: int = 10,
    max_dimension: int = 2048,
    use_jpeg: bool = True,
    jpeg_quality: int = 85,
) -> List[str]:
    """One-shot: PDF -> list of base64 data URLs ready for vision API."""
    images = pdf_to_images(pdf_input, dpi=dpi, max_pages=max_pages, max_dimension=max_dimension)
    fmt = "JPEG" if use_jpeg else "PNG"
    return [image_to_base64_data_url(img, fmt=fmt, jpeg_quality=jpeg_quality) for img in images]


def get_pdf_page_count(pdf_input: Union[PathLike, bytes]) -> int:
    """Return the total page count of a PDF without rendering it."""
    doc = _open_doc(pdf_input)
    try:
        return len(doc)
    finally:
        doc.close()
