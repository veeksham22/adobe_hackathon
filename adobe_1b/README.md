# Adobe 1B PDF Selector & Extractor

## Approach
This solution processes a set of PDFs and a JSON input to select and extract relevant information based on the challenge requirements. It uses heuristics and text analysis to match and extract the required content, outputting structured JSON files for downstream use.

## Models and Libraries Used
- **PyMuPDF (fitz):** For PDF parsing and text extraction.
- **Python Standard Library:** For file operations, JSON handling, and regular expressions.

## How to Build and Run

### Prerequisites
- Docker (recommended)
- Or: Python 3.8+ and pip (if running locally)

### Using Docker (Recommended)
1. Build the Docker image:
   ```sh
   docker build -t adobe-1b .
   ```
2. Run the container:
   ```sh
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-1b
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
- Place your PDF files and the challenge input JSON in the `input/` directory.
- Example: `input/challenge1b_input.json`, `input/South of France - Cuisine.pdf`

### Output
- The extracted/selected data will be saved as JSON files in the `output/` directory, e.g.:
  - `output/challenge1b_output.json`
  - `output/South of France - Cuisine.json`

#### Example Output (snippet)
```json
{
    "selected": [
        {"file": "South of France - Cuisine.pdf", "content": "..."}
    ]
}
```

## More Details
See `approach_explanation.md` for a detailed explanation of the methodology.
