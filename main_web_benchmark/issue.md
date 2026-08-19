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
