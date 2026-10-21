<?php
ini_set('memory_limit', '512M');

$n = 10000;
$arr = [];
for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $n - $i;
}

for ($i = 0; $i < $n; $i++) {
    $limit = $n - $i - 1;
    for ($j = 0; $j < $limit; $j++) {
        if ($arr[$j] > $arr[$j + 1]) {
            $temp = $arr[$j];
            $arr[$j] = $arr[$j + 1];
            $arr[$j + 1] = $temp;
        }
    }
}

$lastIdx = $n - 1;
echo "Sample Result [0]: {$arr[0]}, [{$lastIdx}]: {$arr[$lastIdx]}\n";
