<?php
ini_set('memory_limit', '512M');

function playOptimal($n) {
    $pardoned = 0;
    $inDrawer = [];
    for ($i = 0; $i < 100; $i++) {
        $inDrawer[$i] = $i;
    }

    $seed = 42;

    for ($r = 0; $r < $n; $r++) {
        for ($i = 99; $i > 0; $i--) {
            $seed = ($seed * 1664525 + 1013904223) & 0x7fffffff;
            $j = $seed % ($i + 1);
            $temp = $inDrawer[$i];
            $inDrawer[$i] = $inDrawer[$j];
            $inDrawer[$j] = $temp;
        }

        $allFound = true;
        for ($prisoner = 0; $prisoner < 100; $prisoner++) {
            $found = false;
            $reveal = $prisoner;
            for ($step = 0; $step < 50; $step++) {
                $card = $inDrawer[$reveal];
                if ($card === $prisoner) {
                    $found = true;
                    break;
                }
                $reveal = $card;
            }
            if (!$found) {
                $allFound = false;
                break;
            }
        }
        if ($allFound) {
            $pardoned++;
        }
    }
    return ($pardoned / $n) * 100.0;
}

$n = 1000000;
printf("Optimal play wins: %.4f%%\n", playOptimal($n));
