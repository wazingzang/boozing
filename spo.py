from playwright.sync_api import sync_playwright
import time
import random
import subprocess
from multiprocessing import Process

# List of proxy servers
proxies = [
    "185.199.229.156:7492",
    "185.199.228.220:7300",
    "185.199.231.45:8382",
    "188.74.210.207:6286",
    "188.74.183.10:8279",
    # Add more proxy server URLs as needed
]

# Define a function to perform actions on a page
def perform_actions(page, url, proxy):
    # Print the proxy being used for this instance
    print(f"Navigating To URL Using [{proxy}]")

    # Go to the specified URL
    page.goto(url)

    # Locate a Button to ensure the page is loaded
    locate_button = page.locator('button:has-text("Play All")')
    print("Page Loaded")

    # Button Locator To Click Play
    play_song = page.locator('button:has-text("Play All")')
    play_song.click()
    print("Clicked Play All")

# Define a function to run an instance
def run_instance():
    with sync_playwright() as p:
        # Select a random proxy from the list
        proxy = random.choice(proxies)

        # Create a new browser instance with the selected proxy
        browser = p.chromium.launch(headless=False, proxy={"server": proxy})
        context = browser.new_context()
        page = context.new_page()

        # Define the URL you want to navigate to
        url = "https://www.boomplay.com/albums/31470318?from=artists"

        # Perform actions on the current instance up to clicking "Play All"
        perform_actions(page, url, proxy)

        # Wait for 120 seconds after clicking "Play All"
        time.sleep(120)

        # Close the browser instance
        browser.close()

if __name__ == '__main__':
    # Infinite loop to continuously run the script
    while True:
        # Create and start two processes to run instances concurrently
        processes = []
        for _ in range(2):
            process = Process(target=run_instance)
            process.start()
            processes.append(process)

        # Wait for both processes to complete
        for process in processes:
            process.join()

        # Shuffle the list of proxies to randomize their order
        random.shuffle(proxies)
