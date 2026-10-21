'use strict';

function main() {
    const n = 10000;
    const arr = new Array(n);
    for (let i = 0; i < n; i++) {
        arr[i] = n - i;
    }

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                const temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    console.log(`Sample Result [0]: ${arr[0]}, [${n - 1}]: ${arr[n - 1]}`);
}

main();
