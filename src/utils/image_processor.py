from PIL import Image
from pathlib import Path

def resize_image_if_needed(image_path: Path, max_width: int = 2000) -> Path:
    """
    Checks if an image width exceeds a max value and resizes it if necessary.

    Args:
        image_path (Path): The path to the image file.
        max_width (int): The maximum allowed width.

    Returns:
        Path: The path to the (potentially resized) image.
              Returns the original path if no resizing was needed.
    """
    try:
        with Image.open(image_path) as img:
            if img.width > max_width:
                print(f"Image '{image_path.name}' width ({img.width}px) exceeds {max_width}px. Resizing...")
                
                # Calculate new dimensions, scaling by 50%
                new_width = img.width // 2
                new_height = img.height // 2
                
                # Resize the image
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Construct new path
                new_path = image_path.with_name(f"{image_path.stem}_resized{image_path.suffix}")
                
                # Save the resized image
                resized_img.save(new_path)
                print(f"Saved resized image to '{new_path.name}'")
                return new_path
            else:
                # No resizing needed
                return image_path
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        # Return original path on error to not break the flow
        return image_path
