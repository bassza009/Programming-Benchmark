# pos_web_benchmark: PostgreSQL Web Framework Benchmark Suite

## Overview
**pos_web_benchmark** is a high-load, multi-language web framework benchmark suite designed to evaluate HTTP throughput, latency percentiles, and database query planning performance under heavy concurrent load across 5 major programming runtimes against **PostgreSQL 16**.

The suite measures **Raw SQL Query Performance** against a realistic enterprise dataset of **11,110,000 total records**, comparing:
1. **GET (Read)** operations with secondary indexes vs without secondary indexes.
2. **POST (Write / Transactions)** operations across 1 to 4 tables.
3. **Bare Metal (Host OS)** vs **Docker Containerized** environments.

---

## Tech Stack & Architecture

| Language | Framework | Database Driver / Client | Default Port | Connection Pooling | Concurrency Model |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Python** | FastAPI | `asyncpg` | `8001` | Async Pool (20-100 conns) | Async Event Loop (Uvicorn workers) |
| **Node.js** | Fastify | `pg` (`node-postgres`) | `8002` | Clustered Pool (50 conns/core) | Multi-core Cluster + Event Loop |
| **PHP** | Swoole | `PDO_PGSQL` | `8003` | `Swoole\Database\PDOPool` (64 conns) | Coroutine Event Loop Engine |
| **Go** | Fiber | `jackc/pgx/v5/pgxpool` | `8004` | PGX Pool (20-200 conns) | Lightweight Goroutines |
| **Java** | Spring Boot | `org.postgresql.Driver` | `8005` | HikariCP Pool (50-200 conns) | Multi-threaded JVM Thread Pool |

---

## Large Scale Database Specification

The database runs on **PostgreSQL** (port `5432`, database: `benchmark_db`, user: `admin`, password: `secret`).

### Tables & Record Volumes (Total: 11,110,000 Records)
| Table Name | Target Volume | Primary Key | Description & Relations |
| :--- | :--- | :--- | :--- |
| **`factory`** | **10,000 records** | `id SERIAL` | Manufacturing facilities producing catalog products. |
| **`product`** | **100,000 records** | `id SERIAL` | Goods catalog (`factory_id` references `factory.id`). |
| **`customer`** | **1,000,000 records** | `id SERIAL` | Registered user base with email and geographic attributes. |
| **`orders`** | **10,000,000 records** | `id BIGSERIAL` | High-volume transactions linking customers and products. |

### Secondary Indexing Strategy
Every table includes indexes for optimized query lookup and foreign key joins:
- **`factory`**: `idx_factory_name`, `idx_factory_country`
- **`product`**: `idx_product_factory_id`, `idx_product_category`, `idx_product_price`
- **`customer`**: `idx_customer_email`, `idx_customer_city`
- **`orders`**: `idx_orders_customer_id`, `idx_orders_product_id`, `idx_orders_order_date`, `idx_orders_status`

---

## Concurrency Load Tiers

Load tests are generated using `wrk` with custom Lua statistical reporting (`wrk_json_reporter.lua`):

