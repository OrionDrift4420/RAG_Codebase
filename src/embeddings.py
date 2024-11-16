from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import torch


class CodeEmbedder:
    """Generate embeddings for code snippets and documentation."""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize with a local embedding model."""
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> torch.Tensor:
        """Generate embeddings for a list of text snippets."""
        return self.model.encode(texts, convert_to_tensor=True)

    def process_code_data(self, parsed_data: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """Process parsed code data and generate embeddings."""
        embeddings = {}

        for file_data in parsed_data:
            # Generate embeddings for functions
            for func in file_data['functions']:
                key = f"function:{file_data['path']}:{func['name']}"
                text = f"{func['name']} {func['docstring'] or ''}"
                embeddings[key] = self.generate_embeddings([text])[0]

            # Generate embeddings for classes
            for class_ in file_data['classes']:
                key = f"class:{file_data['path']}:{class_['name']}"
                text = f"{class_['name']} {class_['docstring'] or ''}"
                embeddings[key] = self.generate_embeddings([text])[0]

        return embeddings