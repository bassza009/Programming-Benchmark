<?php
// ตั้งค่า Memory ให้เพียงพอสำหรับการรัน Simulation จำนวนมาก
ini_set('memory_limit', '256M');

/**
 * กลยุทธ์แบบสุ่ม (Random Play)
 */
function play_random($n) {
    $pardoned_count = 0;
    $sampler = range(0, 99);
    
    for ($round = 0; $round < $n; $round++) {
        $in_drawer = range(0, 99);
        shuffle($in_drawer);
        
        $all_found = true;
        for ($prisoner = 0; $prisoner < 100; $prisoner++) {
            $found = false;
            
            // สุ่มเลือก 50 ลิ้นชัก
            $reveal_indices = (array)array_rand($sampler, 50);
            
            foreach ($reveal_indices as $idx) {
                if ($in_drawer[$idx] == $prisoner) {
                    $found = true;
                    break;
                }
            }
            
            if (!$found) {
                $all_found = false;
                break;
            }
        }
        
        if ($all_found) {
            $pardoned_count++;
        }
    }
    return ($pardoned_count / $n) * 100;
}

/**
 * กลยุทธ์แบบหาวัฏจักร (Optimal/Cycle-following Play)
 */
function play_optimal($n) {
    $pardoned_count = 0;
    
    for ($round = 0; $round < $n; $round++) {
        $in_drawer = range(0, 99);
        shuffle($in_drawer);
        
        $all_found = true;
        for ($prisoner = 0; $prisoner < 100; $prisoner++) {
            $reveal = $prisoner;
            $found = false;
            
            for ($go = 0; $go < 50; $go++) {
                $card = $in_drawer[$reveal];
                if ($card == $prisoner) {
                    $found = true;
                    break;
                }
                $reveal = $card; // ไปเปิดลิ้นชักตามหมายเลขที่เจอ (Cycle)
            }
            
            if (!$found) {
                $all_found = false;
                break;
            }
        }
        
        if ($all_found) {
            $pardoned_count++;
        }
    }
    return ($pardoned_count / $n) * 100;
}

// ส่วนการแสดงผล (Main)
$n = 1000000;
echo "Simulation count: " . number_format($n) . "\n";

$start_random = microtime(true);
$random_res = play_random($n);
$end_random = microtime(true);
printf(" Random play wins: %4.1f%% (Time: %.2fs)\n", $random_res, $end_random - $start_random);

$start_optimal = microtime(true);
$optimal_res = play_optimal($n);
$end_optimal = microtime(true);
printf("Optimal play wins: %4.1f%% (Time: %.2fs)\n", $optimal_res, $end_optimal - $start_optimal);