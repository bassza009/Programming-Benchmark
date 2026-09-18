#!/usr/bin/env python3
import argparse
import datetime
import json
import math
import os
import resource
import subprocess
import sys
import time
import urllib.request

try:
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(65535, hard if hard > 0 else 65535), hard))
except Exception as e:
    print(f"Warning raising ulimit: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
SCRIPTS_DIR = os.path.join(os.path.dirname(BASE_DIR), "scripts")

T_CRIT_95 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447,  7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    15: 2.131, 19: 2.093, 20: 2.086, 30: 2.042
}

TIERS_FULL_SPEC = {
    "poc": {
        "name": "POC / Small internal system",
        "scenario": "Thesis project, department website prototype",
        "threads": 2,
        "connections": 20,
        "duration": "30s"
    },
    "small": {
        "name": "Small production website",
        "scenario": "Small company local business",
        "threads": 4,
        "connections": 100,
        "duration": "60s"
    },
    "general": {
        "name": "General web application",
        "scenario": "University system e-commerce CMS",
        "threads": 8,
        "connections": 500,
        "duration": "60s"
    },
    "high": {
        "name": "High-density website",
        "scenario": "Popular portals SaaS platforms",
        "threads": 8,
        "connections": 2000,
        "duration": "120s"
    },
    "stress": {
        "name": "Stress testing",
        "scenario": "Find saturation point",
        "threads": 16,
        "connections": 10000,
        "duration": "300s"
    }
}

ENDPOINTS = ["/raw/1table", "/raw/2join", "/raw/3join", "/raw/4join"]

def get_t_crit(n):
    if n <= 1:
        return 1.96
    df = n - 1
    if df in T_CRIT_95:
        return T_CRIT_95[df]
    for k in sorted(T_CRIT_95.keys()):
        if df <= k:
            return T_CRIT_95[k]
    return 1.96

def compute_average_metrics(runs_list):
    if not runs_list:
        return {
            "requests_per_sec": 0.0, "rps_stdev": 0.0, "rps_ci95_margin": 0.0,
            "rps_ci95_low": 0.0, "rps_ci95_high": 0.0, "latency_mean_ms": 0.0,
            "latency_stdev_ms": 0.0, "latency_ci95_margin": 0.0, "latency_ci95_low": 0.0,
            "latency_ci95_high": 0.0, "latency_p50_ms": 0.0, "latency_p90_ms": 0.0,
            "latency_p95_ms": 0.0, "latency_p99_ms": 0.0, "latency_max_ms": 0.0,
            "errors": 0, "runs_count": 0
        }
    n = len(runs_list)
    rps_vals = [r.get("requests_per_sec", 0.0) for r in runs_list]
    lat_vals = [r.get("latency_mean_ms", 0.0) for r in runs_list]
    p50_vals = [r.get("latency_p50_ms", r.get("latency_mean_ms", 0.0)) for r in runs_list]
    p90_vals = [r.get("latency_p90_ms", r.get("latency_mean_ms", 0.0)) for r in runs_list]
    p95_vals = [r.get("latency_p95_ms", r.get("latency_mean_ms", 0.0)) for r in runs_list]
    p99_vals = [r.get("latency_p99_ms", r.get("latency_mean_ms", 0.0)) for r in runs_list]

    avg_rps = sum(rps_vals) / n
    avg_lat = sum(lat_vals) / n
    avg_p50 = sum(p50_vals) / n
    avg_p90 = sum(p90_vals) / n
    avg_p95 = sum(p95_vals) / n
    avg_p99 = sum(p99_vals) / n

    if n > 1:
        rps_stdev = math.sqrt(sum((x - avg_rps) ** 2 for x in rps_vals) / (n - 1))
        lat_stdev = math.sqrt(sum((x - avg_lat) ** 2 for x in lat_vals) / (n - 1))
        t_crit = get_t_crit(n)
        rps_ci_margin = t_crit * (rps_stdev / math.sqrt(n))
        lat_ci_margin = t_crit * (lat_stdev / math.sqrt(n))
    else:
        rps_stdev = 0.0
        lat_stdev = runs_list[0].get("latency_stdev_ms", 0.0)
        rps_ci_margin = 0.0
        lat_ci_margin = 0.0

    max_lat = max((r.get("latency_max_ms", 0.0) for r in runs_list), default=0.0)
    total_errors = sum(r.get("errors", 0) for r in runs_list)

    return {
        "requests_per_sec": round(avg_rps, 2),
        "rps_stdev": round(rps_stdev, 2),
        "rps_ci95_margin": round(rps_ci_margin, 2),
        "rps_ci95_low": round(max(0.0, avg_rps - rps_ci_margin), 2),
        "rps_ci95_high": round(avg_rps + rps_ci_margin, 2),
        "latency_mean_ms": round(avg_lat, 2),
        "latency_stdev_ms": round(lat_stdev, 2),
        "latency_ci95_margin": round(lat_ci_margin, 2),
        "latency_ci95_low": round(max(0.0, avg_lat - lat_ci_margin), 2),
        "latency_ci95_high": round(avg_lat + lat_ci_margin, 2),
        "latency_p50_ms": round(avg_p50, 2),
        "latency_p90_ms": round(avg_p90, 2),
        "latency_p95_ms": round(avg_p95, 2),
        "latency_p99_ms": round(avg_p99, 2),
        "latency_max_ms": round(max_lat, 2),
        "errors": total_errors,
        "runs_count": n
    }

