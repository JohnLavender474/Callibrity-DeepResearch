import uuid
from typing import List

from fastapi import APIRouter, Request, HTTPException

from qdrant_client.models import PointStruct

from model.document_insertion import DocumentInsertion
from model.search_query import SearchQuery


router = APIRouter(prefix="/api/embedding", tags=["embedding"])


@router.post("/collections/{collection_name}")
async def create_collection(collection_name: str, request: Request):
    embedding_service = request.app.state.embedding_service
    vector_client = request.app.state.vector_client
    
    if vector_client.collection_exists(collection_name):
        raise HTTPException(
            status_code=409,
            detail=f"Collection '{collection_name}' already exists"
        )
    
    vector_size = embedding_service.get_dimension()
    vector_client.create_collection(collection_name, vector_size)
    
    return {
        "status": "ok",
        "collection": collection_name,
        "vector_size": vector_size
    }


@router.post("/collections/{collection_name}/embed")
async def embed(
    collection_name: str,
    page: DocumentInsertion,
    request: Request
):
    embedding_service = request.app.state.embedding_service
    vector_client = request.app.state.vector_client
    
    if not vector_client.collection_exists(collection_name):
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' does not exist"
        )
    
    vector = embedding_service.embed(page.content)
    
    point_id = str(uuid.uuid4())
    point = PointStruct(
        id=point_id,
        vector=vector,
        payload=page.metadata
    )
    
    vector_client.upsert(collection_name, [point])
    
    return {"status": "ok", "id": point_id}


@router.post("/collections/{collection_name}/embed_batch")
async def embed_batch(
    collection_name: str,
    pages: List[DocumentInsertion],
    request: Request
):
    embedding_service = request.app.state.embedding_service
    vector_client = request.app.state.vector_client
    
    if not vector_client.collection_exists(collection_name):
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' does not exist"
        )
    
    points = []
    for page in pages:
        vector = embedding_service.embed(page.content)
        point_id = str(uuid.uuid4())
        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload=page.metadata
            )
        )
    
    batch_size = 64
    for i in range(0, len(points), batch_size):
        vector_client.upsert(collection_name, points[i : i + batch_size])
    
    return {"status": "ok", "indexed": len(points)}


@router.post("/collections/{collection_name}/search")
async def search(
    collection_name: str,
    query: SearchQuery,
    request: Request
):
    embedding_service = request.app.state.embedding_service
    vector_client = request.app.state.vector_client
    
    if not vector_client.collection_exists(collection_name):
        raise HTTPException(
            status_code=404,
            detail=f"Collection '{collection_name}' does not exist"
        )
    
    query_vector = embedding_service.embed(query.query)
    
    results = vector_client.search(
        collection_name,
        query_vector,
        top_k=query.top_k
    )
    
    return {"results": results}
