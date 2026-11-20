<?php defined('APP') || exit;
cache_private();
session_boot();
unset($_SESSION['admin'], $_SESSION['admin_ua']);
session_regenerate_id(true);
redirect('/admin/login/');
