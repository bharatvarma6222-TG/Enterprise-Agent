# 🌐 API Reference

Enterprise Agent exposes REST APIs using **FastAPI**.

Interactive documentation is automatically available through Swagger.

---

## Base URL

Local

```text
http://localhost:8000
```

Production

```text
https://your-backend-domain
```

---

## Swagger Documentation

FastAPI automatically generates API documentation.

```text
GET /docs
```

---

## Available Endpoints

### Health Check

Returns the current application status.

```http
GET /health
```

Example Response

```json
{
  "status": "healthy"
}
```

---

### Chat

Generates an AI response using the LangGraph workflow.

```http
POST /chat
```

Request

```json
{
  "message": "Explain Retrieval-Augmented Generation.",
  "session_id": "user-123"
}
```

Response

```json
{
  "response": "..."
}
```

---

### Upload PDF

Uploads a PDF and indexes it into the vector database.

```http
POST /upload
```

Request

```text
multipart/form-data
```

Fields

| Name | Type |
| ---- | ---- |
| file | PDF  |

Response

```json
{
  "message": "PDF indexed successfully."
}
```

---

## Response Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 400  | Invalid Request       |
| 404  | Resource Not Found    |
| 500  | Internal Server Error |

---

## Authentication

Current version:

* No authentication

Planned:

* JWT Authentication
* API Keys
* OAuth2

---

## Future Endpoints

Planned additions:

* Conversation History
* Delete Session
* Document Management
* User Profile
* Admin Dashboard
* Analytics
