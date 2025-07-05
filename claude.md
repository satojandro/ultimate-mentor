│ > Never include code attributions to Claude when doing git commits    │

Project Briefing: The Ultimate Hackathon Mentor
To: Claude Code Assistant
From: Alejandro & Nova
RE: Project Onboarding for ETH Global Cannes Hackathon

1. High-Level Vision & Mission
We are building a prototype for the "Ultimate Hackathon Mentor," an AI agent designed to accelerate developer innovation by providing trustworthy, verifiable answers about the web3 ecosystem.

Our core mission is twofold:

For Builders: To create a tool that helps them break out of "beginner mode." By learning from the entire history of past hackathon projects, builders can stand on the shoulders of giants, avoid reinventing the wheel, and create more sophisticated and impactful solutions.

For the Ecosystem: To solve the "black box" problem of AI and increase sponsor ROI. By building a blueprint for trustworthy, autonomous AI systems on-chain, we provide a model for verifiable intelligence and ensure that sponsor capital is directed towards projects with higher potential, ultimately moving the entire ecosystem forward.

The key is that the agent's knowledge, "thoughts," and actions can be independently verified by any user.

2. The Core Problem
This project addresses fundamental pain points for both builders and sponsors:

For Builders (The "Beginner Loop"):

Information Overload: It's difficult to parse the vast amount of information from dozens of sponsor bounties and documentation.

Lack of Historical Context: It's hard to learn from what has already been built, leading to redundant, entry-level submissions.

AI Trust Deficit: Standard AI chatbots are helpful but operate as black boxes. You can't verify their sources or trust their strategic advice.

For Sponsors (The ROI Problem):

High Cost, Low Signal: Sponsorship is expensive, and it's difficult to gauge the quality and potential of submissions until the very end.

Low Project Continuation: Many hackathon projects are abandoned immediately after the event, representing a low return on investment for the ecosystem.

3. The Winning Architecture & Tech Stack
Our solution is a multi-layered AI system where each component provides a piece of the "trust puzzle."

Agent Logic (ASI): The core agent is built using the Artificial Superintelligence Alliance (ASI) uAgent framework.

Secure Compute (Oasis Protocol): The agent's logic will be deployed inside an Oasis Protocol ROFL TEE for confidentiality.

Verifiable Knowledge (The Graph): The agent's knowledge base is indexed as a Subgraph on The Graph.

Immutable Logging (Hedera): Agent actions are logged to the Hedera Consensus Service (HCS).

Data Pipeline:

Scraping (Firecrawl): We use firecrawl to scrape raw data.

Vector Database (Supabase): We use Supabase for vector embeddings and semantic search.

4. Project Roadmap (Phased Implementation)
We are executing this in three main phases:

Phase 1: Setup & Data Pipeline (IN PROGRESS)

Task 1: Environment Setup (COMPLETE)

Task 2: Data Scraping (The Scribe) (COMPLETE)

Task 3: Data Cleaning & Structuring (The Librarian): Parse raw markdown from past project showcases, generate embeddings, and load into Supabase and The Graph.

Phase 2: Core Agent Logic

Task 4: Build The Guide Agent (ASI): Create the main uAgent to answer questions by querying the Supabase vector DB.

Task 5: Integrate The Graph: Enhance the agent to pull structured metadata from our Subgraph.

Phase 3: Advanced Integrations & Deployment

Task 6: Deploy Agent to Oasis TEE

Task 7: Add Hedera Logging

Task 8: Final Polish & Demo

5. Current Status
We have just successfully completed Task 2. Our next immediate step is to begin Task 3: writing the librarian.py script to process data from past hackathon project showcases.