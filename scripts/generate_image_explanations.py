import os
import sys
import argparse
from typing import List
import re

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.ollama_client import OllamaClient

def get_relative_image_path(output_file_path: str, image_path: str) -> str:
    """Calculates the relative path for the image from the output file's location."""
    try:
        output_dir = os.path.dirname(os.path.abspath(output_file_path))
        relative_path = os.path.relpath(os.path.abspath(image_path), output_dir)
        return relative_path.replace("\\\\", "/")
    except Exception:
        # Fallback for any path issue
        return image_path

def generate_explanations(image_dir: str, model: str, output_file: str, prompt: str):
    """
    Generates explanations for all images in a directory using Ollama and saves them to a Markdown file.

    Args:
        image_dir (str): Path to the directory containing images.
        model (str): The Ollama model to use for explanations.
        output_file (str): Path to the output Markdown file.
        prompt (str): The prompt to use for the multimodal model.
    """
    if not os.path.isdir(image_dir):
        print(f"Error: Image directory not found at {image_dir}")
        return

    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])
    if not image_files:
        print(f"No images found in directory: {image_dir}")
        return

    print(f"Found {len(image_files)} images. Initializing model and starting explanations...")

    try:
        client = OllamaClient(model=model)
        available_models = client.list_models()
        if model not in available_models:
            print(f"Error: Model '{model}' is not available. Please pull it first.")
            print(f"Available models: {available_models}")
            return
    except Exception as e:
        print(f"Failed to initialize OllamaClient: {e}")
        return

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Image Explanations\n\n")
        f.write(f"This document contains AI-generated explanations for images in the `{os.path.basename(image_dir)}` directory, using the `{model}` model.\n\n---\n\n")

        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)
            print(f"Processing: {image_file}...")

            try:
                client.clear_history()
                response = client.chat(prompt, image_paths=[image_path])
                
                # Sanitize filename for use as title/header
                title = os.path.splitext(image_file)[0]
                
                # Use a relative path for the image in the Markdown file
                relative_img_path = get_relative_image_path(output_file, image_path)

                f.write(f"## {title}\n\n")
                f.write(f"![{title}]({relative_img_path})\n\n")
                f.write("### AI-Generated Explanation\n\n")
                f.write(f"{response}\n\n---\n\n")
                print(f"  -> Success.")

            except Exception as e:
                error_message = f"An error occurred while processing {image_file}: {e}"
                print(f"  -> {error_message}")
                f.write(f"## {image_file}\n\n")
                f.write(f"### Explanation Failed\n\n`{error_message}`\n\n---\n\n")

    print(f"All explanations have been saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate explanations for images in a directory using a multimodal model.")
    parser.add_argument("--image-dir", type=str, required=True, help="Directory containing the images.")
    parser.add_argument("--model", type=str, default="gemma3:4b", help="The Ollama model to use (e.g., 'llava').")
    parser.add_argument("--output-file", type=str, required=True, help="The Markdown file to save explanations to.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="As a senior industry analyst, provide a detailed explanation of this image in Chinese. Your analysis should cover: 1. What is the core content and data presented? 2. What is the key message or insight it's trying to convey? 3. What role might this image play in a broader presentation or report?",
        help="The prompt to use for the model."
    )

    args = parser.parse_args()
    generate_explanations(args.image_dir, args.model, args.output_file, args.prompt)
