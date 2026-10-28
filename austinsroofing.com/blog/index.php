<?php
require dirname(__DIR__) . '/includes/layout.php';
require AR_ROOT . '/includes/blog-list.php';
blog_list('Austin Roofing Blog', '/blog/', [['Blog', '/blog/']],
    'Roofing Blog | Costs, Materials & Storm Tips | Austin Roofing',
    'Roofing guides from Austin Roofing: shingle prices per square, underlayment types, roof replacement costs, insurance claims, permits, warranties and more.',
    'Practical roofing guides from Austin roofers — costs, materials, insurance and maintenance, written for Central Texas homeowners and property managers.');
