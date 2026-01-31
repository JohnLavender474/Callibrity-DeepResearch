#!/bin/bash

CONTAINER_NAME="deepresearch_qdrant_db"

running_containers=$(docker ps --format '{{.Names}}')
all_containers=$(docker ps -a --format '{{.Names}}')

container_is_running=$(echo "$running_containers" | grep -q "^${CONTAINER_NAME}$" && echo true || echo false)

if [ "$container_is_running" = false ]; then
    container_exists=$(echo "$all_containers" | grep -q "^${CONTAINER_NAME}$" && echo true || echo false)

    if [ "$container_exists" = true ]; then
        echo "Restarting existing Qdrant container..."
        docker start ${CONTAINER_NAME}
    else
        echo "Creating and starting Qdrant container..."
        docker run -d --name ${CONTAINER_NAME} -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
    fi

    echo "Qdrant service started on port 6333."
else
    echo "Qdrant is already started and running."
fi

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

echo "Embedding service started on port 8000."