# Persona-Driven Document Intelligence (Adobe Hack 1b)

## How it works
- Uses your 1a extractor (PyMuPDF, font-size/outline based)
- Chunks text by heading, tags with document, section, and page
- Uses TF-IDF vector search (no network, fast, reproducible)
- Ranks all sections using semantic search w.r.t persona/task string
- For each top section, finds the most relevant paragraph as a refined sub-section

## How to run

```
docker build --platform linux/amd64 -t adobe-1b .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1b

- Input: All challenge PDFs + challenge1b_input.json in `input/`
- Output: challenge1b_output.json in `output/`

## Approach
Modular: Separates outline extraction and section relevance ranking

Generalized: No hardcoding of keywords. Persona/task to section matching uses semantic similarity

Offline and Efficient: TF-IDF model, no internet calls, instant scoring. Embedding model (<1GB) can be swapped in.

Output: See the provided sample format. Each "extracted section" includes document, title, rank, page; sub-section analysis finds the best granular paragraph per section.
