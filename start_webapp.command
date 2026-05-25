#!/bin/bash

cd "$(dirname "$0")"

PORT=8000

echo "Cleaning port $PORT..."
kill -9 $(lsof -ti :$PORT) 2>/dev/null

echo "Starting web app..."
(sleep 2 && open http://127.0.0.1:$PORT) &
python3 webapp.py --host 127.0.0.1 --port $PORT
