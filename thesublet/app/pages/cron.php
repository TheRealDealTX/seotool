<?php defined('APP') || exit;
cache_private();
$key = (string)cfg('cron_key', '');
if ($key === '' || !hash_equals($key, get('key'))) { http_response_code(403); exit('forbidden'); }
json_out(['ok' => true] + run_expiry_jobs());
