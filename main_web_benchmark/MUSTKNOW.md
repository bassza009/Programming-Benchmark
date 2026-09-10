# MUSTKNOW.md — Thesis Defense Q&A Prep
## เอกสารเตรียมตอบคำถามกรรมการ (Programming Benchmark)

> Purpose: rehearsed, direct answers to what a thesis committee is likely to ask about this benchmark research. Not a re-explanation of the code — see `README.md` for the full spec and `issue.md` for the full bug audit trail.
>
> วัตถุประสงค์: คำตอบที่เตรียมไว้ล่วงหน้าสำหรับคำถามที่กรรมการสอบมีแนวโน้มจะถาม อ่าน `README.md` สำหรับสเปกฉบับเต็ม และ `issue.md` สำหรับรายงานบั๊กทั้งหมด

**Status as of 2026-09-09:** POST/BME benchmark run is currently **in progress / re-running** (`POST/bme_benchmark_results.json` reset to `{}`). Do not cite POST-BME numbers until this finishes and `results/export_excel.py` regenerates the report. GET (no-index/with-index, both BME+Docker) and POST-DKR are complete.

---

## 1. Design Rationale / เหตุผลการออกแบบงานวิจัย

### Q1.1: ทำไมถึงเลือก 5 ภาษา/เฟรมเวิร์กนี้ (Python, Node.js, PHP, Go, Java)?
**TH:** เลือกเพื่อให้ครอบคลุม **โมเดล concurrency ที่ต่างกัน** ไม่ใช่แค่ต่างภาษา: Python/FastAPI (async event loop เดี่ยว + Uvicorn workers), Node.js/Fastify (event loop + cluster หลายคอร์), PHP/Swoole (coroutine engine), Go/Fiber (goroutine น้ำหนักเบา), Java/Spring Boot (thread-per-request บน JVM thread pool). ทำให้เปรียบเทียบได้ว่าโมเดล concurrency แบบไหนรับมือ I/O-bound workload (query MySQL) ได้ดีที่สุด
**EN:** Chosen to span distinct **concurrency models**, not just different languages: Python/FastAPI (single async event loop + Uvicorn workers), Node.js/Fastify (event loop + multi-core cluster), PHP/Swoole (coroutine engine), Go/Fiber (lightweight goroutines), Java/Spring Boot (thread-per-request on the JVM thread pool). This lets the study isolate which concurrency model handles an I/O-bound (MySQL-bound) workload best.

### Q1.2: ทำไมใช้ Raw SQL เท่านั้น ไม่ใช้ ORM?
**TH:** เพื่อตัดตัวแปรกวนจาก ORM abstraction layer (query builder overhead, lazy loading, N+1 query patterns ที่ต่างกันในแต่ละ ORM) ออกไป ทำให้วัด **performance ของ driver/runtime/framework ล้วนๆ** โดยไม่มี ORM มาบิดเบือนผลเปรียบเทียบระหว่างภาษา
**EN:** To eliminate the confounding variable of ORM abstraction overhead (query builders, lazy loading, differing N+1 patterns per ORM). This isolates **pure driver/runtime/framework performance**, so cross-language comparisons aren't skewed by ORM implementation quality.

### Q1.3: ทำไมต้องเทียบ Bare Metal (BME) กับ Docker?
**TH:** เพื่อวัด **containerization overhead** จริงๆ ว่าการรันใน Docker (network namespace, cgroup, overlay filesystem) ทำให้ throughput/latency แย่ลงแค่ไหนเมื่อเทียบกับรันตรงบน host OS ซึ่งเป็นคำถามที่มีผลจริงต่อการตัดสินใจ deploy ในโปรดักชัน
**EN:** To quantify real **containerization overhead** — how much network namespacing, cgroups, and overlay filesystems degrade throughput/latency versus running directly on the host OS. This has direct production deployment relevance.

### Q1.4: ทำไมต้องมีทั้ง GET แบบมี index และไม่มี index?
**TH:** เพื่อแยกผลกระทบของ **query planner / index optimization ระดับฐานข้อมูล** ออกจากผลกระทบของภาษา/เฟรมเวิร์ก ถ้าไม่มีชุดนี้เปรียบเทียบคู่กัน จะตอบไม่ได้ว่าความต่างของผลลัพธ์มาจากภาษาหรือมาจาก index
**EN:** To isolate the effect of **database-level query planning/index optimization** from the effect of language/framework. Without this paired comparison, it's impossible to attribute performance differences to the language versus the index.

