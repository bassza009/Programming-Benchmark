'use strict';

function countPrimes(limit) {
    let count = 0;
    for (let i = 2; i <= limit; i++) {
        let isPrime = true;
        // ลูปชั้นที่ 2: ใช้ j * j <= i เพื่อประสิทธิภาพสูงสุด
        for (let j = 2; j * j <= i; j++) {
            if (i % j === 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) {
            count++;
        }
    }
    return count;
}

const n = 10000000;
console.log(`Starting Prime Count (Node.js): ${n}`);


const result = countPrimes(n);


console.log(`Primes count: ${result}`);
