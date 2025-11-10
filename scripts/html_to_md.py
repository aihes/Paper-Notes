#!/usr/bin/env python3
"""
Webpage to Markdown Converter

Fetches HTML content from a URL, extracts the main article,
and converts it to Markdown.
"""

import argparse
import sys
import requests
import html2text
from bs4 import BeautifulSoup

def fetch_and_convert(url: str, output_path: str):
    """
    Fetches HTML from a URL, converts it to Markdown, and saves it to a file.
    """
    try:
        # 1. Fetch HTML content
        print(f"ℹ️ Fetching content from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html_content = response.text
        print("✅ Content fetched successfully.")

        # 2. Parse HTML and find the main article
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common tags for main content
        main_content = soup.find('article') or soup.find('main')
        
        if not main_content:
            print("⚠️ Could not find <article> or <main> tag. Falling back to <body>.", file=sys.stderr)
            main_content = soup.body

        if not main_content:
            raise Exception("Could not find any main content in the page.")

        # 3. Convert the article HTML to Markdown
        print("ℹ️ Converting HTML to Markdown...")
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0  # No line wrapping
        markdown_content = h.handle(str(main_content))
        print("✅ Conversion successful.")

        # 4. Save to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✅ Markdown content saved to: {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching URL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a webpage to a clean Markdown file.")
    parser.add_argument("--url", required=True, help="The URL of the webpage to convert.")
    parser.add_argument("--output", required=True, help="The path to save the output Markdown file.")
    
    args = parser.parse_args()
    
    fetch_and_convert(args.url, args.output)
