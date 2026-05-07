'use strict';
const n = 1000;
const a = new Float64Array(n * n);
const b = new Float64Array(n * n);
const res = new Float64Array(n * n);

for (let i = 0; i < n * n; i++) {
    a[i] = i % n;
    b[i] = Math.floor(i / n);
}

console.log(`Starting Matrix Multiplication (Node.js - Flat): ${n}x${n}`);
const start = performance.now();

for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
            sum += a[i * n + k] * b[k * n + j];
        }
        res[i * n + j] = sum;
    }
}

const end = performance.now();
console.log(`Sample Result [0]: ${res[0]}`);
console.log(`Time: ${((end - start) / 1000).toFixed(4)} sec`);