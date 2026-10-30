<?php
// Dumps $PLANS (inc/plans.php, with derived fields) as JSON for the Python plan-set generator.
// Usage: php generator/export-plans.php > build/plans.json
declare(strict_types=1);
require __DIR__ . '/../site/inc/plans.php';
echo json_encode($PLANS, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES), "\n";