def run_wrk_endpoint(port, ep, lua_script, threads, conns, duration):
    url = f"http://127.0.0.1:{port}{ep}"
    cmd = ["wrk", f"-t{threads}", f"-c{conns}", f"-d{duration}", "-s", lua_script, url]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        stdout = res.stdout.strip()
        j_start = stdout.find("{")
        j_end = stdout.rfind("}") + 1
        if j_start != -1 and j_end > j_start:
            return json.loads(stdout[j_start:j_end])
        return json.loads(stdout)
    except Exception as e:
        print(f"  [!] Error running wrk {ep}: {e}", flush=True)
        return {"requests_per_sec": 0.0, "latency_mean_ms": 0.0, "errors": 1}

def wait_for_port(port, max_retries=40):
    for _ in range(max_retries):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def drop_os_caches():
    try:
        subprocess.run(["sync"], capture_output=True)
        with open("/proc/sys/vm/drop_caches", "w") as f:
            f.write("3\n")
    except Exception:
        pass

def save_checkpoint(target_file, env_type, tier_key, tier_cfg, ep, metrics):
    data = {}
    if os.path.exists(target_file):
        try:
            with open(target_file, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}

    if "Python (opt.)" not in data:
        data["Python (opt.)"] = {"Environment": env_type, "tiers": {}}

    if tier_key not in data["Python (opt.)"]["tiers"]:
        data["Python (opt.)"]["tiers"][tier_key] = {
            "config": tier_cfg,
            "endpoints": {}
        }

    data["Python (opt.)"]["tiers"][tier_key]["endpoints"][ep] = metrics

    with open(target_file, "w") as f:
        json.dump(data, f, indent=2)

