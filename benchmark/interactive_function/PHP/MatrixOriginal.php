<?php
// ตั้งค่าให้ใช้ Memory ได้เต็มที่สำหรับ Matrix ขนาดใหญ่
ini_set('memory_limit', '512M');

$n = 1000;

// 1. เตรียมข้อมูล (ไม่นับรวมในเวลาประมวลผลหลัก)
// ใน PHP 7.4+ การใช้ SplFixedArray จะประหยัด Memory และเร็วกว่า Array ปกติ
$matrixA = new SplFixedArray($n * $n);
$matrixB = new SplFixedArray($n * $n);
$result  = new SplFixedArray($n * $n);

for ($i = 0; $i < $n * $n; $i++) {
    $matrixA[$i] = (double)($i % $n);
    $matrixB[$i] = (double)floor($i / $n);
    $result[$i]  = 0.0;
}

echo "Starting Matrix Multiplication (PHP): {$n}x{$n}\n";

// 2. เริ่มจับเวลา (ตรงตามข้อ 3.5 ในไฟล์วิจัย)


for ($i = 0; $i < $n; $i++) {
    for ($j = 0; $j < $n; $j++) {
        $sum = 0.0;
        for ($k = 0; $k < $n; $k++) {
            // สูตรคำนวณ Index: (row * total_cols) + col
            $sum += $matrixA[$i * $n + $k] * $matrixB[$k * $n + $j];
        }
        $result[$i * $n + $j] = $sum;
    }
}


// 3. แสดงผลลัพธ์


echo "Sample Result [0]: " . $result[0] . "\n";