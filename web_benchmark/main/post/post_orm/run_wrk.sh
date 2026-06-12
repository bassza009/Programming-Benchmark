#!/bin/bash
# Before running this script, execute: chmod +x run_wrk.sh

URL="${1:-http://127.0.0.1:8001/raw/post/1table}"

echo "=================================================="
echo "POST Server Benchmark using wrk"
echo "=================================================="
echo ""
echo "Target URL: $URL"
echo ""

# Warmup phase
echo "Starting warmup phase..."
echo "Running: wrk -t2 -c100 -d10s -s post_script.lua $URL"
wrk -t2 -c100 -d10s -s post_script.lua "$URL" > /dev/null 2>&1
echo "Warmup complete!"
echo ""

# Actual test phase
echo "=================================================="
echo "Starting actual benchmark test..."
echo "Running: wrk -t4 -c500 -d30s -s post_script.lua $URL"
echo "=================================================="
echo ""
wrk -t4 -c500 -d30s -s post_script.lua "$URL"
echo ""
echo "=================================================="
echo "Benchmark complete!"
echo "=================================================="
