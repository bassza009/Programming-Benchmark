# Programming Benchmark: Multi-Language Web Framework Benchmark Suite

## Overview
**Programming Benchmark** is a deterministic, high-performance web framework benchmark suite designed to evaluate HTTP performance under heavy load across 5 programming language runtimes and frameworks.

The suite measures **Raw SQL Query Performance** comparing **GET (read)** operations (with and without database indexes) against **POST (write/insert)** transactions in both **Bare Metal (BME)** and **Docker Containerized** environments under strict process isolation.

---

## Benchmark Scope & Specification

- **Focus Area:** Normal Raw SQL Queries **ONLY** (ORM models and abstraction layers are excluded).
- **Database:** MySQL 8.0 instance running on port `3306` with tuned connection limits (`max_connections=10000`).
- **Load Testing Tool:** `wrk` load generator with custom Lua JSON reporting script (`wrk_json_reporter.lua`).

### Tech Stack & Server Ports

| Language | Framework | Database Driver / Client | Default Port | Connection Pooling | Concurrency Model |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python** | FastAPI | `aiomysql` | `8001` | Async Pool (50 conns/worker) | Async Event Loop (Uvicorn workers) |
| **Node.js** | Fastify | `mysql2/promise` | `8002` | Connection Pool (50 conns/worker) | Multi-core Cluster + Event Loop |
| **PHP** | Swoole | `PDO_MySQL` | `8003` | `Swoole\Database\PDOPool` (64 conns) | Coroutine Event Loop Engine |
| **Go** | Fiber | `database/sql` (`go-sql-driver/mysql`) | `8004` | Standard Pool (100 max open) | Lightweight Goroutines |
| **Java** | Spring Boot | `JdbcTemplate` / `HikariCP` | `8005` | HikariCP Pool (100 max open) | Multi-threaded JVM Thread Pool |

---

## Research Variables Specification

### 1. Independent Variables (ตัวแปรต้น)
* **Execution Environment:** Bare Metal (Host OS) vs Docker (Containerized).
* **Language & Framework:** Python (FastAPI), Node.js (Fastify), PHP (Swoole), Go (Fiber), Java (Spring Boot).
* **Database Indexing:** Unindexed (`get_no_index`) vs Indexed (`get_with_index` with secondary B-Tree foreign keys).
* **Workload Complexity:** 
  - Read (GET): Single table (`users`), 2-Table JOIN, 3-Table JOIN, 4-Table JOIN.
  - Write (POST): Single-table INSERT, 2-Table Tx, 3-Table Tx, 4-Table Tx (with 2 items).
* **Load Intensity:** 5 Concurrency Tiers (POC, Small, General, High, Stress).

### 2. Controlled & Fixed System Variables (ตัวแปรควบคุม)
| Subsystem | Parameter / Variable | Value | Purpose / Notes |
| :--- | :--- | :--- | :--- |
| **MySQL 8.0** | `max_connections` | **`10,000`** | Prevents socket rejection under high concurrency stress tiers. |
| **MySQL 8.0** | `wait_timeout` / `interactive_timeout` | **`28,800`** sec | Avoids connection starvation from premature socket closing. |
| **MySQL 8.0** | Baseline Data Volume | **10,000 rows / table** | Fixed baseline volume across `users`, `profiles`, `orders`, `order_items`. |
| **MySQL 8.0** | Character Set & Collation | `utf8mb4` / `utf8mb4_unicode_ci` | Uniform Unicode encoding. |
| **Linux OS** | `RLIMIT_NOFILE` (`ulimit -n`) | **`65,535`** | Eliminates open file descriptor bottleneck. |
| **Linux OS** | `net.core.somaxconn` & `tcp_max_syn_backlog` | **`65,535`** | Kernel socket backlog queue expansion. |
| **Linux OS** | `net.ipv4.tcp_tw_reuse` | **`1`** | Enables fast TIME_WAIT reuse against port exhaustion. |
| **wrk Load Generator** | Warmup Duration | **3.0 seconds** | Pre-heats JIT and pools prior to metric recording. |
| **wrk Load Generator** | Test Iterations | **20 runs** | Statistical aggregation sample size. |

### 3. Dependent Variables (ตัวแปรตาม)
* **Mean Throughput ($\bar{T}$ Req/sec)** & Standard Deviation ($\sigma_T$) with 95% Confidence Interval.
* **Mean Latency ($\bar{L}$ ms)** & Standard Deviation ($\sigma_L$) with 95% Confidence Interval.
* **Tail Latencies ($p_{50}, p_{90}, p_{95}, p_{99}$)** & Maximum Latency ($L_{\max}$).
* **Reliability Metrics:** Socket connection errors, timeout count, and HTTP status anomalies.
* **Bare Metal Performance Gain ($\Delta_{\text{BME}}$)** & **Index Speedup Factor ($\text{Gain}_{\text{Index}}$)**.

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
* `--runs N` (Default: `1`) - Number of benchmark iterations per endpoint to run and average.
* `--no-warmup` (Default: False) - Disable the 3-second runtime warmup.

### Output Files
* `<bme/dkr>_benchmark_results.json` & `results/<suite>.json`: Contain the statistically **averaged** metrics across all runs.
* `raw_results.json` & `results/raw_results/<suite>_raw.json`: Contain the detailed **raw per-run** metrics for every individual iteration.

### Automated Master Benchmark Runner (`auto_runner.py`)
To run the full end-to-end benchmark suite sequentially with automatic index management, port cleanup, and reporting:

```bash
# Run complete test pipeline (All 6 suites, 20 runs per endpoint)
python3 auto_runner.py

# Run specific tier with custom iteration count
python3 auto_runner.py --tier poc --runs 3

# Filter by language or framework
python3 auto_runner.py --lang python --tier small --runs 5
python3 auto_runner.py --framework fiber --tier general
```

**Pipeline Execution Sequence:**
1. **GET (No Index)**: Removes secondary indexes, runs Docker (`run_dkr_wrk.py`) and Bare Metal (`run_bme_wrk.py`).
2. **GET (With Index)**: Applies secondary indexes on foreign keys, runs Docker and Bare Metal.
3. **POST (Write / Transactions)**: Runs transactional insert benchmarks for Docker and Bare Metal.
4. **Summary & Export**: Automatically executes `results/generate_summary.py` and `results/export_csv.py`.

---

### Manual Execution by Suite

#### 1. Running GET (No Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/GET/get_no_index
python3 run_dkr_wrk.py --tier all
```

#### 2. Running GET (With Index) Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/GET/get_with_index
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all
```

#### 3. Running POST Benchmarks
```bash
# Bare Metal (BME)
cd main_web_benchmark/POST
python3 run_bme_wrk.py --tier all

# Docker Containerized
cd main_web_benchmark/POST
python3 run_dkr_wrk.py --tier all
```
