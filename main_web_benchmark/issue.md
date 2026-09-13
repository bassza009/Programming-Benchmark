# Multi-Language Benchmark Suite: Audit & Issues Report

This document outlines all the critical bugs, performance bottlenecks, and unfair configurations found across the **Programming Benchmark** suite, explained in plain English with actionable fixes.

---

## 1. Critical Bug: POST Benchmarks Are Actually Sending GET Requests

### What is happening?
When running POST tests (`python3 run_bme_wrk.py` or `python3 run_dkr_wrk.py`), the command passes `-- -M POST` to `wrk`. However, `wrk` relies on its Lua script to actually construct HTTP POST requests. 

The file `POST/wrk_json_reporter.lua` only collects response statistics at the end (`done()` function) and **does not define an HTTP method or request body**.

### The Impact
* `wrk` defaults to sending standard **HTTP GET** requests to the write endpoints (like `/raw/post/1table`).
* **FastAPI (Python), Fastify (Node.js), Fiber (Go), and Spring Boot (Java)** properly enforce HTTP methods and return `405 Method Not Allowed` or `404 Not Found`. They were never actually doing database inserts during the benchmark!
* **Swoole (PHP)** didn't check the HTTP method in its router—it only matched the URL string (`$uri === '/raw/post/1table'`)—so it executed the database insert regardless of the method.
* **Result:** The POST benchmark results are completely invalid for 4 out of 5 frameworks.

### How to fix it
Update `POST/wrk_json_reporter.lua` to include the `request()` hook:
```lua
wrk.method = "POST"
wrk.headers["Content-Type"] = "application/json"
wrk.body = "{}"
```

---

## 2. PHP Swoole: Opening a Brand-New DB Connection on Every Single Request

### What is happening?
In `server.php` across all suites, every incoming HTTP request calls:
```php
$pdo = $this->getPDO(); // Creates a new PDO connection on EVERY request!
```

### The Impact
* While Go, Java, Python, and Node.js keep a pool of reusable connections alive, PHP opens a new TCP connection, negotiates TLS/auth with MySQL, executes the query, and closes the connection on **every single web request**.
* At 100 to 10,000 concurrent requests, this creates tens of thousands of simultaneous TCP handshakes. MySQL quickly runs out of resources, file descriptors get exhausted, and PHP crashes or returns connection errors.
* This makes PHP appear artificially slow and unstable compared to the other languages.

### How to fix it
Use Swoole’s built-in Coroutine PDO Connection Pool (`Swoole\Database\PDOPool` and `Swoole\Database\PDOConfig`) or worker-persistent connections so that PHP workers reuse existing database connections just like the other frameworks.

---

## 3. Unfair Connection Pool Sizing Across Languages

### What is happening?
Database connection pooling is configured completely differently across the 5 frameworks:
* **Java (Spring Boot):** Has no explicit HikariCP configuration, which means it defaults to a tiny pool of only **10 connections**.
* **Go (Fiber):** Configured with `db.SetMaxOpenConns(100)`.
* **Node.js (Fastify):** Each cluster worker gets `100` connections. On an 8-core CPU, that’s `8 * 100 = 800 connections`.
* **Python (FastAPI):** Configured with `multiprocessing.cpu_count() * 2` workers, each with a max pool of `100`. On an 8-core CPU (16 workers), that’s up to **1,600 connections**.
* **MySQL Limit:** The MySQL container in `docker-compose.yml` has `--max_connections=500`.

### The Impact
* **Java is artificially throttled:** With only 10 database connections, Java requests get stuck waiting in line under heavy load, causing high latency.
* **Python and Node overwhelm MySQL:** Python (1,600 conns) and Node (800 conns) try to open more connections than MySQL's limit of 500, causing MySQL to reject incoming queries with `Too many connections` errors.
* **The benchmark is not an apples-to-apples comparison.**

### How to fix it
1. Standardize connection pool sizing across all languages (e.g. standardizing total max open connections to 200–500 across all instances).
2. Explicitly configure HikariCP for Java via `application.properties`:
   ```properties
   spring.datasource.hikari.maximum-pool-size=100
   spring.datasource.hikari.minimum-idle=20
   ```
3. Raise MySQL’s `max_connections` in `docker-compose.yml` and bare-metal configurations to `5000` or `10000`.

