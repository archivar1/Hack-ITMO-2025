#!/bin/bash

echo "Stopping..."

PID=$(ps aux | grep "uvicorn app.main:app" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "Not running"
    exit 1
fi

echo "Found process with PID: $PID"
kill $PID

sleep 2

if ps -p $PID > /dev/null 2>&1; then
    echo "Process not stopped, forced termination..."
    kill -9 $PID
fi

echo "Stopped"
