import asyncio
from playwright.async_api import async_playwright
import os

async def launch_with_playwright():
    """
    Launches a persistent browser session with a remote debugging port enabled.
    This setup allows other Playwright scripts to connect to the running browser
    instance via the Chrome DevTools Protocol (CDP).
    """
    user_data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'playwright_user_data')
    port = 9222
    # The CDP endpoint URL is predictable when using --remote-debugging-port
    cdp_endpoint = f"http://127.0.0.1:{port}"

    os.makedirs(user_data_dir, exist_ok=True)

    print("Attempting to launch browser with a remote debugging port...")
    print(f"Persistent Profile Directory: {user_data_dir}")
    print(f"Remote Debugging Port: {port}")
    
    async with async_playwright() as p:
        try:
            # Use launch_persistent_context to correctly handle the user data directory.
            # The remote debugging port is enabled via the 'args' parameter.
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                args=[
                    f"--remote-debugging-port={port}",
                    '--disable-gpu',
                    '--no-sandbox'
                ]
            )

            print("\nBrowser launched successfully!")
            print("It is now listening for remote connections.")
            print(f"You can connect other Playwright scripts to this browser using the CDP endpoint:")
            print(f"    Endpoint URL: {cdp_endpoint}")
            print("    Example: await playwright.chromium.connect_over_cdp('http://127.0.0.1:9222')")
            
            print("\nTo demonstrate, a new page will be opened to 'https://x.com/home'.")
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto("https://x.com/home")

            print("\nThis browser session will remain active until you press Enter in this terminal.")
            await asyncio.to_thread(input)

            await context.close()
            print("Browser closed.")

        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print(f"Please ensure no other browser instance is using port {port} or the specified user data directory.")

if __name__ == "__main__":
    asyncio.run(launch_with_playwright())
