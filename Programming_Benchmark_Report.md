บทที่ 1บทนำ

1.ความเป็นมาและความสำคัญของปัญหา
ในปัจจุบัน การประเมินประสิทธิภาพของภาษาโปรแกรมมีการศึกษาอย่างหลากหลาย ทว่างานวิจัยส่วนใหญ่มักมุ่งเน้นไปที่มิติเดียว เช่น การวัดความเร็วในการประมวลผลอัลกอริทึมพื้นฐาน การใช้พลังงานในระดับตัวภาษาโดยตรง หรือการทดสอบเว็บเฟรมเวิร์กด้วย Endpoint ที่ไม่มีการเชื่อมต่อฐานข้อมูล [1][2][14][24][25] อย่างไรก็ตาม ในการพัฒนาซอฟต์แวร์ระดับองค์กรยุคใหม่ ระบบไม่ได้ทำงานอย่างเป็นเอกเทศ แต่ต้องอยู่ภายใต้โครงสร้างพื้นฐานที่มีความซับซ้อน โดยเฉพาะการเปลี่ยนผ่านสู่สถาปัตยกรรมแบบ Cloud-Native ที่ต้องทำงานร่วมกับเทคโนโลยีคอนเทนเนอร์ (Containerization) และระบบจัดการฐานข้อมูลเชิงสัมพันธ์ (RDBMS)
งานวิจัยที่ผ่านมาได้ยืนยันแล้วว่าคอนเทนเนอร์มีภาระงานส่วนเกินด้านหน่วยประมวลผลกลางและหน่วยความจำต่ำมากเมื่อเทียบกับเครื่องจริง (Bare Metal) และดีกว่าเครื่องเสมือน (Virtual Machine) แต่มีภาระงานส่วนเกินที่ชัดเจนในส่วนของ Disk I/O และเครือข่าย (Network I/O) [3][4][5][6][19][20] อีกทั้งยังมีงานวิจัยที่เปรียบเทียบสถาปัตยกรรมแบบโมโนลิทิก (Monolithic Architecture) และไมโครเซอร์วิส (Microservices Architecture) [7][8][9][31] และเปรียบเทียบประสิทธิภาพของภาษาโปรแกรมและระบบฐานข้อมูล [10][11][12][13][15][16] แต่การศึกษาเหล่านั้นส่วนใหญ่ใช้ Microbenchmark เชิงสังเคราะห์ ทดสอบเพียงรอบเดียว หรือไม่ได้รายงานค่าทางสถิติ ทำให้ยังตอบคำถามได้ไม่ชัดเจนว่า เมื่อภาษาโปรแกรมและเว็บเฟรมเวิร์กทำงานอยู่ภายในคอนเทนเนอร์ พร้อมทั้งเชื่อมต่อกับฐานข้อมูลภายใต้สภาวะโหลดสูง ประสิทธิภาพการทำงานแบบครบทั้งเส้นทาง (End-to-End: HTTP → Runtime → RDBMS) จะลดทอนลงมากน้อยเพียงใด
ด้วยเหตุนี้ งานวิจัยนี้จึงนำเสนอการประเมินและเปรียบเทียบประสิทธิภาพเชิงลึกภายใต้สภาพแวดล้อมการทำงานที่แตกต่างกัน เพื่อเป็นแนวทางให้นักพัฒนาและสถาปนิกซอฟต์แวร์สามารถเลือกชุดเทคโนโลยี (Technology Stack) และปรับแต่งประสิทธิภาพ (Optimization) ได้อย่างเหมาะสมและคุ้มค่าที่สุดกับสภาพแวดล้อมโครงสร้างพื้นฐานที่มีอยู่
2.วัตถุประสงค์
1. เพื่อประเมินและเปรียบเทียบภาระงานส่วนเกิน (Overhead) ของการทำงานแบบคอนเทนเนอร์ (Docker) เทียบกับการทำงานบนเครื่องจริง (Bare Metal) ในระดับแอปพลิเคชันเว็บที่เชื่อมต่อฐานข้อมูลจริง (End-to-End) แยกตามภาษาโปรแกรมและระดับภาระงาน
2. เพื่อวิเคราะห์และเปรียบเทียบสมรรถนะของภาษาและเว็บเฟรมเวิร์กที่แตกต่างกัน (Python, Node.js, PHP, Go และ Java) ในการรองรับภาระงานฐานข้อมูลทั้งการอ่าน (GET) และการเขียน (POST) ภายใต้ระดับความซับซ้อนของข้อมูลที่หลากหลาย
3. เพื่อศึกษาผลกระทบของดัชนีฐานข้อมูล (Secondary Index) และระดับความพร้อมกันของผู้ใช้งาน (Concurrency) ที่มีต่อเวลาในการตอบสนอง (Response Time) ปริมาณงานที่รองรับได้ (Throughput) และความเสถียรของระบบภายใต้สภาวะโหลดสูง
หมายเหตุ: การเปรียบเทียบสถาปัตยกรรม Monolithic กับ Microservices การเปรียบเทียบคอนเทนเนอร์กับเครื่องเสมือน (VM) และการเปรียบเทียบระบบจัดการฐานข้อมูล (MySQL กับ PostgreSQL) มีงานวิจัยที่ศึกษาไว้แล้วอย่างเพียงพอ งานวิจัยนี้จึงอ้างอิงผลเหล่านั้นแทนการทดลองซ้ำ (ดูบทที่ 2 หัวข้อ แผนการวิจัยและการนำเสนอผล)

บทที่ 2เอกสารและงานวิจัยที่เกี่ยวข้อง

