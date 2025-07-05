import os
import time
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# --- Configuration ---
# Load environment variables from a .env file
load_dotenv()

# Get your Firecrawl API key from the environment variables
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# The directory where we will save our scraped data
OUTPUT_DIR = "hackathon_data_md"

# List of hackathon showcases we want to scrape
# We will scrape all pages for each of these
SHOWCASE_BASE_URLS = {
    "prague_projects": "https://ethglobal.com/showcase/prague-2024",
    "sydney_projects": "https://ethglobal.com/showcase/sydney-2024",
    "london_projects": "https://ethglobal.com/showcase/ethlondon-2023",
}

# The prizes pages (these are single pages, no pagination needed)
PRIZE_URLS = {
    "prague_prizes": "https://ethglobal.com/events/prague-2024/prizes",
    "sydney_prizes": "https://ethglobal.com/events/sydney-2024/prizes",
    "london_prizes": "https://ethglobal.com/events/ethlondon-2023/prizes",
}


# --- Main Scribe Agent Logic ---

def initialize_app():
    """Initializes the FirecrawlApp and checks for API key."""
    if not FIRECRAWL_API_KEY:
        print("Error: FIRECRAWL_API_KEY not found in .env file.")
        return None
    return FirecrawlApp(api_key=FIRECRAWL_API_KEY)

def scrape_single_page(app: FirecrawlApp, url: str, output_path: str):
    """Scrapes a single URL and saves the content."""
    print(f"Scribing single page: {url}")
    try:
        scraped_data = app.scrape_url(url)
        if scraped_data and scraped_data.markdown:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(scraped_data.markdown)
            print(f"-> Successfully saved to: {output_path}")
        else:
            print(f"-> No content found for {url}")
    except Exception as e:
        print(f"-> An error occurred: {e}")

def scrape_paginated_showcase(app: FirecrawlApp, base_url: str, output_path: str):
    """
    Scrapes all pages of a hackathon showcase and combines them into one file.
    """
    print(f"Scribing paginated showcase: {base_url}")
    all_markdowns = []
    page = 1
    while True:
        # Construct the URL for the current page
        paginated_url = f"{base_url}?page={page}"
        print(f"  - Scraping page {page}: {paginated_url}")

        try:
            scraped_data = app.scrape_url(paginated_url)
            
            # Check if the page has meaningful content. An empty showcase page has very little markdown.
            # This threshold helps us detect the last page.
            if not scraped_data or len(scraped_data.markdown) < 500:
                print(f"  - Page {page} appears to be empty. Concluding showcase scrape.")
                break
            
            all_markdowns.append(scraped_data.markdown)
            page += 1
            time.sleep(1) # Be polite to the server, wait a second between requests

        except Exception as e:
            print(f"  - An error occurred on page {page}: {e}. Concluding showcase scrape.")
            break
            
    if all_markdowns:
        # Combine all pages into a single markdown file
        full_content = "\n\n<!-- Nova: Page Break -->\n\n".join(all_markdowns)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"-> Successfully combined {len(all_markdowns)} pages and saved to: {output_path}")
    else:
        print("-> No content was scraped for this showcase.")


# This block ensures the script runs only when executed directly
if __name__ == "__main__":
    firecrawl_app = initialize_app()
    if firecrawl_app:
        # --- MODIFICATION: Commented out the prize scraping to avoid re-running ---
        # print("--- Scraping Prize Pages ---")
        # for name, url in PRIZE_URLS.items():
        #     scrape_single_page(firecrawl_app, url, os.path.join(OUTPUT_DIR, f"{name}.md"))
        #     time.sleep(1)

        # Scrape all the showcase pages
        print("\n--- Scraping Showcase Pages ---")
        for name, url in SHOWCASE_BASE_URLS.items():
            scrape_paginated_showcase(firecrawl_app, url, os.path.join(OUTPUT_DIR, f"{name}.md"))
            time.sleep(1)
        
        print("\n--- The Great Scrape is complete! ---")

