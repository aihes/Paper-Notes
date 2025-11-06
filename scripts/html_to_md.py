import sys
import html2text
from bs4 import BeautifulSoup

def convert_html_to_markdown(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main article content
        article = soup.find('article')
        
        if article:
            # Convert the article HTML to Markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            markdown_content = h.handle(str(article))
            print(markdown_content)
        else:
            print("Could not find the main article content.", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: The file '{html_file_path}' was not found.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html_to_md.py <html_file_path>", file=sys.stderr)
        sys.exit(1)
        
    html_file = sys.argv[1]
    convert_html_to_markdown(html_file)