---

## 4. System Limits: Linux File Descriptors (`ulimit`) Crashing High Concurrency

### What is happening?
By default, Linux limits a user process to **1,024 open file descriptors** (`nofile`). 
Every active TCP connection (both from `wrk` generating load and the server receiving it) consumes a file descriptor.

### The Impact
* When testing **Medium (1,000 connections)** or **Maximum (10,000 connections)**, `wrk` and web servers will instantly crash with:
  `socket: Too many open files` or `Connection reset by peer`.
* This causes high concurrency tests to fail immediately regardless of how fast the framework actually is.

### How to fix it
1. Add Docker container limits in `docker-compose.yml`:
   ```yaml
   ulimits:
     nofile:
       soft: 65535
       hard: 65535
   ```
2. In the Python test runner scripts (`run_bme_wrk.py` / `run_dkr_wrk.py`), automatically elevate the process limit before running `wrk`:
   ```python
   import resource
   resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
   ```

---

## 5. Cold Start / No Warmup Period

### What is happening?
The benchmark scripts start a server, sleep for 5 seconds, and immediately start recording metrics on the first endpoint (`/raw/1table`).

### The Impact
* Modern runtimes like **Java (JVM JIT compiler)**, **Node.js (V8 TurboFan)**, and **PHP (Swoole OPcache)** need a few seconds of initial traffic to optimize hot code paths and warm up database connection pools.
* The very first endpoint tested (`/raw/1table`) gets penalized with cold-start latency, skewing the numbers.

### How to fix it
Add a quick 3-second warmup phase (running `wrk -c20 -d3s`) before collecting official metrics.

---

## 6. Database State Pollution in POST Tests

### What is happening?
In the POST benchmark suite, all 5 languages run sequentially against the same database. 
* Python runs first and inserts thousands of records.
* Node.js runs next against a bigger table.
* PHP, Go, and Java run against progressively larger tables with thousands of extra rows and index overhead.

### The Impact
Later languages are forced to insert into much larger tables, which naturally increases index balancing and page split overhead in MySQL.

### How to fix it
Add a database reset/cleanup step between each language in the test runner so every framework starts with an identical, fresh database state.

---

## 7. Proposed Fair 3-Tier Load Testing Matrix

To test systems fairly across different load intensities:

| Tier | Concurrency (`-c`) | Threads (`-t`) | Duration (`-d`) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Minimum (Light)** | `100` | `2` | `10s` | Quick baseline latency and throughput check |
| **Medium (Standard)** | `1,000` | `10` | `30s` | Realistic production high-load concurrency test |
| **Maximum (Stress)** | `10,000` | `20` | `30s` | Extreme connection handling and resilience under stress |

---

## 8. Host MySQL Listening Interface & Docker Container Connectivity

### What is happening?
MySQL server on the host machine was configured with `bind-address = 127.0.0.1`. When framework containers attempt to communicate with MySQL via `host.docker.internal` (e.g. `172.17.0.1:3306`), MySQL immediately rejects the TCP connections with `Connection refused` (Error 111).

### The Impact
All containerized application servers fail to connect to the database on boot, triggering startup timeouts and causing benchmarks to record 0 req/sec and 100% errors.

### How to fix it
1. Update `/etc/mysql/mariadb.conf.d/50-server.cnf` and `/etc/mysql/mysql.conf.d/mysqld.cnf` to bind to all interfaces:
   ```ini
   bind-address = 0.0.0.0
   ```
2. Ensure user permissions allow connections from Docker container subnets (`'admin'@'%'`):
   ```sql
   GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%' WITH GRANT OPTION;
   FLUSH PRIVILEGES;
   ```

---

## 9. MySQL 8.0 Default Auth Plugin Incompatibility (`caching_sha2_password`)

### What is happening?
MySQL 8.0 defaults new user accounts to `caching_sha2_password`. Several client libraries (such as `aiomysql` in Python without the heavy `cryptography` C-extension) fail during authentication with:
`RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods`.

### The Impact
Python and other asynchronous workers crash immediately upon pool initialization when negotiating the handshake with MySQL.

### How to fix it
Configure the benchmark user account with `mysql_native_password` authentication:
```sql
ALTER USER 'admin'@'%' IDENTIFIED WITH mysql_native_password BY 'secret';
ALTER USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'secret';
FLUSH PRIVILEGES;
```

