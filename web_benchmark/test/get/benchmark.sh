#!/bin/bash

# GET Request Benchmarking Script
# Benchmarks different web servers implemented in multiple languages

set -e

RESULTS_DIR="./results"
TIMESTAMP=$(date +%s)
SERVERS=(
    "python:8001:Python"
    "nodejs:8002:Node.js"
    "php:8003:PHP"
    "go:8004:Go"
    "java:8005:Java"
)

# Configuration
DURATION=30  # seconds per benchmark
THREADS=4
CONNECTIONS=100

# Function to check if server is ready
check_server() {
    local host=$1
    local port=$2
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if timeout 2 bash -c "cat < /dev/null > /dev/tcp/$host/$port" 2>/dev/null; then
            echo " Server on port $port is ready"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    echo " Failed to connect to server on port $port"
    return 1
}

# Create results directory
mkdir -p "$RESULTS_DIR"

echo "=========================================="
echo "GET Request Benchmarking Suite"
echo "=========================================="
echo "Timestamp: $TIMESTAMP"
echo "Duration per test: ${DURATION}s"
echo "Threads: $THREADS"
echo "Connections: $CONNECTIONS"
echo ""

# Check if wrk is available
if ! command -v wrk &> /dev/null; then
    echo "  wrk not found. Installing wrk..."
    apt-get update && apt-get install -y build-essential libssl-dev git
    git clone https://github.com/wg/wrk.git /tmp/wrk
    cd /tmp/wrk
    make
    cp wrk /usr/local/bin/
    cd - > /dev/null
fi

# Benchmark each server
for SERVER_INFO in "${SERVERS[@]}"; do
    IFS=':' read -r name port language <<< "$SERVER_INFO"
    
    echo ""
    echo "=========================================="
    echo "Benchmarking: $language (port $port)"
    echo "=========================================="
    
    # Wait for server to be ready
    if ! check_server localhost $port; then
        echo "Skipping $language - server not reachable"
        continue
    fi
    
    # Create result file
    RESULT_FILE="$RESULTS_DIR/${name}_get_${TIMESTAMP}.json"
    
    # Run benchmark with wrk
    echo "Running benchmark for $language..."
    wrk -t $THREADS -c $CONNECTIONS -d "${DURATION}s" \
        --script=benchmark.lua \
        http://localhost:$port/ > "$RESULT_FILE" 2>&1 || true
    
    echo "Results saved to: $RESULT_FILE"
    
    # Parse and display results
    if [ -f "$RESULT_FILE" ]; then
        echo ""
        echo "Results:"
        cat "$RESULT_FILE"
    fi
done

echo ""
echo "=========================================="
echo "Benchmark Complete!"
echo "Results saved to: $RESULTS_DIR"
echo "=========================================="
