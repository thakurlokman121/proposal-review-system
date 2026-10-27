from __future__ import annotations

import fitz


def extract_pdf_text(pdf_bytes: bytes) -> str:
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            text = "\n\n".join(page.get_text("text") for page in document)
    except Exception as exc:
        raise ValueError(f"Could not read the uploaded PDF: {exc}") from exc
    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if len(cleaned) < 40:
        raise ValueError("The PDF contains too little extractable text. Use a text-based PDF rather than a scanned image.")
    return cleaned