# Web Server Benchmark with MySQL Database I/O

High-performance web servers in Go, Node.js, Python, Java, and PHP Swoole, all with MySQL integration for database I/O benchmarking.

## Features

- **Connection Pooling**: Each server uses the most popular raw SQL driver for its language with max pool size of 100
- **Schema Initialization**: Auto-creates tables and inserts 10,000 mock rows on startup
- **4 Query Endpoints**: Tests 1-table, 2-join, 3-join, and 4-join queries
- **Multi-threading/Cluster**: Uses all CPU cores for maximum performance
- **Minimal Logging**: Request logging disabled to ensure accurate benchmarks

## Quick Start with Docker

```bash
docker-compose up -d
```

This will start:
- MySQL on port 3306
- Go Fiber server on port 8080
- Node.js Fastify server on port 8081
- Python FastAPI server on port 8082
- Java Spring Boot server on port 8083
- PHP Swoole server on port 8084

## Endpoints

- `/` - Health check
- `/raw/1table` - SELECT * FROM users LIMIT 100
- `/raw/2join` - 2-table join (users + profiles)
- `/raw/3join` - 3-table join (users + profiles + orders)
- `/raw/4join` - 4-table join (users + profiles + orders + order_items)

## Running Individual Servers

### Go
```bash
go run server.go
```

### Node.js
```bash
npm install
node server.js
```

### Python
```bash
pip install -r requirements.txt
python server.py
```

### Java
```bash
mvn spring-boot:run
```

### PHP Swoole
```bash
php server.php
```

## Benchmarking with wrk

```bash
bash run_wrk.sh [URL]
# Default: bash run_wrk.sh http://127.0.0.1:8080/
```

## Database Schema

- **users**: id, name, email
- **profiles**: id, user_id, age, address
- **orders**: id, user_id, total_amount
- **order_items**: id, order_id, product_name, price
