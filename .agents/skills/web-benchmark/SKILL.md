---
name: web-benchmark
description: "Use this skill to run, manage, analyze, and compare multi-language web framework benchmarks (FastAPI, Fastify, Swoole, Fiber, Spring Boot) in Docker or Bare Metal across load tiers."
---

# Web Framework Benchmark Suite Skill

This skill provides step-by-step procedures for running, monitoring, and analyzing multi-language web framework benchmarks across Bare Metal and Docker environments.

---

## 1. Remote Server Prerequisites Check

When running on a fresh remote SSH Linux server, verify the system setup:

```bash
# 1. Check Docker daemon & Compose
docker info
docker compose version

# 2. Verify / elevate File Descriptor limits (nofile >= 65535)
ulimit -n 65535

# 3. Verify wrk load generator
which wrk || sudo apt-get install -y wrk
```

---

## 2. Benchmark Execution Workflows

### A. Docker Containerized Mode (Recommended for Remote Servers)
Docker handles dependencies, isolation, and MySQL tuning automatically.

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

*Tier Options:*
* `--tier min` : 100 connections, 2 threads, 10s (Baseline)
* `--tier med` : 1,000 connections, 10 threads, 30s (High-Load)
* `--tier max` : 10,000 connections, 20 threads, 30s (Stress)
* `--tier all` : Runs min, med, and max tiers sequentially

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
