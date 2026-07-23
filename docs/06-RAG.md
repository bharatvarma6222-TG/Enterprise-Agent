# 🧠 Memory System

Enterprise Agent maintains conversation context using **Redis**, allowing the agent to remember previous interactions within a session.

---

## Overview

The memory layer enables:

* Multi-turn conversations
* Context-aware responses
* Session persistence
* Improved reasoning across messages

Current memory implementation:

```text id="u8o1t6"
Redis (Upstash)
```

---

## Memory Flow

```text id="x6srlh"
User Message
      │
      ▼
Redis Lookup
      │
      ▼
Previous Messages
      │
      ▼
LangGraph State
      │
      ▼
LLM
      │
      ▼
Assistant Response
      │
      ▼
Save Back to Redis
```

---

## Stored Information

Each session stores:

* User messages
* Assistant responses
* Conversation history
* Session identifier

This allows the agent to continue conversations naturally.

---

## Session Management

Every conversation is identified by a unique session ID.

Example:

```text id="8ezv1j"
session_id

↓

Conversation History

↓

Redis
```

Different users have isolated conversation histories.

---

## Redis Responsibilities

Redis is responsible for:

* Fast reads and writes
* Temporary conversation memory
* Session persistence
* Low-latency access

---

## Current Architecture

```text id="c6h1v7"
User
 │
 ▼
FastAPI
 │
 ▼
Redis Memory
 │
 ▼
LangGraph
 │
 ▼
LLM
```

---

## Why Redis?

Redis was selected because it provides:

* In-memory performance
* Simple key-value storage
* Excellent scalability
* Cloud-hosted deployment through Upstash

---

## Future Enhancements

Planned memory improvements include:

* Long-term memory
* User profiles
* Conversation summarization
* Semantic memory retrieval
* Memory expiration policies
* Knowledge graph integration

---

## Current Stack

| Component        | Technology |
| ---------------- | ---------- |
| Memory Store     | Redis      |
| Provider         | Upstash    |
| Framework        | LangGraph  |
| Session Handling | FastAPI    |

---

## Benefits

* Context-aware conversations
* Faster responses
* Persistent chat sessions
* Modular memory architecture
* Ready for long-term memory expansion
