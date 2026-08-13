#!/usr/bin/env python3
import json
import subprocess
import time

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
    print("=== Starting Project Antigravity GET No-Index Bare Metal (BME) Benchmark ===")
    
    for lang in LANGUAGES:
        print(f"\n---> Starting Server: {lang['name']} on Port {lang['port']}")
        
        subprocess.run(["fuser", "-k", f"{lang['port']}/tcp"], capture_output=True)
        time.sleep(1)

        proc = subprocess.Popen(lang["cmd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)

        lang_results = {
            "Environment": "BME",
            "endpoints": {}
        }

        for ep in ENDPOINTS:
            print(f"Benchmarking {lang['name']} GET (No Index) {ep}...")
            ep_res = run_wrk(lang['port'], ep)
            lang_results["endpoints"][ep] = ep_res

        RESULTS[lang["name"]] = lang_results

        proc.terminate()
        try:
            proc.wait(timeout=5)
        except:
            proc.kill()
        subprocess.run(["fuser", "-k", f"{lang['port']}/tcp"], capture_output=True)
        time.sleep(2)

    with open("bme_benchmark_results.json", "w") as f:
        json.dump(RESULTS, f, indent=2)

    print("\n=== GET No-Index BME Benchmark Finished! Results written to bme_benchmark_results.json ===")

if __name__ == "__main__":
    main()
