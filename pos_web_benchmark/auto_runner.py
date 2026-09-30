#!/usr/bin/env python3
"""
auto_runner.py - Automated Master Benchmark Pipeline for pos_web_benchmark (PostgreSQL)
Orchestrates:
  1. GET (get_no_index): Drops secondary indexes, runs DKR and BME suites
  2. GET (get_with_index): Applies secondary indexes, runs DKR and BME suites
  3. POST: Runs transactional insert benchmarks for DKR and BME suites
  4. Reporting: Generates aggregated SUMMARY.md, SUMMARY.csv, and Excel reports
"""

import argparse
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "db")

PG_HOST = os.getenv("DB_HOST", "127.0.0.1")
PG_PORT = os.getenv("DB_PORT", "5432")
PG_USER = os.getenv("DB_USER", "admin")
PG_PASS = os.getenv("DB_PASS", "secret")
PG_DB = os.getenv("DB_NAME", "benchmark_db")

def run_cmd(cmd, cwd=None):
    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    print(f"\n=======================================================")
    print(f"[AUTO-RUNNER] Executing: {cmd_str}")
    print(f"[AUTO-RUNNER] Working Dir: {cwd or BASE_DIR}")
    print(f"=======================================================\n", flush=True)
    res = subprocess.run(cmd, cwd=cwd or BASE_DIR, shell=isinstance(cmd, str))
    if res.returncode != 0:
        print(f"[AUTO-RUNNER ERROR] Command failed with exit code {res.returncode}", file=sys.stderr)
        return False
    return True

def run_pg_query(sql):
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASS
    cmd = [
        "psql",
        "-h", PG_HOST,
        "-p", str(PG_PORT),
        "-U", PG_USER,
        "-d", PG_DB,
        "-t", "-A",
        "-c", sql
    ]
    return subprocess.run(cmd, env=env, capture_output=True, text=True)

def cleanup_environment():
    """Ensure no leftover benchmark processes or containers occupy ports 8001-8005."""
    print("[AUTO-RUNNER] Cleaning up background processes and network ports (8001-8005)...", flush=True)
    for port in [8001, 8002, 8003, 8004, 8005]:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True)

    for suite_dir in [
        os.path.join(BASE_DIR, "GET", "get_no_index"),
        os.path.join(BASE_DIR, "GET", "get_with_index"),
        os.path.join(BASE_DIR, "POST")
    ]:
        compose_file = os.path.join(suite_dir, "docker-compose.yml")
        if os.path.exists(compose_file):
            subprocess.run(["docker", "compose", "-f", compose_file, "down"], capture_output=True)

    time.sleep(2)

def drop_secondary_indexes():
    """Drop secondary indexes for get_no_index benchmarks."""
    print("[AUTO-RUNNER] Dropping secondary indexes for GET get_no_index...", flush=True)
    drop_sql_file = os.path.join(DB_DIR, "drop_indexes.sql")
    if os.path.exists(drop_sql_file):
        env = os.environ.copy()
        env["PGPASSWORD"] = PG_PASS
        subprocess.run([
            "psql", "-h", PG_HOST, "-p", str(PG_PORT), "-U", PG_USER, "-d", PG_DB, "-f", drop_sql_file
        ], env=env, capture_output=True)
    print("[AUTO-RUNNER] Secondary indexes dropped.")

def add_secondary_indexes():
    """Apply secondary indexes for get_with_index benchmarks."""
    print("[AUTO-RUNNER] Applying secondary indexes for GET get_with_index...", flush=True)
    add_sql_file = os.path.join(DB_DIR, "add_indexes.sql")
    if os.path.exists(add_sql_file):
        env = os.environ.copy()
        env["PGPASSWORD"] = PG_PASS
        subprocess.run([
            "psql", "-h", PG_HOST, "-p", str(PG_PORT), "-U", PG_USER, "-d", PG_DB, "-f", add_sql_file
        ], env=env, capture_output=True)
    print("[AUTO-RUNNER] Secondary indexes created and VACUUM ANALYZE executed.")

