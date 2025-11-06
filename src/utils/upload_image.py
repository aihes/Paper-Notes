import os
import requests
from dotenv import load_dotenv

def upload_image_from_base64(base64_string, filename):
    """
    Uploads an image to the specified API endpoint using a base64 string.

    Args:
        base64_string (str): The base64 encoded image string (including the data URI scheme).
        filename (str): The desired filename for the image on the server.

    Returns:
        requests.Response: The response object from the API call.
    """
    load_dotenv()

    api_url = os.getenv("XHS_API_URL")
    api_key = os.getenv("XHS_API_KEY")

    if not api_url or not api_key:
        raise ValueError("XHS_API_URL and XHS_API_KEY must be set in the .env file")

    endpoint = f"{api_url}/api/images/upload-base64"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "image": base64_string,
        "filename": filename
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        print(f"Successfully uploaded {filename}.")
        print("Response:", response.json())
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # A 1x1 transparent pixel PNG
    dummy_base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
    upload_image_from_base64(dummy_base64_image, "my-test-image")
