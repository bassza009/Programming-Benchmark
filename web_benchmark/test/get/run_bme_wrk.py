#!/usr/bin/env python3
import json
import subprocess

LANGUAGE_PORTS = {
    "Python": 8001,
    "Node": 8002,
    "PHP": 8003,
    "Go": 8004,
    "Java": 8005,
}

ENDPOINTS = ["/", "/health", "/api/data"]
OUTPUT_FILE = "bme_benchmark_results.json"
LUA_REPORTER = "wrk_json_reporter.lua"


def run_wrk(port: int, endpoint: str) -> dict:
    url = f"http://127.0.0.1:{port}{endpoint}"
    print(f" Running wrk for {url}")
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

        # ค้นหาปีกกาเพื่อตัดเอาเฉพาะโครงสร้าง JSON
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1

        if start_idx != -1 and end_idx != -1:
            json_str = output[start_idx:end_idx]
            
            #  ป้องกันบั๊กงอแง: แปลงค่า nan / inf ที่ผิดมาตรฐาน JSON ให้เป็น 0.0
            json_str = json_str.replace("-nan", "0.0").replace("nan", "0.0").replace("inf", "0.0")
            
            return json.loads(json_str)
        else:
            print(f"  [พัง] wrk ไม่ได้ส่งค่าเป็น JSON กลับมา (เช็คว่าเปิด Server พอร์ต {port} หรือยัง?)")
            return None
    except Exception as e:
        print(f"  [พัง] รันคำสั่ง wrk ไม่สำเร็จ: {e}")
        return None


def main() -> None:
    print(" Starting Bare Metal Environment benchmark run...")
    aggregated = {}

    for language, port in LANGUAGE_PORTS.items():
        print(f"\n=== Testing {language} on port {port} ===")
        language_data = {"Environment": "BME", "endpoints": {}}

        for endpoint in ENDPOINTS:
            metrics = run_wrk(port, endpoint)
            if metrics:
                language_data["endpoints"][endpoint] = metrics
                print(f" Collected data for {language} {endpoint}")
            else:
                print(f" ข้าม {language} {endpoint} เพราะดึงข้อมูลไม่ได้เนื่องจาก Server เออเร่อ")

        aggregated[language] = language_data

    print(f"\n Writing aggregated results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(aggregated, output_file, indent=2)

    print(" Benchmark run complete!")


if __name__ == "__main__":
    main()