<?php
// The old store's search URL (/search.php?search_query=rake) still has links
// pointing at it from other sites. Send those visitors to the new search page.
$q = $_GET['search_query'] ?? $_GET['q'] ?? '';
header('Location: /search/' . ($q !== '' ? '?q=' . rawurlencode((string)$q) : ''), true, 301);
