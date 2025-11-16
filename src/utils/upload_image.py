import os
import sys
import requests
import argparse
import base64
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urljoin

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.utils.image_processor import resize_image_if_needed

def image_path_to_base64_uri(path: Path) -> str | None:
    """Converts a local image file path to a Base64 Data URI."""
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type or not mime_type.startswith('image'):
        print(f"Skipping non-image file: {path}")
        return None
    try:
        with open(path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        print(f"Error encoding image {path}: {e}")
        return None

def upload_image_from_base64(base64_string: str, filename: str) -> str | None:
    """
    Uploads an image using a base64 string and returns the full URL.
    """
    load_dotenv()
    api_url = os.getenv("XHS_API_URL")
    api_key = os.getenv("XHS_API_KEY")

    if not api_url or not api_key:
        raise ValueError("XHS_API_URL and XHS_API_KEY must be set in the .env file")

    endpoint = urljoin(api_url, "api/images/upload-base64")
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    data = {"image": base64_string, "filename": filename}

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        relative_url = response_data.get("url")

        if relative_url:
            full_url = urljoin(api_url, relative_url)
            print(f"Successfully uploaded {filename}. URL: {full_url}")
            return full_url
        else:
            print(f"Upload of {filename} succeeded but no URL was returned.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while uploading {filename}: {e}")
        return None

def main():
    """
    Main function to run the image uploader as a script.
    """
    parser = argparse.ArgumentParser(description="Uploads all images from a directory and saves their URLs to a file.")
    parser.add_argument("--image-dir", type=str, required=True, help="Directory to scan for image files.")
    parser.add_argument("--output-file", type=str, required=True, help="File to save the uploaded image URLs.")
    args = parser.parse_args()

    image_dir_path = Path(args.image_dir)
    output_file_path = Path(args.output_file)

    if not image_dir_path.is_dir():
        print(f"Error: --image-dir '{args.image_dir}' is not a valid directory.")
        sys.exit(1)

    supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    uploaded_urls = []

    print(f"Scanning directory for images: {args.image_dir}")
    for item in sorted(image_dir_path.iterdir()):
        if item.is_file() and item.suffix.lower() in supported_extensions:
            print(f"\nProcessing {item.name}...")
            
            # 1. Resize image if needed
            processed_image_path = resize_image_if_needed(item)
            
            # 2. Convert to Base64
            base64_uri = image_path_to_base64_uri(processed_image_path)
            if not base64_uri:
                continue
                
            # 3. Upload image
            image_url = upload_image_from_base64(base64_uri, item.name)
            if image_url:
                uploaded_urls.append(image_url)

    if uploaded_urls:
        print(f"\nSuccessfully uploaded {len(uploaded_urls)} images.")
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for url in uploaded_urls:
                    f.write(url + '\n')
            print(f"Image URLs saved to: {output_file_path}")
        except IOError as e:
            print(f"Error writing to output file {output_file_path}: {e}")
            sys.exit(1)
    else:
        print("No images were uploaded.")
        # Create an empty file to indicate no images
        output_file_path.touch()

if __name__ == '__main__':
    main()
