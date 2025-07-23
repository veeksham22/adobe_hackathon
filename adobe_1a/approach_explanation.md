# Approach Explanation: Adobe 1A PDF Outline Extractor

## Overview
The goal of this solution is to extract a structured outline from PDF documents, identifying section headings and their hierarchy. This is particularly challenging due to the diversity of PDF layouts, inconsistent use of fonts, and the presence of decorative or non-informative elements. Our approach leverages text properties such as font size, boldness, and spatial layout to robustly identify headings and build a meaningful outline.

## Methodology

### 1. Text Extraction
We use the PyMuPDF (fitz) library to parse PDF files and extract text content along with detailed metadata for each text span, including font size, font flags (for bold/italic), and position. This allows us to analyze not just the text, but also its visual presentation on the page.

### 2. Font Size Analysis
A key insight is that headings are usually presented in larger font sizes compared to body text. We scan all text spans in the document to build a frequency map of font sizes. The largest font size is typically assigned as the document title, followed by the next largest sizes for H1, H2, and H3 headings. This dynamic mapping adapts to the specific font usage of each document.

### 3. Heading Detection Logic
- **Title Extraction:** The largest font size on the first page is used to extract the document title.
- **Headings:** For each page, we analyze each line of text. A line is considered a heading if:
  - It is in a heading-level font size (H1, H2, H3), and is either bold or the first line in its block.
  - It is the first line of the page (even if not large or bold), as these often represent section starts.
  - It is immediately followed by an empty line, which often visually separates headings from content.
  - The line must contain at least one alphanumeric character to avoid picking up decorative elements.

### 4. Handling PDF Quirks
PDFs often contain decorative lines, bullet points, or other non-informative elements. We filter out lines that are only symbols or whitespace. The logic is robust to multi-column layouts and ignores non-text blocks.

### 5. Output Structure
The extracted outline is saved as a JSON file, listing the document title and an array of headings, each with its level, text, and page number. This structured output can be used for navigation, summarization, or further downstream processing.

## Design Choices
- **Heuristic-based:** The approach is fully heuristic and does not require training data, making it robust and generalizable.
- **No External Dependencies:** Only PyMuPDF and standard Python libraries are used, ensuring easy deployment.
- **Dockerized:** The solution is containerized for reproducibility and ease of use.

## Conclusion
This methodology balances accuracy and robustness, handling a wide variety of PDF layouts and styles. It is designed to be easily extensible for more complex document analysis tasks. 