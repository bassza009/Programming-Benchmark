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
