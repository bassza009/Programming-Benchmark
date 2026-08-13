#!/usr/bin/env python3
import json
import subprocess
import time

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

RESULTS = {}

def run_wrk(port, endpoint):
    url = f"http://127.0.0.1:{port}{endpoint}"
    cmd = [
        "wrk",
        "-t4",
        "-c100",
        "-d10s",
        "-s", "wrk_json_reporter.lua",
        url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout.strip())
        return data
    except Exception as e:
        print(f"Error running wrk for {url}: {e}")
        return {
            "requests_per_sec": 0.0,
            "latency_mean_ms": 0.0,
            "latency_max_ms": 0.0,
            "errors": 1
        }

def main():
    print("=== Starting Project Antigravity GET No-Index Docker Benchmark ===")
    
    print("---> Starting MySQL container...")
    subprocess.run(["docker", "compose", "up", "-d", "mysql"], check=True)
    time.sleep(10)

    for s in SERVICES:
        print(f"\n---> Spinning up Docker container: {s['service']} on Port {s['port']}")
        subprocess.run(["docker", "compose", "up", "-d", "--build", s['service']], check=True)
        time.sleep(8)

        lang_results = {
            "Environment": "Docker",
            "endpoints": {}
        }

        for ep in ENDPOINTS:
            print(f"Benchmarking Docker Container {s['name']} GET (No Index) {ep}...")
            ep_res = run_wrk(s['port'], ep)
            lang_results["endpoints"][ep] = ep_res

        RESULTS[s["name"]] = lang_results

        print(f"---> Stopping container {s['service']}...")
        subprocess.run(["docker", "compose", "stop", s['service']], check=True)
        subprocess.run(["docker", "compose", "rm", "-f", s['service']], check=True)
        time.sleep(2)

    subprocess.run(["docker", "compose", "down"], check=True)

    with open("dkr_benchmark_results.json", "w") as f:
        json.dump(RESULTS, f, indent=2)

    print("\n=== GET No-Index Docker Benchmark Finished! Results written to dkr_benchmark_results.json ===")

if __name__ == "__main__":
    main()
