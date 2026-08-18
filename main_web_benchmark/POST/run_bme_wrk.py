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

LANGUAGES = [
    {"name": "Python", "port": 8001, "cmd": ["python3", "server.py"]},
    {"name": "Node.js", "port": 8002, "cmd": ["node", "server.js"]},
    {"name": "PHP", "port": 8003, "cmd": ["php", "server.php"]},
    {"name": "Go", "port": 8004, "cmd": ["./server"]},
    {"name": "Java", "port": 8005, "cmd": ["java", "-jar", "app.jar"]}
]

ENDPOINTS = [
    "/raw/post/1table",
    "/raw/post/2table",
    "/raw/post/3table",
    "/raw/post/4table"
]

TIERS = {
    "min": {"name": "Minimum (Light)", "threads": 2, "connections": 100, "duration": "10s"},
    "med": {"name": "Medium (Standard)", "threads": 10, "connections": 1000, "duration": "30s"},
    "max": {"name": "Maximum (Stress)", "threads": 20, "connections": 10000, "duration": "30s"}
}

def reset_db():
    try:
        cmd = [
            "mysql",
            "-h", "127.0.0.1",
            "-P", "3306",
            "-u", "admin",
            "-psecret",
            "-e", "SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE order_items; TRUNCATE TABLE orders; TRUNCATE TABLE profiles; TRUNCATE TABLE users; SET FOREIGN_KEY_CHECKS=1;",
            "benchmark_db"
        ]
        subprocess.run(cmd, capture_output=True, timeout=10)
    except Exception:
        pass

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
    parser = argparse.ArgumentParser(description="POST Bare Metal Benchmark Runner")
    parser.add_argument("--tier", choices=["min", "med", "max", "all"], default="all", help="Tier to execute (default: all)")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase")
    args = parser.parse_args()

    selected_tiers = list(TIERS.keys()) if args.tier == "all" else [args.tier]

    print("=================================================================")
    print(" Project Antigravity: POST Write/Transaction Bare Metal Benchmark")
    print(f" Selected Tiers: {', '.join(selected_tiers).upper()} | Warmup: {not args.no_warmup}")
    print("=================================================================")

    ALL_RESULTS = {}

    for lang in LANGUAGES:
        print(f"\n---> Resetting Database for {lang['name']}...")
        reset_db()

        print(f"---> Starting Server: {lang['name']} on Port {lang['port']}")
        subprocess.run(["fuser", "-k", f"{lang['port']}/tcp"], capture_output=True)
        time.sleep(1)

        proc = subprocess.Popen(lang["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(6)

        lang_results = {
            "Environment": "BME",
            "tiers": {}
        }

        for tier_key in selected_tiers:
            t_cfg = TIERS[tier_key]
            print(f"\n  >> Running Tier: {t_cfg['name']} (-t{t_cfg['threads']} -c{t_cfg['connections']} -d{t_cfg['duration']})")
            tier_endpoints = {}

            for ep in ENDPOINTS:
                if not args.no_warmup:
                    warmup(lang['port'], ep)
                    time.sleep(1)

                print(f"     Benchmarking {lang['name']} POST {ep}...")
                ep_res = run_wrk(lang['port'], ep, t_cfg)
                tier_endpoints[ep] = ep_res
                print(f"     -> Req/sec: {ep_res.get('requests_per_sec', 0):.2f} | Avg Latency: {ep_res.get('latency_mean_ms', 0):.2f}ms | Errors: {ep_res.get('errors', 0)}")

            lang_results["tiers"][tier_key] = {
                "config": t_cfg,
                "endpoints": tier_endpoints
            }

        ALL_RESULTS[lang["name"]] = lang_results

        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        subprocess.run(["fuser", "-k", f"{lang['port']}/tcp"], capture_output=True)
        time.sleep(2)

    with open("bme_benchmark_results.json", "w") as f:
        json.dump(ALL_RESULTS, f, indent=2)

    print("\n=================================================================")
    print(" POST BME Benchmark Finished! Results in bme_benchmark_results.json")
    print("=================================================================")

if __name__ == "__main__":
    main()
