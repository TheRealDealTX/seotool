<?php

function tools_index(): void
{
    $me = require_login();
    $agreements = (int)val('SELECT COUNT(*) FROM agreements WHERE user_a = ? OR user_b = ?', [$me['id'], $me['id']]);
    render('tools', ['title' => 'Roommate tools', 'agreements' => $agreements]);
}

function tools_rent(): void
{
    $me = require_login();
    $friends = all("SELECT u.name, u.username FROM friendships f JOIN users u ON u.id = IF(f.requester_id = ?, f.addressee_id, f.requester_id)
        WHERE f.status = 'accepted' AND (f.requester_id = ? OR f.addressee_id = ?) AND u.status = 'active' ORDER BY u.name", [$me['id'], $me['id'], $me['id']]);
    render('rent_split', ['title' => 'Rent split calculator', 'friends' => $friends]);
}
