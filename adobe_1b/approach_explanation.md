# Approach Explanation: Round 1B: Persona-Driven Document Intelligence
## Overview

The objective of this solution is to address Adobe Hackathon Challenge 1B by selecting and extracting the most relevant sections from a collection of PDF documents, guided by a given persona and job-to-be-done. The goal is not only to parse and structure document content but also to evaluate which sections are contextually important to the provided criteria and rank them accordingly.

This solution builds upon the heading-level extraction logic from Challenge 1A and extends it with a semantic scoring and ranking mechanism that supports relevance-based document exploration.

## Methodology

### 1. Input Handling

The system is designed to process:
- A directory of PDF documents
- A `challenge1b_input.json` file which includes:
  - A persona with a specified role
  - A task that the persona wants to accomplish
  - A list of target documents by filename

These files are placed inside an `input/` folder. The system reads and processes all specified PDFs using the PyMuPDF (`fitz`) library to access both layout information and full page text content.

### 2. Outline Extraction and Chunking

This phase leverages the existing heading-based outline extraction logic from Challenge 1A:
- Font sizes are analyzed across each PDF to infer heading levels such as Title, H1, H2, and H3.
- Each heading is associated with a page number and its corresponding raw page text.
- The extracted headings and pages are chunked into discrete sections, each representing a potential content block for relevance evaluation.

To ensure clean data, the following filters are applied:
- Only headings with alphanumeric content and a minimum length threshold are included.
- Decorative headings consisting of symbols (e.g., bullets, asterisks) are discarded.

Each chunk is represented as a dictionary containing:
- Document name
- Heading text (section title)
- Full text of the page
- Page number

This prepares the content for downstream scoring.

### 3. Relevance Scoring and Section Ranking

This is the core component of the 1B solution.

#### a. Query Construction

A natural language query is synthesized from the persona and task fields in the input JSON. For example:

#### b. Vectorization with TF-IDF

To maintain a fast and lightweight implementation suitable for Docker-based environments, the system uses a TF-IDF (Term Frequency-Inverse Document Frequency) vectorizer:

- The synthesized query and all extracted section texts are vectorized.
- Cosine similarity is computed between the query vector and each section vector.
- This allows the system to estimate the textual relevance of each chunk to the query without relying on large pretrained language models or internet connectivity.

#### c. Similarity-Based Ranking

- Each section is assigned a similarity score relative to the query.
- All chunks are then ranked in descending order of their scores.
- The top 5 sections are selected for final extraction.

This scoring method favors sections with vocabulary overlap and thematic similarity, making it well-suited for structured travel documents and guides.

---

## 4. Output Generation

The final output is written to `/output/challenge1b_output.json` in the following structure:

- `metadata`: Contains the list of input documents, persona role, task, and processing timestamp.
- `extracted_sections`: Lists the top 5 matched sections with:
  - Document name
  - Section title
  - Page number
  - Rank
- `subsection_analysis`: Provides the full raw text of each selected section for detailed inspection.

This structured output ensures downstream compatibility for either human evaluation or integration into other systems.

---

## Design Choices

### Modular Architecture

The system is organized into distinct functional modules:

- `extractor.py` handles outline and heading extraction
- `utils.py` performs page chunking and validation
- `selector.py` executes the core ranking logic
- `main.py` orchestrates the full workflow

This modularity improves code readability, testing, and potential extension to other document types or scoring algorithms.

### Lightweight Semantic Scoring

The choice of TF-IDF over heavier semantic models was driven by the following considerations:

- Faster build and runtime performance, especially in Docker environments
- No internet or GPU dependency
- Deterministic and explainable scoring
- Ease of integration and debugging

For the scope of this challenge, TF-IDF provides sufficiently accurate relevance ranking.

### Robustness and Safety

The system includes safeguards against:

- PDFs with no headings
- Sections with invalid or unreadable content
- Missing or malformed input JSON
- Sections with no meaningful text content

All such edge cases are logged and handled gracefully to ensure the system completes execution without crashing.

---

## Future Extensions

While the current implementation meets the challenge requirements efficiently, several improvements are possible:

- Replace TF-IDF with contextual embeddings (e.g., Sentence Transformers or OpenAI Embeddings) for deeper semantic understanding.
- Add multilingual support by detecting and translating non-English PDFs.
- Use named entity recognition (NER) to extract destinations, activities, or people from each section.
- Implement a user interface to interactively explore ranked sections.
- Integrate itinerary generation or interactive document summarization.

---

## Conclusion

This solution demonstrates a clean, fast, and extensible pipeline to rank and extract meaningful sections from a collection of PDFs based on persona-specific goals. It combines traditional text extraction and information retrieval techniques to deliver structured insights without requiring cloud APIs or large-scale models. Its lightweight architecture and Docker-based reproducibility make it suitable for real-world deployment in constrained environments.


