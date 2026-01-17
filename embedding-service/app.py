from fastapi import FastAPI

from service.embedding_service import EmbeddingService
from client.qdrant_client import QdrantVectorClient
from router import embedding_router
from config.vars import QDRANT_URL, SENTENCE_TRANSFORMER_MODEL


app = FastAPI(title="Deep Research Embedding Service")

embedding_service = EmbeddingService(SENTENCE_TRANSFORMER_MODEL)
vector_client = QdrantVectorClient(url=QDRANT_URL)

app.state.embedding_service = embedding_service
app.state.vector_client = vector_client

app.include_router(embedding_router.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
