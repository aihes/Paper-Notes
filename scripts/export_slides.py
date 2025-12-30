import os
import time
from playwright.sync_api import sync_playwright

def export_slides(html_path, output_dir):
    abs_html_path = os.path.abspath(html_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})

        # Load the page
        url = f'file://{abs_html_path}'
        print(f"Loading {url}...")
        page.goto(url)

        # Wait for Reveal to be ready
        page.wait_for_selector('.reveal')
        
        # Disable controls for cleaner screenshots if needed, but Reveal usually hides them or they are small.
        # Let's ensure we are at the start
        page.evaluate("Reveal.slide(0, 0)")
        time.sleep(1)

        slide_index = 0
        while True:
            # Generate filename
            filename = f"slide_{slide_index:03d}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Screenshot
            page.screenshot(path=filepath)
            print(f"Saved {filename}")

            # Check if last slide using Reveal API
            is_last = page.evaluate("Reveal.isLastSlide()")
            if is_last:
                break

            # Move next
            page.evaluate("Reveal.next()")
            
            # Wait for transition (default is usually ~500ms, let's wait 1s to be safe)
            time.sleep(1)
            
            slide_index += 1

        browser.close()
        print(f"Export complete. Images saved to {output_dir}")

if __name__ == "__main__":
    html_file = "blog/spec-driven-development/presentation.html"
    output_directory = "blog/spec-driven-development/images/slides"
    
    # Ensure relative path works from workspace root
    if not os.path.exists(html_file):
        print(f"Error: Could not find {html_file}")
    else:
        export_slides(html_file, output_directory)