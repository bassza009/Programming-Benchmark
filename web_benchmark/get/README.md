# GET Request Benchmark

Benchmarks GET request performance across different programming languages and runtimes.

## Supported Languages

- **Python** (built-in http.server)
- **Node.js** (native http module)
- **PHP** (Swoole HTTP Server for concurrent async requests)
- **Go** (net/http package)
- **Java** (com.sun.net.httpserver with thread pool executor)

## Architecture

Each language implements a simple HTTP GET server with these endpoints:

- `GET /` - Returns basic server info (JSON)
- `GET /health` - Health check endpoint
- `GET /api/data` - Returns benchmark data

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start all servers
docker-compose up --build

# In another terminal, run benchmark
python3 benchmark.py [duration] [threads]

# Example: 30 second benchmark with 4 threads
python3 benchmark.py 30 4

# Stop servers
docker-compose down
```

### Option 2: Run Servers Individually

**Python:**
```bash
python3 server.py
# Server runs on port 8080 by default
# Or set: PORT=9000 python3 server.py
```

**Node.js:**
```bash
node server.js
# Port 8080 (or set PORT environment variable)
```

**PHP:**
```bash
php server.php
# Server runs on port 8003 by default
# Or set: PORT=8003 php server.php
# Note: Requires Swoole extension (uses openswoole/swoole Docker image)
```

**Go:**
```bash
go run server.go
# Port 8080 (or set PORT environment variable)
```

**Java:**
```bash
# Compilation
javac server.java

# Run (uses thread pool executor sized at 2x CPU cores)
java server
# Port 8005 by default (or set PORT environment variable)
```

### Running Benchmarks

```bash
# Default: 30 seconds, 4 threads
python3 benchmark.py

# Custom: 60 seconds duration, 8 threads
python3 benchmark.py 60 8

# For quick test: 10 seconds, 2 threads
python3 benchmark.py 10 2
```

## New wrk Benchmarking

The repository also supports `wrk`-based benchmarking using the Lua JSON reporter.

- `wrk_json_reporter.lua` formats `wrk` output as strict JSON.
- `run_bme_wrk.py` benchmarks locally running servers and writes `bme_benchmark_results.json`.
- `run_dkr_wrk.py` benchmarks Docker containers and writes `dkr_benchmark_results.json`.

### Example wrk benchmark commands

```bash
# Run local Bare Metal Environment benchmark
python3 run_bme_wrk.py

# Run Docker benchmark
python3 run_dkr_wrk.py
```

> Ensure `wrk` is installed and servers are already running for `run_bme_wrk.py`.

## Benchmark Script Features

The `benchmark.py` script:

- Tests multiple endpoints (`/`, `/health`, `/api/data`)
- Concurrent request generation using thread pool
- Calculates detailed statistics:
  - Min/Max/Mean/Median response times
  - Standard deviation
  - Percentiles (P95, P99)
  - Requests per second
  - Error rate
- Saves results to JSON format
- Automatic server health checks

## Results

Results are saved in `results/get_benchmark_<timestamp>.json` with format:

```json
{
  "Python": {
    "server": "Python",
    "url": "http://localhost:8001",
    "timestamp": 1234567890,
    "endpoints": {
      "/": {
        "requests": 5000,
        "success": 4950,
        "errors": 50,
        "mean_ms": 12.34,
        "median_ms": 11.5,
        "p95_ms": 25.0,
        "p99_ms": 35.5,
        "requests_per_sec": 166.67,
        "error_rate": 1.0
      }
    }
  }
}
```

## Configuration

Edit these variables in scripts for customization:

**benchmark.py:**
- `duration`: Benchmark duration per endpoint (seconds)
- `threads`: Number of concurrent threads
- `servers`: List of servers to test

**docker-compose.yml:**
- `cpus`: CPU limit per container
- `mem_limit`: Memory limit per container
- `ports`: Port mappings

## Building Docker Images Separately

```bash
# Python
docker build -f Dockerfile.python -t get-benchmark-python .

# Node.js
docker build -f Dockerfile.nodejs -t get-benchmark-nodejs .

# PHP
docker build -f Dockerfile.php -t get-benchmark-php .

# Go
docker build -f Dockerfile.go -t get-benchmark-go .

# Java
docker build -f Dockerfile.java -t get-benchmark-java .
```

## Performance Tuning

For more accurate benchmarks:

1. **Resource Isolation**: Run on a dedicated machine
2. **Kernel Parameters**: Adjust system limits (file descriptors, ports)
3. **Warm-up**: First 100 requests are warm-up, results are from subsequent requests
4. **Duration**: Longer durations (60+s) give more stable results
5. **Threads**: Match to available CPU cores

### Adjust System Limits (Linux):

```bash
# Increase file descriptor limit
ulimit -n 65536

# Increase open ports
sudo sysctl net.ipv4.ip_local_port_range="1024 65535"
```

## Troubleshooting

**"Connection refused"**
- Ensure Docker containers are running: `docker-compose ps`
- Check ports aren't already in use: `netstat -tulpn | grep 800[0-5]`

**Low request rates**
- Increase `threads` parameter
- Run on less loaded system
- Check network latency

**Java OutOfMemory**
- Increase `mem_limit` in docker-compose.yml
- Set `JAVA_OPTS=-Xmx256m` environment variable

**PHP "Address already in use"**
- Kill previous PHP process: `pkill -f "php -S"`
- Or use different port

## Next Steps

1. Analyze results in `results/` directory
2. Create graphs/visualizations from JSON data
3. Compare performance across languages
4. Identify bottlenecks and optimization opportunities
5. Scale tests with larger payload sizes or more concurrency

## File Structure

```
get/
├── server.py              # Python HTTP server
├── server.js              # Node.js HTTP server
├── server.php             # PHP HTTP server
├── server.go              # Go HTTP server
├── server.java            # Java HTTP server
├── Dockerfile.python      # Python container
├── Dockerfile.nodejs      # Node.js container
├── Dockerfile.php         # PHP container
├── Dockerfile.go          # Go container
├── Dockerfile.java        # Java container
├── docker-compose.yml     # Multi-container orchestration
├── benchmark.py           # Python benchmark script
├── benchmark.sh           # Bash benchmark script (requires wrk)
└── README.md              # This file
```

## References

- Python `http.server`: https://docs.python.org/3/library/http.server.html
- Node.js `http`: https://nodejs.org/api/http.html
- PHP built-in server: https://www.php.net/manual/en/features.commandline.webserver.php
- Go `net/http`: https://golang.org/pkg/net/http/
- Java `HttpServer`: https://docs.oracle.com/javase/11/docs/api/com.sun.net.httpserver/com/sun/net/httpserver/HttpServer.html
