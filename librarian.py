import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings

# --- Configuration ---
load_dotenv()

# Get Supabase and OpenAI credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# The JSON file containing our scraped project data
DATA_FILE = "hackathon_data_md/prague_projects.json"

# --- Main Librarian Logic ---

def initialize_clients():
    """Initialize and return Supabase and OpenAI clients."""
    if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
        print("Error: Missing SUPABASE_URL, SUPABASE_KEY, or OPENAI_API_KEY in .env file.")
        return None, None
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return supabase, embeddings

def process_and_upload_data(supabase: Client, embeddings_client: OpenAIEmbeddings, data_file: str):
    """
    Reads project data from a JSON file, generates embeddings, and uploads to Supabase.
    """
    print(f"Librarian activated. Processing data from: {data_file}")

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_file}. Please ensure it exists.")
        return

    for project in projects:
        # Combine the most important text fields to create a single document for embedding
        content_to_embed = f"Project: {project.get('name', '')}\nTagline: {project.get('tagline', '')}\nDescription: {project.get('description', '')}\nTechnology: {project.get('howItsMade', '')}"
        
        print(f"  - Processing and embedding project: {project.get('name')}")
        
        try:
            # Generate the vector embedding for the content
            embedding = embeddings_client.embed_query(content_to_embed)
            
            # Prepare the data for upload
            data_to_upload = {
                "name": project.get("name"),
                "tagline": project.get("tagline"),
                "description": project.get("description"),
                "how_its_made": project.get("howItsMade"),
                "github_url": project.get("githubUrl"),
                "project_url": project.get("projectUrl"),
                "showcase_url": project.get("showcaseUrl"),
                "embedding": embedding,
            }
            
            # Insert the data into the 'projects' table in Supabase
            response = supabase.table("projects").insert(data_to_upload).execute()
            
            # Check for errors in the response
            if response.data:
                 print(f"    -> Successfully uploaded '{project.get('name')}' to Supabase.")
            else:
                print(f"    -> Failed to upload '{project.get('name')}'. Response: {response}")


        except Exception as e:
            print(f"    -> An error occurred while processing '{project.get('name')}': {e}")

    print("\nLibrarian has finished processing all projects.")


if __name__ == "__main__":
    supabase_client, openai_embeddings = initialize_clients()
    if supabase_client and openai_embeddings:
        process_and_upload_data(supabase_client, openai_embeddings, DATA_FILE)

