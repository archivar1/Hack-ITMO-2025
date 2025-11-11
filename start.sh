#!/bin/bash

cd "$(dirname "$0")"
echo "Starting..."
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
