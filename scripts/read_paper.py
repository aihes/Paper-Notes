import fitz  # PyMuPDF
import os

def read_pdf_text(pdf_path):
    """
    Reads and extracts text from a PDF file.
    """
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"

    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"An error occurred: {e}"

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", help="The path to the PDF file to read.")
    parser.add_argument("--output_path", help="Optional. The path to save the extracted text file.", default=None)

    args = parser.parse_args()

    extracted_text = read_pdf_text(args.pdf_path)

    if args.output_path:
        try:
            with open(args.output_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            print(f"Successfully extracted text to {args.output_path}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        # Print the full extracted text to standard output
        print(extracted_text)
