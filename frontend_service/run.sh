#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Starting Vue.js development server on port 8004..."

npm run dev
