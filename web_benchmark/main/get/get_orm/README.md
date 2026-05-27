# Web Server ORM Benchmark with MySQL Database I/O

ORM benchmark servers in Go, Node.js, Python, Java, and PHP Swoole, all using MySQL and standard ORM layers.

## Features

- **Connection Pooling**: Each server uses a standard ORM with max pool size of 100.
- **Schema Initialization**: Auto-creates tables and inserts 10,000 mock rows on startup.
- **4 Query Endpoints**: Tests 1-table, 2-join, 3-join, and 4-join ORM queries.
- **Minimal Logging**: Request logging is disabled to preserve benchmark accuracy.

## Quick Start with Docker

```bash
docker-compose up -d
```

This will start:
- MySQL on port 3306
- Python FastAPI server on port 8001
- Node.js Fastify server on port 8002
- PHP Swoole server on port 8003
- Go Fiber server on port 8004
- Java Spring Boot server on port 8005

## Endpoints

- `/` - Health check
- `/orm/1table` - SELECT * FROM users LIMIT 100 via ORM
- `/orm/2join` - 2-table join (users + profiles) via ORM
- `/orm/3join` - 3-table join (users + profiles + orders) via ORM
- `/orm/4join` - 4-table join (users + profiles + orders + order_items) via ORM

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

> Note: when running locally, these servers listen on ports 8001–8005.

## Benchmarking with wrk

```bash
# Run local Bare Metal Environment benchmark
python3 run_bme_wrk.py

# Build Docker images for container benchmark
docker build -f Dockerfile.python -t bench-python .
docker build -f Dockerfile.nodejs -t bench-node .
docker build -f Dockerfile.php -t bench-php .
docker build -f Dockerfile.go -t bench-go .
docker build -f Dockerfile.java -t bench-java .

# Run Docker container benchmark
python3 run_dkr_wrk.py
```

For a single endpoint quick test:

```bash
chmod +x run_wrk.sh
./run_wrk.sh http://127.0.0.1:8001/orm/1table
```

## Database Schema

- **users**: id, name, email
- **profiles**: id, user_id, age, address
- **orders**: id, user_id, total_amount
- **order_items**: id, order_id, product_name, price