def update_readmes_from_summary(repo_root):
    summary_path = os.path.join(RESULTS_DIR, "SUMMARY.md")
    if not os.path.exists(summary_path):
        return
    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_content = f.read()

        if "## Executive Comparison: Docker vs Bare Metal" not in summary_content:
            return
        sec = summary_content.split("## Executive Comparison: Docker vs Bare Metal")[1]
        sec = sec.split("## Suite:")[0].strip()
        table_lines = [line.strip() for line in sec.splitlines() if line.strip().startswith("|") and not line.strip().startswith("| :---")]
        if len(table_lines) < 2:
            return
        data_rows = table_lines[1:]

        # README.md
        readme_path = os.path.join(repo_root, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                t = f.read()
            s = t.find("| Suite | Language | Docker (Req/s ± SD) |")
            e = t.find("*\\*Note on Historical Python GET BME Anomaly:")
            if s != -1 and e != -1:
                new_table = "| Suite | Language | Docker (Req/s ± SD) | Bare Metal (Req/s ± SD) | Docker p50 / p95 (ms) | BME p50 / p95 (ms) | Overhead / Gain |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
                for r in data_rows:
                    cols = [c.strip() for c in r.split("|")[1:-1]]
                    if len(cols) == 7:
                        new_table += f"| {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} | {cols[4]} | {cols[5]} | {cols[6]} |\n"
                t = t[:s] + new_table + "\n" + t[e:]
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(t)

        # README_TH.md
        readme_th_path = os.path.join(repo_root, "README_TH.md")
        if os.path.exists(readme_th_path):
            with open(readme_th_path, "r", encoding="utf-8") as f:
                t_th = f.read()
            s_th = t_th.find("| ชุดทดสอบ | ภาษา | Docker (Req/s ± SD) |")
            e_th = t_th.find("*\\*หมายเหตุเกี่ยวกับความผิดปกติของข้อมูล Python GET บน Bare Metal ในอดีต:")
            if s_th != -1 and e_th != -1:
                new_table_th = "| ชุดทดสอบ | ภาษา | Docker (Req/s ± SD) | Bare Metal (Req/s ± SD) | Docker p50 / p95 (ms) | BME p50 / p95 (ms) | ผลต่าง Overhead / Gain |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n"
                for r in data_rows:
                    cols = [c.strip() for c in r.split("|")[1:-1]]
                    if len(cols) == 7:
                        gain_th = cols[6]
                        if "-" in gain_th:
                            gain_th = gain_th.replace("BME", "Docker สูงกว่า")
                        elif "BME" in gain_th:
                            gain_th = gain_th.replace("BME", "BME เร็วกว่า")
                        new_table_th += f"| {cols[0]} | {cols[1]} | {cols[2]} | {cols[3]} | {cols[4]} | {cols[5]} | {gain_th} |\n"
                t_th = t_th[:s_th] + new_table_th + "\n" + t_th[e_th:]
                with open(readme_th_path, "w", encoding="utf-8") as f:
                    f.write(t_th)
    except Exception as err:
        print(f"[SYNC !] Warning syncing READMEs: {err}", flush=True)

def sync_reports_and_git(commit_message):
    print(f"\n[SYNC] Re-exporting reports and pushing to GitHub...", flush=True)
    try:
        subprocess.run([sys.executable, "export_excel.py"], cwd=RESULTS_DIR, check=True)
        subprocess.run([sys.executable, "generate_summary.py"], cwd=RESULTS_DIR, check=True)
        subprocess.run([sys.executable, "export_csv.py"], cwd=RESULTS_DIR, check=True)
        
        repo_root = os.path.dirname(BASE_DIR)
        update_readmes_from_summary(repo_root)

        sync_script = os.path.join(SCRIPTS_DIR, "sync_benchmark_report.py")
        if os.path.exists(sync_script):
            subprocess.run([sys.executable, sync_script, "--docx"], cwd=SCRIPTS_DIR, capture_output=True)
        
        subprocess.run(["git", "add", "."], cwd=repo_root, capture_output=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_root, capture_output=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=repo_root, capture_output=True)
        print(f"[SYNC ✓] Pushed progress upstream: {commit_message}", flush=True)
    except Exception as e:
        print(f"[SYNC !] Warning during sync: {e}", flush=True)

def benchmark_endpoint(env_name, port, ep, lua_script, t_cfg, runs):
    # Warmup run (3s)
    subprocess.run(["wrk", "-t2", "-c20", "-d3s", "-s", lua_script, f"http://127.0.0.1:{port}{ep}"], capture_output=True)

    runs_data = []
    for r in range(runs):
        run_start = time.time()
        data = run_wrk_endpoint(port, ep, lua_script, t_cfg["threads"], t_cfg["connections"], t_cfg["duration"])
        runs_data.append(data)
        elapsed = time.time() - run_start
        rps = data.get("requests_per_sec", 0.0)
        lat = data.get("latency_mean_ms", 0.0)
        errs = data.get("errors", 0)
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"      [{now_str}] [{env_name}] Run {r+1:>2}/{runs} ({elapsed:>4.1f}s): {rps:>9.2f} Req/s | Latency: {lat:>6.2f} ms | Errors: {errs}", flush=True)
        time.sleep(0.5)

    return compute_average_metrics(runs_data)

