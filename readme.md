Antoine - The Ultimate Hackathon Mentor
Antoine is a prototype for a trustworthy, verifiable AI agent designed to accelerate developer innovation. It provides deep, non-obvious insights into the web3 ecosystem by learning from the entire history of past hackathon projects.

Our mission is to help builders break out of the "beginner loop" and to provide a blueprint for building AI systems that you don't have to blindly trust, because you can verify their work on-chain.

The Problem
This project solves two fundamental problems in the hackathon ecosystem:

For Builders: It tackles information overload and the lack of historical context. By providing intelligent, searchable access to past projects, it helps builders stand on the shoulders of giants, avoid reinventing the wheel, and create more sophisticated solutions.

For Sponsors & The Ecosystem: It addresses the "AI trust deficit" and low project ROI. Our architecture provides a model for verifiable AI, ensuring higher quality insights and helping to foster projects with a greater potential for long-term success.

Core Architecture & Current Status
The MVP of Antoine is a fully functional, local application that proves our core concept.

Agent Logic (ASI): The core agent is built using the Artificial Superintelligence Alliance (ASI) uagents framework. It is successfully registered and discoverable on the ASI testnet Almanac.

Data Foundation (Supabase): We have manually curated a high-quality dataset of 33 projects from ETHGlobal Prague. This data has been processed, vectorized, and stored in a Supabase Postgres database, which acts as the agent's "long-term memory."

Live Demo: The agent can be run locally via the guide.py script, allowing users to ask complex questions and receive insightful answers in the terminal.

Frontend Assets: The project includes a polished demo.html for video presentations and a landing.html with a live Supabase email capture form to build a community waitlist.

How to Run & Engage with the Project
There are two main components to this project: the functional Backend Agent and the Frontend UIs.

1. Running the Backend Agent
The backend is a Python script that runs our AI agent. It will listen for questions and print its answers directly in the terminal.

Activate Environment: Make sure you are in the ultimate-mentor directory and your virtual environment is active:

source venv/bin/activate

Check Configuration: Ensure your .env file is populated with your SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY, and NGROK_AUTH_TOKEN.

Run the Agent:

python guide.py

Interact: The terminal will display a Your question: prompt. You can now ask the agent questions about the projects in the database (e.g., "What projects used ZK-proofs?").

2. Engaging with the Frontend
We have created two separate HTML files located in the frontend/ directory. You can open these directly in your browser.

frontend/demo.html (The Mock Demo): This is a high-fidelity mockup with a pre-scripted conversation, perfect for video presentations.

frontend/landing.html (The Landing Page): This is a live landing page that captures emails and saves them to our Supabase database.

Project Roadmap & Future Features
This MVP is the foundation for a much larger vision. Our roadmap is focused on building out the "trust stack" and enhancing the agent's intelligence.

Expand the Knowledge Base:

Index More Projects: Systematically scrape and process project data from all recent ETHGlobal hackathons to give Antoine a comprehensive memory of the ecosystem.

Index Prize Data: Create a separate data pipeline and database table for all sponsor prizes. This will allow Antoine to answer questions like, "What were the most valuable bounties for DeFi projects at ETHGlobal London?" and to find synergies between prizes and projects.

Finalize The Graph Integration:

Deploy our existing subgraph scaffold to The Graph's hosted service.

Modify Antoine to query this public GraphQL endpoint. This is a critical step that makes our agent's knowledge base fully transparent and verifiable by anyone, solidifying our "AI Trust" narrative.

Deploy Live Frontend:

Build a simple API wrapper (e.g., using FastAPI) around our Python agent.

Connect the frontend/index.html UI to this API, creating a fully interactive web experience for users.

Integrate Oasis for Secure & Private Compute:

Containerize Antoine with Docker.

Deploy the agent as a ROFL instance on the Oasis Sapphire testnet. This will ensure that all user queries and the agent's internal "thought processes" are completely confidential and tamper-proof.

Add Hedera for an Immutable Audit Trail:

Integrate the Hedera Consensus Service (HCS) to create a public, timestamped log of Antoine's most important actions (e.g., "New data source added," "Query received," "Answer provided"). This provides the final layer of trust: a complete, unchangeable audit trail of the agent's behavior.