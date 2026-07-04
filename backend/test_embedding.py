from langchain_cohere import CohereEmbeddings
from app.core.config import settings

emb = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=settings.COHERE_API_KEY,
)

vec = emb.embed_query("hello")

print(len(vec))
