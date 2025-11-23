import argparse
from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_dir, format='png'):
    """
    Converts each page of a PDF file to an image.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory to save the output images.
        format (str): The image format (e.g., 'png', 'jpeg').
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        images = convert_from_path(pdf_path, fmt=format)
        for i, image in enumerate(images):
            image_name = f"page_{i + 1}.{format}"
            image_path = os.path.join(output_dir, image_name)
            image.save(image_path, format.upper())
            print(f"Saved: {image_path}")
        print("Conversion complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nPlease ensure you have 'poppler' installed on your system.")
        print("On macOS, you can install it with Homebrew: 'brew install poppler'")
        print("On Debian/Ubuntu, use: 'sudo apt-get install poppler-utils'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to a series of images.")
    parser.add_argument("pdf_path", help="The path to the PDF file.")
    parser.add_argument("output_dir", help="The directory to save the output images.")
    parser.add_argument("--format", default="png", help="The output image format (e.g., png, jpeg).")

    args = parser.parse_args()

    convert_pdf_to_images(args.pdf_path, args.output_dir, args.format)
