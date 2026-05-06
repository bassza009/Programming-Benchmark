<?php
function countPrimes($limit) {
    $count = 0;
    for ($i = 2; $i <= $limit; $i++) {
        $isPrime = true;
        for ($j = 2; $j * $j <= $i; $j++) {
            if ($i % $j === 0) {
                $isPrime = false;
                break;
            }
        }
        if ($isPrime) $count++;
    }
    return $count;
}
print(countPrimes(10000000))

?>