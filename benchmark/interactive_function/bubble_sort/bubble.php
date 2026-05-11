<?php
$n = 1000000;
$arr = new SplFixedArray($n);

for ($i = 0; $i < $n; $i++) {
    $arr[$i] = $n - $i;
}

echo "Starting Bubble Sort (PHP): {$n} items\n";


for ($i = 0; $i < $n; $i++) {
    for ($j = 0; $j < $n - $i - 1; $j++) {
        if ($arr[$j] > $arr[$j + 1]) {
            $temp = $arr[$j];
            $arr[$j] = $arr[$j + 1];
            $arr[$j + 1] = $temp;
        }
    }
}


echo "Sample Result [0]: " . $arr[0] . "\n";
