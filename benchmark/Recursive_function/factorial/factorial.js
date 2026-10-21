'use strict';

function factorial(n) {
    if (n <= 1) {
        return 1.0;
    }
    return n * factorial(n - 1);
}

function main() {
    const n = 100;
    console.log(factorial(n).toExponential(6));
}

main();