def benchmark_tier_dkr(suite_dir, lua_script, target_file, t_key, t_cfg, runs):
    print(f"\n  ---> Starting DOCKER (DKR) Container for Tier {t_key.upper()}...", flush=True)
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)
    drop_os_caches()

    subprocess.run(["docker", "compose", "up", "-d", "server-python"], cwd=suite_dir, check=True)
    if not wait_for_port(8001):
        print(f"  [!] Failed to start Docker container for {t_key}", flush=True)
        subprocess.run(["docker", "compose", "down"], cwd=suite_dir, capture_output=True)
        return False

    print(f"  [✓] Docker container server-python is UP on port 8001", flush=True)
    for ep_idx, ep in enumerate(ENDPOINTS, 1):
        print(f"\n    [DKR] [{t_key.upper()}] Endpoint {ep_idx}/4: {ep} ({runs} runs x {t_cfg['duration']})...", flush=True)
        avg = benchmark_endpoint("DKR", 8001, ep, lua_script, t_cfg, runs)
        print(f"    [DKR ✓] Completed -> Mean: {avg['requests_per_sec']:>9.2f} Req/s | Latency: {avg['latency_mean_ms']:>6.2f} ms | Errors: {avg['errors']}", flush=True)
        save_checkpoint(target_file, "DKR", t_key, t_cfg, ep, avg)

    subprocess.run(["docker", "compose", "stop", "server-python"], cwd=suite_dir, capture_output=True)
    subprocess.run(["docker", "compose", "rm", "-f", "server-python"], cwd=suite_dir, capture_output=True)
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)
    return True

def benchmark_tier_bme(suite_dir, lua_script, target_file, t_key, t_cfg, runs):
    print(f"\n  ---> Starting BARE METAL (BME) Server for Tier {t_key.upper()}...", flush=True)
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)
    drop_os_caches()

    server_cwd = os.path.join(suite_dir, "frameworks", "python", "fastapi")
    proc = subprocess.Popen(["python3", "server.py"], cwd=server_cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not wait_for_port(8001):
        print(f"  [!] Failed to start Bare Metal server for {t_key}", flush=True)
        proc.kill()
        return False

    print(f"  [✓] Bare Metal server is UP on port 8001", flush=True)
    for ep_idx, ep in enumerate(ENDPOINTS, 1):
        print(f"\n    [BME] [{t_key.upper()}] Endpoint {ep_idx}/4: {ep} ({runs} runs x {t_cfg['duration']})...", flush=True)
        avg = benchmark_endpoint("BME", 8001, ep, lua_script, t_cfg, runs)
        print(f"    [BME ✓] Completed -> Mean: {avg['requests_per_sec']:>9.2f} Req/s | Latency: {avg['latency_mean_ms']:>6.2f} ms | Errors: {avg['errors']}", flush=True)
        save_checkpoint(target_file, "BME", t_key, t_cfg, ep, avg)

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)
    return True

def run_suite(suite_dir, lua_script, dkr_file, bme_file, runs=20, selected_tiers=None, env_choice="both"):
    suite_name = os.path.basename(suite_dir)
    print(f"\n=======================================================")
    print(f" Running Suite: {suite_name} (Environment: {env_choice.upper()}, Runs: {runs})")
    print(f" Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=======================================================", flush=True)

    tiers_to_run = selected_tiers or list(TIERS_FULL_SPEC.keys())

    for t_idx, t_key in enumerate(tiers_to_run, 1):
        t_cfg = TIERS_FULL_SPEC[t_key]
        print(f"\n" + ("#" * 70), flush=True)
        print(f" [{suite_name}] TIER {t_idx}/{len(tiers_to_run)}: {t_key.upper()} ({t_cfg['connections']} conns, {t_cfg['duration']}/run, {runs} runs)", flush=True)
        print(f" Scenario: {t_cfg.get('scenario', '')}", flush=True)
        print(("#" * 70), flush=True)

        if env_choice in ["dkr", "both"]:
            benchmark_tier_dkr(suite_dir, lua_script, dkr_file, t_key, t_cfg, runs)

        if env_choice in ["bme", "both"]:
            benchmark_tier_bme(suite_dir, lua_script, bme_file, t_key, t_cfg, runs)

        commit_msg = f"benchmarks: Python (opt.) {suite_name} tier {t_key.upper()} completed ({runs} runs {env_choice.upper()})"
        sync_reports_and_git(commit_msg)

    return True

