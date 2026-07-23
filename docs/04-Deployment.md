# 🚀 Deployment

Enterprise Agent is designed for cloud deployment using modern managed services.

---

## Deployment Stack

| Component       | Platform      |
| --------------- | ------------- |
| Backend         | Railway       |
| Frontend        | Netlify       |
| Vector Database | Qdrant Cloud  |
| Memory          | Upstash Redis |
| LLM             | Groq          |
| Embeddings      | Cohere        |
| Web Search      | Tavily        |

---

## Backend Deployment (Railway)

### 1. Push your code

```bash id="b8p1zn"
git add .

git commit -m "Deploy"

git push
```

---

### 2. Create Railway Project

* Login to Railway
* Create a new project
* Deploy from GitHub
* Select your repository

---

### 3. Configure Service

Root Directory

```text id="j2lxv8"
backend
```

Start Command

```text id="tndkqt"
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### 4. Add Environment Variables

Configure the following variables in Railway:

```text id="0lly6j"
GROQ_API_KEY
COHERE_API_KEY
TAVILY_API_KEY
QDRANT_URL
QDRANT_API_KEY
REDIS_URL
```

---

### 5. Generate Public Domain

Navigate to:

```text id="a9o6v3"
Settings
→ Networking
→ Generate Domain
```

Your backend will be available at:

```text id="n6p8g7"
https://your-app.up.railway.app
```

---

## Frontend Deployment (Netlify)

* Connect your GitHub repository
* Select the frontend project
* Deploy automatically

Configure:

Build Command

```text id="2m4n0u"
npm run build
```

Publish Directory

```text id="6qg9nk"
dist
```

---

## Production Checklist

Before deployment, verify:

* ✅ Environment variables configured
* ✅ Redis connected
* ✅ Qdrant collection created
* ✅ API starts successfully
* ✅ Swagger available
* ✅ Frontend communicates with backend

---

## Updating Production

Deployments are automatic after every push.

```bash id="lp2l4o"
git add .

git commit -m "Update"

git push
```

Railway and Netlify will redeploy the latest version.

---

## Monitoring

Useful dashboards:

* Railway Logs
* Qdrant Dashboard
* Upstash Console
* Groq Console
* Cohere Dashboard

These help monitor application health and diagnose issues.

---

## Future Deployment Options

Enterprise Agent can also be deployed using:

* Docker
* Docker Compose
* Kubernetes
* Terraform
* GitHub Actions
* AWS
* Azure
* Google Cloud
