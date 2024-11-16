import chromadb
from chromadb.config import Settings
from typing import Dict, List, Any
import numpy as np


class VectorStore:
    """Store and query code embeddings using ChromaDB."""

    def __init__(self, persist_directory: str = "data/chroma"):
        """Initialize ChromaDB with local persistence."""
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            is_persistent=True
        ))
        self.collection = self.client.get_or_create_collection("code_embeddings")

    def add_embeddings(self, embeddings: Dict[str, np.ndarray], metadata: Dict[str, Any]):
        """Add embeddings and metadata to the vector store."""
        documents = []
        ids = []
        embeddings_list = []
        metadata_list = []

        for key, embedding in embeddings.items():
            documents.append(key)
            ids.append(key)
            embeddings_list.append(embedding.numpy())
            metadata_list.append(metadata.get(key, {}))

        self.collection.add(
            documents=documents,
            ids=ids,
            embeddings=embeddings_list,
            metadatas=metadata_list
        )

    def query(self, query_embedding: np.ndarray, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store for similar code snippets."""
        results = self.collection.query(
            query_embeddings=[query_embedding.numpy()],
            n_results=n_results
        )
        return results