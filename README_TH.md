# โครงการ Project Antigravity: ชุดทดสอบเปรียบเทียบประสิทธิภาพ Web Framework หลายภาษาและหลายสภาพแวดล้อม

> ภาษา / Language: [English](README.md) | **ภาษาไทย (Thai)**

---

## 1. บทสรุปสำหรับผู้บริหาร (Executive Summary)

ในวงการพัฒนาซอฟต์แวร์ Backend ยุคปัจจุบัน มีการประเมินและเปรียบเทียบภาษาและ Web Framework เพื่อค้นหาเทคโนโลยีที่เหมาะสมกับระบบที่ต้องการ Throughput สูง และมี Latency ต่ำ:
* Go เร็วกว่า Node.js อย่างมีนัยสำคัญหรือไม่?
* Java Spring Boot ทำงานได้มีประสิทธิภาพเพียงใดภายใต้ Concurrency สูง?
* รันไทม์ Asynchronous ของ PHP (เช่น Swoole) สามารถแข่งขันกับภาษา Compiled ได้หรือไม่?
* Python FastAPI มีพฤติกรรมอย่างไรเมื่องานส่วนใหญ่เป็น Database I/O?
* การ Deploy งานบน Docker Container ส่งผลกระทบต่อประสิทธิภาพมากน้อยเพียงใด?

การทดสอบประสิทธิภาพส่วนใหญ่บนอินเทอร์เน็ตมักทดสอบเฉพาะโปรแกรมอย่างง่าย เช่น "Hello World" ซึ่งส่งค่าข้อความสั้นๆ กลับมา ซึ่งไม่สะท้อนความเป็นจริงของระบบ Production ที่ต้องเชื่อมต่อฐานข้อมูล MySQL จริง, จัดการ Connection Pool, ประมวลผลคำสั่ง SQL JOIN หลายตาราง และรับมือกับคำขอพร้อมกันในปริมาณมาก

**Project Antigravity** คือ ชุดทดสอบประสิทธิภาพมาตรฐานที่ออกแบบมาเพื่อประเมิน **5 ภาษาและ Web Framework** ภายใต้ **ภาระงานฐานข้อมูลจริง** เปรียบเทียบระหว่าง **Bare Metal** กับ **Docker Container** ครอบคลุม **5 ระดับโหลดตามสถานการณ์จริง** (ตั้งแต่ 20 ถึง 10,000 Concurrent Connections)

---

## 2. วัตถุประสงค์ของโครงการ

### 1. การทดสอบกับภาระงานฐานข้อมูลจริง
ทดสอบการทำงานกับฐานข้อมูล MySQL จริงที่มีข้อมูลหลักหมื่นแถว ครอบคลุมการสืบค้นตารางเดี่ยว, การ JOIN ข้อมูล 2 ถึง 4 ตาราง, และธุรกรรมการเขียนข้อมูล (Transactions)

### 2. การวัดต้นทุนความหน่วงของ Containerization
วัดความแตกต่างของ Throughput และ Latency ระหว่างการรันบนระบบปฏิบัติการโดยตรง (Bare Metal) กับการรันภายใน Docker Container ที่มีระบบ Network เสมือน

### 3. การวิเคราะห์ผลกระทบของ Database Index ภายใต้โหลดสูง
ประเมินความเร็วและเสถียรภาพของการสืบค้นข้อมูลระหว่างแบบมี Secondary Index และไม่มี Index เมื่อปริมาณการเชื่อมต่อเพิ่มสูงขึ้น

### 4. การหาจุดอิ่มตัวและขีดจำกัดความเสถียร (Saturation Limits)
ศึกษาว่าแต่ละ Framework จัดการ Connection Pool และทรัพยากร Socket อย่างไรเมื่อต้องรับโหลดสูงถึง 10,000 Concurrent Connections

### 5. มาตรฐานการทดสอบที่เท่าเทียมและโปร่งใส
- กำหนดขนาด Database Connection Pool เท่ากันในทุกภาษา
- มีช่วง Warmup เพื่อเตรียมความพร้อมของ Process ก่อนบันทึกผล
- รีเซ็ตสถานะฐานข้อมูลระหว่างรอบการทดสอบ
- กำหนดค่า File Descriptor ของระบบปฏิบัติการ (`ulimit -n 65535`)
- รองรับการรันซ้ำหลายรอบ (`--runs N`) เพื่อคำนวณค่าเฉลี่ยทางสถิติ และบันทึก Log การรันดิบทุกรอบใน `raw_results.json`

