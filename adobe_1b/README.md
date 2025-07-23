# Adobe Challenge 1B – Relevant PDF Section Selector

This project solves Adobe Hackathon Challenge 1B by selecting and ranking the most relevant sections from a set of PDFs based on a given persona and job-to-be-done.

## Objective

Given:
- A directory of PDFs
- A `challenge1b_input.json` file with:
  - A persona (e.g., Travel Planner)
  - A task (e.g., Plan a trip of 4 days for 10 college friends)

The system returns:
- Top 5 relevant sections
- Full text of each matched section

## How It Works

1. Extracts structured headings from PDFs using font-size-based logic.
2. For each heading, collects corresponding page text.
3. Converts all section texts and the input query into TF-IDF vectors.
4. Computes cosine similarity between the query and each section.
5. Ranks and returns the top 5 sections.

## Input Format

Place in `/input`:
- PDFs
- `challenge1b_input.json`:
```json
{
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": { "task": "Plan a trip of 4 days for a group of 10 college friends." },
  "documents": [
    { "filename": "South of France - Cities.pdf" },
    ...
  ]
}
```
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
### Dependencies
```text
pymupdf
scikit-learn
numpy
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
