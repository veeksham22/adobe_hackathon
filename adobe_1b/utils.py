import os
import fitz
import re
from extractor import extract_outline_from_pdf

def is_valid_heading(text):
    # Allow short but meaningful headings (min 4 chars with at least 1 alphanumeric)
    return bool(re.search(r'[a-zA-Z0-9]', text)) and len(text.strip()) > 3

def chunk_pdf_texts(input_dir):
    result = []

    for file in os.listdir(input_dir):
        if not file.endswith(".pdf"):
            continue

        pdf_path = os.path.join(input_dir, file)
        doc = fitz.open(pdf_path)
        outline = extract_outline_from_pdf(pdf_path)["outline"]

        doc_chunks = []
        for item in outline:
            if not is_valid_heading(item["text"]):
                continue  # Skip meaningless headings

            try:
                page = doc[item["page"] - 1]
                full_text = page.get_text().strip()

                doc_chunks.append({
                    "heading": item["text"],
                    "text": full_text,
                    "page": item["page"]
                })

            except Exception:
                continue

        print(f"[DEBUG] Extracted {len(doc_chunks)} valid chunks from: {file}")

        result.append({
            "filename": file,
            "chunks": doc_chunks
        })

    return result
