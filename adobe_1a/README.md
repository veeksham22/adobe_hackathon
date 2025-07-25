# Adobe 1A PDF Outline Extractor

## Approach
This solution extracts the outline (headings and structure) from PDF files using font size, boldness, and spatial layout heuristics. It identifies headings by analyzing text properties such as font size, boldness, and their position on the page. The extractor is robust to various PDF layouts and ignores decorative or non-informative elements.The code is language-neutral by default and is likely to work for text-based, Unicode-compliant ```multilingual``` PDFs as well.

## Models and Libraries Used
- **PyMuPDF (fitz):** For PDF parsing and text extraction.
- **Python Standard Library:** For file operations, JSON handling, and regular expressions.
- **unicodedata.category:** For visible character checks, which is robust for multilingual text.


## How to Build and Run

### Prerequisites
- Docker (recommended)
- Or: Python 3.8+ and pip (if running locally)

### Using Docker (Recommended)
1. Build the Docker image:
   ```sh
   docker build -t adobe-1a .
   ```
2. Run the container:
   ```sh
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1a
   ```
   (On Windows PowerShell, use `${PWD}` instead of `$(pwd)`.)

### Running Locally (Without Docker)
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the script:
   ```sh
   python main.py
   ```

## Sample Input/Output

### Input
Place your PDF files in the `input/` directory. For example:
- `input/file01.pdf`
- `input/South of France - Cuisine.pdf`

### Output
The extracted outlines will be saved as JSON files in the `output/` directory, e.g.:
- `output/file01.json`
- `output/South of France - Cuisine.json`

#### Example Output (snippet)
```json
{
    "title": "South of France - Cuisine",
    "outline": [
        {"level": "H1", "text": "Overview of the Region", "page": 1},
        {"level": "H2", "text": "Travel Tips", "page": 2}
    ]
}
```

## More Details
See `approach_explanation.md` for a detailed explanation of the methodology.
