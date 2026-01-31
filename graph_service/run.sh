# !/bin/bash

python -m uvicorn app:app --host 0.0.0.0 --port 8001 --reload

echo "Graph service started on port 8001."