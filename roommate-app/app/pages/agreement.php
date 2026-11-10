<?php

const AGREEMENT_FIELDS = [
    'address' => ['Home address', 'text', ''],
    'lease_start' => ['Lease start', 'date', ''],
    'lease_end' => ['Lease end', 'date', ''],
    'rent_total' => ['Total monthly rent ($)', 'number', ''],
    'rent_a' => ['Rent — {A} ($)', 'number', ''],
    'rent_b' => ['Rent — {B} ($)', 'number', ''],
    'rent_due' => ['Rent is due on', 'text', 'the 1st, paid to the property portal'],
    'deposit' => ['Security deposit split', 'text', '50 / 50'],
    'utilities' => ['Utilities & internet', 'text', 'Split evenly; {A} sets up electric, {B} sets up internet'],
    'quiet_from' => ['Quiet hours from', 'time', '22:00'],
    'quiet_to' => ['Quiet hours until', 'time', '07:00'],
    'guests' => ['Guests', 'textarea', 'Give a heads-up for guests. Overnight guests max 2 nights a week.'],
    'chores' => ['Chores & cleaning', 'textarea', "Kitchen: clean as you go\nTrash & recycling: alternate weeks\nBathroom & common areas: deep clean every other Sunday"],
    'shared' => ['Shared groceries & supplies', 'textarea', 'Split paper towels, soap and cleaning supplies. Food is separate unless agreed.'],
    'pets_smoking' => ['Pets & smoking', 'text', 'No smoking indoors.'],
    'parking' => ['Parking & storage', 'text', ''],
    'moving_out' => ['If someone needs to move out', 'textarea', 'Give 60 days notice and help find a replacement roommate approved by both.'],
    'other' => ['Anything else', 'textarea', ''],
];

function agreement_pair(int $me, int $other): array
{
    return $me < $other ? [$me, $other] : [$other, $me];
}

function agreement_list(): void
{
    $me = require_login();
    $rows = all("SELECT a.*, u.name, u.username, u.avatar FROM agreements a JOIN users u ON u.id = IF(a.user_a = ?, a.user_b, a.user_a)
        WHERE a.user_a = ? OR a.user_b = ? ORDER BY a.updated_at DESC", [$me['id'], $me['id'], $me['id']]);
    $friends = all("SELECT u.name, u.username, u.avatar FROM friendships f JOIN users u ON u.id = IF(f.requester_id = ?, f.addressee_id, f.requester_id)
        WHERE f.status = 'accepted' AND (f.requester_id = ? OR f.addressee_id = ?) AND u.status = 'active' ORDER BY u.name", [$me['id'], $me['id'], $me['id']]);
    render('agreements', ['title' => 'Roommate agreements', 'rows' => $rows, 'friends' => $friends]);
}

function agreement_show(string $username): void
{
    $me = require_login();
    $myId = (int)$me['id'];
    $other = one("SELECT * FROM users WHERE username = ? AND status = 'active'", [strtolower($username)]);
    if (!$other || (int)$other['id'] === $myId) not_found();
    if (friend_status($myId, (int)$other['id']) !== 'friends') {
        flash('error', 'You need to be friends with ' . $other['name'] . ' to create a roommate agreement.');
        redirect('/u/' . $other['username']);
    }
    [$a, $b] = agreement_pair($myId, (int)$other['id']);
    $row = one('SELECT * FROM agreements WHERE user_a = ? AND user_b = ?', [$a, $b]);
    $names = [$a => $a === $myId ? $me['name'] : $other['name'], $b => $b === $myId ? $me['name'] : $other['name']];
    $fill = fn($s) => strtr($s, ['{A}' => explode(' ', $names[$a])[0], '{B}' => explode(' ', $names[$b])[0]]);

    if (is_post()) {
        $act = input('action');
        if ($act === 'sign' && $row) {
            $col = $myId === $a ? 'signed_a' : 'signed_b';
            q("UPDATE agreements SET $col = NOW() WHERE id = ?", [$row['id']]);
            notify((int)$other['id'], 'agreement_signed', $myId);
            flash('success', 'You signed the agreement.');
        } elseif ($act === 'save') {
            $data = [];
            foreach (AGREEMENT_FIELDS as $k => [, $type]) {
                $data[$k] = mb_substr(trim((string)($_POST['f'][$k] ?? '')), 0, $type === 'textarea' ? 2000 : 200);
            }
            $json = json_encode($data, JSON_UNESCAPED_UNICODE);
            if ($row) {
                if ($row['data'] !== $json) {
                    q('UPDATE agreements SET data = ?, signed_a = NULL, signed_b = NULL, updated_by = ?, updated_at = NOW() WHERE id = ?', [$json, $myId, $row['id']]);
                    notify((int)$other['id'], 'agreement', $myId);
                    flash('success', 'Saved. Any previous signatures were cleared so you can both review the changes.');
                }
            } else {
                q('INSERT INTO agreements (user_a, user_b, data, updated_by) VALUES (?, ?, ?, ?)', [$a, $b, $json, $myId]);
                notify((int)$other['id'], 'agreement', $myId);
                flash('success', 'Agreement created. ' . $other['name'] . ' can now review and sign it.');
            }
        }
        redirect('/agreement/' . $other['username']);
    }

    $data = $row ? (json_decode($row['data'], true) ?: []) : [];
    if (!$row) {
        foreach (AGREEMENT_FIELDS as $k => [, , $default]) $data[$k] = $fill($default);
    }
    $signedMe = $row ? ($myId === $a ? $row['signed_a'] : $row['signed_b']) : null;
    $signedThem = $row ? ($myId === $a ? $row['signed_b'] : $row['signed_a']) : null;
    $labels = [];
    foreach (AGREEMENT_FIELDS as $k => [$label, $type]) $labels[$k] = [$fill($label), $type];
    render('agreement', [
        'title' => 'Roommate agreement with ' . $other['name'], 'other' => $other, 'row' => $row, 'data' => $data, 'labels' => $labels,
        'signedMe' => $signedMe, 'signedThem' => $signedThem, 'editing' => !$row || input('edit') === '1',
        'updatedBy' => $row && $row['updated_by'] ? ((int)$row['updated_by'] === $myId ? 'you' : $other['name']) : null,
    ]);
}
