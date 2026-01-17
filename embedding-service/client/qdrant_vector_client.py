import logging

from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    Distance,
    VectorParams
)


logger = logging.getLogger(__name__)


class QdrantVectorClient:

    def __init__(self, url: str):
        logger.info(f"Initializing QdrantVectorClient with URL: {url}")
        self.client = QdrantClient(url=url)
        logger.debug("QdrantVectorClient initialized successfully")


    def create_collection(
        self,
        collection_name: str,
        vector_size: int
    ):
        logger.info(f"Creating collection '{collection_name}' with vector size {vector_size}")
        client: QdrantClient = self.client
        try:
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                ),
            )
            logger.info(f"Collection '{collection_name}' created successfully")
        except Exception as e:
            logger.error(f"Failed to create collection '{collection_name}': {e}")
            raise Exception(f"Failed to create collection: {e}")


    def upsert(
        self,
        collection_name: str,
        points: List[PointStruct]
    ):
        logger.debug(f"Upserting {len(points)} points to collection '{collection_name}'")
        client: QdrantClient = self.client
        try:
            client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.debug(f"Successfully upserted {len(points)} points to collection '{collection_name}'")
        except Exception as e:
            logger.error(f"Failed to upsert points to collection '{collection_name}': {e}")
            raise


    def collection_exists(self, collection_name: str) -> bool:
        try:
            self.client.get_collection(collection_name=collection_name)
            logger.debug(f"Collection '{collection_name}' exists")
            return True
        except Exception:
            logger.debug(f"Collection '{collection_name}' does not exist")
            return False


    def search(
        self,
        collection_name: str,
        query_vector: List[float],
        top_k: int
    ) -> List[Dict[str, Any]]:
        logger.debug(f"Searching collection '{collection_name}' with top_k={top_k}")
        client: QdrantClient = self.client
        try:
            hits = client.search(
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
            logger.debug(f"Search returned {len(results)} results from collection '{collection_name}'")
            return results
        except Exception as e:
            logger.error(f"Search failed on collection '{collection_name}': {e}")
            raise
