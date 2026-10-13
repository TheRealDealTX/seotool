<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/blog-list.php';
render_post_list('/blog/', 'All Articles', 'Blog | Sugar Land Public Adjuster | +1 (832) 503-5866',
    'Insurance claim guides from a Sugar Land public adjuster: hurricane, hail, fire and water claims, public adjuster fees, and how to choose the right adjuster.',
    [['Home', '/'], ['Blog', '/blog/']]);
