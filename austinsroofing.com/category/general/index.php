<?php
require dirname(__DIR__, 2) . '/includes/layout.php';
require AR_ROOT . '/includes/blog-list.php';
blog_list('General Roofing Articles', '/category/general/', [['Blog', '/blog/'], ['General', '/category/general/']],
    'General Roofing Articles | Austin Roofing Blog',
    'All general roofing articles from Austin Roofing — shingle costs, underlayment, roof replacement, metal roofing, warranties, permits and storm insurance.',
    'Every roofing guide in our General category, from shingle prices per square to storm insurance coverage.');
