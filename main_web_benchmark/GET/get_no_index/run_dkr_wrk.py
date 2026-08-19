#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
import urllib.request

try:
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    target = min(65535, hard if hard > 0 else 65535)
    if soft < target:
        resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
except Exception:
    pass

LANG_ALIASES = {
    "python": "python", "py": "python",
    "nodejs": "nodejs", "node": "nodejs", "js": "nodejs",
    "php": "php",
    "go": "go", "golang": "go",
    "java": "java"
}

FW_ALIASES = {
    "fastapi": "fastapi",
    "fastify": "fastify",
    "swoole": "swoole",
    "fiber": "fiber",
    "springboot": "springboot", "spring": "springboot", "spring-boot": "springboot"
}

SERVICES = [
    {"name": "Python", "lang": "python", "framework": "FastAPI", "framework_key": "fastapi", "service": "server-python", "port": 8001},
    {"name": "Node.js", "lang": "nodejs", "framework": "Fastify", "framework_key": "fastify", "service": "server-node", "port": 8002},
    {"name": "PHP", "lang": "php", "framework": "Swoole", "framework_key": "swoole", "service": "server-php", "port": 8003},
    {"name": "Go", "lang": "go", "framework": "Fiber", "framework_key": "fiber", "service": "server-go", "port": 8004},
    {"name": "Java", "lang": "java", "framework": "Spring Boot", "framework_key": "springboot", "service": "server-java", "port": 8005}
]

ENDPOINTS = [
    "/raw/1table",
    "/raw/2join",
    "/raw/3join",
    "/raw/4join"
]

TIERS = {
    "poc": {"name": "POC / Small internal system", "scenario": "Thesis project, department website prototype", "threads": 2, "connections": 20, "duration": "30s"},
    "small": {"name": "Small production website", "scenario": "Small company local business", "threads": 4, "connections": 100, "duration": "60s"},
    "general": {"name": "General web application", "scenario": "University system e-commerce CMS", "threads": 8, "connections": 500, "duration": "60s"},
    "high": {"name": "High-density website", "scenario": "Popular portals SaaS platforms", "threads": 8, "connections": 2000, "duration": "120s"},
    "stress": {"name": "Stress testing", "scenario": "Find saturation point", "threads": 16, "connections": 10000, "duration": "300s"}
}

def wait_for_server(port, max_wait=30):
    start = time.time()
    url = f"http://127.0.0.1:{port}/"
    while time.time() - start < max_wait:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def warmup(port, endpoint):
    url = f"http://127.0.0.1:{port}{endpoint}"
    cmd = ["wrk", "-t2", "-c20", "-d3s", "-s", "wrk_json_reporter.lua", url]
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except Exception:
        pass

