import fitz  # PyMuPDF
import os
import json
import unicodedata

def is_visible_text(text):
    # Removes control characters
    return bool(text.strip()) and not all(unicodedata.category(c)[0] == 'C' for c in text)

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    outline = []
    font_size_map = {}

    # Step 1: Collect font sizes
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if not is_visible_text(text):
                        continue
                    size = round(span["size"], 1)
                    font_size_map[size] = font_size_map.get(size, 0) + 1

    # Step 2: Determine heading levels
    ranked_sizes = sorted(font_size_map.items(), key=lambda x: -x[0])
    size_to_level = {}
    for i, (size, _) in enumerate(ranked_sizes[:4]):
        level = ["Title", "H1", "H2", "H3"][i] if i < 4 else None
        size_to_level[size] = level

    # Step 3: Extract outline with page numbers
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    size = round(span["size"], 1)
                    level = size_to_level.get(size)

                    if not level or not is_visible_text(text):
                        continue

                    clean_text = text.rstrip()  # remove only trailing spaces

                    if level == "Title" and not title:
                        title = clean_text
                    elif level in ["H1", "H2", "H3"]:
                        outline.append({
                            "level": level,
                            "text": clean_text,
                            "page": page_num
                        })

    return {
        "title": title,
        "outline": outline
    }

def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            result = extract_outline_from_pdf(os.path.join(input_dir, file))
            out_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
