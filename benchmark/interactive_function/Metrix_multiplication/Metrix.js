'use strict';

function main() {
    const n = 1000;
    const a = new Array(n * n);
    const b = new Array(n * n);
    const result = new Array(n * n);

    for (let i = 0; i < n * n; i++) {
        a[i] = i % n;
        b[i] = Math.floor(i / n);
    }

    for (let i = 0; i < n; i++) {
        const rowOffset = i * n;
        for (let j = 0; j < n; j++) {
            let sum = 0.0;
            for (let k = 0; k < n; k++) {
                sum += a[rowOffset + k] * b[k * n + j];
            }
            result[rowOffset + j] = sum;
        }
    }

    console.log(`Sample Result [0]: ${result[0].toFixed(2)}`);
}

main();
