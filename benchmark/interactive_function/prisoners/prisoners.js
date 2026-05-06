'use strict';

function playOptimal(n) {
    let pardoned = 0;
    const inDrawer = Array.from({length: 100}, (_, i) => i);

    for (let r = 0; r < n; r++) {
        // Shuffle
        for (let i = 99; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [inDrawer[i], inDrawer[j]] = [inDrawer[j], inDrawer[i]];
        }

        let allFound = true;
        for (let prisoner = 0; prisoner < 100; prisoner++) {
            let found = false;
            let reveal = prisoner;
            for (let go = 0; go < 50; go++) {
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
        if (allFound) pardoned++;
    }
    return (pardoned / n) * 100;
}

const n = 1000000;
console.log(`Optimal play wins (Node.js): ${playOptimal(n).toFixed(1)}%`);