#!/bin/bash

cd "$(dirname "$0")"

echo "Starting..."

PID=$(ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}')

if [ ! -z "$PID" ]; then
    echo "Already running (PID: $PID)"
    exit 1
fi

nohup poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &

sleep 2
PID=$(ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}')

if [ ! -z "$PID" ]; then
    echo "Started (PID: $PID)"
else
    echo "Failed"
    exit 1
fi