---

## 3. ภาษาและ Framework ที่นำมาประเมิน

| ภาษา (Language) | Web Framework | Database Driver / Client | โมเดลการประมวลผล (Concurrency) | Port มาตรฐาน |
| :--- | :--- | :--- | :--- | :--- |
| **Python** | **FastAPI** (Uvicorn) | `aiomysql` (Async Pool) | Multi-process Async Event Loop | `8001` |
| **Node.js** | **Fastify** | `mysql2/promise` (Pool) | Multi-core Cluster + Event Loop | `8002` |
| **PHP** | **Swoole** | `PDO_MySQL` (`PDOPool`) | Coroutine Event Loop | `8003` |
| **Go** | **Fiber** (v2) | `database/sql` (`go-sql-driver`) | Goroutines | `8004` |
| **Java** | **Spring Boot** (v3) | `JdbcTemplate` + `HikariCP` | Multi-threaded JVM Pool | `8005` |

---

## 4. รูปแบบการทดสอบและระดับโหลด (Scenarios & Tiers)

### A. หมวดการอ่านข้อมูล / GET Suites (Raw SQL)
* `/raw/1table`: สืบค้นตารางเดี่ยว (`SELECT * FROM users LIMIT 100`)
* `/raw/2join`: สืบค้นแบบเชื่อม 2 ตาราง (`users` + `profiles`)
* `/raw/3join`: สืบค้นแบบเชื่อม 3 ตาราง (`users` + `profiles` + `orders`)
* `/raw/4join`: สืบค้นแบบเชื่อม 4 ตาราง (`users` + `profiles` + `orders` + `order_items`)

ทดสอบใน 2 สภาวะ:
1. **`GET/get_no_index`**: สืบค้นแบบไม่มี Secondary Index (Table Scans)
2. **`GET/get_with_index`**: สืบค้นแบบมี Secondary Index บน Foreign Key

### B. หมวดการเขียนข้อมูล / POST Suite (Database Transactions)
* `/raw/post/1table`: บันทึกข้อมูลลงตาราง `users` 1 รายการ
* `/raw/post/2table`: บันทึกข้อมูลแบบ Transaction เชื่อมโยง `users` และ `profiles`
* `/raw/post/3table`: บันทึกข้อมูลแบบ Transaction เชื่อมโยง `users`, `profiles`, และ `orders`
* `/raw/post/4table`: บันทึกข้อมูลแบบ Transaction ครบวงจร `users`, `profiles`, `orders`, และ `order_items` หลายรายการ

### C. 5 ระดับโหลดตามสถานการณ์จริง (ทดสอบด้วย `wrk`)

| ตัวเลือกระดับโหลด (`--tier`) | สถานการณ์ (Scenario) | ตัวอย่างระบบจริง (Typical Website) | เธรด (`-t`) | Connections (`-c`) | ระยะเวลา (`-d`) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **`poc`** | **POC / Small internal system** | โปรเจกต์จบการศึกษา, ระบบต้นแบบในแผนก | `2` | `20` | `30s` |
| **`small`** | **Small production website** | เว็บไซต์บริษัทขนาดเล็ก, ธุรกิจท้องถิ่น | `4` | `100` | `60s` |
| **`general`** | **General web application** | ระบบมหาวิทยาลัย, ระบบอีคอมเมิร์ซ, CMS | `8` | `500` | `60s` |
| **`high`** | **High-density website** | เว็บพอร์ทัลยอดนิยม, แพลตฟอร์ม SaaS | `8` | `2,000` | `120s` |
| **`stress`** | **Stress testing** | หาจุดอิ่มตัวและขีดจำกัดสูงสุดของระบบ | `16` | `10,000` | `300s` |
| **`all`** | **ทุกระดับโหลด (ค่าเริ่มต้น)** | รันครบทั้ง 5 สถานการณ์ต่อเนื่องกัน | Sequential | Sequential | Cumulative |

