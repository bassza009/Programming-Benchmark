<?php
// Set memory limit for large matrices
ini_set('memory_limit', '1G');

$n = 1000;

// 1. Prepare Data using simple arrays
// Pre-filling with 0.0 helps PHP allocate the memory block upfront
$matrixA = array_fill(0, $n * $n, 0.0);
$matrixB = array_fill(0, $n * $n, 0.0);
$result  = array_fill(0, $n * $n, 0.0);

for ($i = 0; $i < $n * $n; $i++) {
    $matrixA[$i] = (double)($i % $n);
    $matrixB[$i] = (double)floor($i / $n);
}

echo "Starting Optimized Matrix Multiplication (Simple Array): {$n}x{$n}\n";

// --- OPTIMIZATION START ---

// 1. Transpose Matrix B: Flip rows and columns
// This creates a "Linear" access pattern for the innermost loop
$matrixB_T = array_fill(0, $n * $n, 0.0);
for ($i = 0; $i < $n; $i++) {
    $row_off = $i * $n;
    for ($j = 0; $j < $n; $j++) {
        $matrixB_T[$j * $n + $i] = $matrixB[$row_off + $j];
    }
}

// 2. Main Multiplication Loop
for ($i = 0; $i < $n; $i++) {
    $i_off = $i * $n; // Pre-calculate row offset for Matrix A and Result
    
    for ($j = 0; $j < $n; $j++) {
        $j_off = $j * $n; // Pre-calculate row offset for Transposed Matrix B
        $sum = 0.0;
        
        for ($k = 0; $k < $n; $k++) {
            // Memory access is now linear/consecutive in both arrays
            $sum += $matrixA[$i_off + $k] * $matrixB_T[$j_off + $k];
        }
        $result[$i_off + $j] = $sum;
    }
}

// --- OPTIMIZATION END ---
echo "Done.\n";
