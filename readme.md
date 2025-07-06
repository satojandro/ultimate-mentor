The Ultimate Hackathon Mentor (Antoine)
The Ultimate Hackathon Mentor is a prototype for a trustworthy, verifiable AI agent designed to accelerate developer innovation. It provides deep, non-obvious insights into the web3 ecosystem by learning from the entire history of past hackathon projects.

Our mission is to help builders break out of the "beginner loop" and to provide a blueprint for building AI systems that you don't have to blindly trust, because you can verify their work on-chain.

The Problem
This project solves two fundamental problems in the hackathon ecosystem:

For Builders: It tackles information overload and the lack of historical context. By providing intelligent, searchable access to past projects, it helps builders stand on the shoulders of giants, avoid reinventing the wheel, and create more sophisticated solutions.

For Sponsors & The Ecosystem: It addresses the "AI trust deficit" and low project ROI. Our architecture provides a model for verifiable AI, ensuring higher quality insights and helping to foster projects with a greater potential for long-term success.

Core Architecture
The Mentor (codenamed Antoine) is built on a multi-layered, decentralized stack where each component provides a piece of the "trust puzzle."

Agent Logic (ASI): The core agent is built using the Artificial Superintelligence Alliance (ASI) uagents framework.

Data Foundation (Supabase): Project data is processed and stored in a Supabase Postgres database with pgvector for powerful semantic search capabilities.

Verifiable Knowledge (The Graph): (Roadmap) The agent's knowledge base will be indexed as a Subgraph on The Graph, allowing anyone to independently query and verify the data the agent is using.

Secure Compute (Oasis Protocol): (Roadmap) The agent's core logic will be deployed inside an Oasis Protocol ROFL TEE for confidentiality of user queries and agent "thoughts."

Immutable Logging (Hedera): (Roadmap) Agent actions will be logged to the Hedera Consensus Service (HCS) to create a tamper-proof audit trail.

How to Run & Engage with the Project
There are two main components to this project: the functional Backend Agent and the Frontend UIs.

1. Running the Backend Agent
The backend is a Python script that runs our AI agent. It will listen for questions and print its answers directly in the terminal.

Activate Environment: Make sure you are in the ultimate-mentor directory and your virtual environment is active:

source venv/bin/activate

Check Configuration: Ensure your .env file is populated with your SUPABASE_URL, SUPABASE_KEY, and OPENAI_API_KEY.

Run the Agent:

python guide.py

Interact: The terminal will display a Your question: prompt. You can now ask the agent questions about the projects in the database (e.g., "What projects used ZK-proofs?").

2. Engaging with the Frontend
We have created two separate HTML files located in the frontend/ directory. You can open these directly in your Brave (or any other) browser.

frontend/demo.html (The Mock Demo):

Purpose: This is a high-fidelity, polished mockup designed for video presentations.

How to use: Open the file in your browser. To start the pre-scripted conversation, simply click the "SEND" button or press Enter. The entire conversation will play out automatically.

frontend/index.html (The Live UI):

Purpose: This is the clean user interface that is ready to be connected to a live backend API in the future.

How to use: Open the file in your browser. You can type messages, but it will currently only return a placeholder response as it is not connected to our Python agent.

Project Roadmap
Our MVP has a functional local backend and two frontend assets. The next steps on our critical path are to integrate the core "trust" layers of our architecture.

[High Priority] The Graph Integration: Create a Subgraph to index our project data from the Supabase DB. Modify the Guide Agent to query this Subgraph, making its knowledge base publicly verifiable.

[Stretch Goal] Oasis TEE Deployment: Containerize the Guide Agent with Docker and deploy it as a ROFL instance on the Oasis Sapphire testnet. This will make the agent's operations confidential.

[Future] Full API & Frontend Connection: Build a simple API (e.g., using FastAPI) around our Python agent and connect it to the index.html file to create a fully interactive web experience.

[Future] Hedera Logging: Integrate the Hedera SDK to log key agent actions (queries received, data sources consulted) to the Hedera Consensus Service for a full audit trail.