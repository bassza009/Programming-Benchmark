#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "admin"
MYSQL_PASS = "secret"
MYSQL_DB = "benchmark_db"

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

def run_mysql_query(sql, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASS, db=MYSQL_DB):
    cmd = [
        "mysql",
        f"-h{host}",
        f"-P{port}",
        f"-u{user}",
        f"-p{password}",
        db,
        "-e",
        sql
    ]
    return subprocess.run(cmd, capture_output=True, text=True)

def cleanup_environment():
    """Ensure no leftover benchmark processes or containers occupy ports 8001-8005."""
    print("[AUTO-RUNNER] Cleaning up background processes and network ports (8001-8005)...", flush=True)
    for port in [8001, 8002, 8003, 8004, 8005]:
        subprocess.run(["fuser", "-k", f"{port}/tcp"], capture_output=True)
    
    # Tear down any lingering compose stacks across benchmark directories
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
    print("[AUTO-RUNNER] Checking and dropping secondary indexes on benchmark tables...", flush=True)
    idx_drops = [
        ("profiles", "idx_profiles_user_id"),
        ("orders", "idx_orders_user_id"),
        ("order_items", "idx_order_items_order_id")
    ]
    for table, index_name in idx_drops:
        res = run_mysql_query(f"SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';")
        if index_name in res.stdout:
            print(f"[AUTO-RUNNER] Dropping index `{index_name}` on table `{table}`...")
            run_mysql_query(f"ALTER TABLE {table} DROP INDEX {index_name};")
        else:
            print(f"[AUTO-RUNNER] Index `{index_name}` on `{table}` already dropped.")

def add_secondary_indexes():
    """Apply secondary indexes for get_with_index benchmarks."""
    print("[AUTO-RUNNER] Applying secondary database indexes for get_with_index...", flush=True)
    idx_creates = [
        ("profiles", "idx_profiles_user_id", "user_id"),
        ("orders", "idx_orders_user_id", "user_id"),
        ("order_items", "idx_order_items_order_id", "order_id")
    ]
    for table, index_name, column in idx_creates:
        res = run_mysql_query(f"SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';")
        if index_name not in res.stdout:
            print(f"[AUTO-RUNNER] Adding index `{index_name}` on `{table}({column})`...")
            run_mysql_query(f"ALTER TABLE {table} ADD INDEX {index_name} ({column});")
        else:
            print(f"[AUTO-RUNNER] Index `{index_name}` on `{table}` already exists.")

def main():
    parser = argparse.ArgumentParser(
        description="Automated Master Benchmark Runner for Programming Benchmark",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("runs_pos", type=int, nargs="?", default=None, help="Number of benchmark iterations per endpoint (optional positional, e.g. 20)")
    parser.add_argument("-r", "--runs", type=int, default=None, help="Number of benchmark iterations per endpoint (default: 20)")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase before recording metrics")
    args = parser.parse_args()

    runs_count = args.runs if args.runs is not None else (args.runs_pos if args.runs_pos is not None else 20)
    common_args = ["--tier", "all", "--runs", str(runs_count)]
    if args.no_warmup:
        common_args.append("--no-warmup")

    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: AUTOMATED FULL BENCHMARK SUITE RUNNER")
    print(" Execution Plan:")
    print("   1. GET get_no_index   -> Docker (DKR) & Bare-Metal (BME)")
    print("   2. GET get_with_index -> Docker (DKR) & Bare-Metal (BME)")
    print("   3. POST               -> Docker (DKR) & Bare-Metal (BME)")
    print("   4. Aggregated Statistical Summary & CSV Export")
    print(f" Parameters: Runs/Endpoint: {runs_count} | Warmup: {not args.no_warmup} | Tiers: ALL (poc, small, general, high, stress)")
    print("=================================================================\n", flush=True)

    # -------------------------------------------------------------
    # 1. GET (get_no_index) - DKR & BME
    # -------------------------------------------------------------
    get_no_idx_dir = os.path.join(BASE_DIR, "GET", "get_no_index")
    
    # Ensure secondary indexes are removed for unindexed read benchmarks
    drop_secondary_indexes()

    # 1.1 GET get_no_index Docker (DKR)
    print("\n\n>>> STEP 1/6: Running GET get_no_index Docker (DKR)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_no_idx_dir):
        print("[!] Warning: GET No-Index Docker benchmark encountered errors, continuing...", file=sys.stderr)

    # 1.2 GET get_no_index Bare-Metal (BME)
    print("\n\n>>> STEP 2/6: Running GET get_no_index Bare-Metal (BME)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_no_idx_dir):
        print("[!] Warning: GET No-Index Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 2. GET (get_with_index) - DKR & BME
    # -------------------------------------------------------------
    get_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")

    # Apply secondary indexes before indexed benchmarks
    add_secondary_indexes()

    # 2.1 GET get_with_index Docker (DKR)
    print("\n\n>>> STEP 3/6: Running GET get_with_index Docker (DKR)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_with_idx_dir):
        print("[!] Warning: GET With-Index Docker benchmark encountered errors, continuing...", file=sys.stderr)

    # 2.2 GET get_with_index Bare-Metal (BME)
    print("\n\n>>> STEP 4/6: Running GET get_with_index Bare-Metal (BME)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_with_idx_dir):
        print("[!] Warning: GET With-Index Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 3. POST - DKR & BME
    # -------------------------------------------------------------
    post_dir = os.path.join(BASE_DIR, "POST")

    # 3.1 POST Docker (DKR)
    print("\n\n>>> STEP 5/6: Running POST Docker (DKR)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=post_dir):
        print("[!] Warning: POST Docker benchmark encountered errors, continuing...", file=sys.stderr)

    # 3.2 POST Bare-Metal (BME)
    print("\n\n>>> STEP 6/6: Running POST Bare-Metal (BME)...", flush=True)
    cleanup_environment()
    if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=post_dir):
        print("[!] Warning: POST Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 4. Generate Summaries & CSVs
    # -------------------------------------------------------------
    print("\n\n>>> STEP 7: Generating Aggregated Summaries and Matrices...", flush=True)
    cleanup_environment()
    results_dir = os.path.join(BASE_DIR, "results")
    run_cmd(["python3", "generate_summary.py"], cwd=results_dir)
    run_cmd(["python3", "export_csv.py"], cwd=results_dir)

    print("\n=======================================================")
    print(" ALL 6 BENCHMARK SUITES & SUMMARIES COMPLETED SUCCESSFULLY!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
