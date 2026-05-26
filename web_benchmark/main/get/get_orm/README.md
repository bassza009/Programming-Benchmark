# Web Server ORM Benchmark with MySQL Database I/O

Benchmark servers in Go, Node.js, Python, Java, and PHP Swoole using standard ORMs for database access.

## Features

- **ORM Overhead Benchmark**: each language uses the same framework as raw SQL version, but via ORM models and relationships.
- **Connection Pooling**: every ORM is configured with a maximum pool size of exactly 100.
- **Schema Initialization**: Auto-creates tables and inserts 10,000 mock rows on startup.
- **4 Query Endpoints**: ORM queries for 1-table, 2-join, 3-join, and 4-join.

## Endpoints

- `/` - Health check
- `/orm/1table` - Fetch 100 users
- `/orm/2join` - Join `users` + `profiles`
- `/orm/3join` - Join `users` + `profiles` + `orders`
- `/orm/4join` - Join `users` + `profiles` + `orders` + `order_items`

## Ports

- Python: 8001
- Node.js: 8002
- PHP: 8003
- Go: 8004
- Java: 8005
