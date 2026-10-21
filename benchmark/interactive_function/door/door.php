<?php
ini_set('memory_limit', '512M');

$n = 1000000;
$doors = array_fill(0, $n + 1, false);

for ($pass = 1; $pass <= $n; $pass++) {
    for ($d = $pass; $d <= $n; $d += $pass) {
        $doors[$d] = !$doors[$d];
    }
}

$openCount = 0;
for ($i = 1; $i <= $n; $i++) {
    if ($doors[$i]) {
        $openCount++;
    }
}
echo "Open doors: {$openCount}\n";
