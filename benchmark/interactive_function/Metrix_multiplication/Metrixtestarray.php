<?php
ini_set('memory_limit', '512M');

$n = 1000;
$a = array_fill(0, $n * $n, 0.0);
$b = array_fill(0, $n * $n, 0.0);
$result = array_fill(0, $n * $n, 0.0);

for ($i = 0; $i < $n * $n; $i++) {
    $a[$i] = (float)($i % $n);
    $b[$i] = (float)intdiv($i, $n);
}

for ($i = 0; $i < $n; $i++) {
    $rowOffset = $i * $n;
    for ($j = 0; $j < $n; $j++) {
        $sum = 0.0;
        for ($k = 0; $k < $n; $k++) {
            $sum += $a[$rowOffset + $k] * $b[$k * $n + $j];
        }
        $result[$rowOffset + $j] = $sum;
    }
}

printf("Sample Result [0]: %.2f\n", $result[0]);
