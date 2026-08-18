#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time

try:
    import resource
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    target = min(65535, hard if hard > 0 else 65535)
    if soft < target:
        resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard))
except Exception:
    pass

SERVICES = [
    {"name": "Python", "service": "server-python", "port": 8001},
    {"name": "Node.js", "service": "server-node", "port": 8002},
    {"name": "PHP", "service": "server-php", "port": 8003},
    {"name": "Go", "service": "server-go", "port": 8004},
    {"name": "Java", "service": "server-java", "port": 8005}
]

ENDPOINTS = [
    "/raw/1table",
    "/raw/2join",
    "/raw/3join",
    "/raw/4join"
]

TIERS = {
    "min": {"name": "Minimum (Light)", "threads": 2, "connections": 100, "duration": "10s"},
    "med": {"name": "Medium (Standard)", "threads": 10, "connections": 1000, "duration": "30s"},
    "max": {"name": "Maximum (Stress)", "threads": 20, "connections": 10000, "duration": "30s"}
}

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
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout.strip())
        return data
    except Exception as e:
        print(f"  [!] Error running wrk for {url}: {e}")
        return {
            "requests_per_sec": 0.0,
            "latency_mean_ms": 0.0,
            "latency_max_ms": 0.0,
            "errors": 1
        }

def main():
    parser = argparse.ArgumentParser(description="GET No-Index Docker Benchmark Runner")
    parser.add_argument("--tier", choices=["min", "med", "max", "all"], default="all", help="Tier to execute (default: all)")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase")
    args = parser.parse_args()

    selected_tiers = list(TIERS.keys()) if args.tier == "all" else [args.tier]

    print("=================================================================")
    print(" Project Antigravity: GET (No Index) Docker Benchmark")
    print(f" Selected Tiers: {', '.join(selected_tiers).upper()} | Warmup: {not args.no_warmup}")
    print("=================================================================")

    print("\n---> Starting MySQL container...")
    subprocess.run(["docker", "compose", "up", "-d", "mysql"], check=True)
    time.sleep(10)

    ALL_RESULTS = {}

    for s in SERVICES:
        print(f"\n---> Spinning up Docker container: {s['service']} on Port {s['port']}")
        subprocess.run(["docker", "compose", "up", "-d", "--build", s['service']], check=True)
        time.sleep(8)

        lang_results = {
            "Environment": "Docker",
            "tiers": {}
        }

        for tier_key in selected_tiers:
            t_cfg = TIERS[tier_key]
            print(f"\n  >> Running Tier: {t_cfg['name']} (-t{t_cfg['threads']} -c{t_cfg['connections']} -d{t_cfg['duration']})")
            tier_endpoints = {}

            for ep in ENDPOINTS:
                if not args.no_warmup:
                    warmup(s['port'], ep)
                    time.sleep(1)

                print(f"     Benchmarking Docker {s['name']} GET {ep}...")
                ep_res = run_wrk(s['port'], ep, t_cfg)
                tier_endpoints[ep] = ep_res
                print(f"     -> Req/sec: {ep_res.get('requests_per_sec', 0):.2f} | Avg Latency: {ep_res.get('latency_mean_ms', 0):.2f}ms | Errors: {ep_res.get('errors', 0)}")

            lang_results["tiers"][tier_key] = {
                "config": t_cfg,
                "endpoints": tier_endpoints
            }

        ALL_RESULTS[s["name"]] = lang_results

        print(f"---> Stopping container {s['service']}...")
        subprocess.run(["docker", "compose", "stop", s['service']], check=True)
        subprocess.run(["docker", "compose", "rm", "-f", s['service']], check=True)
        time.sleep(2)

    subprocess.run(["docker", "compose", "down"], check=True)

    with open("dkr_benchmark_results.json", "w") as f:
        json.dump(ALL_RESULTS, f, indent=2)

    print("\n=================================================================")
    print(" GET No-Index Docker Benchmark Finished! Results in dkr_benchmark_results.json")
    print("=================================================================")

if __name__ == "__main__":
    main()
