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

LANGUAGES = [
    {"name": "Python", "port": 8001, "cmd": ["python3", "server.py"]},
    {"name": "Node.js", "port": 8002, "cmd": ["node", "server.js"]},
    {"name": "PHP", "port": 8003, "cmd": ["php", "server.php"]},
    {"name": "Go", "port": 8004, "cmd": ["./server"]},
    {"name": "Java", "port": 8005, "cmd": ["java", "-jar", "app.jar"]}
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

def main():
    parser = argparse.ArgumentParser(description="GET With-Index Bare Metal Benchmark Runner")
    parser.add_argument("--tier", choices=["min", "med", "max", "all"], default="all", help="Tier to execute (default: all)")
    parser.add_argument("--no-warmup", action="store_true", help="Disable 3-second warmup phase")
    args = parser.parse_args()

    selected_tiers = list(TIERS.keys()) if args.tier == "all" else [args.tier]

    print("=================================================================")
    print(" Project Antigravity: GET (With Index) Bare Metal (BME) Benchmark")
    print(f" Selected Tiers: {', '.join(selected_tiers).upper()} | Warmup: {not args.no_warmup}")
    print("=================================================================")

    ALL_RESULTS = {}

    for lang in LANGUAGES:
        print(f"\n---> Starting Server: {lang['name']} on Port {lang['port']}")
        subprocess.run(["fuser", "-k", f"{lang['port']}/tcp"], capture_output=True)
        time.sleep(1)

        proc = subprocess.Popen(lang["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"     Waiting for {lang['name']} server to be ready on port {lang['port']}...")
        if not wait_for_server(lang['port'], max_wait=30):
            print(f"  [!] Timeout waiting for {lang['name']} server on port {lang['port']}")

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

                print(f"     Benchmarking {lang['name']} GET {ep}...")
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

    res_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "results"))
    os.makedirs(res_dir, exist_ok=True)
    with open(os.path.join(res_dir, "get_with_index_bme.json"), "w") as f:
        json.dump(ALL_RESULTS, f, indent=2)

    print("\n=================================================================")
    print(" GET With-Index Bare-Metal Benchmark Finished! Results in bme_benchmark_results.json and results/get_with_index_bme.json")
    print("=================================================================")

if __name__ == "__main__":
    main()
