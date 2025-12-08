import fitz  # PyMuPDF
import os
import sys

def extract_images_from_pdf(pdf_path, output_dir):
    """
    Extracts all images from a PDF file and saves them to a specified directory.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where extracted images will be saved.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    doc = fitz.open(pdf_path)
    image_count = 0

    print(f"Extracting images from '{os.path.basename(pdf_path)}'...")

    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        image_list = page.get_images(full=True)

        if image_list:
            for image_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"image-p{page_index + 1}-{image_index + 1}.{image_ext}"
                image_path = os.path.join(output_dir, image_filename)
                
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)
                
                image_count += 1

    print(f"Successfully extracted {image_count} images to '{output_dir}'.")
    doc.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_images.py <path_to_pdf> <output_directory>")
        sys.exit(1)
    
    pdf_file_path = sys.argv[1]
    output_directory = sys.argv[2]
    
    extract_images_from_pdf(pdf_file_path, output_directory)