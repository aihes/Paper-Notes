import os
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv

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

    endpoint = f"{api_url}/api/twitter/publish"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "account": account,
        "text": text,
        "images": images if images else []
    }

    try:
        print(f"Sending request to: {endpoint}")
        print(f"Payload: {data}")
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        print("Successfully published to Twitter.")
        print("Response:", response.json())
        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while publishing to Twitter: {e}")
        if e.response:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
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
            supported_extensions = ['.png', '.jpg', '.jpeg', '.gif']
            local_images = []
            for item in image_dir_path.iterdir():
                if item.is_file() and item.suffix.lower() in supported_extensions:
                    # Convert to absolute file URI
                    file_uri = item.resolve().as_uri()
                    local_images.append(file_uri)
            
            if local_images:
                print(f"Found {len(local_images)} local images.")
                all_images.extend(local_images)
        else:
            print(f"Error: --image-dir '{args.image_dir}' is not a valid directory.")

    if not tweet_text:
        print("Error: Tweet text is empty.")
        exit(1)

    publish_to_twitter(args.account, tweet_text, all_images)