1.งานด้านการเปรียบเทียบภาษาโปรแกรมและเว็บเฟรมเวิร์ก
Wickramage และ Weerawarana (2005) [1]: นำเสนอ "A Benchmark for Web Service Frameworks" ในงานประชุม IEEE SCC'05 ซึ่งเป็นเกณฑ์มาตรฐานที่จำลองบริการทางธุรกิจในโลกความเป็นจริง เพื่อใช้ประเมินและเปรียบเทียบประสิทธิภาพของโครงร่างบริการเว็บ (Web Service Frameworks) พบว่าความซับซ้อนของข้อความ SOAP และขนาดของข้อมูล (Payload size) เป็นปัจจัยหลักที่มีผลต่อเวลาตอบสนองไป-กลับ (Round-trip Time)
Prechelt (2000) [2]: ศึกษาเชิงประจักษ์ "An Empirical Comparison of Seven Programming Languages" โดยเปรียบเทียบโปรแกรมเดียวกัน 80 ชุดที่เขียนด้วยภาษา C, C++, Java, Perl, Python, Rexx และ Tcl พบว่าภาษา Scripting ใช้เวลาเขียนและจำนวนบรรทัดประมาณครึ่งหนึ่ง แต่ใช้หน่วยความจำประมาณ 2 เท่าของ C/C++ และความแปรปรวนระหว่างผู้เขียนโปรแกรม (Inter-programmer variability) มีขนาดใกล้เคียงกับความแตกต่างระหว่างภาษา
Lei et al. (2014) [11]: เปรียบเทียบเทคโนโลยีเว็บ PHP, Python และ Node.js ผ่าน Benchmark และการทดสอบตามสถานการณ์ พบว่า Node.js รองรับคำร้องขอได้มากที่สุดและเหมาะกับงานที่เน้น I/O
Effendy et al. (2021) [10]: ศึกษา "Performance Comparison of Web Backend and Database: A Case Study of Node.JS, Golang and MySQL, Mongo DB" เปรียบเทียบ 4 ชุดผสม (Node.js/Go × MySQL/MongoDB) พบว่า Go ร่วมกับ MySQL ใช้ CPU และหน่วยความจำดีที่สุด ขณะที่ Node.js ร่วมกับ MySQL ให้เวลาตอบสนองดีที่สุด
Choma et al. (2023) [12]: เปรียบเทียบ Express, Django และ Spring Boot ภายใต้ภาระงาน 1,000–16,000 คำร้องขอที่เชื่อมต่อฐานข้อมูลเดียวกัน พบว่า Spring Boot เร็วที่สุด แต่มีอัตราความผิดพลาดสูงกว่า Express ที่ภาระงานสูงสุด และ Django ช้าและผิดพลาดมากที่สุด
Azzahidi et al. (2025) [13]: เปรียบเทียบ REST API ของ Spring Boot, Flask, Express.js, Laravel (FrankenPHP) และ Gin ด้านเวลาตอบสนอง Throughput และการใช้ทรัพยากร พบว่า Spring Boot ดีที่สุดในทุกตัวชี้วัด ซึ่งเป็นงานที่ใกล้เคียงกับงานวิจัยนี้มากที่สุดในด้านชุดภาษา
Ala'anzy et al. (2026) [14]: ทดสอบ Throughput และ Latency (p50–p95) ของเฟรมเวิร์กภาษา Go, Rust, Node.js, Java, C# และ Python ภายใต้ทรัพยากรจำกัด พบว่าเฟรมเวิร์กที่คอมไพล์เป็น Native Binary ให้ประสิทธิภาพดีกว่ากลุ่ม Managed Runtime แต่เป็นการทดสอบด้วยข้อมูล JSON คงที่โดยไม่มีฐานข้อมูล
The Benchmarker (2017–2026) [25]: โครงการ "Web Frameworks Benchmark" บน GitHub (ผู้ดูแลหลัก M. Rabbâa) ทดสอบเฟรมเวิร์กจำนวนมากภายในคอนเทนเนอร์ด้วย Endpoint พื้นฐาน (GET /, GET /user/:id, POST /user) โดยไม่มีฐานข้อมูล และระบุไว้เองว่าไม่ควรนำผลไปอนุมานกับภาระงานที่มีฐานข้อมูล ผลอันดับเปลี่ยนแปลงอยู่ตลอดเวลา
TechEmpower (2025) [26]: โครงการ "TechEmpower Web Framework Benchmarks" รอบสุดท้าย (Round 23, มี.ค. 2568) ประกอบด้วยการทดสอบ 7 ประเภท ได้แก่ JSON, Single Query, Multiple Queries, Fortunes, Database Updates, Plaintext และ Cached Queries ร่วมกับ PostgreSQL, MySQL และ MongoDB โครงการยุติและเก็บถาวรเมื่อ มี.ค. 2569 และทดสอบบนเครื่องจริงเท่านั้น ไม่ได้เปรียบเทียบกับคอนเทนเนอร์
Pereira et al. (2021) [24]: จัดอันดับภาษาโปรแกรม 27 ภาษาตามประสิทธิภาพพลังงาน เวลา และหน่วยความจำ งานวิจัยนี้จึงอ้างอิงผลด้านพลังงานจากงานดังกล่าวแทนการวัดซ้ำ

