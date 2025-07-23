import os
import json
from extractor import process_folder
from utils import chunk_pdf_texts
from selector import rank_sections  # renamed from 1b_selector to selector.py for valid import
from datetime import datetime

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"

    # Step 1: Process PDFs to generate JSON outlines (1A)
    process_folder(input_dir, output_dir)

    # Step 2: Check for presence of challenge1b_input.json (1B requirement)
    persona_file = os.path.join(input_dir, "challenge1b_input.json")
    if os.path.exists(persona_file):
        with open(persona_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        # Step 3: Load extracted headings and full text
        pdf_chunks = chunk_pdf_texts(input_dir)

        # Step 4: Rank sections based on persona + task
        extracted, refined = rank_sections(config["persona"], config["job_to_be_done"], pdf_chunks)

        # Step 5: Prepare output JSON
        final_output = {
            "metadata": {
                "input_documents": [doc["filename"] for doc in config["documents"]],
                "persona": config["persona"]["role"],
                "job_to_be_done": config["job_to_be_done"]["task"],
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": extracted,
            "subsection_analysis": refined
        }

        # Step 6: Save 1B output
        with open(os.path.join(output_dir, "challenge1b_output.json"), "w", encoding="utf-8") as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)
    else:
        print("1B skipped: No challenge1b_input.json found in input folder.")
