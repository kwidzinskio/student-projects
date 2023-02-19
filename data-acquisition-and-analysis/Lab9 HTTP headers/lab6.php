<?php
	$file = uniqid('6lab_');
	file_put_contents($file . '.json', json_encode($_POST));
?>