2.งานด้านคอนเทนเนอร์ เครื่องเสมือน และเครื่องจริง
Morabito, Kjällman และ Komu (2015) [3]: ศึกษา "Hypervisors vs. Lightweight Virtualization: A Performance Comparison" ในงานประชุม IEEE IC2E 2015 เปรียบเทียบ Native, KVM, LXC, Docker และ OSv ด้วย Microbenchmark (Y-cruncher, NBENCH, Linpack, Bonnie++, dd, STREAM และ netperf) ทำซ้ำ 15 รอบและรายงานค่าเฉลี่ยและส่วนเบี่ยงเบนมาตรฐาน พบว่า CPU ของคอนเทนเนอร์ใกล้เคียงเครื่องจริง (ประสิทธิภาพ Y-cruncher แบบหลายแกน: Native 98.27%, Docker 98.16%, KVM 97.51%) แต่ Docker มีความหน่วงเครือข่ายแบบ Request-Response (TCP_RR) ลดลงประมาณ 19.4% (KVM 47.4%) และ Random Write ของดิสก์ลดลงประมาณ 14.7% (KVM 50.3%) ข้อจำกัดของงานนี้คือใช้เพียง Microbenchmark เชิงสังเคราะห์บนเครื่องเดียว ไม่มีภาระงานระดับแอปพลิเคชัน (เว็บเฟรมเวิร์กจริงที่เชื่อมต่อฐานข้อมูล)
Felter et al. (2015) [4]: ศึกษา "An Updated Performance Comparison of Virtual Machines and Linux Containers" พบว่า Docker มีประสิทธิภาพเท่ากับหรือดีกว่า KVM เกือบทุกกรณี ภาระงานส่วนเกินด้าน CPU และหน่วยความจำแทบไม่มี แต่มีภาระงานส่วนเกินในส่วน I/O และระบบเครือข่ายแบบ NAT ของ Docker
Amaral et al. (2015) [6]: ศึกษา "Performance Evaluation of Microservices Architectures Using Containers" ด้วย Sysbench และ Netperf พบว่าไม่มีภาระงานส่วนเกินด้าน CPU ที่มีนัยสำคัญ แต่การเชื่อมต่อเครือข่ายผ่าน Linux Bridge หรือ Open vSwitch ให้ Throughput ประมาณครึ่งหนึ่งและความหน่วงประมาณ 2 เท่าเมื่อเทียบกับเครือข่ายของเครื่องโฮสต์โดยตรง
Shetty et al. (2017) [5]: ศึกษา "An Empirical Performance Evaluation of Docker Container, OpenStack Virtual Machine and Bare Metal Server" ด้วย Phoronix Test Suite (CPU, หน่วยความจำ, ดิสก์ และ Apache Benchmark) พบว่า Docker ให้ผลเท่ากับหรือดีกว่า VM ในทุกการทดสอบ โดย VM ช้ากว่าเครื่องจริงประมาณ 21–30% และในการเขียนดิสก์ (IOzone) VM ลดลงประมาณ 54% ขณะที่ Docker ลดลงประมาณ 13% อย่างไรก็ตาม งานนี้ไม่มีฐานข้อมูล และไม่รายงานจำนวนรอบการทดสอบหรือช่วงความเชื่อมั่น
Wen et al. (2023) [19] และ Baumgartner et al. (2023) [20]: งานวิจัยล่าสุดยืนยันว่าคอนเทนเนอร์สูญเสียประสิทธิภาพด้าน CPU หน่วยความจำ และเครือข่ายประมาณ 0–5% และด้านดิสก์ประมาณ 5–15% เมื่อเทียบกับเครื่องจริง ขณะที่ VM สูญเสียมากกว่า

