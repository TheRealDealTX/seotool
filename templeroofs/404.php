<?php
/** Apache ErrorDocument fallback — renders the site's 404 page. */
require __DIR__ . '/includes/bootstrap.php';
require TR_INC . '/router.php';

render_page('404', []);
