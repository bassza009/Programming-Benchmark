#!/usr/bin/env python3
import json
import subprocess
import time

LANGUAGE_CONFIG = {
    "Python": {"port": 8001},
    "Node": {"port": 8002},
    "PHP": {"port": 8003},
    "Go": {"port": 8004},
    "Java": {"port": 8005},
}

ENDPOINTS = ["/raw/post/1table", "/raw/post/2table", "/raw/post/3table", "/raw/post/4table"]
OUTPUT_FILE = "wrk_benchmark_results.json"
LUA_SCRIPT = "post_script.lua"


def run_wrk(port: int, endpoint: str) -> dict:
    url = f"http://127.0.0.1:{port}{endpoint}"
    print(f"🚀 Running wrk for {url}")
    cmd = [
        "wrk",
        "-t4",
        "-c500",
        "-d30s",
        "-s",
        LUA_SCRIPT,
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout

        # Parse wrk output for key metrics
        metrics = {
            "endpoint": endpoint,
            "raw_output": output.strip()
        }

        # Try to extract basic metrics
        for line in output.split('\n'):
            if 'Requests/sec' in line:
                metrics['requests_per_sec'] = line.strip()
            elif 'Avg Latency' in line:
                metrics['avg_latency'] = line.strip()
            elif 'Max Latency' in line:
                metrics['max_latency'] = line.strip()

        return metrics
    except subprocess.TimeoutExpired:
        print(f"⚠️  [Error] wrk timeout")
        return None
    except Exception as e:
        print(f"⚠️  [Error] Failed to run wrk: {e}")
        return None


def main() -> None:
    print("📊 Starting POST benchmark run...")
    aggregated = {}

    for language, config in LANGUAGE_CONFIG.items():
        port = config["port"]
        print(f"\n=== Testing {language} on port {port} ===")

        language_data = {"port": port, "endpoints": {}}

        try:
            print(f"⏳ Waiting 2 seconds for server readiness...")
            time.sleep(2)

            for endpoint in ENDPOINTS:
                metrics = run_wrk(port, endpoint)
                if metrics:
                    language_data["endpoints"][endpoint] = metrics
                    print(f"✅ Collected data for {language} {endpoint}")
                else:
                    print(f"❌ Skipped {endpoint} due to error")
                time.sleep(1)

        except Exception as exc:
            print(f"⚠️  Error while benchmarking {language}: {exc}")

        aggregated[language] = language_data

    print(f"\n💾 Writing aggregated results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(aggregated, output_file, indent=2)

    print("🎉 Benchmark run complete!")


if __name__ == "__main__":
    main()
