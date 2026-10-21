'use strict';

function countPrimes(limit) {
    let count = 0;
    for (let i = 2; i <= limit; i++) {
        let isPrime = true;
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

function main() {
    const n = 1000000;
    const result = countPrimes(n);
    console.log(`Primes count: ${result}`);
}

main();
