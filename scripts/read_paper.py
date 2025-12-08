import fitz  # PyMuPDF
import sys
import os

def extract_text_from_pdf(pdf_path, output_path):
    """
    Extracts text from a PDF file and saves it to a markdown file.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
    
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully extracted text from {pdf_path} to {output_path}")
    
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/read_paper.py <path_to_pdf> <output_md_path>", file=sys.stderr)
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)
        
    extract_text_from_pdf(pdf_path, output_path)
