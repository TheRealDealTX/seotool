<?php
// Minimal configuration for tools/external-import.php (no database, no secrets).
return [
    'base_url'  => getenv('RODEOTEXAS_SITE') ?: 'https://rodeotexas.org',
    'site_name' => 'Rodeo Texas',
    'db'        => ['host' => '', 'port' => 0, 'name' => '', 'user' => '', 'pass' => ''],
    'app_secret' => 'unused-in-runner',
    'import'    => ['user_agent' => 'RodeoTexasBot/1.0 (+https://rodeotexas.org/about/)'],
    'geocoder'  => ['enabled' => false],
    'debug'     => false,
];
