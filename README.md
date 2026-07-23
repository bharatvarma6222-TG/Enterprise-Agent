# 🤖 Enterprise Agent


**Enterprise-grade Agentic AI Platform powered by LangGraph, Hybrid RAG, Redis Memory, Qdrant, and FastAPI.**

# ✨ Highlights

* 🤖 Multi-LLM Support (Groq • OpenAI • Anthropic • Ollama)
* 📄 Intelligent PDF Knowledge Base
* 🔍 Hybrid Retrieval-Augmented Generation (RAG)
* 🧠 Redis Conversation Memory
* 🌐 Tavily Web Search
* 📦 Qdrant Vector Database
* ⚡ LangGraph Agent Workflow
* 🚀 FastAPI REST Backend
* ☁️ Cloud Deployment Ready

---

# 🏗 Architecture

```text
             User
               │
               ▼
        FastAPI Backend
               │
               ▼
       LangGraph Workflow
     ┌─────────┼─────────┐
     ▼         ▼         ▼
  Memory     Tools      LLM
     │         │
     ▼         ▼
 Redis    Qdrant + Tavily
```

---

# 🛠 Tech Stack

| Category        | Technologies                    |
| --------------- | ------------------------------- |
| 🐍 Backend      | FastAPI, Python                 |
| 🤖 AI Framework | LangGraph, LangChain            |
| 🧠 LLMs         | Groq, OpenAI, Anthropic, Ollama |
| 📦 Vector DB    | Qdrant                          |
| 🔤 Embeddings   | Cohere                          |
| 💾 Memory       | Redis (Upstash)                 |
| 🌍 Search       | Tavily                          |
| ☁️ Deployment   | Railway (Planned)               |

---

# 📚 Documentation

| 📖 Guide              | 🔗 Link                         |
| --------------------- | ------------------------------- |
| 🏗 Architecture       | `docs/01-Architecture.md`       |
| ⚙️ Installation       | `docs/02-Installation.md`       |
| 🔑 Configuration      | `docs/03-Configuration.md`      |
| 🚀 Deployment         | `docs/04-Deployment.md`         |
| 📚 RAG Pipeline       | `docs/05-RAG-Pipeline.md`       |
| 🧠 Memory System      | `docs/06-Memory-System.md`      |
| 🔄 LangGraph Workflow | `docs/07-LangGraph-Workflow.md` |
| 📁 Project Structure  | `docs/08-Project-Structure.md`  |
| 🌐 API Reference      | `docs/09-API-Reference.md`      |
| 🛣 Roadmap            | `docs/10-Roadmap.md`            |

---

# 🚀 Quick Start

```bash
git clone https://github.com/<YOUR_USERNAME>/enterprise-agent.git

cd enterprise-agent

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

# 📸 Preview

> Screenshots and workflow diagrams are available in the **docs/Images/** directory.

---

# ⭐ Roadmap

* ✅ Hybrid RAG
* ✅ LangGraph Workflow
* ✅ Redis Memory
* ✅ Qdrant Integration
* ✅ Tavily Search
* 🚧 Railway Deployment
* 🚧 React Frontend
* 📅 Multi-Agent Collaboration
* 📅 Long-Term Memory
* 📅 Docker & Terraform Support

---

# 🤝 Contributing

Pull requests, feature requests, and suggestions are welcome!

See **CONTRIBUTING.md** for contribution guidelines.

---

# 📄 License

Released under the **MIT License**.
