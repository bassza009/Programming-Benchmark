<?php
// บังคับให้ใช้ Memory คงที่และเปิดการรายงาน Error ทั้งหมด
ini_set('memory_limit', '1G');
error_reporting(E_ALL);

function playOptimal($n) {
    $pardoned = 0;
    $inDrawer = range(0, 99);

    for ($r = 0; $r < $n; $r++) {
        // ใช้ shuffle แบบปกติ แต่ตรวจสอบว่า Seed ถูกต้อง
        shuffle($inDrawer);
        
        $allFound = true;
        for ($prisoner = 0; $prisoner < 100; $prisoner++) {
            $found = false;
            $reveal = $prisoner;
            for ($go = 0; $go < 50; $go++) {
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
        if ($allFound) $pardoned++;
    }
    return ($pardoned / $n) * 100;
}

$n = 1000000;
// เริ่มจับเวลาแบบละเอียด
//$start = microtime(true);
$res = playOptimal($n);
//$end = microtime(true);

printf("Result: %.2f%%\n", $res);
//printf("Time: %.4f sec\n", $end - $start);