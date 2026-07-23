# 📁 Project Structure

Enterprise Agent follows a modular architecture where each directory has a single responsibility.

---

## Directory Layout

```text
enterprise-agent/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── cache/
│   │   ├── core/
│   │   ├── graph/
│   │   ├── ingestion/
│   │   ├── llm/
│   │   ├── memory/
│   │   ├── retrieval/
│   │   ├── tools/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── testing/
│   ├── requirements.txt
│   └── reset_collection.py
│
├── frontend/
│
├── docs/
│
└── README.md
```

---

## Backend Modules

### api/

Contains all FastAPI routes and request handlers.

Examples:

* Chat endpoint
* PDF upload
* Health check

---

### cache/

Responsible for Redis integration and caching.

---

### core/

Application configuration and shared settings.

Examples:

* Environment variables
* Configuration management

---

### graph/

Contains the LangGraph workflow responsible for orchestrating the AI agent.

---

### ingestion/

Handles document processing.

Responsibilities:

* PDF loading
* Text extraction
* Chunk generation

---

### llm/

Contains language model integrations.

Supported providers include:

* Groq
* OpenAI
* Anthropic
* Ollama

---

### memory/

Manages conversation history using Redis.

---

### retrieval/

Responsible for:

* Embeddings
* Vector search
* Qdrant integration

---

### tools/

Contains tools that the agent can invoke.

Examples:

* PDF Search
* Web Search

---

### utils/

Shared helper functions used across the project.

---

## Frontend

Contains the web interface for interacting with Enterprise Agent.

---

## docs/

Project documentation including:

* Architecture
* Installation
* Configuration
* Deployment
* RAG Pipeline
* Memory
* LangGraph Workflow

---

## Design Principles

The project is organized around:

* Separation of concerns
* Modular components
* Easy extensibility
* Production-ready structure
* Maintainable codebase