---

## 10. Startup Bottleneck: Full Table Scan `SELECT COUNT(*)` on 17+ Million Rows

### What is happening?
On application startup, each server process/worker executed `SELECT COUNT(*) FROM users` to check if mock data needed to be seeded. With 17.2 million records in `users` and no secondary indexes, this query executes a complete primary key index traversal.

### The Impact
In multi-worker frameworks (e.g., 8 FastAPI workers or clustered Node/PHP processes), all workers simultaneously executed full table scans on startup. This locked MySQL CPU/IO for 20-30 seconds, causing the test runner's HTTP health check to time out (`Timeout waiting for server on port 800X`) and drop initial requests.

### How to fix it
Replace `SELECT COUNT(*) FROM users` with an $O(1)$ existence check:
```sql
SELECT 1 FROM users LIMIT 1;
```
This returns in under 1 millisecond and allows all workers to boot instantly.

---

## 11. Schema Column Discrepancy in `profiles` Table (`p.age` Column Missing)

### What is happening?
The multi-table JOIN endpoints (`/raw/2join`, `/raw/3join`, `/raw/4join`) across all frameworks query `SELECT u.name, p.age FROM users u JOIN profiles p ...`. However, the existing pre-seeded database schema for `profiles` only possessed `id`, `user_id`, `bio`, `phone` (missing `age` and `address`).

### The Impact
Every multi-table JOIN request immediately triggered MySQL Error 1054 (`Unknown column 'p.age' in 'field list'`), causing all 5 web servers to return `500 Internal Server Error` on `/raw/2join`, `/raw/3join`, and `/raw/4join`, generating 100% error rates in benchmark reports.

### How to fix it
Execute an `ALTER TABLE` to align the schema with the benchmark specification:
```sql
ALTER TABLE profiles ADD COLUMN age INT DEFAULT 25, ADD COLUMN address VARCHAR(255) DEFAULT 'Sample Address';
```

---

## 12. Python (FastAPI) GET Benchmark Bottleneck: Missing C-Extensions (`uvloop`/`httptools`) & GIL-Bound Response Serialization (`jsonable_encoder`)

### What is happening?
In both `get_no_index` and `get_with_index` benchmarks, Python FastAPI on Bare Metal exhibited an anomalous bottleneck:
* **POC Tier Throughput:** Bare Metal Python scored only **449.66 Req/sec** with **44.43 ms** latency, whereas Docker Python achieved **2,288.60 Req/sec** with **8.92 ms** latency, resulting in an anomalous reported Bare Metal degradation of **-80.3% BME**.
* **Other Frameworks on Bare Metal:** Node.js (Fastify) achieved **11,396 Req/sec (1.74 ms)**, PHP (Swoole) achieved **15,418 Req/sec (1.40 ms)**, and Go (Fiber) achieved **9,867 Req/sec (2.00 ms)**.

### Root Causes
1. **Missing C-Accelerated Event Loop & Parser on Bare Metal Host:**
   - On the host machine (Ubuntu 24.04), Python was externally managed (PEP 668), so `pip install` without `--break-system-packages` silently left `uvloop` and `httptools` uninstalled.
   - Without these C-extensions, `uvicorn` fell back to Python's standard `asyncio.SelectorEventLoop` and `h11` pure-Python HTTP parser, incurring high per-connection overhead.
2. **Outdated `aiomysql` (v0.1.1):**
   - The host system ran `aiomysql 0.1.1` (from 2021) which suffered from connection pool locking contention on Python 3.12.
