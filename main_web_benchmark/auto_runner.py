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
    parser.add_argument("--tier", default="all", help="Tier to execute: poc, small, general, high, stress, all (default: all)")
    parser.add_argument(
        "--suite",
        choices=["post_bme", "all", "get_no_index", "get_with_index", "post", "post_dkr"],
        default="post_bme",
        help="Benchmark suite to execute. Defaults to 'post_bme' for focused POST bare-metal runs."
    )
    parser.add_argument("--all", action="store_true", help="Execute ALL benchmark suites (equivalent to --suite all)")
    parser.add_argument("--lang", choices=["python", "py", "node", "nodejs", "js", "php", "go", "golang", "java", "all"], default=None, help="Filter by language")
    parser.add_argument("--framework", "--fw", choices=["fastapi", "fastify", "swoole", "fiber", "springboot", "spring-boot", "spring", "all"], default=None, help="Filter by framework")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase before recording metrics")
    parser.add_argument("--skip-get-no-index", action="store_true", help="Skip GET No-Index suite")
    parser.add_argument("--skip-get-with-index", action="store_true", help="Skip GET With-Index suite")
    parser.add_argument("--skip-post", action="store_true", help="Skip POST suite")
    parser.add_argument("--skip-dkr", action="store_true", help="Skip Docker benchmarks")
    parser.add_argument("--skip-bme", action="store_true", help="Skip Bare-Metal benchmarks")
    args = parser.parse_args()

    suite_mode = "all" if args.all else args.suite

    runs_count = args.runs if args.runs is not None else (args.runs_pos if args.runs_pos is not None else 20)
    common_args = ["--tier", args.tier, "--runs", str(runs_count)]
    if args.lang:
        common_args.extend(["--lang", args.lang])
    if args.framework:
        common_args.extend(["--framework", args.framework])
    if args.no_warmup:
        common_args.append("--no-warmup")

    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: AUTOMATED BENCHMARK SUITE RUNNER")
    print(f" Mode/Suite: {suite_mode.upper()} (Default: POST BME)")
    print(f" Parameters: Runs/Endpoint: {runs_count} | Warmup: {not args.no_warmup} | Tiers: {args.tier.upper()}")
    print("=================================================================\n", flush=True)

    # Flags to determine which steps to run
    run_get_no_idx = (suite_mode in ["all", "get_no_index"]) and not args.skip_get_no_index
    run_get_with_idx = (suite_mode in ["all", "get_with_index"]) and not args.skip_get_with_index
    run_post_dkr = (suite_mode in ["all", "post", "post_dkr"]) and not args.skip_post and not args.skip_dkr
    run_post_bme = (suite_mode in ["all", "post", "post_bme"]) and not args.skip_post and not args.skip_bme

    # -------------------------------------------------------------
    # 1. GET (get_no_index) - DKR & BME
    # -------------------------------------------------------------
    if run_get_no_idx:
        get_no_idx_dir = os.path.join(BASE_DIR, "GET", "get_no_index")
        drop_secondary_indexes()

        if not args.skip_dkr:
            print("\n\n>>> STEP: Running GET get_no_index Docker (DKR)...", flush=True)
            cleanup_environment()
            if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_no_idx_dir):
                print("[!] Warning: GET No-Index Docker benchmark encountered errors, continuing...", file=sys.stderr)

        if not args.skip_bme:
            print("\n\n>>> STEP: Running GET get_no_index Bare-Metal (BME)...", flush=True)
            cleanup_environment()
            if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_no_idx_dir):
                print("[!] Warning: GET No-Index Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 2. GET (get_with_index) - DKR & BME
    # -------------------------------------------------------------
    if run_get_with_idx:
        get_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")
        add_secondary_indexes()

        if not args.skip_dkr:
            print("\n\n>>> STEP: Running GET get_with_index Docker (DKR)...", flush=True)
            cleanup_environment()
            if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=get_with_idx_dir):
                print("[!] Warning: GET With-Index Docker benchmark encountered errors, continuing...", file=sys.stderr)

        if not args.skip_bme:
            print("\n\n>>> STEP: Running GET get_with_index Bare-Metal (BME)...", flush=True)
            cleanup_environment()
            if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=get_with_idx_dir):
                print("[!] Warning: GET With-Index Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 3. POST - DKR & BME
    # -------------------------------------------------------------
    post_dir = os.path.join(BASE_DIR, "POST")

    if run_post_dkr:
        print("\n\n>>> STEP: Running POST Docker (DKR)...", flush=True)
        cleanup_environment()
        if not run_cmd(["python3", "run_dkr_wrk.py"] + common_args, cwd=post_dir):
            print("[!] Warning: POST Docker benchmark encountered errors, continuing...", file=sys.stderr)

    if run_post_bme:
        print("\n\n>>> STEP: Running POST Bare-Metal (BME)...", flush=True)
        cleanup_environment()
        if not run_cmd(["python3", "run_bme_wrk.py"] + common_args, cwd=post_dir):
            print("[!] Warning: POST Bare-Metal benchmark encountered errors, continuing...", file=sys.stderr)

    # -------------------------------------------------------------
    # 4. Generate Summaries, CSVs, and Styled Excel Report
    # -------------------------------------------------------------
    print("\n\n>>> Generating Aggregated Summaries, CSVs, and Excel Report...", flush=True)
    cleanup_environment()
    results_dir = os.path.join(BASE_DIR, "results")
    run_cmd(["python3", "generate_summary.py"], cwd=results_dir)
    run_cmd(["python3", "export_csv.py"], cwd=results_dir)
    run_cmd(["python3", "export_excel.py"], cwd=results_dir)

    print("\n=======================================================")
    print(" BENCHMARK EXECUTION & SUMMARIES COMPLETED SUCCESSFULLY!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
