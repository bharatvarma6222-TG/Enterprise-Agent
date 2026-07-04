from langchain_cohere import CohereEmbeddings
from app.core.config import settings

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=settings.COHERE_API_KEY,
    embedding_types=["float"],
    input_type="search_document",
    output_dimension=1024,
)

print("Cohere embeddings initialized.")
