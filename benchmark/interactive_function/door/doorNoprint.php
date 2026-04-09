<?php

for ($i = 1; $i <= 1000000;$i++) {
	$root = sqrt($i);
	$state = ($root == ceil($root)) ? 'open' : 'closed';
	if ($state === "open"){
	// 	echo "Door {$i}: {$state}\n";
	}
}

?>