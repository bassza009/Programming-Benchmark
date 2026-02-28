<body>
<div class="container">
    <h1>🛠️ Environment Setup & System Architecture</h1>
    <p>ส่วนนี้คือการเตรียมสภาพแวดล้อมสำหรับการทดลอง เพื่อให้มั่นใจว่าผลการวัดประสิทธิภาพ (Benchmarking) มีความแม่นยำและสามารถทำซ้ำได้ (Reproducible) </p>
    <h2>1. Hardware Specifications</h2>
    <p>เพื่อให้การทดลองอยู่ในสภาวะควบคุม (Controlled Conditions) เครื่องที่ใช้ทดสอบมีรายละเอียดดังนี้:</p>
    <div>
        server
    </div>
    <!--<div class="spec-grid">
        <div class="spec-item"><strong>Processor:</strong> Intel Core i5-8300H (Acer Nitro 5)</div>
        <div class="spec-item"><strong>Memory:</strong> 16GB DDR4</div>
        <div class="spec-item"><strong>Storage:</strong> NVMe SSD</div>
        <div class="spec-item"><strong>Operating System:</strong> Ubuntu 22.04 LTS / Windows 11</div>
    </div>-->
    <h2>2. Software Stack & Runtime Paradigms</h2>
    <p>การทดสอบครอบคลุม 4 ภาษาที่เป็นตัวแทนของแต่ละรูปแบบการทำงาน (Runtime Paradigms):</p>
    <table>
        <thead>
            <tr>
                <th>Language</th>
                <th>Runtime Paradigm </th>
                <th>Execution Model </th>
            </tr>
        </thead>
        <tbody>
            <tr><td><strong>Go</strong></td><td>Compiled</td><td>Goroutine-based concurrency</td></tr>
            <tr><td><strong>Java</strong></td><td>Virtual Machine</td><td>JVM with JIT Compilation</td></tr>
            <tr><td><strong>Node.js</strong></td><td>Event-driven</td><td>Non-blocking I/O</td></tr>
            <tr><td><strong>PHP</strong></td><td>Synchronous</td><td>Request-response model</td></tr>
        </tbody>
    </table>
    <h2>3. Containerization (Docker Setup)</h2>
    <p>ใช้ Docker เพื่อแยกส่วนประกอบของระบบ (Isolation) และควบคุมทรัพยากรให้คงที่:</p>
    <ul>
        <li><strong>Docker Engine:</strong> Version 24.x+ [cite: 63]</li>
        <li><strong>Container Isolation:</strong> ใช้ Linux namespaces และ control groups ในการจัดการ process </li>
        <li><strong>Resource Limit:</strong> กำหนดค่า <code>--cpus</code> และ <code>--memory</code> ใน Docker Compose ให้เท่ากันทุก Container เพื่อความยุติธรรมในการทดสอบ [cite: 126]</li>
    </ul>
    <h2>4. Database Configuration</h2>
    <p>ใช้ฐานข้อมูล 2 รูปแบบเพื่อวิเคราะห์ความแตกต่างของการจัดการข้อมูลภายใต้ Workload ที่หลากหลาย:</p>
    <ul>
        <li><strong>MySQL:</strong> สำหรับทดสอบการทำงานแบบ Transactional (CRUD) ทั่วไป </li>
        <li><strong>PostgreSQL:</strong> สำหรับทดสอบการ Query ที่มีความซับซ้อน (Complex Joins)</li>
    </ul>
    <div class="note">
        <strong>Note:</strong> ทั้งคู่ต้องใช้ Schema, Indexes และชุดข้อมูล (Dataset) ขนาดเดียวกันทั้งหมดเพื่อให้ผลลัพธ์เปรียบเทียบกันได้
    </div>
    <h2>5. Load Generation Tool</h2>
    <p>ใช้ <strong>Apache JMeter</strong> ในการจำลองภาระงาน (Load Generation) ภายใต้ระดับความหนาแน่นที่ต่างกัน:</p>
    <ul>
        <li><strong>Concurrency Levels:</strong> ทดสอบที่ระดับ 50, 100, 200 จนถึง 500 users </li>
        <li><strong>Warm-up Phase:</strong> ก่อนเก็บผลจริง ต้องมีการรันระบบทิ้งไว้ช่วงหนึ่งเพื่อลดผลกระทบจาก Cache และ JIT bias </li>
    </ul>
</div>
</body>



