import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin

def upload_image_from_base64(base64_string, filename):
    """
    Uploads an image to the specified API endpoint using a base64 string.

    Args:
        base64_string (str): The base64 encoded image string (including the data URI scheme).
        filename (str): The desired filename for the image on the server.

    Returns:
        tuple[str, requests.Response] | tuple[None, None]: A tuple containing the full image URL and the response object, or (None, None) on failure.
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
        
        response_data = response.json()
        relative_url = response_data.get("url")
        
        if relative_url:
            full_url = urljoin(api_url, relative_url)
            print(f"Successfully uploaded {filename}.")
            print(f"Full URL: {full_url}")
            return full_url, response
        else:
            print(f"Successfully uploaded {filename}, but no URL was returned in the response.")
            print("Response:", response_data)
            return None, response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == '__main__':
    # Example usage:
    # A 1x1 transparent pixel PNG
    dummy_base64_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gAAAABJRU5ErkJggg=="
    uploaded_url, _ = upload_image_from_base64(dummy_base64_image, "my-test-image-2")
    if uploaded_url:
        print("\nTest successful. The function returned the full URL.")
