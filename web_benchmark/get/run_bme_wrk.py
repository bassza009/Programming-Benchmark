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
LUA_REPORTER = "benchmark/wrk_json_reporter.lua"


def run_wrk(port, endpoint):
    url = f"http://127.0.0.1:{port}{endpoint}"
    cmd = ["wrk", "-t4", "-c500", "-d30s", "-s", "wrk_json_reporter.lua", url]
    
    try:
        # สั่งรัน wrk
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        # ค้นหาปีกกาเพื่อตัดเอาเฉพาะโครงสร้าง JSON
        start_idx = output.find('{')
        end_idx = output.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = output[start_idx:end_idx]
            return json.loads(json_str)
        else:
            print(f"\n❌ [พัง] wrk ไม่ได้ส่งค่าเป็น JSON กลับมา (เช็คว่าเปิด Server หรือยัง?)")
            print(f"ข้อความจาก wrk: {output.strip()}")
            return None
            
    except Exception as e:
        print(f"\n❌ [พัง] รันคำสั่ง wrk ไม่สำเร็จ: {e}")
        return None
    

def main() -> None:
    print("📊 Starting Bare Metal Environment benchmark run...")
    aggregated = {}

    for language, port in LANGUAGE_PORTS.items():
        print(f"=== Testing {language} on port {port} ===")
        language_data = {"Environment": "BME", "endpoints": {}}

        for endpoint in ENDPOINTS:
            metrics = run_wrk(port, endpoint)
            language_data["endpoints"][endpoint] = metrics
            print(f"✅ Collected data for {language} {endpoint}")

        aggregated[language] = language_data

    print(f"💾 Writing aggregated results to {OUTPUT_FILE}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        json.dump(aggregated, output_file, indent=2)

    print("🎉 Benchmark run complete!")


if __name__ == "__main__":
    main()
