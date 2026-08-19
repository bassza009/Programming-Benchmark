---
name: web-benchmark
description: "Use this skill to run, manage, analyze, and compare multi-language web framework benchmarks (FastAPI, Fastify, Swoole, Fiber, Spring Boot) in Docker or Bare Metal across load tiers."
---

# Web Framework Benchmark Suite Skill

This skill provides step-by-step procedures for running, monitoring, and analyzing multi-language web framework benchmarks across Bare Metal and Docker environments.

---

## 1. Remote Server Prerequisites Check

When running on a remote or local environment, verify the system setup:

```bash
# 1. Start / verify local MySQL 8.0 instance on port 3306
# User: admin, Password: secret, Database: benchmark_db
mysql -uadmin -psecret -h127.0.0.1 -e "SELECT 1;"

# 2. Check Docker daemon & Compose (if running Docker mode)
docker info
docker compose version

# 3. Verify / elevate File Descriptor limits (nofile >= 65535)
ulimit -n 65535

# 4. Verify wrk load generator
which wrk || sudo apt-get install -y wrk
```

---

## 2. Benchmark Execution Workflows

### A. Docker Containerized Mode
Docker runs framework containers connecting to the local host MySQL database.

```bash
# GET (No Index) Suite
cd main_web_benchmark/GET/get_no_index
python3 run_dkr_wrk.py --tier all

# GET (With Index) Suite
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all

# POST (Write/Transaction) Suite
cd main_web_benchmark/POST
python3 run_dkr_wrk.py --tier all
```

*Tier & Filter Options:*
* `--tier poc`     : 20 connections, 2 threads, 30s (POC / Small internal system)
* `--tier small`   : 100 connections, 4 threads, 60s (Small production website)
* `--tier general` : 500 connections, 8 threads, 60s (General web application)
* `--tier high`    : 2,000 connections, 8 threads, 120s (High-density website)
* `--tier all`     : Runs all 5 tiers sequentially
* `--lang <name>`  : Run all frameworks under a specific language (e.g. `python`, `go`, `nodejs`, `php`, `java`)
* `--framework <name>` / `--fw <name>`: Run a specific framework (e.g. `fastapi`, `fiber`, `fastify`, `swoole`, `springboot`)
* `--runs N`       : Repeat each benchmark N times and calculate the statistical average (e.g. `--runs 3`)
* `--no-warmup`    : Disable the 3-second warmup phase
* **Outputs**: Averaged results in `bme/dkr_benchmark_results.json` and raw per-iteration logs in `raw_results.json` (and `results/raw_results/`).

---

### B. Bare Metal (BME) Mode

1. Start a local MySQL 8.0 instance on port 3306 with user `admin`, password `secret`, database `benchmark_db`.
2. Run the BME benchmark runner:
```bash
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py --tier all
```

---

## 3. Comparing and Summarizing Results

After running benchmarks, use the comparison script to generate ranking tables:

```bash
cd main_web_benchmark
python3 compare_results.py GET/get_no_index/dkr_benchmark_results.json
```
