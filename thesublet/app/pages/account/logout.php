<?php defined('APP') || exit;
cache_private();
session_boot();
unset($_SESSION['owner_id']);
session_regenerate_id(true);
redirect('/');
