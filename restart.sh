#!/bin/bash

cd "$(dirname "$0")"

echo "restarting..."

./stop.sh

sleep 1

./start.sh
