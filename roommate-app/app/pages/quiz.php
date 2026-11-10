<?php

/** Each option: label, points per type, profile fields it sets. */
const QUIZ = [
    ['q' => "It's Friday night. You're most likely…", 'opts' => [
        ['🍿', 'On the couch with a show and snacks', ['homebody' => 3], ['guests' => 'rarely']],
        ['🎲', 'Hosting friends for games or dinner', ['social' => 3], ['guests' => 'often']],
        ['🎟️', 'Out at a concert, bar or event', ['adventurer' => 2, 'social' => 1], ['guests' => 'sometimes']],
        ['💻', 'Working late or deep in a project', ['owl' => 2, 'pro' => 1], []],
    ]],
    ['q' => 'Your alarm usually goes off…', 'opts' => [
        ['🌅', 'Before 7 — early bird', ['planner' => 2, 'pro' => 1], ['sleep_schedule' => 'early']],
        ['☀️', 'Around 8 or 9', ['homebody' => 1, 'pro' => 1], ['sleep_schedule' => 'normal']],
        ['🌙', 'Late morning or later', ['owl' => 3], ['sleep_schedule' => 'night']],
        ['🔀', 'Depends on the day — I\'m flexible', ['adventurer' => 2], ['sleep_schedule' => 'normal']],
    ]],
    ['q' => 'Dishes in the sink. How long until they bug you?', 'opts' => [
        ['⚡', 'Immediately. Clean as you go', ['planner' => 3], ['cleanliness' => 5]],
        ['🧽', 'By the end of the day', ['planner' => 1, 'pro' => 1], ['cleanliness' => 4]],
        ['🤷', 'A day or two is fine', ['homebody' => 1, 'adventurer' => 1], ['cleanliness' => 3]],
        ['😎', 'Honestly, I barely notice', ['owl' => 1, 'social' => 1], ['cleanliness' => 2]],
    ]],
    ['q' => 'How often would you have people over?', 'opts' => [
        ['🙅', 'Rarely — home is my sanctuary', ['homebody' => 2, 'planner' => 1], ['guests' => 'rarely']],
        ['👋', 'A friend now and then', ['pro' => 1, 'homebody' => 1], ['guests' => 'sometimes']],
        ['🥳', 'Often — the more the merrier', ['social' => 3], ['guests' => 'often']],
        ['✈️', 'I\'m usually the one out', ['adventurer' => 2], ['guests' => 'rarely']],
    ]],
    ['q' => 'A typical weekday for you looks like…', 'opts' => [
        ['🏢', 'Long days at work, home to sleep', ['pro' => 3], ['work_from_home' => 0]],
        ['🏠', 'Working from home', ['homebody' => 2, 'owl' => 1], ['work_from_home' => 1]],
        ['📚', 'Classes and studying', ['owl' => 1, 'planner' => 1], ['work_from_home' => 0]],
        ['🌀', 'Shifts that change week to week', ['owl' => 2, 'adventurer' => 1], ['work_from_home' => 0]],
    ]],
    ['q' => 'Pets in the apartment?', 'opts' => [
        ['🐶', 'I have one (or more)!', ['social' => 1, 'homebody' => 1], ['pets' => 'have']],
        ['😍', 'Love them, but don\'t have one', ['adventurer' => 1, 'homebody' => 1], ['pets' => 'ok']],
        ['🙂', 'Fine either way', ['pro' => 1], ['pets' => 'ok']],
        ['🤧', 'Rather not — allergies or preference', ['planner' => 1], ['pets' => 'no_pets']],
    ]],
    ['q' => 'Splitting groceries and household stuff?', 'opts' => [
        ['📊', 'Shared app, everything tracked', ['planner' => 3], []],
        ['🛒', 'Split the basics, buy our own food', ['pro' => 2], []],
        ['🍝', 'Let\'s cook and share meals!', ['social' => 2, 'homebody' => 1], []],
        ['🤙', 'We\'ll figure it out as we go', ['adventurer' => 2], []],
    ]],
    ['q' => 'Your ideal roommate is…', 'opts' => [
        ['🤝', 'A friend I hang out with', ['social' => 2, 'adventurer' => 1], []],
        ['🔕', 'Friendly, but we mostly do our own thing', ['pro' => 2, 'homebody' => 1], []],
        ['✅', 'Reliable and respectful — that\'s it', ['planner' => 2], []],
        ['🌃', 'Someone who doesn\'t mind my late hours', ['owl' => 3], []],
    ]],
];

function quiz_index(): void
{
    $me = require_login();
    if (is_post()) {
        $answers = (array)($_POST['a'] ?? []);
        $points = array_fill_keys(array_keys(QUIZ_TYPES), 0);
        $fields = [];
        foreach (QUIZ as $i => $item) {
            $choice = $item['opts'][(int)($answers[$i] ?? -1)] ?? null;
            if (!$choice) continue;
            foreach ($choice[2] as $t => $p) $points[$t] += $p;
            foreach ($choice[3] as $f => $v) $fields[$f] = $v;
        }
        if (count($answers) < count(QUIZ)) {
            flash('error', 'Please answer every question.');
            redirect('/quiz');
        }
        arsort($points);
        $type = array_key_first($points);
        $fields['quiz_type'] = $type;
        $sets = implode(', ', array_map(fn($k) => "$k = ?", array_keys($fields)));
        q("UPDATE users SET $sets WHERE id = ?", array_merge(array_values($fields), [$me['id']]));
        redirect('/quiz?result=1');
    }
    if (input('result') && $me['quiz_type']) {
        $t = QUIZ_TYPES[$me['quiz_type']];
        $best = $t['best'];
        $in = implode(',', array_map(fn($x) => db()->quote($x), $best));
        $people = all("SELECT * FROM users WHERE status = 'active' AND profile_visible = 1 AND id <> ? AND quiz_type IN ($in) ORDER BY last_seen DESC LIMIT 6", [$me['id']]);
        render('quiz_result', ['title' => 'Your roommate type', 'type' => $me['quiz_type'], 't' => $t, 'people' => $people]);
        return;
    }
    render('quiz', ['title' => 'Roommate Quiz', 'quiz' => QUIZ]);
}
