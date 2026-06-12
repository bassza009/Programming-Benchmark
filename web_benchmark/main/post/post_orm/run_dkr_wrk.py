#!/usr/bin/env python3
import json
import subprocess
import time

LANGUAGE_CONFIG = {
    "Python": {"image": "bench-python", "port": 8001},
    "Node": {"image": "bench-node", "port": 8002},
    "PHP": {"image": "bench-php", "port": 8003},
    "Go": {"image": "bench-go", "port": 8004},
    "Java": {"image": "bench-java", "port": 8005},
}

ENDPOINTS = ["/orm/post/1table", "/orm/post/2table", "/orm/post/3table", "/orm/post/4table"]
OUTPUT_FILE = "dkr_benchmark_results.json"
LUA_REPORTER = "wrk_json_reporter.lua"
CONTAINER_NAME = "bench_current"


def run_wrk(port: int, endpoint: str) -> dict:
    url = f"http://127.0.0.1:{port}{endpoint}"
    print(f"🚀 Running wrk for {url}")
    cmd = [
        "wrk",
        "-t4",
        "-c500",
        "-d30s",
        "-s",
        LUA_REPORTER,
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        # Extract JSON from wrk output
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            json_str = output[start_idx:end_idx]

            # Handle invalid JSON values
            json_str = json_str.replace("-nan", "0.0").replace("nan", "0.0").replace("inf", "0.0")

            return json.loads(json_str)
        else:
            print(f"⚠️  [Error] wrk failed to connect")
            print(f"Details from wrk: {output.strip()} {result.stderr.strip()}")
            return None
    except Exception as e:
        print(f"⚠️  [Error] Failed to run wrk: {e}")
        return None


def start_container(image: str, port: int) -> None:
    print(f"🐳 Starting Docker container from image {image} on port {port}")
    subprocess.run(
        ["docker", "run", "-d", "--network","host", "--name", CONTAINER_NAME, image],
        capture_output=True,
        text=True,
    )


def stop_container() -> None:
    print(f"🛑 Stopping container {CONTAINER_NAME}")
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        capture_output=True,
        text=True,
    )


def main() -> None:
    print("📊 Starting Docker benchmark run...")
    aggregated = {}

    # Clean up any leftover containers
    stop_container()

    for language, config in LANGUAGE_CONFIG.items():
        image = config["image"]
        port = config["port"]
        print(f"\n=== Testing {language} using {image} on port {port} ===")

        language_data = {"Environment": "Docker", "endpoints": {}}
        container_started = False

        try:
            start_container(image, port)
            container_started = True
            print("⏳ Waiting 5 seconds for container initialization...")
            time.sleep(5)

            for endpoint in ENDPOINTS:
                metrics = run_wrk(port, endpoint)
                if metrics:
                    language_data["endpoints"][endpoint] = metrics
                    print(f"✅ Collected data for {language} {endpoint}")
                else:
                    print(f"❌ Skipped {endpoint} due to error")

        except Exception as exc:
            print(f"⚠️  Error while benchmarking {language}: {exc}")
        finally:
            if container_started:
                stop_container()

        aggregated[language] = language_data

    print(f"\n💾 Writing aggregated results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(aggregated, output_file, indent=2)

    print("🎉 Docker benchmark run complete!")


if __name__ == "__main__":
    main()
