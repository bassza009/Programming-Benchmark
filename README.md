# Project Antigravity: Multi-Language & Multi-Environment Web Benchmark Suite

> Language: **English** | [Thai (ภาษาไทย)](README_TH.md)

---

## 1. Executive Summary

In modern backend software development, engineering teams frequently evaluate backend programming languages and web frameworks for high-throughput, low-latency workloads:
* Is Go significantly faster than Node.js?
* How does Java Spring Boot perform under high concurrency?
* Can modern async PHP runtimes (such as Swoole) compete with compiled languages?
* How does Python FastAPI compare under heavy I/O load?
* What is the performance penalty introduced by Docker containerization?

Most publicly available benchmarks only test synthetic "Hello World" endpoints that return static strings in isolation. However, production web applications perform database I/O, execute relational queries with multiple joins, manage database connection pools, and handle transactions under high concurrent load.

**Project Antigravity** is a reproducible benchmark suite designed to evaluate **5 backend languages and frameworks** under **realistic database workloads** across **Bare Metal** and **Docker Containerized** environments across **5 load scenarios** (from 20 to 10,000 concurrent connections).

---

## 2. Project Goals

### 1. Realistic Database Workloads
Tests real MySQL database operations with tens of thousands of records, including single-table lookups, 2 to 4-table relational joins, and multi-table write transactions.

### 2. Containerization Overhead Measurement
Measures the throughput and latency difference between running directly on the host operating system (Bare Metal) versus running inside Docker containers with virtualized network stacks.

### 3. Database Indexing Analysis Under Concurrency
Evaluates the impact of secondary indexes on query throughput and latency under escalating concurrency levels.

### 4. Concurrency Breakdown and Saturation Limits
Identifies where frameworks reach saturation, manage connection pools, or encounter socket bottlenecks under stress levels up to 10,000 concurrent connections.

### 5. Standardized and Fair Evaluation
- Standardizes connection pool sizing across all frameworks.
- Applies process warmup phases before measurements.
- Resets database state between test runs.
- Configures operating system file descriptor limits (`ulimit -n 65535`).
- Supports multi-run iterations (`--runs N`) to calculate statistical averages while collecting raw logs in `raw_results.json`.

---

## 3. Evaluated Technologies and Frameworks

| Language | Web Framework | Database Driver / Client | Concurrency Model | Port |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | **FastAPI** (Uvicorn) | `aiomysql` (Async Pool) | Multi-process Async Event Loop | `8001` |
| **Node.js** | **Fastify** | `mysql2/promise` (Pool) | Multi-core Cluster + Event Loop | `8002` |
| **PHP** | **Swoole** | `PDO_MySQL` (`PDOPool`) | Coroutine Event Loop | `8003` |
| **Go** | **Fiber** (v2) | `database/sql` (`go-sql-driver`) | Goroutines | `8004` |
| **Java** | **Spring Boot** (v3) | `JdbcTemplate` + `HikariCP` | Multi-threaded JVM Pool | `8005` |

---

## 4. Test Scenarios and Load Tiers

### A. Read (GET) Suites (Raw SQL)
* `/raw/1table`: Single-table query (`SELECT * FROM users LIMIT 100`)
* `/raw/2join`: 2-table relational JOIN (`users` + `profiles`)
* `/raw/3join`: 3-table relational JOIN (`users` + `profiles` + `orders`)
* `/raw/4join`: 4-table relational JOIN (`users` + `profiles` + `orders` + `order_items`)

Evaluated across two database states:
1. **`GET/get_no_index`**: Queries executed without secondary indexes (table scans).
2. **`GET/get_with_index`**: Queries executed with secondary indexes on foreign key columns.

### B. Write (POST) Suite (Database Transactions)
* `/raw/post/1table`: Single-table insert into `users`.
* `/raw/post/2table`: Transactional insert across `users` and `profiles`.
* `/raw/post/3table`: Transactional insert across `users`, `profiles`, and `orders`.
* `/raw/post/4table`: Transactional insert across `users`, `profiles`, `orders`, and multiple `order_items`.

### C. Concurrency Load Tiers (via `wrk`)

| Tier Option (`--tier`) | Scenario | Typical Website | Threads (`-t`) | Connections (`-c`) | Duration (`-d`) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **`poc`** | **POC / Small internal system** | Thesis project, department website prototype | `2` | `20` | `30s` |
| **`small`** | **Small production website** | Small company, local business | `4` | `100` | `60s` |
| **`general`** | **General web application** | University system, e-commerce, CMS | `8` | `500` | `60s` |
| **`high`** | **High-density website** | Popular portals, SaaS platforms | `8` | `2,000` | `120s` |
| **`stress`** | **Stress testing** | Saturation point / connection limits | `16` | `10,000` | `300s` |
| **`all`** | **All Scenarios (Default)** | Sequential evaluation across all 5 tiers | Sequential | Sequential | Cumulative |

---

## 5. How to Run the Benchmarks

### Prerequisites
* MySQL 8.0 running locally on port `3306` (`user=admin`, `password=secret`, `database=benchmark_db`).
* Python 3.10+ and `wrk` installed.
* Docker (for containerized mode).

### Step-by-Step Execution
```bash
# 1. Run GET (No Index) Bare Metal Benchmark (3 iterations averaged)
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py --tier all --runs 3

# 2. Run GET (With Index) Docker Benchmark
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all --runs 3

# 3. Run POST Write Benchmark
cd main_web_benchmark/POST
python3 run_bme_wrk.py --tier all --runs 3
```

### CLI Arguments
* `--tier {poc,small,general,high,stress,all}` (Default: `all`): Choose the concurrency load scenario.
* `--runs N` (Default: `1`): Number of test iterations per endpoint to run and calculate the statistical average.
* `--no-warmup` (Default: False): Disable the 3-second warmup phase.

---

## 6. Output Files and Results Processing

### Generated Files
* **Averaged Results**: Saved locally in `<bme/dkr>_benchmark_results.json` and centralized in `main_web_benchmark/results/<suite>.json`.
* **Raw Iteration Logs**: Every individual run's raw metrics are saved in `raw_results.json` and `main_web_benchmark/results/raw_results/<suite>_raw.json`.

### Summarizing and Comparing Results
```bash
# View formatted comparison table from a result file
cd main_web_benchmark
python3 compare_results.py GET/get_no_index/dkr_benchmark_results.json

# Generate centralized Markdown summary and CSV export
cd main_web_benchmark/results
python3 generate_summary.py
```

---

## 7. Directory Structure

```text
main_web_benchmark/
├── GET/
│   ├── get_no_index/          # GET endpoints without secondary DB indexes
│   │   ├── run_bme_wrk.py
│   │   └── run_dkr_wrk.py
│   └── get_with_index/        # GET endpoints with secondary DB indexes
│       ├── run_bme_wrk.py
│       └── run_dkr_wrk.py
├── POST/                      # POST write/transaction benchmark suite
│   ├── run_bme_wrk.py
│   └── run_dkr_wrk.py
├── results/                   # Centralized benchmark results and summaries
│   ├── raw_results/           # Raw per-iteration logs
│   ├── generate_summary.py    # Generates SUMMARY.md and SUMMARY.csv
│   ├── SUMMARY.md             # Consolidated markdown results
│   └── SUMMARY.csv            # Consolidated CSV results
├── compare_results.py         # CLI comparison table formatter
├── issue.md                   # Technical audit and benchmark issue analysis
└── README.md                  # Suite documentation
```
