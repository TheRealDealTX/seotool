<?php
/**
 * SHARED SCRIPTS loaded just before </body> on every public page.
 * Add site-wide JavaScript (chat widgets, deferred pixels, etc.) here.
 * Page-specific scripts can be passed through $page['scripts'] (array of URLs).
 */
defined('RT_APP') || exit;
?>
<script src="<?= e(asset('assets/js/app.js')) ?>" defer></script>
<?php foreach ((array) ($page['scripts'] ?? []) as $__src): ?>
<script src="<?= e($__src) ?>" defer></script>
<?php endforeach; ?>
<!-- Site-wide end-of-body scripts go here. -->
</body>
</html>
