## 🚀Fintech-Risk-Platform
A FastAPI backend for the Fintech Risk Intelligence Platform. Uses the Anthropic Claude API, RAG pipelines, and real market data via yfinance to calculate portfolio risk metrics, analyse company filings, and generate plain-English risk briefs. Built and deployed from scratch.

### 🔗 Live demo: https://fintech-risk-intelligence-platform-george.vercel.app 

⚠️ Warning the site is slow on first opening due to the container. You will need to wait 30-60 seconds for it to warm up after the first API call.

### 📦 Frontend repo: https://github.com/GeorgeSinfield/fintech-frontend/tree/main

## 🛠️Technologies
- Python, FastAPI, uvicorn
- Anthropic Claude API
- ChromaDB
- sentence-transformers (all-MiniLM-L6-v2)
- yfinance, pandas, numpy
- pypdf
- Docker, Azure Container Apps

## ✨Features
- Four REST endpoints:
   - 📊/risk-brief, gets all the risk data and creates a summary with highlighted risk factors on a users portfolio.
   - 📄/upload-10k, lets users upload a pdf file and get a detailed summary.
   - 🔍/search-ticker, an auto complete allowing users to enter a company name and get its relating ticker.
   - 💬/ask, allows users to ask questions to a bot with prebuilt context.
- RAG pipeline - A pipeline that takes a pdf, reads it, chunks it, embeds it, and keeps it in vector storage.
- Agent News Monitoring - A built in news agent that gets the latest information of a company and feeds this information back creating a more relevant summary of a company.
- Quantitative risk metrics - A quantitative engine that calculates the VaR, volatility, correlation and drawdown of the users portfolio.
- Persistent ChromaDB vector storage - So the user can use one feature, leave and come back without having to re-enter any data.

## 🔄The process
The whole process of making the backend was split into 3 phases.
#### 🏗️Phase 1 
  - I started by building the RAG pipeline first before anything else. The idea was to get the AI working on real financial documents before worrying about APIs or frontends. I loaded PDFs using pypdf, split them into chunks, embedded each chunk using sentence-transformers, and stored everything in ChromaDB. Once I could search a 10-K by meaning rather than keywords I built the ask() function on top of that, then extract_risk_categories() which calls ask() five times for each risk type and returns structured JSON.
#### ⚙️Phase 2
  - Phase 2 was the portfolio risk engine. I built this completely separately from the AI layer first. I wrote each function individually: returns, volatility, correlation, VaR, max drawdown, all in plain pandas and numpy with no LLM involved. Getting the maths right before adding AI meant I could trust the numbers the brief was actually talking about. The news agent came next, which was the first time I used tool use. The LLM decides when to call get_news() and reasons over the results rather than just answering a question. Then generate_risk_brief() tied everything together, feeding the quant metrics, news analysis, and filing risk factors into one prompt and getting back a 4-paragraph brief.
#### 🚢Phase 3
  - Phase 3 was turning the scripts into a real service. I wrapped everything in FastAPI which was straightforward once I understood that endpoints are just functions with a decorator. The trickier part was fixing the three blockers that would have broken FastAPI imports. Switching ChromaDB to a persistent client, adding if name guards to stop code running on import, and making the collection names dynamic so any PDF could be processed, not just the test one. Then Docker and Azure. Writing the Dockerfile was simpler than I expected, the harder part was setting up the Azure Container Registry and Container Apps for the first time and debugging the CORS issues between the deployed frontend and backend.

## 📚What I learned 
During this project I've learnt skills and better understandings of complex ideas, which have improved my logical thinking.
### 🧠RAG
  - Before this project I had heard of RAG but never implemented it. I now understand how embeddings turn text into vectors that capture meaning rather than just keywords, why chunking matters for staying within model context limits, and how cosine similarity is used to find the most relevant chunks for a given query. Building this on a real 200-page financial document made the tradeoffs concrete in a way that reading about it wouldn't have.
### 🤖Agentic AI
  - I learnt how tool use works at the code level. The LLM doesn't run Python it decides when to request a tool call, your code intercepts that, runs the actual function, and sends the result back. Understanding this loop made it clear why agents are more powerful than simple prompt-response patterns, and also where they can go wrong.
### 🐳Docker
  - This was my first time fully deploying a project. I learnt how to write a Dockerfile, and how to connect a containerised backend to a separately deployed frontend. The CORS debugging was also a practical lesson in how browsers enforce security between different origins.
### 🌐CORS
  - I learnt why browsers block cross-origin requests by default and how servers signal permission using response headers. Debugging this between the Azure backend and Vercel frontend made the concept concrete rather than theoretical.

## 📈Overall growth
Overall I have learnt a lot. Practically I have learnt about building and deploying a full AI-powered service. I have also gained more experience with Git, creating a project from scratch to a finished product and using RAG, APIs and agents.

## 🔧How can it be improved?
- Cold start latency on Azure free tier
- ChromaDB resets on container restart (no persistent volume mounted)
- No authentication on the API
- News agent makes sequential calls (slow for large portfolios)
- Could add proper eval framework for the RAG pipeline

## ▶️How to run the project?
1. Clone the repo
2. Create a .env file with ANTHROPIC_API_KEY=your_key
3. pip install -r requirements.txt
4. uvicorn main:app --reload

## Video

In progress...
