# POST Benchmark Server

High-performance benchmark server implementations for testing POST endpoints with raw SQL transactions across multiple languages.

## Overview

This project implements POST endpoints that perform raw SQL INSERT operations with database transactions. Each implementation uses the framework's standard connection pool and raw SQL (no ORM) to ensure consistent, fair benchmarking across languages.

## Endpoints

All servers expose 4 POST endpoints for testing transaction handling:

### `POST /raw/post/1table`
Insert 1 row into `users` table.
- **Response:** `201 Created` with `{"user_id": <id>}`
- **Error:** `500` with error message

### `POST /raw/post/2table`
Transaction: Insert into `users`, then `profiles` using the new user_id.
- **Response:** `201 Created` with `{"user_id": <id>}`
- **Error:** `500` with error message (rollback on failure)

### `POST /raw/post/3table`
Transaction: Insert into `users` → `profiles` → `orders`.
- **Response:** `201 Created` with `{"user_id": <id>}`
- **Error:** `500` with error message (rollback on failure)

### `POST /raw/post/4table`
Transaction: Insert into `users` → `profiles` → `orders` → 2 rows in `order_items`.
- **Response:** `201 Created` with `{"user_id": <id>}`
- **Error:** `500` with error message (rollback on failure)

## Database Schema

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    bio VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10, 2)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_name VARCHAR(100),
    price DECIMAL(10, 2)
);
```

## Implementation Details

### Key Requirements
- **Raw SQL Only:** No ORM functions used
- **Prepared Statements:** All queries use prepared statements to prevent SQL injection
- **Connection Pooling:** Framework's standard database connection pool
- **Transactions:** Endpoints 2, 3, 4 use SQL transactions with COMMIT/ROLLBACK
- **Unique Emails:** Random UUID appended to email addresses to prevent duplicate key errors

### Language Implementations

| Language | Framework | Port | Status |
|----------|-----------|------|--------|
| Python | FastAPI | 8001 | ✓ Working |
| Node.js | Fastify | 8002 | ✓ Working |
| PHP | Swoole | 8003 | Created* |
| Go | Fiber | 8004 | ✓ Working |
| Java | Spring Boot WebFlux | 8005 | ✓ Working |

*PHP requires Swoole extension installation

## Running the Servers

### Python
```bash
cd web_benchmark/main/post/post_normal
python3 -m pip install -r requirements.txt
python3 server.py
```

### Node.js
```bash
cd web_benchmark/main/post/post_normal
npm install
node server.js
```

### Go
```bash
cd web_benchmark/main/post/post_normal
go mod tidy
go build -o server_go server.go
./server_go
```

### Java
```bash
cd web_benchmark/main/post/post_normal
mvn clean package
java -jar target/benchmark-0.0.1-SNAPSHOT.jar
```

### PHP (requires Swoole)
```bash
cd web_benchmark/main/post/post_normal
php server.php
```

## Testing

Example request using Python:
```python
import urllib.request
import json

url = 'http://127.0.0.1:8001/raw/post/1table'
req = urllib.request.Request(url, method='POST')
with urllib.request.urlopen(req) as response:
    data = json.load(response)
    print(data)  # {"user_id": 1}
```

## Database Connection

All servers connect to:
- **Host:** 127.0.0.1
- **Port:** 3306
- **User:** admin
- **Password:** secret
- **Database:** benchmark_db

Ensure MySQL/MariaDB is running and the database exists.

## Features

- **Connection Pooling:** Each implementation uses the framework's connection pool (100 max connections)
- **Multi-worker Support:** Python and Node.js use multiple worker processes
- **Error Handling:** Proper transaction rollback on errors
- **JSON Responses:** Consistent JSON response format across all implementations
- **Performance Focused:** Minimal logging and optimized for throughput

## Architecture

Each server:
1. Initializes database connection pool at startup
2. Creates tables if they don't exist
3. Handles concurrent POST requests
4. Uses prepared statements for all SQL queries
5. Manages transactions with BEGIN/COMMIT/ROLLBACK
6. Returns consistent JSON responses

## Benchmarking

### Using wrk (Shell Script)

Single endpoint test:
```bash
./run_wrk.sh http://127.0.0.1:8001/raw/post/1table
```

Manual wrk command:
```bash
wrk -t4 -c500 -d30s -s post_script.lua http://127.0.0.1:8001/raw/post/1table
```

### Using Python Benchmark Script

Run benchmarks across all languages:
```bash
# Ensure all servers are running on ports 8001-8005
python3 run_wrk.py
```

This script will:
1. Test all 5 language implementations
2. Run all 4 POST endpoints for each language
3. Collect performance metrics
4. Save results to `wrk_benchmark_results.json`

**Note:** All servers must be running before executing the Python benchmark script.

## Files

- `server.py` - Python/FastAPI implementation
- `server.js` - Node.js/Fastify implementation
- `server.php` - PHP/Swoole implementation
- `server.go` - Go/Fiber implementation
- `src/main/java/com/benchmark/server.java` - Java/Spring Boot implementation
- `pom.xml` - Java Maven configuration
- `package.json` - Node.js dependencies
- `requirements.txt` - Python dependencies
- `go.mod`, `go.sum` - Go module files
- `plaintext` - Original specification document
