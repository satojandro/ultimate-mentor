Subgraph for The Ultimate Mentor

This directory contains the subgraph for the "Ultimate Mentor" project. The purpose of this subgraph is to provide a decentralized, verifiable, and queryable data layer for our AI agent's knowledge base.

The Role of The Graph in Our Mission
Our project's core mission is to build a trustworthy AI. The Graph is the foundational component for achieving this.

By indexing our hackathon project data into a subgraph, we move it from a private, centralized database into a public, open protocol. This means:

Transparency: Anyone can see the exact data our AI agent is using to form its conclusions. There are no hidden sources.

Verifiability: The data on The Graph is immutable and content-addressed, ensuring that the information our agent relies on is accurate and has not been tampered with.

Composability: Other developers and applications can directly access and build on top of our curated dataset, fostering a more collaborative ecosystem.

This subgraph is the "proof" behind our agent's knowledge.

Current Status
The subgraph is currently configured to index data from a local JSON file (prague_projects.json). The schema and mappings are defined to structure this data into Project entities.

Next Steps
Deploy to Studio: The next step is to deploy this subgraph to The Graph's hosted Subgraph Studio. This will give us a public GraphQL API endpoint.

Integrate with Guide Agent: Modify the guide.py agent to query this public GraphQL endpoint instead of the local Supabase database. This will complete the loop and make our agent's knowledge fully verifiable.

Expand Data Sources: In the future, we can add more data sources to this subgraph, including prize information and data from other hackathons, to enrich the agent's knowledge base.