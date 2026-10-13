<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/blog-list.php';
render_post_list('/category/general/', 'General', 'General Archives | Sugar Land Public Adjuster',
    'General insurance claim articles from Sugar Land Public Adjuster—claim strategy, fees, storm claims and choosing a public adjuster in Sugar Land, TX.',
    [['Home', '/'], ['Blog', '/blog/'], ['General', '/category/general/']]);