def run_wrk(port, endpoint, tier_cfg):
    url = f"http://127.0.0.1:{port}{endpoint}"
    cmd = [
        "wrk",
        f"-t{tier_cfg['threads']}",
        f"-c{tier_cfg['connections']}",
        f"-d{tier_cfg['duration']}",
        "-s", "wrk_json_reporter.lua",
        url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        stdout = res.stdout.strip()
        json_start = stdout.find("{")
        json_end = stdout.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            data = json.loads(stdout[json_start:json_end])
            return data
        data = json.loads(stdout)
        return data
    except Exception as e:
        print(f"  [!] Error running wrk for {url}: {e}")
        return {
            "requests_per_sec": 0.0,
            "latency_mean_ms": 0.0,
            "latency_max_ms": 0.0,
            "errors": 1
        }

import math

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

def is_target(item, filter_lang=None, filter_fw=None):
    if filter_lang and filter_lang.lower() != "all":
        norm_lang = LANG_ALIASES.get(filter_lang.lower(), filter_lang.lower())
        if item.get("lang") != norm_lang:
            return False
    if filter_fw and filter_fw.lower() != "all":
        norm_fw = FW_ALIASES.get(filter_fw.lower(), filter_fw.lower())
        item_fw = item.get("framework_key", item.get("framework", "").lower().replace("-", "").replace("_", "").replace(" ", ""))
        if item_fw != norm_fw:
            return False
    return True

def main():
    parser = argparse.ArgumentParser(description="GET No-Index Docker Benchmark Runner")
    parser.add_argument("--tier", choices=list(TIERS.keys()) + ["all"], default="all", help="Tier to execute (default: all)")
    parser.add_argument("--lang", choices=["python", "py", "node", "nodejs", "js", "php", "go", "golang", "java", "all"], default=None, help="Language to benchmark (runs all frameworks in language if --framework is not set)")
    parser.add_argument("--framework", "--fw", choices=["fastapi", "fastify", "swoole", "fiber", "springboot", "spring-boot", "spring", "all"], default=None, help="Framework to benchmark")
    parser.add_argument("--runs", type=int, default=1, help="Number of iterations per endpoint to average (default: 1)")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase")
    args = parser.parse_args()

    filter_desc = []
    if args.lang and args.lang.lower() != "all":
        filter_desc.append(f"Lang: {args.lang.upper()}")
    if args.framework and args.framework.lower() != "all":
        filter_desc.append(f"Framework: {args.framework.upper()}")
    filter_label = " | ".join(filter_desc) if filter_desc else "ALL"

    selected_tiers = list(TIERS.keys()) if args.tier == "all" else [args.tier]
    target_services = [s for s in SERVICES if is_target(s, args.lang, args.framework)]

    if not target_services:
        print(f"[!] No services matched filter (Lang: {args.lang}, Framework: {args.framework})")
        return

    print("=================================================================")
    print(" Project Antigravity: GET (No Index) Docker Benchmark")
    print(f" Target Filter: {filter_label} | Selected Tiers: {', '.join(selected_tiers).upper()} | Runs/Endpoint: {args.runs} | Warmup: {not args.no_warmup}")
    print(f" Target Services: {', '.join([s['name'] + ' (' + s['framework'] + ')' for s in target_services])}")
    print("=================================================================")

    ALL_RESULTS = {}
    RAW_RESULTS = {}
    if os.path.exists("dkr_benchmark_results.json"):
        try:
            with open("dkr_benchmark_results.json", "r") as f:
                ALL_RESULTS = json.load(f)
        except Exception:
            pass
    if os.path.exists("raw_results.json"):
        try:
            with open("raw_results.json", "r") as f:
                RAW_RESULTS = json.load(f)
        except Exception:
            pass

    for s in target_services:
        print(f"\n---> Spinning up Docker container: {s['service']} on Port {s['port']}")
        subprocess.run(["docker", "compose", "up", "-d", "--build", s['service']], check=True)
        
        print(f"     Waiting for {s['name']} server to be ready on port {s['port']}...")
        if not wait_for_server(s['port'], max_wait=30):
            print(f"  [!] Timeout waiting for {s['name']} server on port {s['port']}")

        lang_results = {
            "Environment": "Docker",
            "tiers": {}
        }
        raw_lang_results = {
            "Environment": "Docker",
            "tiers": {}
        }

        for tier_key in selected_tiers:
            t_cfg = TIERS[tier_key]
            print(f"\n  >> Running Tier: {t_cfg['name']} (-t{t_cfg['threads']} -c{t_cfg['connections']} -d{t_cfg['duration']})")
            tier_endpoints = {}
            raw_tier_endpoints = {}

            for ep in ENDPOINTS:
                if not args.no_warmup:
                    warmup(s['port'], ep)
                    time.sleep(1)

                runs_data = []
                for run_idx in range(1, args.runs + 1):
                    run_label = f" (Run {run_idx}/{args.runs})" if args.runs > 1 else ""
                    print(f"     Benchmarking Docker {s['name']} GET {ep}{run_label}...")
                    ep_res = run_wrk(s['port'], ep, t_cfg)
                    ep_res_with_meta = dict(ep_res)
                    ep_res_with_meta["run_index"] = run_idx
                    runs_data.append(ep_res_with_meta)
                    print(f"     -> Run {run_idx}: Req/sec: {ep_res.get('requests_per_sec', 0):.2f} | Latency: {ep_res.get('latency_mean_ms', 0):.2f}ms | Errors: {ep_res.get('errors', 0)}")
                    if run_idx < args.runs:
                        time.sleep(1)

                avg_res = compute_average_metrics(runs_data)
                tier_endpoints[ep] = avg_res
                raw_tier_endpoints[ep] = {
                    "average": avg_res,
                    "raw_runs": runs_data
                }

                if args.runs > 1:
                    print(f"     ==> Average ({args.runs} runs): Req/sec: {avg_res['requests_per_sec']:.2f} | Avg Latency: {avg_res['latency_mean_ms']:.2f}ms | Total Errors: {avg_res['errors']}")

            lang_results["tiers"][tier_key] = {
                "config": t_cfg,
                "endpoints": tier_endpoints
            }
            raw_lang_results["tiers"][tier_key] = {
                "config": t_cfg,
                "endpoints": raw_tier_endpoints
            }

        ALL_RESULTS[s["name"]] = lang_results
        RAW_RESULTS[s["name"]] = raw_lang_results

        print(f"---> Stopping container {s['service']}...")
        subprocess.run(["docker", "compose", "stop", s['service']], check=True)
        subprocess.run(["docker", "compose", "rm", "-f", s['service']], check=True)
        time.sleep(2)

    subprocess.run(["docker", "compose", "down"], check=True)

    # Save local results
    with open("dkr_benchmark_results.json", "w") as f:
        json.dump(ALL_RESULTS, f, indent=2)

    with open("raw_results.json", "w") as f:
        json.dump(RAW_RESULTS, f, indent=2)

    # Save centralized results
    res_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "results"))
    os.makedirs(res_dir, exist_ok=True)
    raw_res_dir = os.path.join(res_dir, "raw_results")
    os.makedirs(raw_res_dir, exist_ok=True)

    with open(os.path.join(res_dir, "get_no_index_dkr.json"), "w") as f:
        json.dump(ALL_RESULTS, f, indent=2)

    with open(os.path.join(raw_res_dir, "get_no_index_dkr_raw.json"), "w") as f:
        json.dump(RAW_RESULTS, f, indent=2)

    print("\n=================================================================")
    print(" GET No-Index Docker Benchmark Finished!")
    print(" Averaged Results in: dkr_benchmark_results.json & results/get_no_index_dkr.json")
    print(" Raw Iteration Results in: raw_results.json & results/raw_results/get_no_index_dkr_raw.json")
    print("=================================================================")

if __name__ == "__main__":
    main()
