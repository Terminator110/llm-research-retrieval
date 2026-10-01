from pathlib import Path
import json
import re

import requests
import pymupdf

PDF_URLS = [
    "https://arxiv.org/pdf/2512.08592",
]

RAW_DIR = Path("data/raw/")
PROCESSED_DIR = Path("data/processed/")

HEADERS = {
    "User-Agent": "llm-rag-baseline/1.0"
}

# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def download_pdf(url: str, output_path: Path):
    """Download a PDF from a URL."""

    print(f"Downloading: {url}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=60,
    )

    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()

    if "pdf" not in content_type:
        raise ValueError(
            f"Expected PDF but received "
            f"Content-Type: {content_type}"
        )

    output_path.write_bytes(response.content)

    print(f"Saved: {output_path}")

def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and line breaks."""

    # Remove extra whitespace and line breaks.
    clean_text = re.sub(r" {3,}", "  ", text)

    return clean_text



def extract_pdf(pdf_path: Path) -> dict:
    """Extract page-level plain text from a PDF."""

    print(f"Extracting: {pdf_path.name}")

    pages = []

    with pymupdf.open(pdf_path) as document:

        for page_number, page in enumerate(document, start=1):

            clean_flags = pymupdf.TEXTFLAGS_TEXT & ~pymupdf.TEXT_PRESERVE_LIGATURES
            text = page.get_text(
                "text",
                flags=clean_flags,
                sort=True,
            )

            text = normalize_text(text)

            pages.append(
                {
                    "page": page_number,
                    "text": text,
                    "char_count": len(text),
                }
            )

    return {
        "document_id": pdf_path.stem,
        "source_file": pdf_path.name,
        "pages": pages,
    }


def save_extracted_text(
    document: dict,
    output_path: Path,
) -> None:
    """Save extracted document as JSON."""

    output_path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Saved: {output_path}")




def main():

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for i in PDF_URLS:
        url=i
        filename = url.rstrip("/").split("/")[-1]
        if not filename.endswith(".pdf"):
            filename += ".pdf"

        pdf_path = RAW_DIR/filename
                
        json_path = PROCESSED_DIR / f"{pdf_path.stem}.json"
        
        if not pdf_path.exists():
            download_pdf(url, pdf_path)
        else:
            print(f"Already exists: {pdf_path}")

        if json_path.exists():
            print(f"Already processed: {json_path}")
            continue

        doc = extract_pdf(pdf_path)


        save_extracted_text(
            doc,
            json_path,
        )    



if __name__ == "__main__":
    main()