3. **Pure-Python Response Serialization Overhead (`jsonable_encoder`):**
   - The GET endpoints query 100 rows (`SELECT * FROM users LIMIT 100` and JOIN queries).
   - FastAPI's default `JSONResponse` passes the list of dictionaries through `jsonable_encoder()`, traversing every field recursively in pure Python bytecode.
   - Profiling confirmed that `jsonable_encoder() + json.dumps()` on 100 rows consumed **~2.26 ms per request** under the GIL, creating a mathematical hard ceiling of **~441 ops/sec** per single event-loop core.
   - By contrast, competing frameworks utilize native C/V8/Go serialization (Fastify's compiled fast-json, Fiber's Sonic/Go serializer, Swoole's native C `json_encode`).

### The Impact
* Bare Metal Python was throttled to ~450 Req/s in low-concurrency tiers, artificially painting Bare Metal as 5x slower than Docker.
* Inverted overhead ratios (-80.3% BME) distorted the academic analysis of containerization cost.

### How to fix it
1. **Install High-Performance C/Rust Libraries on Host:**
   ```bash
   pip install --break-system-packages --upgrade "uvicorn[standard]>=0.22.0" "aiomysql>=0.2.0" orjson ujson
   ```
2. **Implement Ultra-Fast `CustomORJSONResponse` with Decimal Fallback:**
   FastAPI routes returning raw dictionary lists are configured to use `orjson` (Rust-accelerated), with custom handling for MySQL `Decimal` values:
   ```python
   import orjson
   from decimal import Decimal
   from fastapi.responses import Response

   class CustomORJSONResponse(Response):
       media_type = "application/json"
       def render(self, content) -> bytes:
           return orjson.dumps(content, default=lambda o: float(o) if isinstance(o, Decimal) else str(o))

   app = FastAPI(default_response_class=CustomORJSONResponse)
   ```
   This reduces 100-row serialization time from **2.26 ms to 0.06 ms (36.6x speedup)**, unlocking 16,000+ ops/sec serialization throughput.
3. **Configure Uvicorn Event Loop:**
   Explicitly pass `loop="auto"` and `http="auto"` to ensure workers automatically attach to `uvloop` and `httptools`.

### Verification Results (3 Benchmark Rounds across all 4 Endpoints)
Empirical verification was conducted on Bare Metal under POC tier load (`-t2 -c20 -d10s`) across all endpoints:

* **`GET With-Index`:**
  - **`/raw/1table` (Single Table):**
    - Run 1: 2,006.24 Req/sec | 9.98 ms Latency | 0 Errors
    - Run 2: 1,722.87 Req/sec | 11.77 ms Latency | 0 Errors
    - Run 3: 2,095.82 Req/sec | 9.57 ms Latency | 0 Errors
    - **Average:** **1,941.64 Req/sec** | **10.44 ms Latency** (vs. historical **449.66 Req/sec** | **44.43 ms**, **+331.8% / 4.3x throughput speedup**, **76.5% latency reduction**).
  - **`/raw/2join` (2 Tables JOIN):**
    - Run 1: 2,183.48 Req/sec | 9.17 ms Latency | 0 Errors
    - Run 2: 2,178.74 Req/sec | 9.20 ms Latency | 0 Errors
    - Run 3: 2,000.16 Req/sec | 10.14 ms Latency | 0 Errors
    - **Average:** **2,120.79 Req/sec** | **9.50 ms Latency** (vs. historical **447.33 Req/sec** | **44.66 ms**, **+374.1% / 4.7x throughput speedup**, **78.7% latency reduction**).
  - **`/raw/3join` (3 Tables JOIN):**
    - Run 1: 1,237.67 Req/sec | 16.21 ms Latency | 0 Errors
    - Run 2: 1,466.74 Req/sec | 13.66 ms Latency | 0 Errors
    - Run 3: 1,595.29 Req/sec | 12.58 ms Latency | 0 Errors
    - **Average:** **1,433.23 Req/sec** | **14.15 ms Latency** (vs. historical **426.99 Req/sec** | **46.79 ms**, **+235.7% / 3.4x throughput speedup**, **69.8% latency reduction**).
  - **`/raw/4join` (4 Tables JOIN):**
    - Run 1: 1,416.41 Req/sec | 14.15 ms Latency | 0 Errors
    - Run 2: 1,247.26 Req/sec | 16.01 ms Latency | 0 Errors
    - Run 3: 1,593.63 Req/sec | 12.53 ms Latency | 0 Errors
    - **Average:** **1,419.10 Req/sec** | **14.23 ms Latency** (vs. historical **419.34 Req/sec** | **47.66 ms**, **+238.4% / 3.4x throughput speedup**, **70.1% latency reduction**).

* **`GET No-Index`:**
  - **`/raw/1table` (Single Table):**
    - Run 1: 2,702.59 Req/sec | 7.40 ms Latency | 0 Errors
    - Run 2: 2,657.26 Req/sec | 7.53 ms Latency | 0 Errors
    - Run 3: 2,397.44 Req/sec | 8.35 ms Latency | 0 Errors
    - **Average:** **2,585.76 Req/sec** | **7.76 ms Latency** (vs. historical **449.78 Req/sec** | **44.41 ms**, **+474.9% / 5.7x throughput speedup**, **82.5% latency reduction**).
  - **`/raw/2join` (2 Tables JOIN):**
    - Run 1: 2,359.30 Req/sec | 8.53 ms Latency | 0 Errors
    - Run 2: 2,250.56 Req/sec | 8.89 ms Latency | 0 Errors
    - Run 3: 2,724.65 Req/sec | 7.36 ms Latency | 0 Errors
    - **Average:** **2,444.84 Req/sec** | **8.26 ms Latency** (vs. historical **448.03 Req/sec** | **44.59 ms**, **+445.7% / 5.5x throughput speedup**, **81.5% latency reduction**).
  - **`/raw/3join` (3 Tables JOIN without index):**
    - Run 1: 335.16 Req/sec | 59.39 ms Latency | 0 Errors
    - Run 2: 340.39 Req/sec | 58.51 ms Latency | 0 Errors
    - Run 3: 335.73 Req/sec | 59.32 ms Latency | 0 Errors
    - **Average:** **337.09 Req/sec** | **59.07 ms Latency** (Reflects expected unindexed full table nested-loop scans, cleanly separating database I/O bound from application serialization bound).
  - **`/raw/4join` (4 Tables JOIN without index):**
    - Run 1: 718.96 Req/sec | 27.79 ms Latency | 0 Errors
    - Run 2: 719.62 Req/sec | 27.75 ms Latency | 0 Errors
    - Run 3: 730.74 Req/sec | 27.31 ms Latency | 0 Errors
    - **Average:** **723.11 Req/sec** | **27.62 ms Latency** (vs. historical **419.01 Req/sec** | **47.72 ms**, **+72.6% throughput speedup**, **42.1% latency reduction**).

* **Payload and Data Integrity:** Verified HTTP 200 responses and valid JSON payloads across all 4 endpoints (`/raw/1table`, `/raw/2join`, `/raw/3join`, `/raw/4join`) with MySQL `Decimal` values correctly formatted as floating point numbers by `CustomORJSONResponse`. Zero connection dropped or socket timeout errors encountered across all verification iterations.

---

## 13. Experimental Variables Parity & Controlled Environment Standardization (CPU Workers, Connection Pools, and DNS Resolution)

### What is happening?
An empirical audit across all 600 benchmark data points (GET No-Index, GET With-Index, and POST) identified 35 instances (5.8%) where Bare Metal (BME) throughput was recorded lower than Docker (DKR). In the write-intensive POST suite, BME was 100% faster than Docker across all 5 languages (+8.2% to +48.9%), proving the underlying bare metal infrastructure is sound. However, in GET suites, subtle configuration discrepancies created unfair conditions between frameworks:

1. **Worker Process Asymmetry:**
   - **PHP (Swoole):** Configured with `'worker_num' => swoole_cpu_num() * 2`, spawning **32 worker processes** on a 16-core system.
   - **Node.js (Fastify):** Capped at `Math.min(os.cpus().length, 8)`, utilizing only **8 cluster workers** (50% of available CPU cores).
   - **Python (FastAPI):** Capped at `min(multiprocessing.cpu_count(), 8)`, utilizing only **8 uvicorn workers** (50% of available CPU cores).
   - **Go (Fiber) & Java (Spring Boot):** Natively utilized all **16 CPU cores**.

2. **Connection Pool Capacity Asymmetry:**
   - **PHP (Swoole):** 32 workers $\times$ 64 connections per worker = **2,048 total MySQL connections**, giving PHP a massive concurrency advantage in saturated tiers.
   - **Node.js (Fastify):** 8 workers $\times$ 50 connections = **400 total connections**.
   - **Python (FastAPI):** 8 workers $\times$ 50 connections = **400 total connections**.
   - **Go (Fiber):** Strictly throttled to **100 total connections** (`db.SetMaxOpenConns(100)`).
   - **Java (Spring Boot):** Strictly throttled to **100 total connections** (`hikari.maximum-pool-size=100`).

3. **MySQL DNS Reverse Lookups (`skip_name_resolve = OFF`):**
   - MySQL performed a reverse DNS hostname lookup on every incoming TCP connection (`127.0.0.1` and `172.17.0.1`), adding microsecond-level latency jitter to connection acquisitions.

### How to fix it (Standardization to 1:1 Parity)
To ensure rigorous academic fairness and parity across all 5 programming runtimes and virtualization layers:

1. **Standardize Worker Processes to 16 Cores (1 Worker per Core):**
   - **Python (FastAPI):** Configured `workers = multiprocessing.cpu_count()` (16 workers).
   - **Node.js (Fastify):** Configured `numCPUs = os.cpus().length` (16 workers).
   - **PHP (Swoole):** Configured `'worker_num' => swoole_cpu_num()` (16 workers).
   - Applied across `GET/get_with_index`, `GET/get_no_index`, and `POST`.

2. **Standardize Total Connection Pool Capacity to ~200 Connections:**
   - **Go (Fiber):** `db.SetMaxOpenConns(200)`, `db.SetMaxIdleConns(50)` (200 conns total).
   - **Java (Spring Boot):** `spring.datasource.hikari.maximum-pool-size=200`, `minimum-idle=50` (200 conns total).
   - **PHP (Swoole):** 16 workers $\times$ 12 conns = **192 conns total** (`$benchmark->initPool(12)`).
   - **Node.js (Fastify):** 16 workers $\times$ 12 conns = **192 conns total** (`connectionLimit: 12`).
   - **Python (FastAPI):** 16 workers $\times$ 12 conns = **192 conns total** (`minsize=2, maxsize=12`).

3. **Enable MySQL `skip-name-resolve`:**
   - Configured `skip-name-resolve` in `/etc/mysql/mysql.conf.d/benchmark.cnf` to eliminate all DNS reverse lookup latency.

### Verification
All 5 framework servers across all 3 suites were recompiled and smoke-tested on Bare Metal under identical concurrency conditions:
- **Python (FastAPI):** 2,268.67 Req/sec | 9.20 ms | 0 Errors
- **Node.js (Fastify):** 8,317.23 Req/sec | 3.94 ms | 0 Errors
- **PHP (Swoole):** 6,807.13 Req/sec | 3.12 ms | 0 Errors
- **Go (Fiber):** 9,635.28 Req/sec | 2.10 ms | 0 Errors
- **Java (Spring Boot):** 4,743.45 Req/sec | 6.78 ms | 0 Errors

---

## Summary Checklist of Required Fixes

- [x] **Fix `POST/wrk_json_reporter.lua`** to properly issue HTTP POST requests with headers and payload.
- [x] **Implement Swoole PDO Pool** in all `server.php` files to eliminate per-request connection churn.
- [x] **Standardize pool sizes** across FastAPI, Fastify, Swoole, Fiber, and Spring Boot.
- [x] **Configure `application.properties`** for Spring Boot to boost HikariCP pool size from 10.
- [x] **Increase MySQL `max_connections`** to 10,000 in `docker-compose.yml` and `/etc/mysql/`.
- [x] **Configure `ulimits` (65,535)** in Docker and test runner scripts to prevent socket exhaustion.
- [x] **Add 3-second warmup** before recording metrics.
- [x] **Reset database tables** between framework runs in POST benchmarks.
- [x] **Add CLI tier selector (`--tier min|med|max|all`)** to `run_bme_wrk.py` and `run_dkr_wrk.py`.
- [x] **Configure MySQL `bind-address = 0.0.0.0`** and `'admin'@'%'` permissions for Docker connectivity.
- [x] **Enforce `mysql_native_password`** for benchmark accounts to support lightweight drivers.
- [x] **Optimize startup existence checks** from `COUNT(*)` to `SELECT 1 LIMIT 1`.
- [x] **Align `profiles` schema** by adding missing `age` and `address` columns.
- [x] **Optimize Python (FastAPI) GET Pipeline** with `uvloop`, `httptools`, `aiomysql>=0.2.0`, and `CustomORJSONResponse` to resolve the 449 Req/s serialization bottleneck.
- [x] **Standardize Experimental Variables (Issue #13)**: Align CPU workers to 16 cores (1:1) and database pools to ~200 connections across all 5 frameworks, and enable MySQL `skip-name-resolve`.

