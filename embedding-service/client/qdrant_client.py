from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams
)


class QdrantVectorClient:

    def __init__(self, url: str):        
        self.client = QdrantClient(url=url)
        self.url = url


    def create_collection(
        self,
        collection_name: str,
        vector_size: int
    ):
        try:
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                ),
            )
        except Exception as e:
            raise Exception(f"Failed to create collection: {e}")


    def upsert(
        self,
        collection_name: str,
        points: List[PointStruct]
    ):       
        self.client.upsert(
            collection_name=collection_name,
            points=points
        )


    def collection_exists(self, collection_name: str) -> bool:
        try:
            self.client.get_collection(collection_name=collection_name)
            return True
        except Exception:
            return False


    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int
    ) -> List[Dict[str, Any]]:       
        hits = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        results = [
            {
                "id": h.id,
                "score": h.score,
                "metadata": h.payload
            } for h in hits
        ]
        return results
