# Approach Explanation: Adobe 1B PDF Selector & Extractor

## Overview
The objective of this solution is to process a set of PDF documents and a challenge input JSON, selecting and extracting relevant information as required by the task. The challenge involves not just extracting text, but also matching and structuring content according to specific criteria, which may include persona-driven or task-driven requirements.

## Methodology

### 1. Input Handling
The solution expects a directory of PDF files and a JSON input file specifying the selection or extraction criteria. All files are loaded and preprocessed using PyMuPDF, which provides access to both the text and its layout metadata.

### 2. Outline Extraction and Chunking
We leverage the outline extraction logic from the 1A solution to break each PDF into logical sections based on headings. Each section is tagged with its document, section title, and page number. This chunking enables fine-grained selection and relevance ranking.

### 3. Matching and Selection Logic
- **Heuristic Matching:** For each task or persona in the input JSON, we use keyword and semantic matching to identify the most relevant sections of each document. This may involve simple string matching, TF-IDF vector search, or other lightweight semantic similarity measures.
- **Ranking:** All candidate sections are ranked according to their relevance to the input criteria. The top-ranked sections are selected for extraction.
- **Sub-section Extraction:** Within each selected section, the most relevant paragraph or content block is further identified, providing a refined and focused output.

### 4. Output Generation
The selected and extracted content is structured as JSON, listing the source file, section, and extracted content. This format is suitable for downstream consumption or further analysis.

## Design Choices
- **Modular:** The solution separates outline extraction, section chunking, and relevance ranking, making it easy to adapt or extend.
- **Heuristic and Lightweight:** By relying on heuristics and lightweight semantic search, the solution is fast, reproducible, and does not require large models or internet access.
- **Reproducible:** The entire pipeline is containerized with Docker for consistent execution across environments.

## Conclusion
This approach provides a robust and efficient way to select and extract relevant content from a diverse set of PDFs, guided by flexible input criteria. It is designed for extensibility and can be adapted to more complex document intelligence tasks as needed. 