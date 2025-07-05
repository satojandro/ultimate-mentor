import os
import json
import asyncio
import threading
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from uagents import Agent, Context, Model, Bureau
from uagents.setup import fund_agent_if_low

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Initialize Global Clients ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    embeddings_client = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    llm_client = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY)
    print("✅ Clients for Supabase, Embeddings, and LLM initialized successfully.")
except Exception as e:
    print(f"🔥 Error initializing clients: {e}")
    supabase, embeddings_client, llm_client = None, None, None

# --- Agent Definitions ---

class UserQuery(Model):
    text: str

# 1. The Guide Agent (The Mentor)
guide_agent = Agent(
    name="guide_agent",
    seed="ultimate_mentor_secret_seed_phrase"
)

@guide_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Hello, I am the Ultimate Mentor. My address is: {ctx.agent.address}")

@guide_agent.on_message(model=UserQuery)
async def handle_query(ctx: Context, sender: str, msg: UserQuery):
    ctx.logger.info(f"Received query: '{msg.text}'")
    try:
        ctx.logger.info("-> Step 1: Creating embedding...")
        query_embedding = embeddings_client.embed_query(msg.text)

        ctx.logger.info("-> Step 2: Searching database...")
        search_results = supabase.rpc(
            "match_projects",
            {"query_embedding": query_embedding, "match_threshold": 0.75, "match_count": 3},
        ).execute()

        if not search_results.data:
            print("\n--- Your Mentor's Answer ---\nI couldn't find any projects in the database that matched your query. Please try asking in a different way!\n--------------------------\n")
            return

        ctx.logger.info("-> Step 3: Formatting results...")
        context_str = ""
        for i, project in enumerate(search_results.data):
            context_str += f"--- Project {i+1}: {project['name']} ---\nDescription: {project['description']}\nHow It's Made: {project['how_its_made']}\n\n"

        ctx.logger.info("-> Step 4: Synthesizing answer...")
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are the Ultimate Hackathon Mentor. Your goal is to provide clear, insightful answers based on the context provided. Synthesize the information from the projects below to answer the user's question."),
            ("user", "Context from my database:\n\n{context}\n\nBased on this, please answer my question: {question}")
        ])
        chain = prompt_template | llm_client
        response = chain.invoke({"context": context_str, "question": msg.text})
        
        print(f"\n--- Your Mentor's Answer ---\n{response.content}\n--------------------------\n")

    except Exception as e:
        ctx.logger.error(f"An error occurred: {e}")

# 2. The User Agent (The Interface)
user_agent = Agent(
    name="user_agent",
    seed="user_secret_seed_phrase"
)

# This is the main interactive loop for the user.
async def user_interaction_loop(ctx: Context):
    await asyncio.sleep(2.0) # Wait for agents to be ready
    print("\n--- Ultimate Mentor Terminal ---")
    print("Ask your question. Type 'exit' to quit.")
    
    while True:
        try:
            # --- FIX: Pass the input function and its argument separately ---
            query = await asyncio.to_thread(input, "Your question: ")
            if query.lower() == 'exit':
                ctx.bureau.stop()
                break
            
            await ctx.send(guide_agent.address, UserQuery(text=query))

        except (KeyboardInterrupt, EOFError):
            ctx.bureau.stop()
            break

# The user agent will kick off the interactive loop when it starts.
@user_agent.on_event("startup")
async def startup_and_run_main(ctx: Context):
    ctx.logger.info(f"Hello, I am the User Agent. I will start the interactive prompt now.")
    asyncio.create_task(user_interaction_loop(ctx))

# --- Main Execution Block ---
if __name__ == "__main__":
    if not all([supabase, embeddings_client, llm_client]):
        print("🔥 Could not start agents. Check your .env file.")
    else:
        # The Bureau runs both agents together, ensuring they can communicate
        bureau = Bureau()
        bureau.add(guide_agent)
        bureau.add(user_agent)
        bureau.run()