3.งานด้านสถาปัตยกรรม Monolithic และ Microservices
Villamizar et al. (2015) [7]: ศึกษา "Evaluating the Monolithic and the Microservice Architecture Pattern to Deploy Web Applications in the Cloud" ในงานประชุม 10th Computing Colombian Conference โดยพัฒนาแอปพลิเคชันเดียวกันทั้งสองสถาปัตยกรรมบน AWS และทดสอบด้วย JMeter พบว่า Microservices ช่วยลดต้นทุนโครงสร้างพื้นฐานได้ แลกกับเวลาตอบสนองที่สูงขึ้นเล็กน้อย
Blinowski et al. (2022) [8]: ศึกษา "Monolithic vs. Microservice Architecture: A Performance and Scalability Evaluation" (IEEE Access) พัฒนา 4 รุ่น (Java และ C#) ทดสอบทั้งบนเครื่องเดียวและ Azure พบว่าบนเครื่องเดียว Monolithic มีประสิทธิภาพดีกว่า และการขยายแนวตั้ง (Vertical Scaling) คุ้มค่ากว่า
Lauwren และ Setianto (2022) [9]: ศึกษา "Microservice and Monolith Performance Comparison in Transaction Application" (Proxies: Jurnal Informatika) โดยใช้ภาษา Go (Echo สำหรับ Monolith และ Go-kit ผ่าน NGINX สำหรับ Microservices) ร่วมกับ PostgreSQL ทดสอบด้วย JMeter ที่ 100, 1,000 และ 5,000 เธรด พบว่า Monolith มีค่าเฉลี่ยความหน่วงต่ำกว่าเล็กน้อย (7,205 ms เทียบกับ 7,277 ms) ขณะที่ Microservices มีอัตราความสำเร็จสูงกว่าเล็กน้อย (63.66% เทียบกับ 61.44%) และอัตราความสำเร็จลดลงอย่างมากที่ภาระงานสูง ข้อจำกัดคือทดสอบรอบเดียวโดยไม่มีการวิเคราะห์ทางสถิติ
Dirgantara et al. (2024) [31]: เปรียบเทียบ Monolithic และ Microservices โดยใช้ Docker พบว่าผลการเปรียบเทียบกลับด้านขึ้นอยู่กับว่ามีการใช้ Docker หรือไม่ แสดงให้เห็นว่าผลของชั้นคอนเทนเนอร์และผลของสถาปัตยกรรมปะปนกันอยู่
ชาคริต ผาอินทร์ (2560) [27]: พัฒนาระบบจัดเก็บบันทึกจราจรเครือข่ายทั้งแบบ Monolithic และ Microservices พบว่าแบบ Microservices ให้เวลาในการสืบค้นบันทึกสั้นกว่า

4.งานด้านระบบจัดการฐานข้อมูลและดัชนี
Salunke และ Ouda (2024) [15]: ศึกษา "A Performance Benchmark for the PostgreSQL and MySQL Databases" (Future Internet) พบว่า PostgreSQL ทำ SELECT ได้เร็วกว่า MySQL อย่างมาก การ INSERT ใกล้เคียงกัน และเมื่อมีการอ่านและเขียนพร้อมกัน PostgreSQL มีเสถียรภาพกว่า
Truskowski et al. (2020) [16]: เปรียบเทียบ MySQL, MSSQL, PostgreSQL และ Oracle ที่ทำงานภายใน Docker ทำซ้ำ 100 รอบต่อคำสั่ง
Taipalus (2024) [17]: การทบทวนวรรณกรรมอย่างเป็นระบบของงานเปรียบเทียบประสิทธิภาพ DBMS พบว่างานส่วนใหญ่ไม่สะท้อนการใช้งานจริง และรายงานรายละเอียดไม่เพียงพอต่อการทำซ้ำ
Stack Overflow Developer Survey (2023–2025) [18]: PostgreSQL แซงหน้า MySQL เป็นฐานข้อมูลที่นักพัฒนาใช้มากที่สุดตั้งแต่ปี 2023 และในปี 2025 มีผู้ใช้ 55.6% เทียบกับ MySQL 40.5%
Kossmann et al. (2020) [28] และ Ramdhani และ Widodo (2026) [29]: ยืนยันว่าการเลือกดัชนีมีผลอย่างมากต่อต้นทุนของ Query โดยใน PostgreSQL ดัชนี B-Tree ลดเวลาการ JOIN ระดับ Query ลงได้หลายระดับขนาด (Orders of Magnitude) แต่เป็นการวัดที่ระดับ Query (EXPLAIN ANALYZE) ไม่ใช่ระดับ HTTP ทั้งเส้นทาง

5.งานด้านระเบียบวิธีการวัดประสิทธิภาพ
Georges et al. (2007) [21] และ Kalibera และ Jones (2013) [22]: ชี้ว่าการวัดแบบรอบเดียวหรือเลือกค่าที่ดีที่สุดอาจทำให้สรุปผลผิด และเสนอให้ทำซ้ำหลายรอบ แยกช่วงอุ่นเครื่อง (Warm-up) และรายงานช่วงความเชื่อมั่น
Papadopoulos et al. (2021) [23]: เสนอหลักการ 8 ข้อสำหรับการประเมินประสิทธิภาพที่ทำซ้ำได้ในระบบคลาวด์ เช่น การทดลองซ้ำ การรายงานสภาพแวดล้อมครบถ้วน และการเผยแพร่ชุดข้อมูล
Glozer (wrk) และ Tene (wrk2) [30]: เครื่องมือสร้างภาระงาน HTTP ที่ใช้ในงานวิจัยนี้ โดย wrk2 ได้ระบุปัญหา Coordinated Omission ที่อาจทำให้ค่า Tail Latency ของ wrk ต่ำกว่าความเป็นจริง ซึ่งจะระบุเป็นข้อจำกัดของงานวิจัย

ช่องว่างของงานวิจัย (Research Gap)
จากการทบทวนวรรณกรรมข้างต้น พบว่า (1) งานด้านคอนเทนเนอร์ [3][4][5][6][19][20] ใช้ Microbenchmark เชิงสังเคราะห์ (CPU, หน่วยความจำ, ดิสก์, netperf) ไม่มีภาระงานเว็บที่เชื่อมต่อฐานข้อมูลจริง (2) งานด้านภาษาและเฟรมเวิร์ก [10][11][12][13][14][25] ส่วนใหญ่ทดสอบบนสภาพแวดล้อมเดียว ไม่แยกผลของคอนเทนเนอร์ และหลายงานไม่มีฐานข้อมูล (3) งานด้านดัชนี [28][29] วัดผลที่ระดับ Query ไม่ใช่ Throughput และ Tail Latency ของแอปพลิเคชัน และ (4) งานจำนวนมาก [5][9][12] ทดสอบรอบเดียวโดยไม่รายงานค่าทางสถิติ ตรงข้ามกับข้อเสนอของ [21][22][23] งานวิจัยนี้จึงเติมเต็มช่องว่างด้วยการทดลองแบบปัจจัยครบส่วน (Full-factorial) ที่ผสานภาษาโปรแกรม 5 ภาษา สภาพแวดล้อม Bare Metal และ Docker สถานะดัชนี ความซับซ้อนของ Query และระดับ Concurrency 5 ระดับ ทดสอบซ้ำ 20 รอบ พร้อมรายงานค่าเฉลี่ย ส่วนเบี่ยงเบนมาตรฐาน ช่วงความเชื่อมั่น 95% และเปอร์เซ็นไทล์ p50–p99

6.แผนการวิจัยและการนำเสนอผล (Research Plan)
หลักการ: สิ่งที่มีงานวิจัยยืนยันแล้ว จะอ้างอิงโดยไม่ทดลองซ้ำ และทดลองเฉพาะส่วนที่ยังเป็นช่องว่าง

6.1 ประเด็นที่อ้างอิงได้ทันที (ไม่ทดลองซ้ำ)
| ประเด็น | ข้อสรุปที่มีอยู่แล้ว | อ้างอิง | การตัดสินใจในงานวิจัยนี้ |
| :--- | :--- | :--- | :--- |
| MySQL เทียบกับ PostgreSQL | PostgreSQL อ่านข้อมูลเร็วกว่าหรือเท่ากัน มีเสถียรภาพกว่าเมื่ออ่าน-เขียนพร้อมกัน และเป็นฐานข้อมูลที่นักพัฒนาใช้มากที่สุด | [15][16][17][18] | ไม่ทดสอบเปรียบเทียบ DBMS เอง ชุดทดสอบหลัก (main_web_benchmark) ใช้ MySQL 8.0 ซึ่งทดลองเสร็จแล้ว และชุดทดสอบ POS (pos_web_benchmark) เลือกใช้ PostgreSQL 16 เพื่อให้ใกล้เคียงการใช้งานจริง |
| คอนเทนเนอร์เทียบกับ VM | คอนเทนเนอร์ดีกว่า VM เกือบทุกด้าน | [3][4][5][19][20] | ไม่ทดสอบ VM เปรียบเทียบเฉพาะ Bare Metal กับ Docker |
| ภาระงานส่วนเกินระดับ CPU/หน่วยความจำของคอนเทนเนอร์ | ประมาณ 0–5% ภาระงานส่วนเกินหลักอยู่ที่เครือข่ายแบบ NAT/Bridge และดิสก์ | [3][4][6][19][20] | ใช้เป็นสมมติฐานเพื่ออธิบายผลระดับแอปพลิเคชัน |
| Monolithic เทียบกับ Microservices | บนเครื่องเดียว Monolithic เร็วกว่า Microservices คุ้มค่าเมื่อขยายแนวนอน | [7][8][9][31] | ใช้บริการเดี่ยว (Single Service) ต่อภาษา และอ้างอิงผลเหล่านี้แทน |
| ดัชนีระดับ Query | ดัชนี B-Tree ลดเวลา JOIN ได้หลายระดับขนาด | [28][29] | วัดเฉพาะผลที่ส่งต่อถึง Throughput และ Tail Latency ระดับ HTTP |
| ประสิทธิภาพพลังงานของภาษา | จัดอันดับไว้แล้ว 27 ภาษา | [24] | ไม่วัดพลังงาน |

6.2 คำถามวิจัยและผลที่จะนำเสนอ
| คำถามวิจัย | ตัวชี้วัด | รูปแบบการนำเสนอ | แหล่งข้อมูลและสถานะ |
| :--- | :--- | :--- | :--- |
| RQ1: Docker ทำให้ประสิทธิภาพเว็บที่เชื่อมต่อฐานข้อมูลลดลงเท่าใด แยกตามภาษาและระดับภาระงาน | $\text{Gain}_{\text{BME}}$, $\bar{T}$ ± SD, 95% CI, p50/p99 | ตาราง Gain_BME (ภาษา × Tier) แยกตาม Endpoint | main_web_benchmark: เสร็จแล้ว (20 รอบ) / pos_web_benchmark: กำลังดำเนินการ |
| RQ2: ภาษาและเฟรมเวิร์กใดรองรับ GET/POST ได้ดีที่สุดเมื่อมีฐานข้อมูลจริง | $\bar{T}$, $\bar{L}$, p50–p99, $L_{\max}$ | ตารางอันดับตาม Endpoint และกราฟแท่งพร้อม Error Bar (95% CI) | main: เสร็จแล้ว / pos: กำลังดำเนินการ |
| RQ3: ดัชนีช่วยเพิ่ม Throughput ระดับ HTTP ได้กี่เท่า และมีผลต่อการเขียนอย่างไร | Index Speedup Ratio | ตาราง Speedup (ภาษา × จำนวน JOIN) | main: เสร็จแล้ว / pos: กำลังดำเนินการ (ข้อมูล 11.11 ล้านแถว) |
| RQ4: แต่ละภาษาถึงจุดอิ่มตัว (Saturation) ที่ระดับ Concurrency ใด | Throughput ต่อ Tier, จำนวน Error, p99 | กราฟเส้น Throughput และ p99 ตาม Tier พร้อมตาราง Error | main: เสร็จแล้ว / pos: กำลังดำเนินการ |
| RQ5: ผลจาก RQ1–RQ4 ยังคงเดิมหรือไม่เมื่อใช้ฐานข้อมูลขนาดใหญ่ใกล้เคียงระบบ POS จริงบน PostgreSQL | ตัวชี้วัดเดียวกับ RQ1–RQ4 | ตารางเปรียบเทียบแนวโน้มระหว่างสองชุดทดสอบ (ไม่เปรียบเทียบค่าสัมบูรณ์ข้าม DBMS) | pos_web_benchmark: กำลังดำเนินการ |

6.3 แนวทางการเขียนผลการทดลอง
ใช้โครงสร้างตามแบบของ Morabito et al. [3] ได้แก่ บทนำ → พื้นหลังและงานที่เกี่ยวข้อง → ระเบียบวิธี (ตารางฮาร์ดแวร์และเวอร์ชันซอฟต์แวร์ นโยบายการทำซ้ำ) → ผลการทดลองแยกหัวข้อย่อยตามประเภทภาระงาน → สรุปและงานในอนาคต โดยผลแต่ละการทดลองเขียนหนึ่งย่อหน้าที่ระบุเครื่องมือ การตั้งค่า และตารางหรือกราฟที่แสดงค่าร้อยละเทียบกับ Bare Metal พร้อมเพิ่มสิ่งที่งานดังกล่าวไม่มี ได้แก่ ช่วงความเชื่อมั่น 95% เปอร์เซ็นไทล์ และจำนวน Error

6.4 ผลเบื้องต้นจากชุดทดสอบหลัก (main_web_benchmark: MySQL 8.0, 10,000 แถวต่อตาราง, 20 รอบต่อค่า)
ตารางที่ 1 ภาระงานส่วนเกินของ Docker ($\text{Gain}_{\text{BME}}$ %, ค่าบวกหมายถึง Bare Metal เร็วกว่า)
| Endpoint | ภาษา | POC | Small | General | High | Stress |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| GET 1table (with index) | Go | 22.9 | 30.4 | 21.3 | 25.8 | 27.1 |
| GET 1table (with index) | Java | 28.5 | 33.3 | 38.5 | 33.9 | 33.7 |
| GET 1table (with index) | Node.js | 390.3 | 409.5 | 406.6 | 346.2 | 362.6 |
| GET 1table (with index) | PHP | 19.2 | 56.8 | 57.1 | 58.4 | 54.8 |
| GET 1table (with index) | Python (opt.) | -9.5 | 15.1 | 15.0 | 15.2 | 17.1 |
| GET 4join (with index) | Go | -4.6 | -0.3 | -1.4 | 0.9 | 2.8 |
| GET 4join (with index) | Java | -1.7 | 0.8 | 1.5 | 3.3 | 2.9 |
| GET 4join (with index) | Node.js | 41.1 | 20.5 | 24.8 | 11.3 | 12.2 |
| GET 4join (with index) | PHP | -3.8 | -1.8 | -1.9 | -2.8 | -1.3 |
| GET 4join (with index) | Python (opt.) | -5.0 | -1.3 | -0.4 | 1.4 | -2.0 |
| POST 1table | Go | 31.2 | 14.4 | 15.1 | 15.0 | 14.4 |
| POST 1table | Java | 31.5 | 20.0 | 20.3 | 19.9 | 21.0 |
| POST 1table | Node.js | 34.9 | 57.3 | 27.7 | 30.5 | 30.7 |
| POST 1table | PHP | 48.9 | 24.9 | 21.9 | 25.4 | 25.9 |
| POST 1table | Python (opt.) | 8.2 | 59.1 | 21.2 | 23.1 | 27.8 |
| POST 4table | Go | 9.1 | 3.8 | 3.1 | 3.6 | 4.1 |
| POST 4table | Java | 12.6 | 7.3 | 10.3 | 9.9 | 9.1 |
| POST 4table | Node.js | 25.7 | 22.7 | 20.6 | 21.6 | 24.4 |
| POST 4table | PHP | 7.3 | 16.1 | 14.1 | 15.1 | 16.1 |
| POST 4table | Python (opt.) | 8.7 | 9.5 | 7.6 | 5.9 | 6.3 |

ข้อสังเกตเบื้องต้น: สำหรับ Query ที่เบา (1table) ภาระงานส่วนเกินของ Docker อยู่ที่ประมาณ 15–58% ซึ่งสูงกว่าที่ Microbenchmark ด้าน CPU รายงานไว้ (0–5%) [19][20] แต่สอดคล้องกับข้อค้นพบว่าภาระงานส่วนเกินหลักอยู่ที่เครือข่ายแบบ Bridge/NAT [3][4][6] เนื่องจากในการทดลองนี้คอนเทนเนอร์เชื่อมต่อผ่าน Port Mapping และเชื่อมต่อฐานข้อมูลผ่าน host.docker.internal เมื่อ Query หนักขึ้น (4join) ฐานข้อมูลกลายเป็นคอขวด และภาระงานส่วนเกินลดลงเหลือประมาณ ±3% (ยกเว้น Node.js) ส่วน Node.js ใน Docker มีค่าผิดปกติ (Bare Metal เร็วกว่าประมาณ 4 เท่าใน 1table) ซึ่งต้องตรวจสอบการตั้งค่าจำนวน Cluster Worker ภายในคอนเทนเนอร์ก่อนสรุปผล

ตารางที่ 2 อัตราเร่งจากดัชนี (Index Speedup Ratio, Docker, Tier General)
| ภาษา | 1table | 2join | 3join | 4join |
| :--- | ---: | ---: | ---: | ---: |
| Go | 1.0 | 1.0 | 6.8 | 25.7 |
| Java | 1.0 | 1.0 | 6.5 | 25.4 |
| Node.js | 1.0 | 1.0 | 5.5 | 20.4 |
| PHP | 1.0 | 1.0 | 7.0 | 26.8 |
| Python (opt.) | 1.0 | 1.0 | 5.8 | 2.6 |

ข้อสังเกตเบื้องต้น: ดัชนีไม่มีผลต่อ 1table และ 2join แต่เพิ่ม Throughput ระดับ HTTP ได้ประมาณ 5.5–7 เท่าที่ 3join และ 20–27 เท่าที่ 4join ซึ่งน้อยกว่าอัตราเร่งระดับ Query ที่รายงานไว้ใน [29] เพราะเมื่อฐานข้อมูลเร็วขึ้น คอขวดจะย้ายไปอยู่ที่ Runtime และ Connection Pool ค่า 2.6 เท่าของ Python (opt.) ที่ 4join เป็นค่าผิดปกติที่ต้องตรวจสอบเพิ่มเติม

ตารางที่ 3 จุดอิ่มตัว (GET 1table with index: Throughput Req/s / จำนวน Error รวม)
| ภาษา | สภาพแวดล้อม | General (500) | High (2,000) | Stress (10,000) |
| :--- | :--- | :--- | :--- | :--- |
| Go | Docker | 12,987 / 0 | 14,835 / 262,217 | 15,535 / 4,898,881 |
| Go | Bare Metal | 15,759 / 0 | 18,662 / 228,143 | 19,740 / 4,573,078 |
| Java | Docker | 12,169 / 0 | 12,373 / 720 | 12,195 / 193,797 |
| Java | Bare Metal | 16,855 / 0 | 16,567 / 799 | 16,309 / 151,654 |
| Node.js | Docker | 2,110 / 2,211 | 1,984 / 31,227 | 1,972 / 8,247,289 |
| Node.js | Bare Metal | 10,690 / 0 | 8,853 / 21,655 | 9,124 / 176,890 |
| PHP | Docker | 17,203 / 0 | 16,749 / 0 | 16,587 / 263,220 |
| PHP | Bare Metal | 27,030 / 0 | 26,532 / 0 | 25,672 / 0 |
| Python (opt.) | Docker | 4,042 / 149 | 3,913 / 489,562 | 3,515 / 20,247,546 |
| Python (opt.) | Bare Metal | 4,647 / 205 | 4,508 / 429,991 | 4,118 / 18,232,247 |

ข้อสังเกตเบื้องต้น: ทุกภาษาเริ่มเกิด Error ที่ Tier High (2,000 connections) ยกเว้น PHP (Swoole) บน Bare Metal ที่ไม่มี Error แม้ที่ Tier Stress

6.5 ข้อจำกัดที่ต้องระบุ
1. wrk มีปัญหา Coordinated Omission [30] ค่า Tail Latency (p99) อาจต่ำกว่าความเป็นจริง
2. ผลของ main_web_benchmark (MySQL) และ pos_web_benchmark (PostgreSQL) มีขนาดข้อมูลและ Schema ต่างกัน จึงเปรียบเทียบได้เฉพาะแนวโน้ม ไม่เปรียบเทียบค่าสัมบูรณ์ข้าม DBMS
3. ทดสอบบนเครื่องเดียว (ผู้สร้างภาระงาน แอปพลิเคชัน และฐานข้อมูลอยู่บนเครื่องเดียวกัน) ซึ่งทำให้เกิดการแย่งทรัพยากร CPU

บทที่ 3วิธีการดำเนินการวิจัย

งานวิจัยนี้ดำเนินตามระเบียบวิธีวิจัยเชิงทดลอง (Experimental Research) โดยใช้การออกแบบการทดลองแบบปัจจัยครบส่วน (Full-factorial Design) เพื่อศึกษาความสัมพันธ์และผลกระทบระหว่างสภาพแวดล้อมการทำงาน รันไทม์ภาษาโปรแกรม และระบบฐานข้อมูล โดยมีขั้นตอนการดำเนินงานดังนี้
1.สภาพแวดล้อมที่ใช้ในการทดลอง
2.การออกแบบซอฟต์แวร์และระบบ
3.การกำหนดตัวแปรต้นและระดับการทดลอง
4.ประเภทของภาระงานที่ทดสอบ
5.ขั้นตอนการดำเนินการทดลอง
6.การวิเคราะห์ข้อมูล

อ้างอิง

[1] N. Wickramage and S. Weerawarana, "A benchmark for web service frameworks," in Proc. IEEE Int. Conf. Services Comput. (SCC'05), Orlando, FL, USA, 2005, vol. 1, pp. 233–240. doi: 10.1109/SCC.2005.9.

[2] L. Prechelt, "An empirical comparison of seven programming languages," Computer, vol. 33, no. 10, pp. 23–29, Oct. 2000. doi: 10.1109/2.876288.

[3] R. Morabito, J. Kjällman, and M. Komu, "Hypervisors vs. lightweight virtualization: A performance comparison," in Proc. IEEE Int. Conf. Cloud Eng. (IC2E), Tempe, AZ, USA, 2015, pp. 386–393. doi: 10.1109/IC2E.2015.74.

[4] W. Felter, A. Ferreira, R. Rajamony, and J. Rubio, "An updated performance comparison of virtual machines and Linux containers," in Proc. IEEE Int. Symp. Perform. Anal. Syst. Softw. (ISPASS), Philadelphia, PA, USA, 2015, pp. 171–172. doi: 10.1109/ISPASS.2015.7095802.

[5] J. Shetty, S. Upadhaya, H. S. Rajarajeshwari, G. Shobha, and J. Chandra, "An empirical performance evaluation of Docker container, OpenStack virtual machine and bare metal server," Indonesian J. Elect. Eng. Comput. Sci., vol. 7, no. 1, pp. 205–213, Jul. 2017. doi: 10.11591/ijeecs.v7.i1.pp205-213.

[6] M. Amaral, J. Polo, D. Carrera, I. Mohomed, M. Unuvar, and M. Steinder, "Performance evaluation of microservices architectures using containers," in Proc. IEEE 14th Int. Symp. Netw. Comput. Appl. (NCA), Cambridge, MA, USA, 2015, pp. 27–34. doi: 10.1109/NCA.2015.49.

[7] M. Villamizar, O. Garcés, H. Castro, M. Verano, L. Salamanca, R. Casallas, and S. Gil, "Evaluating the monolithic and the microservice architecture pattern to deploy web applications in the cloud," in Proc. 10th Computing Colombian Conf. (10CCC), Bogotá, Colombia, 2015, pp. 583–590. doi: 10.1109/ColumbianCC.2015.7333476.

[8] G. Blinowski, A. Ojdowska, and A. Przybyłek, "Monolithic vs. microservice architecture: A performance and scalability evaluation," IEEE Access, vol. 10, pp. 20357–20374, 2022. doi: 10.1109/ACCESS.2022.3152803.

[9] A. J. Lauwren and Y. D. Setianto, "Microservice and monolith performance comparison in transaction application," Proxies: Jurnal Informatika, vol. 5, no. 2, pp. 86–105, 2022. doi: 10.24167/proxies.v5i2.12447.

[10] F. Effendy, Taufik, and B. Adhilaksono, "Performance comparison of web backend and database: A case study of Node.JS, Golang and MySQL, Mongo DB," Recent Adv. Comput. Sci. Commun., vol. 14, no. 6, pp. 1955–1961, 2021. doi: 10.2174/2666255813666191219104133.

[11] K. Lei, Y. Ma, and Z. Tan, "Performance comparison and evaluation of web development technologies in PHP, Python, and Node.js," in Proc. IEEE 17th Int. Conf. Comput. Sci. Eng. (CSE), Chengdu, China, 2014, pp. 661–668. doi: 10.1109/CSE.2014.142.

[12] D. Choma, K. Chwaleba, and M. Dzieńkowski, "The efficiency and reliability of backend technologies: Express, Django, and Spring Boot," Informatyka, Automatyka, Pomiary w Gospodarce i Ochronie Środowiska, vol. 13, no. 4, pp. 73–78, 2023. doi: 10.35784/iapgos.4279.

[13] A. Azzahidi, B. Wijayanto, and A. Darmawan, "Performance evaluation of backend frameworks for REST API: A comparative study of Spring Boot, Flask, Express.js, Laravel FrankenPHP, and Gin," Jurnal Teknik Informatika (JUTIF), vol. 6, no. 4, pp. 2405–2419, 2025. doi: 10.52436/1.jutif.2025.6.4.4811.

[14] M. A. Ala'anzy, O. Alramli, A. Ibraheem, and A. Al-Hadeethi, "Throughput and latency benchmarking of backend web frameworks under resource-constrained environments," in Proc. 6th Int. Conf. Electr., Comput., Commun. Mechatron. Eng. (ICECET), 2026, pp. 1–5. doi: 10.1109/ICECET65726.2026.11632913.

[15] S. V. Salunke and A. Ouda, "A performance benchmark for the PostgreSQL and MySQL databases," Future Internet, vol. 16, no. 10, Art. no. 382, 2024. doi: 10.3390/fi16100382.

[16] W. Truskowski, R. Klewek, and M. Skublewska-Paszkowska, "Comparison of MySQL, MSSQL, PostgreSQL, Oracle databases performance, including virtualization," Journal of Computer Sciences Institute, vol. 16, pp. 279–284, 2020. doi: 10.35784/jcsi.2026.

[17] T. Taipalus, "Database management system performance comparisons: A systematic literature review," J. Syst. Softw., vol. 208, Art. no. 111872, 2024. doi: 10.1016/j.jss.2023.111872.

[18] Stack Overflow, "2025 Stack Overflow Developer Survey: Technology — Databases," 2025. [Online]. Available: https://survey.stackoverflow.co/2025/technology. [Accessed: Sep. 30, 2026].

[19] L. Wen, M. Rickert, F. Pan, J. Lin, and A. Knoll, "Bare-metal vs. hypervisors and containers: Performance evaluation of virtualization technologies for software-defined vehicles," in Proc. IEEE Intelligent Vehicles Symp. (IV), Anchorage, AK, USA, 2023, pp. 1–8. doi: 10.1109/IV55152.2023.10186789.

[20] J. Baumgartner, C. Lillo, and S. Rumley, "Performance losses with virtualization: Comparing bare metal to VMs and containers," in High Performance Computing (ISC High Performance 2023 Workshops), Lecture Notes in Computer Science, Cham, Switzerland: Springer, 2023, pp. 107–120. doi: 10.1007/978-3-031-40843-4_9.

[21] A. Georges, D. Buytaert, and L. Eeckhout, "Statistically rigorous Java performance evaluation," in Proc. 22nd ACM SIGPLAN Conf. Object-Oriented Program. Syst. Lang. Appl. (OOPSLA), Montreal, QC, Canada, 2007, pp. 57–76. doi: 10.1145/1297105.1297033.

[22] T. Kalibera and R. Jones, "Rigorous benchmarking in reasonable time," in Proc. ACM SIGPLAN Int. Symp. Memory Manage. (ISMM), Seattle, WA, USA, 2013, pp. 63–74. doi: 10.1145/2464157.2464160.

[23] A. V. Papadopoulos et al., "Methodological principles for reproducible performance evaluation in cloud computing," IEEE Trans. Softw. Eng., vol. 47, no. 8, pp. 1528–1543, Aug. 2021. doi: 10.1109/TSE.2019.2927908.

[24] R. Pereira et al., "Ranking programming languages by energy efficiency," Sci. Comput. Program., vol. 205, Art. no. 102609, 2021. doi: 10.1016/j.scico.2021.102609.

[25] M. Rabbâa et al. (The Benchmarker), "Web frameworks benchmark," GitHub repository, 2017–2026. [Online]. Available: https://github.com/the-benchmarker/web-frameworks. [Accessed: Sep. 30, 2026].

[26] TechEmpower, "TechEmpower web framework benchmarks, Round 23," 2025. [Online]. Available: https://www.techempower.com/benchmarks/. [Accessed: Sep. 30, 2026].

[27] ชาคริต ผาอินทร์, "การขยายตัวจัดเก็บบันทึกจราจรเครือข่ายด้วยสถาปัตยกรรมไมโครเซอร์วิส," วิทยานิพนธ์ปริญญาวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์, จุฬาลงกรณ์มหาวิทยาลัย, กรุงเทพฯ, 2560. doi: 10.58837/CHULA.THE.2017.1256.

[28] J. Kossmann, S. Halfpap, M. Jankrift, and R. Schlosser, "Magic mirror in my hand, which is the best in the land? An experimental evaluation of index selection algorithms," Proc. VLDB Endow., vol. 13, no. 12, pp. 2382–2395, 2020. doi: 10.14778/3407790.3407832.

[29] A. Ramdhani and S. Widodo, "Comparative analysis of B-Tree and Hash indexes for PostgreSQL query optimization," JURTEKSI (Jurnal Teknologi dan Sistem Informasi), vol. 12, no. 3, pp. 461–468, 2026. doi: 10.33330/jurteksi.v12i3.4653.

[30] W. Glozer, "wrk: Modern HTTP benchmarking tool," GitHub repository. [Online]. Available: https://github.com/wg/wrk; G. Tene, "wrk2: A constant throughput, correct latency recording variant of wrk," GitHub repository. [Online]. Available: https://github.com/giltene/wrk2. [Accessed: Sep. 30, 2026].

[31] D. P. Dirgantara, D. S. Kusumo, and R. G. Utomo, "Docker-based monolithic and microservices architecture performance comparison," Jurnal Teknik Informatika (JUTIF), vol. 5, no. 2, pp. 357–365, 2024. doi: 10.52436/1.jutif.2024.5.2.1338.
