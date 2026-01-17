#!/bin/bash

docker run -d -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest

rm -rf venv

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

uvicorn app:app --host 0.0.0.0 --port 8000 --reload