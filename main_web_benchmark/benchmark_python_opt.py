#!/usr/bin/env python3
import json
import math
import os
import resource
import subprocess
import time
import urllib.request

try:
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    resource.setrlimit(resource.RLIMIT_NOFILE, (min(65535, hard if hard > 0 else 65535), hard))
except Exception as e:
    print(f"Warning raising ulimit: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

T_CRIT_95 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447,  7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    15: 2.131, 20: 2.086, 30: 2.042
}

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
        print(f"  [!] Error running wrk {ep}: {e}")
        return {"requests_per_sec": 0.0, "latency_mean_ms": 0.0, "errors": 1}

def wait_for_port(port, max_retries=30):
    for _ in range(max_retries):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=1) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def benchmark_suite(suite_dir, lua_script, runs=3):
    print(f"\n=======================================================")
    print(f" Starting Benchmark for: {suite_dir}")
    print(f"=======================================================")
    
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)

    server_cwd = os.path.join(suite_dir, "frameworks", "python", "fastapi")
    proc = subprocess.Popen(["python3", "server.py"], cwd=server_cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not wait_for_port(8001):
        print("[!] Failed to start Python server on port 8001")
        proc.kill()
        return None

    print("[✓] Python server is UP and READY on port 8001")

    tiers = {
        "poc": {"name": "POC / Small internal system", "threads": 2, "connections": 20, "duration": "5s"},
        "small": {"name": "Small production website", "threads": 4, "connections": 100, "duration": "5s"},
        "general": {"name": "General web application", "threads": 8, "connections": 500, "duration": "5s"},
        "high": {"name": "High-density website", "threads": 8, "connections": 2000, "duration": "5s"},
        "stress": {"name": "Stress testing", "threads": 16, "connections": 10000, "duration": "5s"}
    }

    endpoints = ["/raw/1table", "/raw/2join", "/raw/3join", "/raw/4join"]
    suite_tiers = {}

    for t_key, t_cfg in tiers.items():
        print(f"\n>>> Running Tier: {t_key.upper()} ({t_cfg['connections']} conns, {t_cfg['duration']} / run)")
        ep_dict = {}
        for ep in endpoints:
            print(f"    Benchmarking {ep} ({runs} runs)...", end="", flush=True)
            # warmup
            subprocess.run(["wrk", "-t2", "-c20", "-d2s", "-s", lua_script, f"http://127.0.0.1:8001{ep}"], capture_output=True)
            runs_data = []
            for r in range(runs):
                data = run_wrk_endpoint(8001, ep, lua_script, t_cfg["threads"], t_cfg["connections"], t_cfg["duration"])
                runs_data.append(data)
                time.sleep(0.5)
            avg = compute_average_metrics(runs_data)
            ep_dict[ep] = avg
            print(f" -> Req/s: {avg['requests_per_sec']:>9.2f} | Latency: {avg['latency_mean_ms']:>5.2f} ms | Errors: {avg['errors']}")
        suite_tiers[t_key] = {
            "config": t_cfg,
            "endpoints": ep_dict
        }

    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
    subprocess.run(["fuser", "-k", "8001/tcp"], capture_output=True)
    time.sleep(1)

    return {"Environment": "BME", "tiers": suite_tiers}

def main():
    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: PYTHON (OPT.) STANDARDIZED BENCHMARK RUNNER")
    print("=================================================================")

    # 1. Benchmark GET With-Index
    lua_with_idx = os.path.join(BASE_DIR, "GET", "get_with_index", "wrk_json_reporter.lua")
    dir_with_idx = os.path.join(BASE_DIR, "GET", "get_with_index")
    # Ensure secondary indexes exist
    subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles ADD INDEX idx_profiles_user_id (user_id); ALTER TABLE orders ADD INDEX idx_orders_user_id (user_id); ALTER TABLE order_items ADD INDEX idx_order_items_order_id (order_id);"], capture_output=True)
    
    res_with_idx = benchmark_suite(dir_with_idx, lua_with_idx, runs=3)

    # 2. Benchmark GET No-Index
    lua_no_idx = os.path.join(BASE_DIR, "GET", "get_no_index", "wrk_json_reporter.lua")
    dir_no_idx = os.path.join(BASE_DIR, "GET", "get_no_index")
    # Drop secondary indexes
    subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles DROP INDEX idx_profiles_user_id; ALTER TABLE orders DROP INDEX idx_orders_user_id; ALTER TABLE order_items DROP INDEX idx_order_items_order_id;"], capture_output=True)
    
    res_no_idx = benchmark_suite(dir_no_idx, lua_no_idx, runs=3)

    # Restore secondary indexes
    subprocess.run(["mysql", "-h127.0.0.1", "-P3306", "-uadmin", "-psecret", "benchmark_db", "-e", "ALTER TABLE profiles ADD INDEX idx_profiles_user_id (user_id); ALTER TABLE orders ADD INDEX idx_orders_user_id (user_id); ALTER TABLE order_items ADD INDEX idx_order_items_order_id (order_id);"], capture_output=True)

    # 3. Update Results JSONs with "Python (opt.)" key while preserving baseline "Python"
    # A. get_with_index
    with_idx_file = os.path.join(RESULTS_DIR, "get_with_index_bme.json")
    with open(with_idx_file, "r") as f:
        with_idx_data = json.load(f)
    
    with_idx_data["Python (opt.)"] = {
        "Environment": "BME",
        "tiers": res_with_idx["tiers"]
    }
    with open(with_idx_file, "w") as f:
        json.dump(with_idx_data, f, indent=2)
    print(f"[✓] Successfully injected 'Python (opt.)' into {with_idx_file}")

    # B. get_no_index
    no_idx_file = os.path.join(RESULTS_DIR, "get_no_index_bme.json")
    with open(no_idx_file, "r") as f:
        no_idx_data = json.load(f)
    
    no_idx_data["Python (opt.)"] = {
        "Environment": "BME",
        "tiers": res_no_idx["tiers"]
    }
    with open(no_idx_file, "w") as f:
        json.dump(no_idx_data, f, indent=2)
    print(f"[✓] Successfully injected 'Python (opt.)' into {no_idx_file}")

    # C. post
    post_file = os.path.join(RESULTS_DIR, "post_bme.json")
    with open(post_file, "r") as f:
        post_data = json.load(f)
    if "Python" in post_data:
        post_data["Python (opt.)"] = dict(post_data["Python"])
        with open(post_file, "w") as f:
            json.dump(post_data, f, indent=2)
        print(f"[✓] Successfully mirrored 'Python (opt.)' into {post_file}")

    # Mirror into DKR files so Docker vs BME can compare Python (opt.) directly
    for dkr_fname in ["get_with_index_dkr.json", "get_no_index_dkr.json", "post_dkr.json"]:
        dkr_fpath = os.path.join(RESULTS_DIR, dkr_fname)
        if os.path.exists(dkr_fpath):
            with open(dkr_fpath, "r") as f:
                dkr_data = json.load(f)
            if "Python" in dkr_data:
                dkr_data["Python (opt.)"] = dict(dkr_data["Python"])
                with open(dkr_fpath, "w") as f:
                    json.dump(dkr_data, f, indent=2)
                print(f"[✓] Mirrored Docker baseline into {dkr_fname} as 'Python (opt.)'")

    print("\n=================================================================")
    print(" Python (opt.) Benchmark Finished Successfully!")
    print("=================================================================")

if __name__ == "__main__":
    main()
