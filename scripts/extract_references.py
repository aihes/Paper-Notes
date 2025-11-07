import sys
from bs4 import BeautifulSoup

def extract_references(html_file_path):
    """
    Parses an HTML file to extract all hyperlink references and image sources.
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        output_lines = ["# Extracted References"]

        # Extract hyperlinks
        output_lines.append("\n## Links\n")
        links = soup.find_all('a', href=True)
        if links:
            for link in links:
                output_lines.append(f"- [{link.text.strip()}]({link['href']})")
        else:
            output_lines.append("No links found.")

        # Extract images
        output_lines.append("\n## Images\n")
        images = soup.find_all('img', src=True)
        if images:
            for img in images:
                alt_text = img.get('alt', 'Image')
                output_lines.append(f"- ![{alt_text}]({img['src']})")
        else:
            output_lines.append("No images found.")
        
        return "\n".join(output_lines)

    except FileNotFoundError:
        return f"Error: The file '{html_file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_references.py <html_file_path>", file=sys.stderr)
        sys.exit(1)
        
    html_file = sys.argv[1]
    references_markdown = extract_references(html_file)
    print(references_markdown)