def main():
    parser = argparse.ArgumentParser(
        description="Automated Master Benchmark Runner for pos_web_benchmark (PostgreSQL)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("runs_pos", type=int, nargs="?", default=None, help="Number of runs per endpoint (e.g. 5)")
    parser.add_argument("-r", "--runs", type=int, default=None, help="Number of runs per endpoint (default: 5)")
    parser.add_argument("--tier", default="all", choices=["poc", "small", "general", "high", "stress", "all"], help="Load tier to execute")
    parser.add_argument(
        "--suite",
        choices=["all", "get_no_index", "get_with_index", "post", "post_dkr", "post_bme"],
        default="all",
        help="Benchmark suite to execute"
    )
    parser.add_argument("--lang", choices=["python", "py", "node", "nodejs", "js", "php", "go", "golang", "java", "all"], default=None, help="Filter by language")
    parser.add_argument("--framework", "--fw", choices=["fastapi", "fastify", "swoole", "fiber", "springboot", "spring-boot", "spring", "all"], default=None, help="Filter by framework")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase")
    parser.add_argument("--skip-dkr", action="store_true", help="Skip Docker benchmarks")
    parser.add_argument("--skip-bme", action="store_true", help="Skip Bare-Metal benchmarks")
    args = parser.parse_args()

    runs_count = args.runs if args.runs is not None else (args.runs_pos if args.runs_pos is not None else 5)
    common_args = ["--tier", args.tier, "--runs", str(runs_count)]
    if args.lang:
        common_args.extend(["--lang", args.lang])
    if args.framework:
        common_args.extend(["--framework", args.framework])
    if args.no_warmup:
        common_args.append("--no-warmup")

    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: POSTGRESQL AUTOMATED SUITE RUNNER")
    print(f" Suite: {args.suite.upper()} | Tiers: {args.tier.upper()} | Runs/EP: {runs_count}")
    print(f" Target DB: PostgreSQL {PG_HOST}:{PG_PORT}/{PG_DB}")
    print("=================================================================\n", flush=True)

    # 1. GET (get_no_index)
    if args.suite in ["all", "get_no_index"]:
        get_no_idx_dir = os.path.join(BASE_DIR, "GET", "get_no_index")
        drop_secondary_indexes()

        if not args.skip_dkr:
            print("\n>>> STEP: Running GET get_no_index Docker (DKR)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_no_idx_dir)

        if not args.skip_bme:
            print("\n>>> STEP: Running GET get_no_index Bare-Metal (BME)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_no_idx_dir)

    # 2. GET (get_with_index)
    if args.suite in ["all", "get_with_index"]:
        get_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")
        add_secondary_indexes()

        if not args.skip_dkr:
            print("\n>>> STEP: Running GET get_with_index Docker (DKR)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_with_idx_dir)

        if not args.skip_bme:
            print("\n>>> STEP: Running GET get_with_index Bare-Metal (BME)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_with_idx_dir)

    # 3. POST (Write / Transactions)
    if args.suite in ["all", "post", "post_dkr", "post_bme"]:
        post_dir = os.path.join(BASE_DIR, "POST")

        if not args.skip_dkr and args.suite in ["all", "post", "post_dkr"]:
            print("\n>>> STEP: Running POST Docker (DKR)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=post_dir)

        if not args.skip_bme and args.suite in ["all", "post", "post_bme"]:
            print("\n>>> STEP: Running POST Bare-Metal (BME)...", flush=True)
            cleanup_environment()
            run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=post_dir)

    # 4. Generate Summaries, CSVs, and Excel Report
    print("\n>>> Generating PostgreSQL Benchmark Summaries and Reports...", flush=True)
    cleanup_environment()
    results_dir = os.path.join(BASE_DIR, "results")
    if os.path.exists(os.path.join(results_dir, "generate_summary.py")):
        run_cmd(["python3", "generate_summary.py"], cwd=results_dir)
    if os.path.exists(os.path.join(results_dir, "export_csv.py")):
        run_cmd(["python3", "export_csv.py"], cwd=results_dir)
    if os.path.exists(os.path.join(results_dir, "export_excel.py")):
        run_cmd(["python3", "export_excel.py"], cwd=results_dir)

    print("\n=======================================================")
    print(" POSTGRESQL BENCHMARK PIPELINE EXECUTION COMPLETED!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