def main():
    parser = argparse.ArgumentParser(description="Full-Spec 20-Run Benchmark for Python (opt.) DKR & BME")
    parser.add_argument("--runs", "-r", type=int, default=20, help="Number of runs per endpoint (default: 20)")
    parser.add_argument("--tiers", nargs="+", default=None, help="Specific tiers to run (e.g. poc small general high stress)")
    parser.add_argument("--suite", choices=["with_index", "no_index", "all"], default="all", help="Suites to benchmark")
    parser.add_argument("--env", choices=["dkr", "bme", "both"], default="both", help="Environment to benchmark (dkr, bme, both)")
    args = parser.parse_args()

    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: PYTHON (OPT.) FULL-SPEC DKR & BME RUNNER")
    print(f" Planned Config: {args.runs} runs/ep | Env: {args.env.upper()} | Suite: {args.suite.upper()}")
    print("=================================================================", flush=True)

    with_idx_dkr = os.path.join(RESULTS_DIR, "get_with_index_dkr.json")
    with_idx_bme = os.path.join(RESULTS_DIR, "get_with_index_bme.json")
    no_idx_dkr = os.path.join(RESULTS_DIR, "get_no_index_dkr.json")
    no_idx_bme = os.path.join(RESULTS_DIR, "get_no_index_bme.json")

    # 1. Benchmark GET With-Index
    if args.suite in ["with_index", "all"]:
        lua_with_idx = os.path.join(BASE_DIR, "GET", "get_with_index", "wrk_json_reporter.lua")
        dir_with_idx = os.path.join(BASE_DIR, "GET", "get_with_index")

        print("\n[DB] Ensuring secondary indexes exist for With-Index suite...", flush=True)
        subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles ADD INDEX idx_profiles_user_id (user_id); ALTER TABLE orders ADD INDEX idx_orders_user_id (user_id); ALTER TABLE order_items ADD INDEX idx_order_items_order_id (order_id);"], capture_output=True)

        run_suite(dir_with_idx, lua_with_idx, with_idx_dkr, with_idx_bme, runs=args.runs, selected_tiers=args.tiers, env_choice=args.env)

    # 2. Benchmark GET No-Index
    if args.suite in ["no_index", "all"]:
        lua_no_idx = os.path.join(BASE_DIR, "GET", "get_no_index", "wrk_json_reporter.lua")
        dir_no_idx = os.path.join(BASE_DIR, "GET", "get_no_index")

        print("\n[DB] Dropping secondary indexes for No-Index suite...", flush=True)
        subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles DROP INDEX idx_profiles_user_id; ALTER TABLE orders DROP INDEX idx_orders_user_id; ALTER TABLE order_items DROP INDEX idx_order_items_order_id;"], capture_output=True)

        run_suite(dir_no_idx, lua_no_idx, no_idx_dkr, no_idx_bme, runs=args.runs, selected_tiers=args.tiers, env_choice=args.env)

        print("\n[DB] Restoring secondary indexes after No-Index suite...", flush=True)
        subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles ADD INDEX idx_profiles_user_id (user_id); ALTER TABLE orders ADD INDEX idx_orders_user_id (user_id); ALTER TABLE order_items ADD INDEX idx_order_items_order_id (order_id);"], capture_output=True)

    print("\n=================================================================")
    print(f" ALL BENCHMARKS COMPLETED SUCCESSFULLY AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}!")
    print("=================================================================", flush=True)

if __name__ == "__main__":
    main()
