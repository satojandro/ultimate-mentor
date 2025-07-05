import os
import time
import json
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- Configuration ---
load_dotenv()
OUTPUT_DIR = "hackathon_data_md"

SHOWCASE_BASE_URLS = {
    "prague_projects": "https://ethglobal.com/showcase?events=prague",
    "bangkok_projects": "https://ethglobal.com/showcase?events=bangkok",
    "brussels_projects": "https://ethglobal.com/showcase?events=brussels",
    "sanfrancisco_projects": "https://ethglobal.com/showcase?events=sanfrancisco2024",
    "singapore_projects": "https://ethglobal.com/showcase?events=singapore2024",
    "taipei_projects": "https://ethglobal.com/showcase?events=taipei",
}

# --- This header is crucial to mimic a real browser request ---
# We will use a generic User-Agent, but in a real scenario might need the cookie
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/x-component",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "RSC": "1", # This header seems important from your screenshot
    "Connection": "keep-alive",
}

# --- Main Scribe Agent Logic ---

def get_project_links_with_selenium(base_url: str, driver):
    """Uses Selenium to scan showcase pages and return a list of project links."""
    project_links = []
    page = 1
    print(f"--- Level 1: Discovering project links for {base_url} ---")
    try:
        while True:
            paginated_url = f"{base_url}&page={page}"
            print(f"  - Scanning page {page}...")
            driver.get(paginated_url)
            time.sleep(5)

            if "No results found" in driver.page_source or "This showcase has no projects" in driver.page_source:
                print(f"  - Page {page} is the last page.")
                break

            links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/showcase/']")
            for link in links:
                href = link.get_attribute('href')
                if href and href not in project_links:
                    project_links.append(href)
            page += 1
            if page > 25: break
    except Exception as e:
        print(f"  - An error occurred during link discovery: {e}")
    return project_links

def get_project_details_from_api(project_url: str):
    """Fetches the detailed project data by mimicking the internal API call."""
    try:
        # Transform the showcase URL into the internal API URL
        api_url = f"{project_url}?_rsc=1" # Adding the required query parameter
        response = requests.get(api_url, headers=HEADERS)
        response.raise_for_status() # Will raise an exception for bad status codes

        # The response is a weird, line-delimited format. We need to find the JSON part.
        for line in response.text.split('\n'):
            if line.startswith('6:'): # The project data is on the line starting with '6:'
                # Clean the line to get pure JSON
                json_part = line[2:] # Remove the '6:' prefix
                data = json.loads(json_part)
                # Navigate the complex structure to find the project details
                project_data = data[3].get('project', {})
                return {
                    "name": project_data.get("name"),
                    "tagline": project_data.get("tagline"),
                    "description": project_data.get("description"),
                    "howItsMade": project_data.get("howItsMade"),
                    "githubUrl": project_data.get("primaryRepository", {}).get("url") if project_data.get("primaryRepository") else None,
                    "projectUrl": project_data.get("url"),
                    "showcaseUrl": project_url,
                }
    except Exception as e:
        print(f"    - Failed to fetch or parse API data for {project_url}. Error: {e}")
    return None

if __name__ == "__main__":
    print("\n--- Initializing Scribe Agent (API-Based) ---")
    
    # Setup Selenium driver once
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    for name, url in SHOWCASE_BASE_URLS.items():
        hackathon_name = name.replace('_projects', '')
        links = get_project_links_with_selenium(url, driver)
        print(f"--- Found {len(links)} links for {hackathon_name}. Now fetching details via API. ---")
        
        hackathon_projects = []
        for i, link in enumerate(links):
            print(f"  - Processing {i+1}/{len(links)}: {link}")
            details = get_project_details_from_api(link)
            if details:
                hackathon_projects.append(details)
            time.sleep(1) # Be polite to the API
        
        # --- FIX: Save a separate JSON file for each hackathon ---
        if hackathon_projects:
            output_path = os.path.join(OUTPUT_DIR, f"{hackathon_name}_projects.json")
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(hackathon_projects, f, indent=2)
            print(f"\n--- SUCCESS! Data for {hackathon_name} saved to {output_path} ---\n")
        else:
            print(f"\n--- No data collected for {hackathon_name}. ---\n")

    driver.quit()
    print("\n--- The Great Scrape is complete! ---")
