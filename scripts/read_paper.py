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

if __name__ == "__main__":
    # Assuming the script is in the 'scripts' directory and the PDF is in the root
    pdf_file_path = os.path.join(os.path.dirname(__file__), '..', 'context2.0.pdf')
    
    extracted_text = read_pdf_text(pdf_file_path)
    
    # Print the full extracted text
    print(extracted_text)
