'use strict';

const N = 1000;

// 1. เตรียมข้อมูล (ไม่นับรวมในเวลาประมวลผลหลัก)
const matrixA = new Float64Array(N * N);
const matrixB = new Float64Array(N * N);
const result = new Float64Array(N * N);

for (let i = 0; i < N * N; i++) {
    matrixA[i] = i % N;
    matrixB[i] = Math.floor(i / N);
}

console.log(`Starting Matrix Multiplication (Node.js): ${N}x${N}`);

// 2. เริ่มจับเวลา (ตรงตามข้อ 3.5 ในไฟล์วิจัย)


for (let i = 0; i < N; i++) {
    for (let j = 0; j < N; j++) {
        let sum = 0;
        for (let k = 0; k < N; k++) {
            // สูตรคำนวณ Index สำหรับ Flat Array: (row * total_cols) + col
            sum += matrixA[i * N + k] * matrixB[k * N + j];
        }
        result[i * N + j] = sum;
    }
}



// 3. แสดงผลลัพธ์

console.log(`Sample Result [0]: ${result[0]}`);