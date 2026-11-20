<?php defined('APP') || exit;
cache_private();
json_out(['token' => csrf_token()]);
