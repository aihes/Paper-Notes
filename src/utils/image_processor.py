import io
from PIL import Image
from pathlib import Path

def resize_image_if_needed(image_path: Path, max_width: int = 1920) -> Path:
    """
    Checks if an image exceeds constraints and resizes/compresses it if necessary.
    Ensures the image is under 2.5MB and max dimension (default 1920px).

    Args:
        image_path (Path): The path to the image file.
        max_width (int): The maximum allowed width.

    Returns:
        Path: The path to the (potentially resized) image.
              Returns the original path if no resizing was needed.
    """
    MAX_SIZE_BYTES = 2.5 * 1024 * 1024 # 2.5MB
    
    try:
        with Image.open(image_path) as img:
            original_format = img.format
            img_format = original_format if original_format else 'JPEG'
            
            # Prepare to check if we need to modify the image
            width, height = img.size
            file_size = image_path.stat().st_size
            
            needs_processing = False
            
            # Check 1: Dimensions
            if width > max_width or height > max_width:
                needs_processing = True
                
            # Check 2: File Size
            if file_size > MAX_SIZE_BYTES:
                needs_processing = True
                
            if not needs_processing:
                return image_path
                
            # Start Processing
            print(f"Processing image '{image_path.name}' (Size: {file_size/1024/1024:.2f}MB, Dim: {width}x{height})...")
            
            # Handle RGBA to RGB for JPEG
            if img_format in ['JPEG', 'JPG'] and img.mode == 'RGBA':
                img = img.convert('RGB')
                
            # Initial Resize if needed
            if width > max_width or height > max_width:
                ratio = min(max_width / width, max_width / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"Resized to {new_width}x{new_height}")

            # Iterative Compression Loop
            quality = 85
            # If we are just resizing and format is not lossy-tunable (like PNG), we might need to just save.
            # But if size is still too big, we might need to switch to JPEG or resize further.
            # For this script, let's keep original format unless we absolutely must change it? 
            # Or just enforce JPEG for non-transparent images if they are huge?
            # Let's stick to simple quality reduction for supported formats.
            
            while True:
                img_byte_arr = io.BytesIO()
                save_kwargs = {'format': img_format, 'optimize': True}
                
                if img_format in ['JPEG', 'JPG', 'WEBP']:
                    save_kwargs['quality'] = quality
                    
                img.save(img_byte_arr, **save_kwargs)
                current_size = img_byte_arr.tell()
                
                if current_size <= MAX_SIZE_BYTES:
                    break
                
                can_reduce_quality = img_format in ['JPEG', 'JPG', 'WEBP'] and quality > 30
                
                if can_reduce_quality:
                    quality -= 10
                    print(f"Size {current_size/1024/1024:.2f}MB > 2.5MB, reducing quality to {quality}")
                else:
                    # Further resize dimensions
                    width, height = img.size
                    if width < 500 or height < 500:
                        print(f"Warning: Image reached min dimensions ({width}x{height}) but still {current_size/1024/1024:.2f}MB")
                        break
                        
                    new_width = int(width * 0.9)
                    new_height = int(height * 0.9)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"Size {current_size/1024/1024:.2f}MB > 2.5MB, resizing to {new_width}x{new_height}")

            # Save to new file
            new_path = image_path.with_name(f"{image_path.stem}_resized{image_path.suffix}")
            with open(new_path, 'wb') as f:
                f.write(img_byte_arr.getvalue())
                
            print(f"Saved optimized image to '{new_path.name}' ({current_size/1024/1024:.2f}MB)")
            return new_path

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        # Return original path on error to not break the flow
        return image_path
