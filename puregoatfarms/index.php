<?php
// puregoatfarms.com front controller. The host serves real files directly and
// sends every other request here (see README). Routes live in app/routes.php.
define('PGF', true);
define('DOCROOT', __DIR__);
define('APP', __DIR__ . '/app');

require APP . '/config.php';
require APP . '/posts.php';
require APP . '/helpers.php';
require APP . '/layout.php';
require APP . '/forms.php';
require APP . '/routes.php';

dispatch($_SERVER['REQUEST_METHOD'] ?? 'GET', $_SERVER['REQUEST_URI'] ?? '/');