| Tier Option | Scenario | Typical Workload Context | Threads (`-t`) | Connections (`-c`) | Duration (`-d`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`poc`** | POC / Small Internal System | Thesis prototype, internal office tool | `2` | `20` | `30s` |
| **`small`** | Small Production Website | Local SME business traffic | `4` | `100` | `60s` |
| **`general`** | General Web Application | E-Commerce store, corporate CMS | `8` | `500` | `60s` |
| **`high`** | High-Density Portal | High-traffic SaaS / web platform | `8` | `2,000` | `120s` |
| **`stress`** | Saturation Stress Testing | Finds bottleneck & saturation limit | `16` | `10,000` | `300s` |
| **`all`** | All Tiers | Executes all 5 tiers sequentially | Cumulative | Cumulative | Cumulative |

---

## Directory Structure

```text
pos_web_benchmark/
├── DATABASE.md                    # Detailed PostgreSQL schema, ER diagram, and query documentation
├── README.md                      # Project documentation (this file)
├── auto_runner.py                 # Master pipeline runner
├── compare_results.py             # CLI results ranking formatter
│
├── db/                            # PostgreSQL Schema, Ingestion & Infrastructure
│   ├── docker-compose-db.yml      # Tuned PostgreSQL 16 container definition
│   ├── schema.sql                 # DDL definitions for the 4 tables
│   ├── seed.sql                   # Fast generate_series bulk ingestion script (11.11M rows)
│   ├── add_indexes.sql            # Index creation script
│   ├── drop_indexes.sql           # Secondary index drop script for get_no_index
│   └── setup_db.py                # Automated Python ingestion manager
│
├── GET/                           # Read Benchmark Suite
│   ├── get_no_index/              # GET endpoints WITHOUT secondary indexes
│   │   ├── frameworks/            # Python, Node.js, PHP, Go, Java implementations
│   │   ├── docker-compose.yml
│   │   ├── run_bme_wrk.py
│   │   └── run_dkr_wrk.py
│   └── get_with_index/            # GET endpoints WITH secondary indexes on join keys
│       ├── frameworks/
│       ├── docker-compose.yml
│       ├── run_bme_wrk.py
│       └── run_dkr_wrk.py
│
├── POST/                          # Write / Transaction Benchmark Suite
│   ├── frameworks/
│   ├── docker-compose.yml
│   ├── run_bme_wrk.py
│   └── run_dkr_wrk.py
│
└── results/                       # Aggregated Metrics, Raw Runs & Reports
    ├── raw_results/
    ├── generate_summary.py
    ├── export_csv.py
    └── export_excel.py
```

---

## Step-by-Step Setup & Execution

### Step 1: Start PostgreSQL & Ingest Data

#### Option A: Using Docker Compose (Recommended)
```bash
cd pos_web_benchmark/db
docker compose -f docker-compose-db.yml up -d
```

#### Option B: Automated Ingestion via Python Script
```bash
cd pos_web_benchmark/db
python3 setup_db.py --host 127.0.0.1 --port 5432 --user admin --password secret --dbname benchmark_db
```

#### Option C: Manual Ingestion via `psql`
```bash
cd pos_web_benchmark/db
psql -h 127.0.0.1 -U admin -d benchmark_db -f schema.sql
psql -h 127.0.0.1 -U admin -d benchmark_db -f seed.sql
psql -h 127.0.0.1 -U admin -d benchmark_db -f add_indexes.sql
```

---

### Step 2: Running Benchmarks

#### Automated Master Pipeline Runner (`auto_runner.py`)
To run all suites end-to-end with automated index dropping/adding and report generation:

```bash
cd pos_web_benchmark

# Run complete benchmark with 5 iterations per endpoint across all tiers
python3 auto_runner.py --runs 5 --tier all

# Run specific tier (e.g. general)
python3 auto_runner.py --runs 3 --tier general

# Run specific suite (e.g. GET with index)
python3 auto_runner.py --suite get_with_index --runs 3

# Filter by language or framework
python3 auto_runner.py --lang python --runs 3
python3 auto_runner.py --framework fiber --runs 3
```

#### Manual Suite Execution
```bash
# 1. GET (With Index) in Docker
cd pos_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all --runs 3

# 2. GET (With Index) in Bare-Metal
cd pos_web_benchmark/GET/get_with_index
python3 run_bme_wrk.py --tier all --runs 3

# 3. POST in Docker
cd pos_web_benchmark/POST
python3 run_dkr_wrk.py --tier all --runs 3

# 4. POST in Bare-Metal
cd pos_web_benchmark/POST
python3 run_bme_wrk.py --tier all --runs 3
```

---

### Step 3: Generating Reports & Comparisons

```bash
# Generate Markdown & CSV summaries
cd pos_web_benchmark/results
python3 generate_summary.py
python3 export_csv.py
python3 export_excel.py

# Compare ranking for any result file
cd pos_web_benchmark
python3 compare_results.py results/get_with_index_dkr.json
```

---

## Benchmark Results: PostgreSQL 11.11M Dataset (POC Tier)

### 1. Executive Performance Summary

All benchmarks executed with **11,110,000 total records** in PostgreSQL 16 under POC concurrency (`-t2 -c20 -d30s`) in Docker containerized environment.

| Language | Framework | GET 1table (Req/s) | GET 4join (Req/s) | POST 1table (Req/s) | POST 4table (Req/s) | Error Count |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PHP** | Swoole | **22,522.87** (0.90ms) | 2,632.64 (7.61ms) | 27,518.46 (0.75ms) | 8,773.15 (2.29ms) | **0** |
| **Node.js** | Fastify | **9,837.01** (2.13ms) | 2,032.21 (9.86ms) | 28,300.84 (0.82ms) | 8,495.46 (2.38ms) | **0** |
| **Java** | Spring Boot | **9,782.76** (2.09ms) | **2,861.28** (6.99ms) | 26,542.69 (0.78ms) | **12,805.47** (1.55ms) | **0** |
| **Go** | Fiber | 4,783.00 (4.15ms) | **3,085.37** (6.48ms) | **31,507.46** (0.63ms) | 10,592.01 (1.88ms) | **0** |
| **Python** | FastAPI | 1,543.17 (12.95ms) | 1,305.66 (15.31ms) | 8,822.72 (2.26ms) | 4,543.08 (4.52ms) | **0** |

---

### 2. The Impact of Secondary Indexes on 10,000,000 Records

Secondary B-tree indexes were evaluated on the high-volume `orders` table (10M rows) joining `customer` (1M rows), `product` (100k rows), and `factory` (10k rows).

| Endpoint | Language | Without Index (Req/s) | With Index (Req/s) | Speedup Ratio ($\times$) | Latency Reduction |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **`/raw/2join`** | **PHP** | 399.17 | **13,006.40** | **32.6×** | 50.59ms $\rightarrow$ **1.55ms** |
| **`/raw/2join`** | **Java** | 466.95 | **9,553.07** | **20.5×** | 42.79ms $\rightarrow$ **2.09ms** |
| **`/raw/2join`** | **Node.js** | 378.83 | **8,682.81** | **22.9×** | 52.72ms $\rightarrow$ **2.32ms** |
| **`/raw/2join`** | **Go** | 436.17 | **5,659.89** | **13.0×** | 45.81ms $\rightarrow$ **3.51ms** |
| **`/raw/2join`** | **Python** | 362.53 | **1,508.03** | **4.2×** | 55.09ms $\rightarrow$ **13.26ms** |
| **`/raw/3join`** | **Java** | 390.99 | **3,580.99** | **9.2×** | 51.10ms $\rightarrow$ **5.58ms** |
| **`/raw/3join`** | **Go** | 379.47 | **3,577.97** | **9.4×** | 52.64ms $\rightarrow$ **5.59ms** |
| **`/raw/4join`** | **Go** | 353.23 | **3,085.37** | **8.7×** | 56.54ms $\rightarrow$ **6.48ms** |
| **`/raw/4join`** | **Java** | 380.42 | **2,861.28** | **7.5×** | 52.49ms $\rightarrow$ **6.99ms** |

*Without foreign key indexes, PostgreSQL performs sequential disk table scans across 10M rows, collapsing throughput to ~350-460 Req/s. With secondary B-tree indexes, execution leverages Index Scans and Memoize nodes, reducing query latency from ~50ms down to 1.5-6.5ms.*

---

### 3. Write / Transactional Insert Rankings (POST)

Atomic relational inserts and multi-table transactions under PostgreSQL 16:

- **Single Table Insert (`/raw/post/1table`)**:
  1. **Go Fiber**: 31,507.46 Req/s (0.63ms latency, $p_{99}$ 1.52ms)
  2. **Node.js Fastify**: 28,300.84 Req/s (0.82ms latency, $p_{99}$ 1.31ms)
  3. **PHP Swoole**: 27,518.46 Req/s (0.75ms latency, $p_{99}$ 1.41ms)
  4. **Java Spring Boot**: 26,542.69 Req/s (0.78ms latency, $p_{99}$ 1.32ms)
  5. **Python FastAPI**: 8,822.72 Req/s (2.26ms latency, $p_{99}$ 3.40ms)

- **4-Table Atomic Transaction (`/raw/post/4table`)**:
  1. **Java Spring Boot**: 12,805.47 Req/s (1.55ms latency, $p_{99}$ 2.35ms)
  2. **Go Fiber**: 10,592.01 Req/s (1.88ms latency, $p_{99}$ 3.72ms)
  3. **PHP Swoole**: 8,773.15 Req/s (2.29ms latency, $p_{99}$ 4.84ms)
  4. **Node.js Fastify**: 8,495.46 Req/s (2.38ms latency, $p_{99}$ 3.59ms)
  5. **Python FastAPI**: 4,543.08 Req/s (4.52ms latency, $p_{99}$ 6.92ms)

> All detailed statistical matrices, raw JSON runs, CSV exports, and the styled Excel report are preserved in [`results/`](results/).

