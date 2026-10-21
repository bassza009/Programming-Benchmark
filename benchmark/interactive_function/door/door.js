'use strict';

function main() {
    const n = 1000000;
    const doors = new Array(n + 1).fill(false);

    for (let pass = 1; pass <= n; pass++) {
        for (let d = pass; d <= n; d += pass) {
            doors[d] = !doors[d];
        }
    }

    let openCount = 0;
    for (let i = 1; i <= n; i++) {
        if (doors[i]) {
            openCount++;
        }
    }
    console.log(`Open doors: ${openCount}`);
}

main();
