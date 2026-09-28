<?php
// Public runtime settings read by site.js (popup on/off, delay). Nothing private.
require __DIR__ . '/lib.php';
$s = sd_settings();
header('Cache-Control: public, max-age=300');
sd_json(['popup_enabled' => (bool)($s['popup_enabled'] ?? true), 'popup_delay' => (int)($s['popup_delay_seconds'] ?? 5)]);
