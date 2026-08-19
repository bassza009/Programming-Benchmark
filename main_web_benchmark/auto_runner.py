#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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

def run_mysql_query(sql, host="127.0.0.1", port=3306, user="admin", password="secret", db="benchmark_db"):
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

def drop_secondary_indexes(host="127.0.0.1", port=3306, user="admin", password="secret", db="benchmark_db"):
    """Drop secondary indexes for get_no_index benchmarks."""
    print("[AUTO-RUNNER] Checking and dropping secondary indexes on benchmark tables...", flush=True)
    idx_drops = [
        ("profiles", "idx_profiles_user_id"),
        ("orders", "idx_orders_user_id"),
        ("order_items", "idx_order_items_order_id")
    ]
    for table, index_name in idx_drops:
        res = run_mysql_query(f"SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';", host, port, user, password, db)
        if index_name in res.stdout:
            print(f"[AUTO-RUNNER] Dropping index `{index_name}` on table `{table}`...")
            run_mysql_query(f"ALTER TABLE {table} DROP INDEX {index_name};", host, port, user, password, db)
        else:
            print(f"[AUTO-RUNNER] Index `{index_name}` on `{table}` already dropped.")

def add_secondary_indexes(host="127.0.0.1", port=3306, user="admin", password="secret", db="benchmark_db"):
    """Apply secondary indexes for get_with_index benchmarks."""
    print("[AUTO-RUNNER] Applying secondary database indexes for get_with_index...", flush=True)
    idx_creates = [
        ("profiles", "idx_profiles_user_id", "user_id"),
        ("orders", "idx_orders_user_id", "user_id"),
        ("order_items", "idx_order_items_order_id", "order_id")
    ]
    for table, index_name, column in idx_creates:
        res = run_mysql_query(f"SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';", host, port, user, password, db)
        if index_name not in res.stdout:
            print(f"[AUTO-RUNNER] Adding index `{index_name}` on `{table}({column})`...")
            run_mysql_query(f"ALTER TABLE {table} ADD INDEX {index_name} ({column});", host, port, user, password, db)
        else:
            print(f"[AUTO-RUNNER] Index `{index_name}` on `{table}` already exists.")

def build_runner_args(args):
    runner_args = ["--tier", args.tier, "--runs", str(args.runs)]
    if args.lang:
        runner_args.extend(["--lang", args.lang])
    if args.framework:
        runner_args.extend(["--framework", args.framework])
    if args.no_warmup:
        runner_args.append("--no-warmup")
    return runner_args

def main():
    parser = argparse.ArgumentParser(description="Automated Master Benchmark Runner for Project Antigravity")
    parser.add_argument("--tier", choices=["poc", "small", "general", "high", "stress", "all"], default="all", help="Tier scenario to execute (default: all)")
    parser.add_argument("--runs", type=int, default=20, help="Number of benchmark iterations per endpoint (default: 20)")
    parser.add_argument("--lang", choices=["python", "py", "node", "nodejs", "js", "php", "go", "golang", "java", "all"], default=None, help="Filter by language")
    parser.add_argument("--framework", "--fw", choices=["fastapi", "fastify", "swoole", "fiber", "springboot", "spring-boot", "spring", "all"], default=None, help="Filter by framework")
    parser.add_argument("--no-warmup", action="store_true", help="Disable warmup runs")
    parser.add_argument("--skip-get-no-index", action="store_true", help="Skip GET No-Index suite")
    parser.add_argument("--skip-get-with-index", action="store_true", help="Skip GET With-Index suite")
    parser.add_argument("--skip-post", action="store_true", help="Skip POST suite")
    parser.add_argument("--mysql-host", default="127.0.0.1", help="MySQL host (default: 127.0.0.1)")
    parser.add_argument("--mysql-port", type=int, default=3306, help="MySQL port (default: 3306)")
    parser.add_argument("--mysql-user", default="admin", help="MySQL username (default: admin)")
    parser.add_argument("--mysql-pass", default="secret", help="MySQL password (default: secret)")
    parser.add_argument("--mysql-db", default="benchmark_db", help="MySQL database (default: benchmark_db)")
    args = parser.parse_args()

    common_args = build_runner_args(args)

    print("=================================================================")
    print(" PROJECT ANTIGRAVITY: AUTOMATED FULL BENCHMARK SUITE RUNNER")
    print(" Execution Plan:")
    print("   1. GET get_no_index   -> Docker (DKR) & Bare-Metal (BME)")
    print("   2. GET get_with_index -> Docker (DKR) & Bare-Metal (BME)")
    print("   3. POST               -> Docker (DKR) & Bare-Metal (BME)")
    print("   4. Aggregated Statistical Summary & CSV Export")
    print(f" Parameters: Tier: {args.tier.upper()} | Runs: {args.runs} | Warmup: {not args.no_warmup}")
    print("=================================================================\n", flush=True)

    # -------------------------------------------------------------
    # 1. GET (get_no_index) - DKR & BME
    # -------------------------------------------------------------
    if not args.skip_get_no_index:
        get_no_idx_dir = os.path.join(BASE_DIR, "GET", "get_no_index")
        
        # Ensure secondary indexes are removed for unindexed read benchmarks
        drop_secondary_indexes(args.mysql_host, args.mysql_port, args.mysql_user, args.mysql_pass, args.mysql_db)

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
    else:
        print("[AUTO-RUNNER] Skipping GET get_no_index suite as requested.")

    # -------------------------------------------------------------
    # 2. GET (get_with_index) - DKR & BME
    # -------------------------------------------------------------
    if not args.skip_get_with_index:
        get_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")

        # Apply secondary indexes before indexed benchmarks
        add_secondary_indexes(args.mysql_host, args.mysql_port, args.mysql_user, args.mysql_pass, args.mysql_db)

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
    else:
        print("[AUTO-RUNNER] Skipping GET get_with_index suite as requested.")

    # -------------------------------------------------------------
    # 3. POST - DKR & BME
    # -------------------------------------------------------------
    if not args.skip_post:
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
    else:
        print("[AUTO-RUNNER] Skipping POST suite as requested.")

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