---

## 5. วิธีการรันทดสอบ

### ข้อกำหนดเบื้องต้น
* เปิดใช้งาน MySQL 8.0 ในเครื่อง Local บนพอร์ต `3306` (`user=admin`, `password=secret`, `database=benchmark_db`)
* ติดตั้ง Python 3.10+ และเครื่องมือ `wrk`
* ติดตั้ง Docker (สำหรับทดสอบในโหมดคอนเทนเนอร์)

### คำสั่งการรันทดสอบ
```bash
# 1. รันการทดสอบ GET (No Index) บน Bare Metal พร้อมหาค่าเฉลี่ย 3 รอบ
cd main_web_benchmark/GET/get_no_index
python3 run_bme_wrk.py --tier all --runs 3

# 2. รันการทดสอบ GET (With Index) บน Docker
cd main_web_benchmark/GET/get_with_index
python3 run_dkr_wrk.py --tier all --runs 3

# 3. รันการทดสอบ POST ธุรกรรมการเขียน
cd main_web_benchmark/POST
python3 run_bme_wrk.py --tier all --runs 3
```

### ตัวเลือกคำสั่ง (CLI Arguments)
* `--tier {poc,small,general,high,stress,all}` (ค่าเริ่มต้น: `all`): เลือกระดับโหลดสถานการณ์ที่ต้องการทดสอบ
* `--runs N` (ค่าเริ่มต้น: `1`): จำนวนรอบที่ต้องการรันซ้ำเพื่อคำนวณค่าเฉลี่ยทางสถิติ
* `--no-warmup` (ค่าเริ่มต้น: False): ปิดช่วง Warmup 3 วินาที

---

## 6. การจัดเก็บผลลัพธ์และประมวลผลข้อมูล

### ไฟล์ผลลัพธ์ที่สร้างขึ้น
* **ผลลัพธ์ค่าเฉลี่ย**: บันทึกใน `<bme/dkr>_benchmark_results.json` และรวบรวมไว้ที่ `main_web_benchmark/results/<suite>.json`
* **Log ข้อมูลดิบรายรอบ**: บันทึกใน `raw_results.json` และรวบรวมไว้ที่ `main_web_benchmark/results/raw_results/<suite>_raw.json`

### การดูและเปรียบเทียบผลลัพธ์
```bash
# ดูตารางสรุปเปรียบเทียบผลลัพธ์จากไฟล์ JSON
cd main_web_benchmark
python3 compare_results.py GET/get_no_index/dkr_benchmark_results.json

# สร้างเอกสารสรุป Markdown และไฟล์ CSV รวมทุกชุดทดสอบ
cd main_web_benchmark/results
python3 generate_summary.py
```

---

## 7. โครงสร้างโฟลเดอร์โครงการ

```text
main_web_benchmark/
├── GET/
│   ├── get_no_index/          # ชุดทดสอบ GET แบบไม่มี Secondary Index
│   │   ├── run_bme_wrk.py
│   │   └── run_dkr_wrk.py
│   └── get_with_index/        # ชุดทดสอบ GET แบบมี Secondary Index
│       ├── run_bme_wrk.py
│       └── run_dkr_wrk.py
├── POST/                      # ชุดทดสอบ POST ธุรกรรมการเขียนข้อมูล
│   ├── run_bme_wrk.py
│   └── run_dkr_wrk.py
├── results/                   # โฟลเดอร์รวมผลลัพธ์และสรุปรายงาน
│   ├── raw_results/           # Log ข้อมูลดิบรายรอบ
│   ├── generate_summary.py    # สคริปต์สร้าง SUMMARY.md และ SUMMARY.csv
│   ├── SUMMARY.md             # รายงานสรุปผลในรูปแบบ Markdown
│   └── SUMMARY.csv            # รายงานสรุปผลในรูปแบบ CSV
├── compare_results.py         # เครื่องมือแสดงตารางเปรียบเทียบผ่าน CLI
├── issue.md                   # รายงานการวิเคราะห์ปัญหาทางเทคนิค
└── README.md                  # เอกสารกำกับชุดทดสอบ
```
