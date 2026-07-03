from langchain_huggingface import HuggingFaceInferenceAPIEmbeddings
from app.core.config import settings

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=settings.HF_TOKEN,
    model_name="BAAI/bge-small-en-v1.5",
)

print("Embeddings initialized")
