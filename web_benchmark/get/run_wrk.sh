#!/bin/bash

# ==============================================================================
# CONFIGURATION: ปรับแก้ Port และคำสั่งรันให้ตรงกับเครื่องของคุณได้ที่นี่
# ==============================================================================
CSV_FILE="web_benchmark_results.csv"
DURATION="30s"      # เวลายิงทดสอบจริง
WARMUP_DURATION="30s" # เวลายิง Warm-up ให้ JIT ทำงาน
THREADS=4
CONNECTIONS=500

# กำหนดชื่อภาษา, Port และคำสั่งรันแบบ Bare Metal (BME)
LANGUAGES=("Python" "Node" "PHP" "Go" "Java")
PORTS=(8001 8002 8003 8004 8005)

# คำสั่งรันเบื้องหลังสำหรับ Bare Metal
START_CMD_Python="python3 -m uvicorn server:app --port 8001 --workers 4"
START_CMD_Node="node server.js"
START_CMD_PHP="php server.php"    # รันผ่าน Swoole
START_CMD_Go="go run server.go"
START_CMD_Java="java server.java" # หรือใช้คลาสที่คอมไพล์แล้วเช่น java Server


# ชื่อ Docker Image ที่ตั้งไว้ตอน Build
DOCKER_IMAGES=("bench-go" "bench-node" "bench-python" "bench-java" "bench-php")

# ==============================================================================
# INITIALIZE CSV FILE
# ==============================================================================
echo "Language,Environment,RequestsPerSec,AvgLatency" > $CSV_FILE

# ฟังก์ชันสำหรับยิงโหลดและตัดคำเอาเฉพาะตัวเลขจาก wrk
run_wrk_test() {
    local lang=$1
    local env=$2
    local port=$3
    local url="http://127.0.0.1:$port/"

    echo "------------------------------------------------------------"
    echo "🚀 Testing $lang ($env) on Port $port..."
    echo "------------------------------------------------------------"
    
    # 1. Warm-up Phase
    echo "🔥 Warming up for $WARMUP_DURATION..."
    wrk -t$THREADS -c$CONNECTIONS -d$WARMUP_DURATION $url > /dev/null
    sleep 2

    # 2. Actual Test Phase
    echo "📊 Running actual benchmark for $DURATION..."
    local wrk_output=$(wrk -t$THREADS -c$CONNECTIONS -d$DURATION $url)
    
    # ดึงค่าด้วย grep และ awk
    local rps=$(echo "$wrk_output" | grep "Requests/sec:" | awk '{print $2}')
    local avg_lat=$(echo "$wrk_output" | grep "Latency" | awk '{print $2}')

    echo "✨ Result -> RPS: $rps | Avg Latency: $avg_lat"
    
    # บันทึกลงไฟล์ CSV
    echo "$lang,$env,$rps,$avg_lat" >> $CSV_FILE
}

# ==============================================================================
# PHASE 1: BARE METAL (BME) BENCHMARKING
# ==============================================================================
echo "=== STARTING BARE METAL (BME) BENCHMARKS ==="

for i in "${!LANGUAGES[@]}"; do
    lang=${LANGUAGES[$i]}
    port=${PORTS[$i]}
    
    # ดึงคำสั่งรันแบบ Dynamic
    cmd_var="START_CMD_$lang"
    start_cmd=${!cmd_var}

    echo "🟩 Starting $lang Server on port $port..."
    $start_cmd > /dev/null 2>&1 &
    server_pid=$!
    
    # รอ 3 วินาทีให้ Server บูทเสร็จ
    sleep 3 

    # รันการทดสอบ
    run_wrk_test "$lang" "BME" "$port"

    # ปิด Server หลังทดสอบเสร็จ
    echo "🟥 Stopping $lang Server (PID: $server_pid)..."
    kill $server_pid
    wait $server_pid 2>/dev/null
    sleep 2
done

# # ==============================================================================
# # PHASE 2: DOCKER BENCHMARKING
# # ==============================================================================
# echo ""
# echo "=== STARTING DOCKER BENCHMARKS ==="

# for i in "${!LANGUAGES[@]}"; do
#     lang=${LANGUAGES[$i]}
#     port=${PORTS[$i]}
#     img_name=${DOCKER_IMAGES[$i]}

#     echo "🐳 Running Docker Container for $lang on port $port..."
#     # ใช้ --network host เพื่อความยุติธรรมสูงสุดในเรื่อง Network Layer บน Linux
#     container_id=$(docker run -d --network host --name "bench-run-$lang" $img_name)
    
#     sleep 3

#     # รันการทดสอบ
#     run_wrk_test "$lang" "Docker" "$port"

#     # ปิดและลบ Container
#     echo "🗑️ Cleaning up Docker Container..."
#     docker stop $container_id > /dev/null
#     docker rm $container_id > /dev/null
#     sleep 2
# done

# echo "============================================================"
# echo "🎉 ALL BENCHMARKS COMPLETED SUCCESSFULLY!"
# echo "📊 Results saved to: $CSV_FILE"
# echo "============================================================"
# cat $CSV_FILE