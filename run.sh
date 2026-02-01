#!/bin/bash

# Remove old virtual environment

rm -rf venv

# Create and activate virtual environment

python3 -m venv venv
source venv/bin/activate

# Install dependencies

pip install --upgrade pip
pip install -r requirements.txt

# Enable job control to make this script a process group leader.
# This ensures all child processes (and their descendants) form a 
# process group that can be terminated together.
set -m

# Set up trap to clean up on exit

cleanup() {
    echo "Shutting down services..."
    # Kill the entire process group ($$) using negative PID syntax
    # This terminates all descendants: bash scripts AND their spawned Python processes
    kill -- -$$ 2>/dev/null
    # Wait for all processes to finish gracefully after receiving SIGTERM
    wait
}

trap cleanup EXIT INT TERM

# Start all services

echo "Starting database service..."
(cd database_service && bash run.sh) &

echo "Starting storage service on port 8002..."
(cd storage_service && bash run.sh) &

echo "Starting embedding service on port 8000..."
(cd embedding_service && bash run.sh) &

echo "Starting graph service..."
(cd graph_service && bash run.sh) &

echo "Starting frontend service on port 8004..."
(cd frontend_service && bash run.sh) &

echo "All services started."

# Keep processes running

wait
