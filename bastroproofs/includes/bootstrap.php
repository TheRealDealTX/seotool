<?php
/**
 * Loaded first by every page: config, helpers and content data.
 * Pages then set $page and call page_start() / page_end().
 */
declare(strict_types=1);

define('ROOT', dirname(__DIR__));

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/components.php';

$SERVICES = require __DIR__ . '/data/services.php';
$AREAS    = require __DIR__ . '/data/areas.php';
$POSTS    = require __DIR__ . '/data/blog.php';
$TOOLS    = require __DIR__ . '/data/tools.php';
