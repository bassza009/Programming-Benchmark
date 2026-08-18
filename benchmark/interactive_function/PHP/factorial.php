<?php
ini_set('memory_limit', '-1');
function factorial($n){
    if($n <=1){
        return 1;
    }
    return $n * factorial($n-1);
}
printf(factorial(10000000),"\n")
?>
