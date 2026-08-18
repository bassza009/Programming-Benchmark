<?php
$n = 1000;
$a = Array($n * $n);
$b = Array($n * $n);
$res = Array($n * $n);

for ($i = 0; $i < $n * $n; $i++) {
    $a[$i] = (double)($i % $n);
    $b[$i] = (double)floor($i / $n);
}

echo "Starting Matrix Multiplication (PHP - Flat): {$n}x{$n}\n";
// $start = microtime(true);

for ($i = 0; $i < $n; $i++) {
    for ($j = 0; $j < $n; $j++) {
        $sum = 0.0;
        for ($k = 0; $k < $n; $k++) {
            $sum += $a[$i * $n + $k] * $b[$k * $n + $j];
        }
        $res[$i * $n + $j] = $sum;
    }
}

// $end = microtime(true);
echo "Sample Result [0]: " . $res[0] . "\n";
// echo "Time: " . round($end - $start, 4) . " sec\n";
?>