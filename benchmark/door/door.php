<?php
$start_time = microtime(true);
for ($i = 1; $i <= 100; $i++) {
	$root = sqrt($i);
	$state = ($root == ceil($root)) ? 'open' : 'closed';
	echo "Door {$i}: {$state}\n";
}
$end_time = microtime(true);
$duration = $end_time - $start_time;

echo "Process duration : " .  round($duration,4) . "sec.\n";
?>