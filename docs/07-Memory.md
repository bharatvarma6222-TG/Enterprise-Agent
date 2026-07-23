# 🔄 LangGraph Workflow

Enterprise Agent uses **LangGraph** as its orchestration engine to coordinate reasoning, memory, retrieval, and tool execution.

Unlike a traditional chatbot, the workflow is represented as a directed graph where each node performs a specific task.

---

# Workflow Overview

```text
               User Query
                    │
                    ▼
             Input Validation
                    │
                    ▼
             Load Chat Memory
                    │
                    ▼
             Query Planner
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
  PDF Retrieval            Web Search
        │                       │
        └───────────┬───────────┘
                    ▼
            Context Builder
                    │
                    ▼
              LLM Generation
                    │
                    ▼
             Store Memory
                    │
                    ▼
             Return Response
```

---

# Workflow Nodes

## Input Validation

Responsible for:

* Validating user requests
* Sanitizing input
* Initial preprocessing

---

## Memory Node

Loads previous conversation history from Redis.

Purpose:

* Maintain context
* Support multi-turn conversations
* Improve response consistency

---

## Planner Node

Determines how the request should be handled.

Possible actions:

* Use document retrieval
* Perform web search
* Generate directly using the LLM

---

## Retrieval Node

Searches uploaded documents stored in Qdrant.

Returns:

* Relevant document chunks
* Associated metadata

---

## Web Search Node

Uses Tavily Search when external knowledge is required.

Typical use cases:

* Current events
* Recent technologies
* Information outside uploaded documents

---

## Context Builder

Combines:

* User query
* Retrieved document context
* Conversation history
* Web search results (if available)

The resulting prompt is passed to the language model.

---

## LLM Node

Generates the final response using the selected provider.

Current providers include:

* Groq
* OpenAI
* Anthropic
* Ollama

---

## Memory Update

After generating the response:

* User message is stored
* Assistant response is stored
* Redis session is updated

---

# State Flow

The workflow maintains state throughout execution.

```text
User Query
      │
      ▼
Current State
      │
      ▼
Memory
      │
      ▼
Retrieved Context
      │
      ▼
Generated Response
```

Each node receives the current state and returns an updated version.

---

# Benefits of LangGraph

* Stateful execution
* Modular workflows
* Easy tool integration
* Scalable architecture
* Clear execution flow
* Extensible graph design

---

# Future Enhancements

Planned workflow improvements:

* Multi-agent collaboration
* Reflection/Critic agent
* Planning agent
* Human-in-the-loop approval
* Parallel tool execution
* MCP integration
* Streaming responses

---

# Summary

LangGraph enables Enterprise Agent to move beyond simple prompt-response interactions by orchestrating memory, retrieval, external tools, and language models within a structured execution graph.
