<?php
// Search/filter/paginated views are not separate indexable pages.
if (!empty($_GET['q']) || !empty($_GET['cat']) || (int) ($_GET['pg'] ?? 1) > 1) {
    $page['noindex'] = true;
}