### Q1.5: ทำไมเลือก MySQL 8.0 ไม่ใช่ Postgres หรือฐานข้อมูลอื่น?
**TH:** MySQL เป็นฐานข้อมูล open-source ที่ใช้แพร่หลายที่สุดในระบบ production จริง (โดยเฉพาะ web application ทั่วไป) และมี driver รองรับครบทั้ง 5 ภาษาที่เลือก ทำให้ควบคุมตัวแปรฝั่งฐานข้อมูลให้เหมือนกันทุก stack ได้ง่าย
**EN:** MySQL is the most widely deployed open-source RDBMS in real production web applications, and has mature drivers for all 5 chosen languages — making it straightforward to hold the database variable constant across every stack.

### Q1.6: ทำไมมี endpoint ระดับ 1/2/3/4-table join?
**TH:** เพื่อจำลอง **ความซับซ้อนของ query ที่เพิ่มขึ้นแบบขั้นบันได** (single table → join มากขึ้นเรื่อยๆ) เหมือนสถานการณ์จริงที่ query ซับซ้อนขึ้นตามฟีเจอร์ของแอป และดูว่า framework ไหนเสื่อมประสิทธิภาพเร็ว/ช้าเมื่อ join เพิ่มขึ้น
**EN:** To simulate **progressively increasing query complexity** (single table → multi-join), mirroring how real applications grow more complex, and to observe which framework's performance degrades faster as join count increases.

### Q1.7: ทำไมมี 5 tier ของ concurrency (poc/small/general/high/stress)?
**TH:** เพื่อให้ครอบคลุมสถานการณ์จริงตั้งแต่ระบบเล็ก (โปรเจกต์ธีสิส, เว็บแผนก) ไปจนถึงระบบ SaaS ที่มีทราฟฟิกสูง และจุดอิ่มตัว (saturation point) — ถ้าทดสอบแค่ tier เดียวจะไม่เห็นว่า framework ไหน scale ได้ดีเมื่อโหลดเพิ่มขึ้น
**EN:** To cover real-world scenarios from small systems (thesis projects, department sites) up to high-traffic SaaS platforms and the saturation point — testing a single tier would hide which frameworks scale well as load increases.

---

## 2. Methodology & Statistics / ระเบียบวิธีวิจัยและสถิติ

### Q2.1: ทำไมต้องรัน 20 ครั้งต่อ endpoint?
**TH:** เพื่อลด noise จากความผันผวนของระบบ (GC pause, OS scheduling, network jitter) และให้สามารถคำนวณค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน และช่วงความเชื่อมั่น 95% (95% CI) ได้อย่างมีนัยสำคัญทางสถิติ แทนที่จะอ้างอิงผลจากการรันครั้งเดียวซึ่งอาจเป็น outlier
**EN:** To reduce noise from system variance (GC pauses, OS scheduling jitter, network jitter) and enable statistically meaningful mean, standard deviation, and 95% confidence interval calculations — instead of relying on a single run that could be an outlier.

### Q2.2: ทำไมต้องมี warmup 3 วินาทีก่อนวัดผลจริง?
**TH:** เพราะ runtime สมัยใหม่อย่าง JVM (JIT compiler), Node.js (V8 TurboFan), PHP Swoole (OPcache) ต้องการทราฟฟิกช่วงแรกเพื่อ "อุ่นเครื่อง" (optimize hot code paths, เติม connection pool) ถ้าวัดผลตั้งแต่ request แรกจะติด cold-start penalty ทำให้ endpoint แรกที่ถูกทดสอบเสียเปรียบอย่างไม่เป็นธรรม
**EN:** Modern runtimes — JVM JIT, Node.js V8 TurboFan, PHP Swoole OPcache — need initial traffic to warm up hot code paths and populate connection pools. Measuring from the very first request would penalize whichever endpoint is tested first with cold-start latency, skewing the comparison.

### Q2.3: วัดตัวแปรตาม (dependent variables) อะไรบ้าง?
**TH:** Throughput เฉลี่ย (req/sec) พร้อมส่วนเบี่ยงเบนมาตรฐานและ 95% CI, Latency เฉลี่ย (ms) พร้อม 95% CI, Tail latency (p50/p90/p95/p99) และ latency สูงสุด, จำนวน error/timeout/socket error, และค่าที่คำนวณเพิ่มคือ Bare-Metal Performance Gain (Δ_BME) กับ Index Speedup Factor (Gain_Index)
**EN:** Mean throughput (req/sec) with std-dev and 95% CI, mean latency (ms) with 95% CI, tail latencies (p50/p90/p95/p99) and max latency, error/timeout/socket-error counts, plus two derived metrics: Bare-Metal Performance Gain (Δ_BME) and Index Speedup Factor (Gain_Index).

