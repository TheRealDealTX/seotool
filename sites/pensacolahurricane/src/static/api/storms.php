<?php
// Active tropical cyclones from the National Hurricane Center, cached 5 minutes.
require __DIR__ . '/_lib.php';
$body = ph_cached_fetch('https://www.nhc.noaa.gov/CurrentStorms.json', 300);
if ($body === null) {
    ph_json(['error' => 'NHC unavailable', 'activeStorms' => []], 502);
}
$data = json_decode($body, true);
ph_json(['activeStorms' => $data['activeStorms'] ?? [], 'source' => 'https://www.nhc.noaa.gov/CurrentStorms.json'], 200, 120);
