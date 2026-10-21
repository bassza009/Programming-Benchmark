'use strict';

function playOptimal(n) {
    let pardoned = 0;
    const inDrawer = new Array(100);
    for (let i = 0; i < 100; i++) {
        inDrawer[i] = i;
    }

    let seed = 42;

    for (let r = 0; r < n; r++) {
        for (let i = 99; i > 0; i--) {
            seed = (seed * 1664525 + 1013904223) & 0x7fffffff;
            const j = seed % (i + 1);
            const temp = inDrawer[i];
            inDrawer[i] = inDrawer[j];
            inDrawer[j] = temp;
        }

        let allFound = true;
        for (let prisoner = 0; prisoner < 100; prisoner++) {
            let found = false;
            let reveal = prisoner;
            for (let step = 0; step < 50; step++) {
                const card = inDrawer[reveal];
                if (card === prisoner) {
                    found = true;
                    break;
                }
                reveal = card;
            }
            if (!found) {
                allFound = false;
                break;
            }
        }
        if (allFound) {
            pardoned++;
        }
    }
    return (pardoned / n) * 100.0;
}

function main() {
    const n = 1000000;
    console.log(`Optimal play wins: ${playOptimal(n).toFixed(4)}%`);
}

main();
