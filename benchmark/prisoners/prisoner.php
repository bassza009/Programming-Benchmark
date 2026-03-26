<?php

function runTrials($n, $numPrisoners, $strategy) {
    $successCount = 0;
    $startTime = microtime(true);

    // แก้ไขจุดนี้: เติม $ หน้าตัวแปร i
    for ($i = 0; $i < $n; $i++) {
        $drawers = range(0, $numPrisoners - 1);
        shuffle($drawers);

        $allFound = true;
        for ($p = 0; $p < $numPrisoners; $p++) {
            $found = false;

            if ($strategy === 'optimal') {
                $choice = $p;
                for ($attempt = 0; $attempt < $numPrisoners / 2; $attempt++) {
                    if ($drawers[$choice] === $p) {
                        $found = true;
                        break;
                    }
                    $choice = $drawers[$choice];
                }
            } else {
                // สำหรับ Random แบบ Benchmark เราจะใช้การสุ่มเลือก Index
                $sampler = range(0, $numPrisoners - 1);
                shuffle($sampler);
                $picks = array_slice($sampler, 0, $numPrisoners / 2);
                
                foreach ($picks as $pick) {
                    if ($drawers[$pick] === $p) {
                        $found = true;
                        break;
                    }
                }
            }

            if (!$found) {
                $allFound = false;
                break;
            }
        }
        if ($allFound) {
            $successCount++;
        }
    }

    $endTime = microtime(true);
    return [
        'winRate' => number_format(($successCount / $n) * 100, 2) . '%',
        'timeUsed' => number_format($endTime - $startTime, 4) . 's'
    ];
}

$numPlays = 10000;
$prisonerCounts = [10, 100];

echo "\nPHP Programming Benchmark - 100 Prisoners Problem\n";
echo "Total Simulations: " . number_format($numPlays) . " rounds\n";
echo str_repeat("-", 65) . "\n";
printf("%-12s | %-12s | %-12s | %-12s\n", "Prisoners", "Strategy", "Win Rate", "Time Used");
echo str_repeat("-", 65) . "\n";

foreach ($prisonerCounts as $np) {
    foreach (['random', 'optimal'] as $strategy) {
        $result = runTrials($numPlays, $np, $strategy);
        printf(
            "%-12d | %-12s | %-12s | %-12s\n",
            $np,
            ucfirst($strategy),
            $result['winRate'],
            $result['timeUsed']
        );
    }
}
echo str_repeat("-", 65) . "\n";