### Q2.4: ทำไมใช้ `wrk` เป็นเครื่องมือ load testing?
**TH:** `wrk` เป็นเครื่องมือมาตรฐานอุตสาหกรรม เขียนด้วย C ทำให้ overhead ของตัว load generator เองต่ำมาก (ไม่กลายเป็นคอขวดก่อนเซิร์ฟเวอร์ที่ทดสอบ) และรองรับ custom Lua script ทำให้เขียน reporter เก็บผลเป็น JSON ได้ตามต้องการ (`wrk_json_reporter.lua`)
**EN:** `wrk` is an industry-standard load generator written in C, so its own overhead is minimal (it won't become the bottleneck before the server under test does), and it supports custom Lua scripting — used here to build a JSON reporter (`wrk_json_reporter.lua`).

### Q2.5: ระบบและเครือข่ายถูกปรับแต่งอย่างไรเพื่อไม่ให้เป็นคอขวดปลอม (artificial bottleneck)?
**TH:** ปรับ `RLIMIT_NOFILE` เป็น 65,535 (กัน file descriptor หมด), ปรับ `net.core.somaxconn`/`tcp_max_syn_backlog` เป็น 65,535 (ขยาย socket backlog), เปิด `tcp_tw_reuse` (ใช้ port ซ้ำเร็วขึ้นตอน TIME_WAIT), และตั้ง MySQL `max_connections=10000` กับ `wait_timeout=28800` วินาที — ทั้งหมดนี้เพื่อให้แน่ใจว่าคอขวดที่วัดได้มาจากตัวภาษา/เฟรมเวิร์กจริงๆ ไม่ใช่จาก OS/DB limit ที่ตั้งค่าไม่เหมาะสม
**EN:** `RLIMIT_NOFILE` raised to 65,535 (prevent fd exhaustion), `net.core.somaxconn`/`tcp_max_syn_backlog` raised to 65,535 (expand socket backlog), `tcp_tw_reuse` enabled (faster TIME_WAIT port reuse), and MySQL `max_connections=10000` with `wait_timeout=28800`s — all to ensure any measured bottleneck is genuinely the language/framework, not a misconfigured OS/DB limit.

---

## 3. Validity & Known Issues / ความน่าเชื่อถือของผลและบั๊กที่พบ

### Q3.1: มั่นใจได้ยังไงว่า benchmark เองไม่มีบั๊ก? (คำถามที่กรรมการชอบถามที่สุด)
**TH:** มีการทำ audit อย่างเป็นระบบและพบ 13 ปัญหา (บันทึกใน `issue.md`) ซึ่งแก้ไขครบทุกข้อแล้ว การเจอและแก้บั๊กเหล่านี้ **เป็นหลักฐานของความเข้มงวดในกระบวนการวิจัย** ไม่ใช่จุดอ่อน — เพราะถ้าไม่ตรวจพบ ผลการทดลองทั้งหมดจะผิดพลาดโดยไม่รู้ตัว
**EN:** A systematic audit found 13 issues (documented in `issue.md`), all of which were fixed. Finding and fixing these bugs **is evidence of methodological rigor**, not a weakness — had they gone undetected, the entire result set would have been silently invalid.

### Q3.2: บั๊กที่ร้ายแรงที่สุดที่พบคืออะไร?
**TH:** POST benchmark เดิมส่ง HTTP GET จริงๆ ไม่ใช่ POST (เพราะ Lua script ไม่ได้ตั้ง `wrk.method`) ทำให้ 4 ใน 5 เฟรมเวิร์ก (ทุกตัวยกเว้น PHP) ตอบ 405/404 และไม่เคย insert ข้อมูลจริงเลยระหว่างทดสอบ ส่วน PHP Swoole กลับ insert จริงเพราะ router เช็คแค่ URL ไม่เช็ค HTTP method — แก้โดยเพิ่ม `wrk.method = "POST"` และ body/headers ใน Lua script
**EN:** The original POST benchmark was actually sending HTTP GET requests (the Lua script never set `wrk.method`), so 4 of 5 frameworks returned 405/404 and never actually performed inserts, while PHP/Swoole *did* insert because its router only matched the URL string, not the HTTP method. Fixed by adding `wrk.method = "POST"` plus headers/body to the Lua script.

### Q3.3: ทำไม PHP ดูช้า/ไม่เสถียรกว่าภาษาอื่นในตอนแรก แก้ยังไง?
**TH:** เดิม PHP Swoole เปิด PDO connection ใหม่ทุก request (ไม่มี pool) ต่างจากภาษาอื่นที่ reuse connection ทำให้ที่ concurrency สูงเกิด TCP handshake จำนวนมหาศาลจน MySQL และ file descriptor หมด — แก้โดยใช้ `Swoole\Database\PDOPool`
**EN:** PHP/Swoole originally opened a brand-new PDO connection on every single request instead of reusing a pool like the other languages, causing massive TCP handshake overload at high concurrency that exhausted MySQL and file descriptors. Fixed with `Swoole\Database\PDOPool`.

### Q3.4: การเปรียบเทียบระหว่างภาษายุติธรรม (apples-to-apples) แค่ไหน เพราะแต่ละภาษามี connection pool ขนาดต่างกันโดยธรรมชาติ?
**TH:** พบว่าตอนแรก pool size ต่างกันมาก (Java default 10 เชื่อมต่อ vs Python สูงสุดถึง 1,600 เชื่อมต่อ) ซึ่งไม่ยุติธรรมและเกิน MySQL `max_connections` เดิม (500) จนเกิด error — แก้โดย standardize ขนาด pool ให้อยู่ในช่วงที่กำหนดชัดเจนทุกภาษา และเพิ่ม `max_connections` ของ MySQL เป็น 10,000 เพื่อรองรับ
**EN:** Pool sizes initially varied wildly (Java defaulted to just 10 connections vs. Python up to 1,600), which was unfair and exceeded MySQL's original `max_connections=500`, causing errors. Fixed by standardizing pool sizes across all languages within a defined range and raising MySQL's `max_connections` to 10,000.

### Q3.5: มีการจัดการ state ของฐานข้อมูลระหว่างการทดสอบ POST ของแต่ละภาษาอย่างไร (กัน bias จากตารางที่โตขึ้นเรื่อยๆ)?
**TH:** เดิมทดสอบภาษาต่อภาษาแบบเรียงลำดับโดยไม่ reset ตาราง ทำให้ภาษาหลังๆ insert เข้าตารางที่ใหญ่กว่า (index overhead มากกว่า) อย่างไม่เป็นธรรม — แก้โดยเพิ่มขั้นตอน reset/cleanup ฐานข้อมูลก่อนเริ่มทดสอบแต่ละภาษา เพื่อให้ทุกภาษาเริ่มจาก state เดียวกัน
**EN:** Originally, languages ran sequentially against the same table without resetting it, so later languages inserted into progressively larger tables with more index overhead — an unfair comparison. Fixed by adding a database reset/cleanup step before each language's POST test, so every language starts from an identical state.

### Q3.6: มีปัญหา schema/environment อื่นที่กระทบผลลัพธ์ไหม?
**TH:** พบ 3 ปัญหาระดับ infrastructure: (1) MySQL bind เฉพาะ `127.0.0.1` ทำให้ container เชื่อมต่อไม่ได้ (2) auth plugin `caching_sha2_password` ของ MySQL 8.0 เข้ากันไม่ได้กับบาง driver เบาๆ อย่าง `aiomysql` (3) query เช็ค data ตอน startup ใช้ `SELECT COUNT(*)` บนตาราง 17 ล้านแถวทำให้ worker ทุกตัวสแกนตารางพร้อมกันจน MySQL ค้าง — ทั้งหมดแก้แล้ว (bind `0.0.0.0`, ใช้ `mysql_native_password`, เปลี่ยนเป็น `SELECT 1 LIMIT 1`)
**EN:** Three infrastructure-level issues were found: (1) MySQL bound only to `127.0.0.1`, blocking container connections, (2) MySQL 8.0's `caching_sha2_password` auth plugin was incompatible with some lightweight drivers (`aiomysql`), (3) the startup existence check used `SELECT COUNT(*)` on a 17-million-row table, causing every worker to full-scan simultaneously and stall MySQL. All fixed (`bind-address=0.0.0.0`, `mysql_native_password`, changed to `SELECT 1 LIMIT 1`).

---

## 4. Results & Findings / ผลการทดลอง

> **[PENDING — รอผลสรุปหลังรันเสร็จและรัน `results/export_excel.py` ใหม่ / fill in after the current run finishes and the report is regenerated]**

- ภาษา/เฟรมเวิร์กใดให้ throughput สูงสุดในแต่ละ tier (poc/small/general/high/stress) สำหรับ GET และ POST? / Which framework had the highest throughput at each tier, for GET vs POST?
- Index Speedup Factor (Gain_Index) มีค่าเท่าไหร่ในแต่ละ join level (1/2/3/4 table)? / What was the Index Speedup Factor at each join level?
- Bare-Metal Performance Gain (Δ_BME) เทียบกับ Docker มีค่าเท่าไหร่ และคงที่ทุกภาษาหรือไม่? / What was the Docker overhead (Δ_BME) and was it consistent across languages?
- โมเดล concurrency แบบไหน (event loop / coroutine / goroutine / thread pool) เสื่อมประสิทธิภาพช้าที่สุดเมื่อ concurrency สูงขึ้น (stress tier)? / Which concurrency model degraded most gracefully under the stress tier?
- ผลลัพธ์ latency tail (p95/p99) ต่างจาก mean latency มากแค่ไหนในแต่ละภาษา — มีภาษาไหนมี tail latency แย่ผิดปกติหรือไม่? / How much did p95/p99 diverge from mean latency per language — any outlier tail behavior?
- มี error/timeout เกิดขึ้นในการรันชุดสุดท้าย (หลังแก้บั๊กทั้ง 13 ข้อ) หรือไม่? / Did the final (post-fix) runs show any errors/timeouts at all?
- ผลลัพธ์สอดคล้องกับสมมติฐานตั้งต้นเรื่องโมเดล concurrency หรือมีอะไรที่ผิดคาด (surprising finding)? / Did results confirm the initial concurrency-model hypothesis, or was there a surprising finding?

---

## 5. Limitations / ข้อจำกัดของงานวิจัย

### Q5.1: งานวิจัยนี้มีข้อจำกัดอะไรบ้างที่ต้องยอมรับตรงๆ?
**TH:**
- ทดสอบบนเครื่องเดียว (single-machine) ไม่มี network latency ระหว่าง node จริงแบบ distributed system หรือ multi-region
- ไม่ครอบคลุมสถานการณ์ auto-scaling / load balancer หลาย instance เหมือนระบบ production จริง
- ไม่มี soak test ระยะยาว (หลายชั่วโมง/วัน) เพื่อดู memory leak หรือ performance degradation ระยะยาว — tier นานสุดคือ stress (300 วินาที)
- ตัดสินใจไม่ใช้ ORM ทำให้ผลลัพธ์อาจไม่สะท้อนแอปพลิเคชันจริงส่วนใหญ่ที่ใช้ ORM
- การปรับแต่ง OS/kernel (ulimit, somaxconn ฯลฯ) เฉพาะสำหรับ environment นี้ อาจไม่ตรงกับค่า default ของ cloud provider หรือ production จริง
- ไม่ได้ทดสอบภายใต้ failure injection (เช่น DB connection drop, network partition) เพื่อดู resilience
- เวอร์ชันของ framework/driver ที่ใช้ ณ เวลาทดสอบอาจล้าสมัยเมื่อเวลาผ่านไป ผลอาจไม่ generalize ไปยังเวอร์ชันอนาคต

**EN:**
- Single-machine testing only — no real distributed-system network latency or multi-region effects.
- Doesn't cover auto-scaling or multi-instance load-balancer scenarios typical of real production deployments.
- No long-duration soak testing (hours/days) to observe memory leaks or long-term degradation — the longest tier (stress) runs 300 seconds.
- The deliberate exclusion of ORMs means results may not generalize to the majority of real-world applications, which do use ORMs.
- OS/kernel tuning (ulimits, somaxconn, etc.) is specific to this test environment and may not match default cloud-provider or production configurations.
- No failure-injection testing (DB connection drops, network partitions) to assess resilience.
- Framework/driver versions are pinned to the test date and may not generalize to future versions.

---

## Where things live / ตำแหน่งไฟล์สำคัญ

| Path | Contents |
| :--- | :--- |
| `results/*.json` | Averaged metrics per suite (`get_no_index_bme.json`, `post_dkr.json`, etc.) |
| `results/raw_results/*_raw.json` | Per-run raw metrics (all 20 iterations, not averaged) |
| `results/generate_summary.py`, `export_csv.py`, `export_excel.py` | Regenerate `SUMMARY.md`/`.csv` and `Programming_Benchmark_Report.xlsx` from the JSON above — **run these after any new benchmark run completes** |
| `issue.md` | Full 13-issue audit trail — cite this if asked "how do you know your methodology is sound" |
| `POST/disk_monitor.py`, `POST/disk_check.txt` | Disk-space watchdog used during long POST runs (raw JSON files can reach ~1MB each × 20 runs × 5 languages) |

**Do not cite as final:** `POST/bme_benchmark_results.json` while it reads `{}` — that means a POST-BME run is mid-flight or was interrupted. Re-check before quoting any POST-BME number.
