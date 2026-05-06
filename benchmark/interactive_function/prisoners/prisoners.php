<?php
function playOptimal($n) {
    $pardoned = 0;
    $inDrawer = range(0, 99);

    for ($r = 0; r < $n; r++) {
        shuffle($inDrawer);
        
        $allFound = true;
        for ($prisoner = 0; $prisoner < 100; $prisoner++) {
            $found = false;
            $reveal = $prisoner;
            for ($go = 0; $go < 50; $go++) {
                $card = $inDrawer[$reveal];
                if ($card === $prisoner) {
                    $found = true;
                    break;
                }
                reveal = $card;
            }
            if (!$found) {
                $allFound = false;
                break;
            }
        }
        if ($allFound) $pardoned++;
    }
    return ($pardoned / $n) * 100;
}

$n = 1000000;
printf("Optimal play wins (PHP): %.1f%%\n", playOptimal($n));