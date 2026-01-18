# Embedding Service

A FastAPI service for document embedding and semantic search using Sentence Transformers and Qdrant vector database.

## Running the Application

Start both Qdrant and the embedding service:

```bash
./run.sh
```

The services will be available at:
- Embedding service: http://localhost:8000
- Qdrant: http://localhost:6333

## API Usage

### Create a Collection

```bash
curl -X POST http://localhost:8000/api/embedding/collections/my-collection
```

### Embed a Document

```bash
curl -X POST http://localhost:8000/api/embedding/collections/my-collection/embed \
  -H "Content-Type: application/json" \
  -d '{"content":"Your document text here","metadata":{"source":"example"}}'
```

### Embed Multiple Documents

```bash
curl -X POST http://localhost:8000/api/embedding/collections/my-collection/embed_batch \
  -H "Content-Type: application/json" \
  -d '[
    {"content":"First document","metadata":{"page":"1"}},
    {"content":"Second document","metadata":{"page":"2"}}
  ]'
```

### Search

```bash
curl -X POST http://localhost:8000/api/embedding/collections/my-collection/search \
  -H "Content-Type: application/json" \
  -d '{"query":"search query text","top_k":5}'
```

## Environment Variables

- `QDRANT_URL` - Qdrant server URL (default: http://localhost:6333)
- `SENTENCE_TRANSFORMER_MODEL` - Model name (default: all-MiniLM-L6-v2)

## Health Check

```bash
curl http://localhost:8000/health
```
