<?php
/**
 * Created by PhpStorm.
 * User: sonic
 * Date: 9. 10. 2016
 * Time: 10:51
 */


function getDirContents($dir, &$results = array()){
    $files = scandir($dir);

    foreach($files as $key => $value){
        $path = realpath($dir.DIRECTORY_SEPARATOR.$value);
        if(!is_dir($path)) {
            $results[] = $path;
        } else if($value != "." && $value != "..") {
            getDirContents($path, $results);
            $results[] = $path;
        }
    }

    return $results;
}

file_put_contents("array.json",json_encode(getDirContents('D:\Git\hackaton\budapest-2016\www-data\images')));
