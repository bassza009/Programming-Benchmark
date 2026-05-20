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

ENDPOINTS = ["/", "/health", "/api/data"]
OUTPUT_FILE = "dkr_benchmark_results.json"
LUA_REPORTER = "benchmark/wrk_json_reporter.lua"
CONTAINER_NAME = "bench_current"


def run_wrk(port: int, endpoint: str) -> dict:
    url = f"http://localhost:{port}{endpoint}"
    print(f"🚀 Running wrk for {url}")
    result = subprocess.run(
        [
            "wrk",
            "-t4",
            "-c500",
            "-d30s",
            "-s",
            LUA_REPORTER,
            url,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"⚠️  wrk failed for {url} (exit code {result.returncode})")
        print(result.stderr.strip())
        raise RuntimeError(f"wrk failed for {url}")

    output = result.stdout.strip()
    if not output:
        raise ValueError(f"No JSON output from wrk for {url}")

    return json.loads(output)


def start_container(image: str) -> None:
    print(f"🐳 Starting Docker container from image {image}")
    result = subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "--rm",
            "--network",
            "host",
            "--name",
            CONTAINER_NAME,
            image,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"❌ Failed to start container {CONTAINER_NAME} from {image}")
        print(result.stderr.strip())
        raise RuntimeError(f"docker run failed for image {image}")

    container_id = result.stdout.strip()
    print(f"✅ Container started: {container_id}")


def stop_container() -> None:
    print(f"🛑 Stopping container {CONTAINER_NAME}")
    subprocess.run(
        ["docker", "stop", CONTAINER_NAME],
        capture_output=True,
        text=True,
    )


def main() -> None:
    print("📊 Starting Docker benchmark run...")
    aggregated = {}

    for language, config in LANGUAGE_CONFIG.items():
        image = config["image"]
        port = config["port"]
        print(f"\n=== Testing {language} using {image} on port {port} ===")

        language_data = {"Environment": "Docker", "endpoints": {}}
        container_started = False

        try:
            start_container(image)
            container_started = True
            print("⏳ Waiting 5 seconds for container initialization...")
            time.sleep(5)

            for endpoint in ENDPOINTS:
                metrics = run_wrk(port, endpoint)
                language_data["endpoints"][endpoint] = metrics
                print(f"✅ Collected data for {language} {endpoint}")

        except Exception as exc:
            print(f"⚠️  Error while benchmarking {language}: {exc}")
        finally:
            if container_started:
                stop_container()

        aggregated[language] = language_data

    print(f"💾 Writing aggregated results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(aggregated, output_file, indent=2)

    print("🎉 Docker benchmark run complete!")


if __name__ == "__main__":
    main()
