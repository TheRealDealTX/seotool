<?php
// Dumps $PLANS (inc/plans.php, with derived fields) as JSON for the Python plan-set generator.
// Usage: php generator/export-plans.php > build/plans.json
// The site's config.php defines the constants and helpers plans.php uses and loads it.
declare(strict_types=1);
require __DIR__ . '/../site/inc/config.php';
echo json_encode($PLANS, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), "\n";
