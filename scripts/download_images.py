import sys
import os
import re
import subprocess

def download_images_from_references(md_file_path, target_domain, output_dir):
    """
    Parses a Markdown file to find image URLs from a specific domain,
    and downloads them to a specified directory.
    """
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex to find Markdown image syntax: ![](url)
        image_urls = re.findall(r'!\[.*?\]\((.*?)\)', content)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")

        downloaded_count = 0
        for url in image_urls:
            # Filter by domain and exclude avatars
            if url.startswith(target_domain) and 'avatar' not in url:
                # Get filename from URL
                filename = url.split('/')[-1].split('?')[0]
                output_path = os.path.join(output_dir, filename)
                
                print(f"Downloading {url} to {output_path}...")
                try:
                    # Using curl to download
                    subprocess.run(['curl', '-o', output_path, '-L', url], check=True)
                    downloaded_count += 1
                except subprocess.CalledProcessError as e:
                    print(f"Failed to download {url}: {e}", file=sys.stderr)
                except FileNotFoundError:
                    print("Error: 'curl' command not found. Please ensure it is installed and in your PATH.", file=sys.stderr)
                    return

        print(f"\nDownload complete. Total images downloaded: {downloaded_count}")

    except FileNotFoundError:
        print(f"Error: The file '{md_file_path}' was not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python download_images.py <md_file_path> <target_domain> <output_dir>", file=sys.stderr)
        sys.exit(1)
        
    md_file = sys.argv[1]
    domain = sys.argv[2]
    out_dir = sys.argv[3]
    
    download_images_from_references(md_file, domain, out_dir)