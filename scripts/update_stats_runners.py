#!/usr/bin/env python3
import os

BASE_DIR = r"D:\github\Programming-Benchmark\main_web_benchmark"
RUNNERS = [
    os.path.join(BASE_DIR, "GET", "get_no_index", "run_bme_wrk.py"),
    os.path.join(BASE_DIR, "GET", "get_no_index", "run_dkr_wrk.py"),
    os.path.join(BASE_DIR, "GET", "get_with_index", "run_bme_wrk.py"),
    os.path.join(BASE_DIR, "GET", "get_with_index", "run_dkr_wrk.py"),
    os.path.join(BASE_DIR, "POST", "run_bme_wrk.py"),
    os.path.join(BASE_DIR, "POST", "run_dkr_wrk.py")
]

new_stats_block = '''import math

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
            "requests_per_sec": 0.0,
            "rps_stdev": 0.0,
            "rps_ci95_margin": 0.0,
            "rps_ci95_low": 0.0,
            "rps_ci95_high": 0.0,
            "latency_mean_ms": 0.0,
            "latency_stdev_ms": 0.0,
            "latency_ci95_margin": 0.0,
            "latency_ci95_low": 0.0,
            "latency_ci95_high": 0.0,
            "latency_p50_ms": 0.0,
            "latency_p90_ms": 0.0,
            "latency_p95_ms": 0.0,
            "latency_p99_ms": 0.0,
            "latency_max_ms": 0.0,
            "errors": 0,
            "runs_count": 0
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
'''

for runner_path in RUNNERS:
    if not os.path.exists(runner_path):
        print(f"Skipping {runner_path} (not found)")
        continue
    with open(runner_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find def compute_average_metrics
    start_idx = content.find("def compute_average_metrics")
    if start_idx == -1:
        print(f"compute_average_metrics not found in {runner_path}")
        continue
    end_idx = content.find("def main():", start_idx)
    if end_idx == -1:
        print(f"def main() not found in {runner_path}")
        continue

    new_content = content[:start_idx] + new_stats_block + "\n" + content[end_idx:]
    with open(runner_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated statistical computation in {runner_path}")

print("All runners updated successfully!")
