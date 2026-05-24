#!/bin/bash
# Before running this script, execute: chmod +x run_wrk.sh

URL="${1:-http://127.0.0.1:8080/}"

echo "=================================================="
echo "Web Server Benchmark using wrk"
echo "=================================================="
echo ""
echo "Target URL: $URL"
echo ""

# Warmup phase
echo "Starting warmup phase..."
echo "Running: wrk -t2 -c100 -d10s $URL"
wrk -t2 -c100 -d10s "$URL" > /dev/null 2>&1
echo "Warmup complete!"
echo ""

# Actual test phase
echo "=================================================="
echo "Starting actual benchmark test..."
echo "Running: wrk -t4 -c500 -d30s $URL"
echo "=================================================="
echo ""
wrk -t4 -c500 -d30s "$URL"
echo ""
echo "=================================================="
echo "Benchmark complete!"
echo "=================================================="
