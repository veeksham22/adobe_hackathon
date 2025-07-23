import fitz  # PyMuPDF
import os
import json
import unicodedata
import re

def is_visible_text(text):
    # Removes control characters
    return bool(text.strip()) and not all(unicodedata.category(c)[0] == 'C' for c in text)

def is_meaningful_heading(text):
    # Accept if contains at least one alphanumeric character
    return any(c.isalnum() for c in text)

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    outline = []
    font_size_map = {}

    # Step 1: Collect font sizes from all pages
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

    # Step 2: Map sizes to heading levels (largest = Title, then H1, H2, H3)
    ranked_sizes = sorted(font_size_map.items(), key=lambda x: -x[0])
    size_to_level = {}
    for i, (size, _) in enumerate(ranked_sizes[:4]):
        level = ["Title", "H1", "H2", "H3"][i] if i < 4 else None
        size_to_level[size] = level

    # Step 3: Extract Title from first page only
    page1 = doc[0]
    blocks = page1.get_text("dict")["blocks"]
    
    # Collect all title-level text from first page
    title_elements = []
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            has_title_font = False
            for span in line["spans"]:
                size = round(span["size"], 1)
                level = size_to_level.get(size)
                if level == "Title":
                    line_text += span["text"]
                    has_title_font = True
            
            if has_title_font and line_text.strip():
                title_elements.append(line_text.strip())
    
    # Join title elements with spaces
    title = " ".join(title_elements).strip()

    # Step 4: Extract headings by processing text blocks spatially
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        first_line_found = False
        for block in blocks:
            if "lines" not in block:
                continue
            for line_idx, line in enumerate(block["lines"]):
                line_heading_level = None
                line_text = ""
                is_bold = False
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not is_visible_text(text):
                        continue
                    size = round(span["size"], 1)
                    level = size_to_level.get(size)
                    if level in ["H1", "H2", "H3"]:
                        if line_heading_level is None:
                            line_heading_level = level
                        if level == line_heading_level:
                            line_text += text + " "
                        if span.get("flags", 0) & 2 != 0:
                            is_bold = True
                    else:
                        line_text += text + " "
                line_text = line_text.strip()
                # Check if this is the first line of the page
                is_first_line_of_page = not first_line_found and is_meaningful_heading(line_text)
                if is_first_line_of_page:
                    outline.append({
                        "level": "H1",  # or a custom level like "PageFirstLine"
                        "text": re.sub(r'\s+', ' ', line_text).strip(),
                        "page": page_num
                    })
                    first_line_found = True
                    continue
                # Check if this line is immediately followed by an empty line
                next_line_empty = False
                if line_idx + 1 < len(block["lines"]):
                    next_line = block["lines"][line_idx + 1]
                    next_line_text = " ".join(span["text"].strip() for span in next_line["spans"] if is_visible_text(span["text"]))
                    if not next_line_text:
                        next_line_empty = True
                # Only consider as heading if:
                # - It is heading-level font size and (is bold or is first line in block)
                # - Or it is followed by an empty line
                # - And contains at least one alphanumeric character
                if (
                    (line_heading_level and line_text and is_meaningful_heading(line_text) and (is_bold or line_idx == 0))
                    or (next_line_empty and is_meaningful_heading(line_text))
                ):
                    outline.append({
                        "level": line_heading_level if line_heading_level else "H1",
                        "text": re.sub(r'\s+', ' ', line_text).strip(),
                        "page": page_num
                    })

    # Step 5: Post-process to merge split headings that are on the same page and level
    merged_outline = []
    i = 0
    
    while i < len(outline):
        current = outline[i]
        
        # Look for potential merges
        merged_text = current["text"]
        j = i + 1
        
        # Check if next items should be merged
        while (j < len(outline) and 
               outline[j]["level"] == current["level"] and 
               outline[j]["page"] == current["page"]):
            
            next_item = outline[j]
            
            # Merge conditions:
            # 1. Current text is just a number (like "1.")
            # 2. Or current text doesn't end with proper punctuation and next doesn't start with number
            should_merge = (
                re.match(r'^\d+\.$', merged_text.strip()) or  # Current is just "1."
                (not merged_text.endswith('.') and 
                 not merged_text.endswith(':') and
                 not merged_text.endswith('?') and
                 not merged_text.endswith('!') and
                 not re.match(r'^\d+\.', next_item["text"]))  # Next doesn't start with "2."
            )
            
            if should_merge:
                merged_text += " " + next_item["text"]
                j += 1
            else:
                break
        
        merged_outline.append({
            "level": current["level"],
            "text": re.sub(r'\s+', ' ', merged_text).strip(),
            "page": current["page"]
        })
        
        i = j

    return {
        "title": title,
        "outline": merged_outline
    }


def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            result = extract_outline_from_pdf(os.path.join(input_dir, file))
            out_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)