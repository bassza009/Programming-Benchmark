const _ = require('lodash');
const { performance } = require('perf_hooks'); // ใช้สำหรับวัดเวลาที่แม่นยำ

const numPlays = 10000; // แนะนำให้ใช้หมื่นรอบก่อน เพราะแบบ Random จะช้ามาก
const numPrisoners = 100;

const setupSecrets = () => {
    let secrets = [];
    for (let i = 0; i < numPrisoners; i++) {
        secrets.push(i);
    }
    return _.shuffle(secrets);
}

const playOptimal = () => {
    let secrets = setupSecrets();
    for (let p = 0; p < numPrisoners; p++) {
        let success = false;
        let choice = p;
        for (let i = 0; i < numPrisoners / 2; i++) {
            if (secrets[choice] === p) {
                success = true;
                break;
            }
            choice = secrets[choice];
        }
        if (!success) return false;
    }
    return true;
}

const playRandom = () => {
    let secrets = setupSecrets();
    for (let p = 0; p < numPrisoners; p++) {
        // สร้างรายการสุ่มเลือก 50 ใบจาก 100 ใบ
        let choices = _.sampleSize(_.range(numPrisoners), numPrisoners / 2);
        let success = false;
        for (let i = 0; i < choices.length; i++) {
            if (secrets[choices[i]] === p) {
                success = true;
                break;
            }
        }
        if (!success) return false;
    }
    return true;
}

// ฟังก์ชันหลักสำหรับทำ Benchmark
const runBenchmark = (name, fn) => {
    console.log(`Running ${name}...`);
    const startTime = performance.now(); // เริ่มจับเวลา
    let successCount = 0;

    for (let i = 0; i < numPlays; i++) {
        if (fn()) successCount++;
    }

    const endTime = performance.now(); // สิ้นสุดจับเวลา
    const durationSeconds = ((endTime - startTime) / 1000).toFixed(3);
    const winRate = ((successCount / numPlays) * 100).toFixed(2);

    return { name, winRate, durationSeconds };
}

// --- ส่วนแสดงผล ---
console.log(`--- 100 Prisoners Benchmark (${numPlays.toLocaleString()} rounds) ---`);

const results = [
    runBenchmark("Optimal Strategy", playOptimal),
    runBenchmark("Random Strategy", playRandom)
];

console.table(results); // แสดงผลเป็นตารางสวยงาม