<?php

function page_landing(): void
{
    if (current_user()) redirect('/home');
    $stats = [
        'members' => (int)val("SELECT COUNT(*) FROM users WHERE status = 'active'"),
        'properties' => (int)val("SELECT COUNT(*) FROM properties WHERE status = 'approved'"),
    ];
    $featured = all("SELECT p.*, (SELECT COUNT(*) FROM user_properties up JOIN users u ON u.id = up.user_id AND u.status = 'active' WHERE up.property_id = p.id) AS interested
        FROM properties p WHERE p.status = 'approved' ORDER BY p.is_featured DESC, interested DESC, p.id DESC LIMIT 6");
    render('landing', ['stats' => $stats, 'featured' => $featured, 'mainClass' => 'main-wide', 'bodyClass' => 'landing']);
}

function page_terms(): void
{
    render('static/terms', ['title' => 'Terms of Use']);
}

function page_privacy(): void
{
    render('static/privacy', ['title' => 'Privacy Policy']);
}

function page_safety(): void
{
    render('static/safety', ['title' => 'Roommate safety tips']);
}
