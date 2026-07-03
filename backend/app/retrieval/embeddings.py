import os

from app.core.config import settings

from langchain_community.embeddings import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
print("Embeddings initialized")
