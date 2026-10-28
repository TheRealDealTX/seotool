<?php
// Copy to config.php on the server (never commit config.php). .htaccess blocks direct access.
return [
    'to' => 'autida@jmautida.com',
    'smtp' => [
        'host' => 'smtp.hostinger.com',
        'port' => 465,
        'user' => 'autida@jmautida.com',
        'pass' => 'MAILBOX-PASSWORD-HERE',
        'from' => 'autida@jmautida.com',
    ],
];
