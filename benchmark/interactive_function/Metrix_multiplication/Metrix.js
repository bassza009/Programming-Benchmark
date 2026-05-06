'use strict';
const n = 1000;
const a = new Float64Array(n * n);
const b = new Float64Array(n * n);
const res = new Float64Array(n * n);

for (let i = 0; i < n * n; i++) {
    a[i] = i % n;
    b[i] = Math.floor(i / n);
}

console.log(`Starting Matrix Multiplication (Node.js): ${n}x${n}`);

for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
        let sum = 0;
        for (let k = 0; k < n; k++) {
            sum += a[i * n + k] * b[k * n + j];
        }
        res[i * n + j] = sum;
    }
}
console.log(`Sample Result [0]: ${res[0]}`);