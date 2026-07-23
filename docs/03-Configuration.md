# 🔑 Configuration

Enterprise Agent uses environment variables to securely manage API keys and external services.

---

## Environment Variables

Create a `.env` file inside the `backend/` directory.

```env
GROQ_API_KEY=

COHERE_API_KEY=

TAVILY_API_KEY=

QDRANT_URL=
QDRANT_API_KEY=

REDIS_URL=
```

---

## Service Configuration

### Groq

Used for:

* Chat completion
* Agent reasoning
* Response generation

Get your API key from:

```text
https://console.groq.com/
```

---

### Cohere

Used for:

* Document embeddings
* Semantic vector generation

Current model:

```text
embed-english-v3.0
```

Embedding dimension:

```text
1024
```

Get your API key:

```text
https://dashboard.cohere.com/
```

---

### Tavily

Used for:

* Web search
* External knowledge retrieval

Dashboard:

```text
https://tavily.com/
```

---

### Qdrant

Stores:

* Document embeddings
* PDF chunks
* Metadata

Required variables:

```text
QDRANT_URL
QDRANT_API_KEY
```

Dashboard:

```text
https://cloud.qdrant.io/
```

---

### Redis

Stores:

* Conversation history
* Session memory

Example URL:

```text
rediss://default:<password>@xxxx.upstash.io:6379
```

---

## Security

Never commit:

* `.env`
* API Keys
* Tokens
* Secrets

Ensure your `.gitignore` contains:

```gitignore
.env
*.env
```

---

## Production

For Railway deployment, configure all variables in:

```text
Railway
→ Variables
```

Do **not** upload your local `.env` file.

---

## Verify Configuration

Run:

```bash
uvicorn app.main:app --reload
```

Successful startup should initialize:

* ✅ Groq
* ✅ Cohere
* ✅ Qdrant
* ✅ Redis
* ✅ Tavily

---

## Common Issues

| Issue           | Solution                                |
| --------------- | --------------------------------------- |
| Missing API Key | Check `.env` values                     |
| Redis Error     | Verify `REDIS_URL`                      |
| Qdrant Error    | Check `QDRANT_URL` and `QDRANT_API_KEY` |
| Embedding Error | Verify `COHERE_API_KEY`                 |
| LLM Error       | Verify `GROQ_API_KEY`                   |
