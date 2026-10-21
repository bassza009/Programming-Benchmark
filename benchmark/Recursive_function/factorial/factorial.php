<?php
function factorial($n) {
    if ($n <= 1) {
        return 1.0;
    }
    return (float)$n * factorial($n - 1);
}

$n = 100;
printf("%.6e\n", factorial($n));
