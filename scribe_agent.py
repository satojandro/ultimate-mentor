import os
import json
from dotenv import load_dotenv
from firecrawl import FirecrawlApp

# --- Configuration ---
# Load environment variables from a .env file
load_dotenv()

# Get your Firecrawl API key from the environment variables
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# The URL of the page we want to scrape. For now, we'll use the Cannes prize page.
# In a real-world scenario, we would scrape a list of project showcase URLs.
TARGET_URL = "https://ethglobal.com/events/cannes/prizes"

# The directory where we will save our scraped data
OUTPUT_DIR = "hackathon_data_md"

# --- Main Scribe Agent Logic ---

def scribe_agent(url: str, output_path: str):
    """
    Uses Firecrawl to scrape a URL and save the content as a markdown file.

    Args:
        url (str): The URL to scrape.
        output_path (str): The path to save the markdown file.
    """
    print(f"Scribe Agent activated. Scraping: {url}")

    # Check if the API key is available
    if not FIRECRAWL_API_KEY:
        print("Error: FIRECRAWL_API_KEY not found in .env file.")
        print("Please get an API key from https://www.firecrawl.dev/ and add it to your .env file.")
        return

    try:
        # Initialize the FirecrawlApp with your API key
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

        # Scrape the URL. This returns a ScrapeResponse object.
        scraped_data = app.scrape_url(url)

        # --- FIX ---
        # Access the markdown content as an attribute, not a dictionary key.
        markdown_content = scraped_data.markdown

        if not markdown_content:
            print("Error: Could not extract markdown content from the scraped data.")
            return

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Save the markdown content to the specified file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Successfully scraped content and saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")


# This block ensures the script runs only when executed directly
if __name__ == "__main__":
    # Define the output file path
    output_file = os.path.join(OUTPUT_DIR, "cannes_prizes.md")
    
    # Run the scribe agent
    scribe_agent(TARGET_URL, output_file)

