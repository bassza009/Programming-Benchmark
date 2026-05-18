#!/bin/bash

# Quick runner script for GET benchmarking

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "GET Request Benchmark Runner"
echo "============================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found"
    exit 1
fi

# Check/install requirements
echo "Checking dependencies..."
python3 -m pip install -q -r requirements.txt || {
    echo "Error: Failed to install dependencies"
    exit 1
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker not found"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose not found"
    exit 1
fi

echo "✓ All dependencies available"
echo ""

# Get duration and threads from arguments
DURATION=${1:-30}
THREADS=${2:-4}

echo "Starting Docker containers..."
docker-compose up --build -d

# Wait for containers to be healthy
echo ""
echo "Waiting for servers to be ready (this may take 30-60 seconds)..."
sleep 10

# Run benchmark
echo ""
echo "Running benchmark..."
echo ""

python3 benchmark.py "$DURATION" "$THREADS"

# Ask to keep or stop containers
echo ""
read -p "Stop Docker containers? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping containers..."
    docker-compose down
else
    echo "Containers still running. Stop them with: docker-compose down"
fi

echo "Done!"
