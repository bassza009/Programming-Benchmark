'use strict';
const n = 20000;
// ใช้ Int32Array เพื่อจำลองความเร็วเหมือน Typed Array ใน Go/Java
const arr = new Int32Array(n);

for (let i = 0; i < n; i++) {
    arr[i] = n - i;
}

console.log(`Starting Bubble Sort (Node.js): ${n} items`);


for (let i = 0; i < n; i++) {
    for (let j = 0; j < n - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
            let temp = arr[j];
            arr[j] = arr[j + 1];
            arr[j + 1] = temp;
        }
    }
}


console.log(`Sample Result [0]: ${arr[0]}`);
