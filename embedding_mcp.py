### Min
### Embedding MCP Tool
### Provides text embedding and vector search functionality for MCP server

from typing import Dict, Any, List
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class EmbeddingTool:
    name: str = "embedding"

    inputSchema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "texts": {"type": "array", "items": {"type": "string"}, "description": "List of texts to vectorize"},
            "model_name": {"type": "string", "default": "all-MiniLM-L6-v2", "description": "Model name to use"},
            "cache_folder": {"type": "string", "default": "./models", "description": "Model cache folder"},
            "operation": {"type": "string", "enum": ["embed", "create_index", "search"], "description": "Operation type"}
        },
        "required": ["texts", "operation"]
    }

    functions: List[str] = ["embed_texts", "create_vector_index", "search_similar"]

    def __init__(self):
        self.model = None
        self.index = None
        self.texts = []

    def embed_texts(self, texts: List[str], model_name: str = "all-MiniLM-L6-v2", cache_folder: str = "./models") -> Dict[str, Any]:
        ### Vectorize a list of texts
        try:
            if self.model is None or model_name != getattr(self.model, 'model_name', None):
                self.model = SentenceTransformer(
                    model_name,
                    cache_folder=cache_folder,
                    use_auth_token=False
                )
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return {
                "success": True,
                "embeddings": embeddings.tolist(),
                "embedding_dim": embeddings.shape[1],
                "num_texts": len(texts),
                "model_name": model_name
            }
        except Exception as e:
            return {"error": f"Failed to embed texts: {str(e)}"}

    def create_vector_index(self, texts: List[str], model_name: str = "all-MiniLM-L6-v2", cache_folder: str = "./models") -> Dict[str, Any]:
        ### Create vector index for a list of texts
        try:
            embed_result = self.embed_texts(texts, model_name, cache_folder)
            if not embed_result.get("success"):
                return embed_result
            embeddings = np.array(embed_result["embeddings"])
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(embeddings.astype(np.float32))
            self.texts = texts
            return {
                "success": True,
                "index_created": True,
                "num_vectors": len(texts),
                "embedding_dim": embeddings.shape[1],
                "model_name": model_name
            }
        except Exception as e:
            return {"error": f"Failed to create vector index: {str(e)}"}

    def search_similar(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        ### Search for similar texts in the index
        try:
            if self.index is None or self.model is None:
                return {"error": "No index or model available. Please create index first."}
            query_embedding = self.model.encode([query], convert_to_numpy=True)
            distances, indices = self.index.search(query_embedding.astype(np.float32), top_k)
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx != -1:
                    results.append({
                        "rank": i + 1,
                        "text": self.texts[idx],
                        "distance": float(distance),
                        "index": int(idx)
                    })
            return {
                "success": True,
                "query": query,
                "top_k": top_k,
                "results": results
            }
        except Exception as e:
            return {"error": f"Failed to search: {str(e)}"}
### #%#