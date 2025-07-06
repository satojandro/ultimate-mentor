import os
import json
import asyncio
import threading
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from uagents import Agent, Context, Model, Bureau, Protocol
from uagents.setup import fund_agent_if_low
from pyngrok import ngrok, conf

# --- Configuration ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

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

class MentorResponse(Model):
    text: str

mentor_protocol = Protocol("UltimateMentor", version="1.0")
"""
Antoine, the Ultimate ETHGlobal Mentor, provides strategic advice for hackathon participants.
It has access to a curated database of past project submissions from events like ETHGlobal Prague, Sydney, and London.
You can ask it for:
- Insights on which technologies are trending.
- Examples of successful projects in a specific domain (e.g., DeFi, ZK, AI).
- Suggestions for novel ideas that build upon previous work.
"""

@mentor_protocol.on_message(model=UserQuery, replies=MentorResponse)
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
            no_match_response = "I couldn't find any projects in the database that matched your query. Please try asking in a different way!"
            print(f"\n--- Antoine's Answer ---\n{no_match_response}\n--------------------------\n")
            await ctx.send(sender, MentorResponse(text=no_match_response))
            return

        ctx.logger.info("-> Step 3: Formatting results...")
        context_str = ""
        for i, project in enumerate(search_results.data):
            context_str += f"--- Project {i+1}: {project['name']} ---\nDescription: {project['description']}\nHow It's Made: {project['how_its_made']}\n\n"

        ctx.logger.info("-> Step 4: Synthesizing answer...")
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are Antoine, the Ultimate Hackathon Mentor. Your goal is to provide clear, insightful answers based on the context provided. Synthesize the information from the projects below to answer the user's question."),
            ("user", "Context from my database:\n\n{context}\n\nBased on this, please answer my question: {question}")
        ])
        chain = prompt_template | llm_client
        response = chain.invoke({"context": context_str, "question": msg.text})
        final_answer = response.content
        
        print(f"\n--- Antoine's Answer ---\n{final_answer}\n--------------------------\n")
        
        await ctx.send(sender, MentorResponse(text=final_answer))

    except Exception as e:
        ctx.logger.error(f"An error occurred: {e}")
        error_message = f"Sorry, an error occurred: {e}"
        await ctx.send(sender, MentorResponse(text=error_message))

# --- ngrok Tunnel Setup ---
def setup_ngrok_tunnel(port: int):
    if NGROK_AUTH_TOKEN:
        conf.get_default().auth_token = NGROK_AUTH_TOKEN
        http_tunnel = ngrok.connect(port, "http")
        print(f"✅ ngrok tunnel created: {http_tunnel.public_url}")
        return http_tunnel.public_url
    else:
        print("🔥 NGROK_AUTH_TOKEN not found. Agent will not be reachable publicly.")
        return None

# --- Agent and Bureau Setup ---
PORT = 8000
public_url = setup_ngrok_tunnel(PORT)

antoine_agent = Agent(
    name="antoine_agent",
    seed="ultimate_mentor_secret_seed_phrase"
)
antoine_agent.include(mentor_protocol, publish_manifest=True)

user_agent = Agent(
    name="user_agent",
    seed="user_secret_seed_phrase"
)

async def user_interaction_loop(ctx: Context):
    await asyncio.sleep(2.0)
    print("\n--- Ultimate Mentor Terminal ---")
    print("Ask your question. Type 'exit' to quit.")
    
    while True:
        try:
            query = await asyncio.to_thread(input, "Your question: ")
            if query.lower() == 'exit':
                ctx.bureau.stop()
                break
            
            await ctx.send(antoine_agent.address, UserQuery(text=query))

        except (KeyboardInterrupt, EOFError):
            ctx.bureau.stop()
            break

@user_agent.on_event("startup")
async def startup_and_run_main(ctx: Context):
    asyncio.create_task(user_interaction_loop(ctx))

@user_agent.on_message(model=MentorResponse)
async def on_mentor_response(ctx: Context, sender: str, msg: MentorResponse):
    ctx.logger.info(f"[Reply from {sender}]: {msg.text[:100]}...")

# --- Main Execution Block ---
if __name__ == "__main__":
    if not all([supabase, embeddings_client, llm_client]):
        print("🔥 Could not start agents. Check your .env file.")
    else:
        # --- FINAL FIX: Pass the public URL as a list to the endpoint parameter ---
        bureau = Bureau(port=PORT, endpoint=[public_url] if public_url else None)
        bureau.add(antoine_agent)
        bureau.add(user_agent)
        bureau.run()
        if public_url:
            ngrok.disconnect(public_url)
