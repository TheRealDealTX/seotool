<?php
// Scheduled publishing for the static site. Run daily by a Hostinger cron job:
//   php /home/u401386392/domains/arriveoutdoors.com/public_html/_releases/publish.php
// Each _releases/YYYY-MM-DD/ folder holds only the files that change on that date
// (the new article page plus the hub pages, sitemap and related links that list it).
// Folders whose date has arrived are copied into the site root once, in date order.
$rel = __DIR__; $root = dirname($rel); $log = $rel . '/applied.txt';
$applied = file_exists($log) ? file($log, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) : [];
$today = (new DateTime('now', new DateTimeZone('America/Los_Angeles')))->format('Y-m-d');
foreach (glob($rel . '/20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]', GLOB_ONLYDIR) as $dir) {
    $d = basename($dir);
    if ($d > $today || in_array($d, $applied, true)) continue;
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS));
    $n = 0;
    foreach ($it as $f) {
        $target = $root . substr($f->getPathname(), strlen($dir));
        if (!is_dir(dirname($target))) mkdir(dirname($target), 0755, true);
        if (copy($f->getPathname(), $target)) $n++;
    }
    file_put_contents($log, $d . PHP_EOL, FILE_APPEND);
    echo "applied $d ($n files)
";
}
