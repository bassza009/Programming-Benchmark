# Multi-Language & Multi-Framework Architecture Guide

This directory organizes all web benchmark servers by **Language** and **Framework** (`<language>/<framework>/`) to provide a standardized, clean, and easily extensible foundation for benchmarking.

---

## 1. Directory Layout

```text
frameworks/
├── go/
│   └── fiber/                 # Go + Fiber (Port 8004)
├── java/
│   └── springboot/            # Java + Spring Boot 3 (Port 8005)
├── nodejs/
│   └── fastify/               # Node.js + Fastify (Port 8002)
├── php/
│   └── swoole/                # PHP + Swoole (Port 8003)
└── python/
    └── fastapi/               # Python + FastAPI (Port 8001)
```

---

## 2. Standard Endpoint Contract

Every framework implementation **must** expose the following unified endpoints to be compatible with the benchmark runner suites:

| HTTP Method | Route | Description | Expected Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Health check endpoint | `{"status": "success", "framework": "<name>"}` |
| `GET` | `/raw/1table` | Single-table read query | `SELECT * FROM users LIMIT 100` |
| `GET` | `/raw/2join` | 2-table relational `JOIN` | `users` ⨝ `profiles` (Limit 100) |
| `GET` | `/raw/3join` | 3-table relational `JOIN` | `users` ⨝ `profiles` ⨝ `orders` (Limit 100) |
| `GET` | `/raw/4join` | 4-table relational `JOIN` | `users` ⨝ `profiles` ⨝ `orders` ⨝ `order_items` (Limit 100) |
| `POST` | `/raw/post/1table` | 1-table atomic insert | Insert into `users`, return `{"user_id": <id>}` |
| `POST` | `/raw/post/2table` | 2-table transaction insert | Insert into `users` + `profiles` |
| `POST` | `/raw/post/3table` | 3-table transaction insert | Insert into `users` + `profiles` + `orders` |
| `POST` | `/raw/post/4table` | 4-table transaction insert | Insert into `users` + `profiles` + `orders` + `order_items` |

---

## 3. Standard Database Configuration

All frameworks read connection settings from environment variables with fallback defaults:

* `DB_HOST`: Hostname or IP of the MySQL server (Default: `127.0.0.1` or `host.docker.internal` in Docker)
* `DB_PORT`: Port number (Default: `3306`)
* `DB_USER`: Username (Default: `admin`)
* `DB_PASS`: Password (Default: `secret`)
* `DB_NAME`: Database name (Default: `benchmark_db`)
* **Connection Pool Settings**: Standardized to `MaxOpen = 50–100`, `MinIdle = 5–20`.

---

## 4. How to Add a New Framework or Language

To add a new language (e.g. `rust`, `csharp`, `elixir`) or a new framework (e.g. `python/flask`, `go/gin`, `nodejs/express`):

1. Create a directory: `frameworks/<language>/<framework>/`
2. Implement the standard endpoints listed in Section 2.
3. Add a `Dockerfile` for containerized execution.
4. Assign a unique port (e.g. `8006`, `8007`, etc.).
5. Run standalone to verify:
   ```bash
   curl http://localhost:<port>/
   curl http://localhost:<port>/raw/1table
   curl -X POST http://localhost:<port>/raw/post/1table
   ```
