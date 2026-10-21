'use strict';

function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

function main() {
    const n = 40;
    console.log(fibonacci(n));
}

main();
