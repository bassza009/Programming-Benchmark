<?php
// ตั้งค่าให้ใช้ Memory ได้เต็มที่สำหรับ Matrix ขนาดใหญ่
//ini_set('memory_limit', '512M');

$n = 100000;

//$result = new SplFixedArray($n * $n);

// Only i and j loops
for ($i = 0; $i < $n; $i++) {
    for ($j = 0; $j < $n; $j++) {
        $value = $i * $n + $j + 1;
    }
}

echo "latest value : " . $value. "\n";
