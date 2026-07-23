# 🏗 Enterprise Agent Architecture

## Overview

Enterprise Agent is a production-inspired Agentic AI platform that combines **LangGraph**, **Hybrid RAG**, **Redis Memory**, **Qdrant**, and multiple LLM providers into a modular architecture.

The project is designed to be scalable, maintainable, and provider-independent.

---

## Architecture

```text
                 User
                  │
                  ▼
           FastAPI Backend
                  │
                  ▼
          LangGraph Workflow
      ┌───────────┼───────────┐
      ▼           ▼           ▼
  Redis      Tool Router     LLM
  Memory          │
                  ▼
         Hybrid RAG Search
          ┌──────────────┐
          ▼              ▼
      Qdrant DB      Tavily Search
```

---

## Core Components

### FastAPI

* REST API
* Request handling
* File upload
* Session management

---

### LangGraph

Responsible for:

* Workflow orchestration
* Agent execution
* Tool routing
* State management

---

### Hybrid RAG

Combines:

* Vector Search (Qdrant)
* Semantic Embeddings (Cohere)
* Retrieved document context

---

### Redis

Stores:

* Conversation history
* Session memory
* Short-term context

---

### Qdrant

Stores:

* Document embeddings
* Metadata
* PDF chunks

---

### LLM Layer

Current supported providers:

* Groq
* OpenAI
* Anthropic
* Ollama

---

## Data Flow

```text
User Query
     │
     ▼
LangGraph
     │
     ▼
Retrieve Context
     │
     ▼
Qdrant + Redis
     │
     ▼
LLM
     │
     ▼
Final Response
```

---

## Project Goals

* Modular architecture
* Easy provider switching
* Production-ready design
* Enterprise AI workflows
* Extensible tool ecosystem
