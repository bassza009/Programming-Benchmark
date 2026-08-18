# Project Antigravity: Multi-Language Web Framework Benchmark Suite

## Overview
**Project Antigravity** is a deterministic, high-performance web framework benchmark suite designed to evaluate HTTP performance under heavy load across 5 programming language runtimes and frameworks.

The suite measures **Raw SQL Query Performance** comparing **GET (read)** operations (with and without database indexes) against **POST (write/insert)** transactions in both **Bare Metal (BME)** and **Docker Containerized** environments under strict process isolation.

---

## Benchmark Scope & Specification

- **Focus Area:** Normal Raw SQL Queries **ONLY** (ORM models and abstraction layers are excluded).
- **Database:** MySQL 8.0 instance running on port `3306` with tuned connection limits (`max_connections=10000`).
- **Load Testing Tool:** `wrk` load generator with custom Lua JSON reporting script (`wrk_json_reporter.lua`).

### Tech Stack & Server Ports

| Language | Framework | Database Driver / Client | Default Port | Connection Pooling |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | FastAPI | `aiomysql` | `8001` | Async Pool (50 conns/worker) |
| **Node.js** | Fastify | `mysql2/promise` | `8002` | Connection Pool (50 conns/worker) |
| **PHP** | Swoole | `PDO_MySQL` | `8003` | `Swoole\Database\PDOPool` (64 conns) |
| **Go** | Fiber | `database/sql` (`go-sql-driver/mysql`) | `8004` | Standard Pool (100 max open) |
| **Java** | Spring Boot | `JdbcTemplate` / `HikariCP` | `8005` | HikariCP Pool (100 max open) |

---

## Load Testing Tiers

All runner scripts support multi-tier benchmarking across 5 realistic production scenarios:

| Tier Option | Scenario | Typical Website | Threads (`-t`) | Connections (`-c`) | Duration (`-d`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`poc`** | POC / Small internal system | Thesis project, department website prototype | `2` | `20` | `30s` |
| **`small`** | Small production website | Small company local business | `4` | `100` | `60s` |
| **`general`** | General web application | University system e-commerce CMS | `8` | `500` | `60s` |
| **`high`** | High-density website | Popular portals SaaS platforms | `8` | `2,000` | `120s` |
| **`stress`** | Stress testing | Find saturation point | `16` | `10,000` | `300s` |
| **`all`** | All Tiers | Full evaluation across all 5 scenarios | Sequential | Sequential | Cumulative |

---

## Directory Structure

```text
main_web_benchmark/
├── issue.md                   # Detailed audit report and issue explanations
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

### CLI Options
All `run_*.py` scripts support the following arguments:
* `--tier {poc,small,general,high,stress,all}` (Default: `all`) - Choose load intensity tier scenario.
* `--no-warmup` (Default: False) - Disable the 3-second runtime warmup.

### 1. Running GET (No Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/GET/get_no_index
python3 run_dkr_wrk.py --tier all
```

### 2. Running GET (With Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_with_index
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all
```

### 3. Running POST Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/POST
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/POST
python3 run_dkr_wrk.py --tier all
```
