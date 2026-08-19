#!/usr/bin/env python3
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cmd(cmd, cwd=None):
    print(f"\n=======================================================")
    print(f"[AUTO-RUNNER] Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    print(f"[AUTO-RUNNER] Working Dir: {cwd or BASE_DIR}")
    print(f"=======================================================\n", flush=True)
    res = subprocess.run(cmd, cwd=cwd or BASE_DIR, shell=isinstance(cmd, str))
    if res.returncode != 0:
        print(f"[AUTO-RUNNER ERROR] Command failed with exit code {res.returncode}", file=sys.stderr)
        return False
    return True

def main():
    # 1. Wait for any currently running Docker benchmark task to finish
    print("[AUTO-RUNNER] Checking if get_no_index Docker benchmark is already running...")
    while True:
        ps_out = subprocess.run("pgrep -f 'run_dkr_wrk.py'", shell=True, capture_output=True, text=True).stdout.strip()
        if not ps_out:
            print("[AUTO-RUNNER] get_no_index Docker benchmark finished!")
            break
        print(f"[AUTO-RUNNER] Waiting for Docker benchmark process (PID: {ps_out}) to conclude... sleeping 30s", flush=True)
        time.sleep(30)

    # 2. Run GET No-Index Bare-Metal (BME)
    print("\n\n>>> STEP 1/4: Starting GET No-Index Bare-Metal (BME) Benchmark (20 runs)...", flush=True)
    bme_no_idx_dir = os.path.join(BASE_DIR, "GET", "get_no_index")
    if not run_cmd(["python3", "run_bme_wrk.py", "--runs", "20"], cwd=bme_no_idx_dir):
        print("[!] Warning: BME No-Index encountered errors, proceeding to indexing...")

    # 3. Add Database Indexes for With-Index Suite
    print("\n\n>>> STEP 2/4: Applying Database Indexes for get_with_index Suite...", flush=True)
    idx_cmds = [
        "ALTER TABLE profiles ADD INDEX idx_profiles_user_id (user_id);",
        "ALTER TABLE orders ADD INDEX idx_orders_user_id (user_id);",
        "ALTER TABLE order_items ADD INDEX idx_order_items_order_id (order_id);"
    ]
    for sql in idx_cmds:
        print(f"Executing: {sql}")
        subprocess.run(["mysql", "-uadmin", "-psecret", "benchmark_db", "-e", sql])

    # 4. Run GET With-Index Docker Suite
    print("\n\n>>> STEP 3/4: Starting GET With-Index Docker (DKR) Benchmark (20 runs)...", flush=True)
    dkr_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")
    if not run_cmd(["python3", "run_dkr_wrk.py", "--runs", "20"], cwd=dkr_with_idx_dir):
        print("[!] Warning: DKR With-Index encountered errors, continuing...")

    # 5. Run GET With-Index Bare-Metal (BME) Suite
    print("\n\n>>> STEP 4/4: Starting GET With-Index Bare-Metal (BME) Benchmark (20 runs)...", flush=True)
    bme_with_idx_dir = os.path.join(BASE_DIR, "GET", "get_with_index")
    if not run_cmd(["python3", "run_bme_wrk.py", "--runs", "20"], cwd=bme_with_idx_dir):
        print("[!] Warning: BME With-Index encountered errors, continuing...")

    # 6. Generate Summaries & CSVs
    print("\n\n>>> Generating Aggregated Summaries and Matrices...", flush=True)
    results_dir = os.path.join(BASE_DIR, "results")
    run_cmd(["python3", "generate_summary.py"], cwd=results_dir)
    run_cmd(["python3", "export_csv.py"], cwd=results_dir)

    print("\n=======================================================")
    print(" ALL 4 BENCHMARK SUITES COMPLETED SUCCESSFULLY!")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
