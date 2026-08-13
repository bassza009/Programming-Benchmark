# Project Antigravity: Multi-Language Web Framework Benchmark Suite

## Overview
**Project Antigravity** is a deterministic, high-performance web framework benchmark suite designed to evaluate HTTP performance under heavy load across 5 programming language runtimes and frameworks.

The suite measures **Raw SQL Query Performance** comparing **GET (read)** operations (with and without database indexes) against **POST (write/insert)** transactions in both **Bare Metal (BME)** and **Docker Containerized** environments under strict process isolation.

---

## Benchmark Scope & Specification

- **Focus Area:** Normal Raw SQL Queries **ONLY** (ORM models and abstraction layers are excluded).
- **Database:** MySQL 8.0 instance running on port `3306` with 10,000 initial mock records.
- **Load Testing Tool:** `wrk` load generator with custom Lua JSON reporting script (`wrk_json_reporter.lua`).

### Tech Stack & Server Ports

| Language | Framework | Database Driver / Client | Default Port |
| :--- | :--- | :--- | :--- |
| **Python** | FastAPI | `aiomysql` | `8001` |
| **Node.js** | Fastify | `mysql2/promise` | `8002` |
| **PHP** | Swoole | `PDO_MySQL` | `8003` |
| **Go** | Fiber | `database/sql` (`go-sql-driver/mysql`) | `8004` |
| **Java** | Spring Boot | `JdbcTemplate` / `HikariCP` | `8005` |

---

## Directory Structure

```text
main_web_benchmark/
├── Pointofproject.md          # Project PRD and technical specification
├── README.md                  # Project documentation (this file)
│
├── GET/                       # Read Benchmark Suite
│   ├── get_no_index/          # GET endpoints WITHOUT secondary DB indexes
│   │   ├── server.* / src_java/
│   │   ├── Dockerfile.* & docker-compose.yml
│   │   ├── run_bme_wrk.py
│   │   └── run_dkr_wrk.py
│   │
│   └── get_with_index/        # GET endpoints WITH secondary DB indexes on join columns
│       ├── server.* / src_java/
│       ├── Dockerfile.* & docker-compose.yml
│       ├── run_bme_wrk.py
│       └── run_dkr_wrk.py
│
└── POST/                      # Write / Transaction Benchmark Suite
    ├── server.* / src_java/
    ├── Dockerfile.* & docker-compose.yml
    ├── run_bme_wrk.py
    └── run_dkr_wrk.py
```

---

## Endpoints Tested

### 1. GET Endpoints (`GET/get_no_index` & `GET/get_with_index`)
- `/raw/1table` - Single table query (`SELECT * FROM users LIMIT 100`)
- `/raw/2join` - 2-Table JOIN query (`users` + `profiles`)
- `/raw/3join` - 3-Table JOIN query (`users` + `profiles` + `orders`)
- `/raw/4join` - 4-Table JOIN query (`users` + `profiles` + `orders` + `order_items`)

### 2. POST Endpoints (`POST/` suite)
- `/raw/post/1table` - Single table INSERT into `users`
- `/raw/post/2table` - Transactional INSERT into `users` + `profiles`
- `/raw/post/3table` - Transactional INSERT into `users` + `profiles` + `orders`
- `/raw/post/4table` - Transactional INSERT into `users` + `profiles` + `orders` + 2 `order_items`

---

## How to Run

### 1. Running GET (No Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py

# Docker Containerized
cd main_web_benchmark/GET/get_no_index
python3 run_dkr_wrk.py
```

### 2. Running GET (With Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_with_index
python3 run_bme_wrk.py

# Docker Containerized
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py
```

### 3. Running POST Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/POST
python3 run_bme_wrk.py

# Docker Containerized
cd main_web_benchmark/POST
python3 run_dkr_wrk.py
```
