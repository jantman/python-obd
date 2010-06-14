<?php

$str = file_get_contents("scantool.dat");
$foo = str_replace("\n", "\r\n", $str);
$fh = fopen("new.dat", "w");
fwrite($fh, $str);
fclose($fh);


?>