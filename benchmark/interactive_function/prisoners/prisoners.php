<?php
// การตั้งค่าเพื่อรองรับการประมวลผลจำนวนมาก
ini_set('memory_limit', '512M');

function playOptimal($n) {
    $pardoned = 0;
    // สร้างลิ้นชัก 0-99
    $inDrawer = range(0, 99); 

    for ($r = 0; $r < $n; $r++) {
        // สลับตำแหน่งการ์ดในลิ้นชัก
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
                // กลยุทธ์ Cycle-following: เปิดลิ้นชักตามหมายเลขที่พบ
                $reveal = $card;
            }
            
            if (!$found) {
                $allFound = false;
                break;
            }
        }
        
        if ($allFound) {
            $pardoned++;
        }
    }
    return ($pardoned / $n) * 100;
}

// กำหนดจำนวนรอบการทดลอง
$n = 100000; 
echo "Simulation count: $n\n";
printf("Optimal play wins (PHP): %.1f%%\n", playOptimal($n));