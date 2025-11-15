import os
import sys
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import base64
import mimetypes
from urllib.parse import urljoin
import markdown
from bs4 import BeautifulSoup

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.utils.upload_image import upload_image_from_base64
from src.utils.image_processor import resize_image_if_needed


def convert_markdown_to_plain_text(md_text: str) -> str:
    """
    Converts a Markdown string to plain text.
    """
    # Convert Markdown to HTML
    html = markdown.markdown(md_text)
    
    # Parse HTML and extract text
    soup = BeautifulSoup(html, "html.parser")
    plain_text = soup.get_text()
    
    return plain_text

def publish_to_twitter(account: str, text: str, images: list[str]):
    """
    Publishes a tweet with text and optional images via the API.

    Args:
        account (str): The Twitter account identifier.
        text (str): The text content of the tweet.
        images (list[str]): A list of image URLs to attach to the tweet.

    Returns:
        requests.Response or None: The response object on success, or None on failure.
    """
    load_dotenv()

    api_url = os.getenv("XHS_API_URL")
    api_key = os.getenv("XHS_API_KEY")

    if not api_url or not api_key:
        print("Error: XHS_API_URL and XHS_API_KEY must be set in the environment or a .env file.")
        return None

    endpoint = urljoin(api_url, "api/twitter/publish")
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    # Convert text from Markdown to plain text
    plain_text = convert_markdown_to_plain_text(text)

    data = {
        "account": account,
        "text": plain_text,
        "images": images if images else []
    }

    try:
        # Prepare a version of the data for safe logging
        log_payload = {
            "account": data["account"],
            "text": data["text"],
            "images": [
                f"{img[:100]}..." if "base64" in img and len(img) > 100 else img
                for img in data.get("images", [])
            ]
        }

        print(f"Sending request to: {endpoint}")
        print(f"Payload: {log_payload}")
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        response_data = response.json()
        print("Successfully published to Twitter.")
        print("Response:", response_data)

        # Construct and print the screenshot URL
        task_id = response_data.get("task_id")
        if task_id and api_url:
            screenshot_path = f"screenshots?taskId={task_id}"
            screenshot_url = urljoin(api_url, screenshot_path)
            print(f"Screenshot URL: {screenshot_url}")

        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while publishing to Twitter: {e}")
        if e.response:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        return None

def image_path_to_base64_uri(path):
    """将本地图片文件路径转换为 Base64 Data URI。"""
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publish a tweet with text and images via the API.")
    parser.add_argument("--account", type=str, required=True, help="The account identifier to use for publishing.")
    parser.add_argument("--text", type=str, required=True, help="The text content of the tweet, or a path to a file containing the text.")
    parser.add_argument("--images", nargs='*', default=[], help="A list of image URLs to attach to the tweet.")
    parser.add_argument("--image-dir", type=str, help="A directory to scan for image files (.png, .jpg, .jpeg, .gif).")

    args = parser.parse_args()

    # --- Process text argument ---
    tweet_text = args.text
    text_path = Path(args.text)
    if text_path.is_file():
        try:
            tweet_text = text_path.read_text(encoding='utf-8')
            print(f"Loaded text content from file: {args.text}")
        except Exception as e:
            print(f"Error reading text file {args.text}: {e}")
            exit(1)

    # --- Process image arguments ---
    all_images = list(args.images)  # Start with URLs from --images

    if args.image_dir:
        image_dir_path = Path(args.image_dir)
        if image_dir_path.is_dir():
            print(f"Scanning directory for images: {args.image_dir}")
            supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
            uploaded_image_urls = []
            for item in image_dir_path.iterdir():
                if item.is_file() and item.suffix.lower() in supported_extensions:
                    # 1. Resize image if it's too large
                    processed_image_path = resize_image_if_needed(item)

                    # 2. Convert image to Base64 URI
                    base64_uri = image_path_to_base64_uri(processed_image_path)
                    if not base64_uri:
                        continue

                    # 3. Upload the Base64 image to get a URL
                    print(f"Uploading {item.name}...")
                    image_url, _ = upload_image_from_base64(base64_uri, item.name)
                    
                    if image_url:
                        uploaded_image_urls.append(image_url)
            
            if uploaded_image_urls:
                print(f"Successfully uploaded {len(uploaded_image_urls)} local images.")
                all_images.extend(uploaded_image_urls)
        else:
            print(f"Error: --image-dir '{args.image_dir}' is not a valid directory.")

    if not tweet_text:
        print("Error: Tweet text is empty.")
        exit(1)

    publish_to_twitter(args.account, tweet_text, all_images)
