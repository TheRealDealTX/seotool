<?php
// One-time: create demo members so the community isn't empty. POST token=<setup_token>&count=36
// Demo accounts are flagged is_demo=1, can't log in, and can all be removed from Admin → Members.
declare(strict_types=1);
header('Content-Type: application/json');
$config = @include __DIR__ . '/app/config.php';
$token = $_POST['token'] ?? '';
if (!is_array($config) || empty($config['setup_token']) || !is_string($token) || !hash_equals($config['setup_token'], $token)) {
    http_response_code(403);
    exit(json_encode(['error' => 'forbidden']));
}
$_SERVER['REQUEST_METHOD'] = 'GET';
require __DIR__ . '/app/bootstrap.php';
migrate();
if (($_POST['action'] ?? '') === 'selfdestruct') exit(json_encode(['ok' => @unlink(__FILE__)]));

mt_srand(20261110);
$pick = fn(array $a) => $a[mt_rand(0, count($a) - 1)];
$people = [
    ['Maya Thompson', 'female'], ['Daniel Ortiz', 'male'], ['Priya Patel', 'female'], ['Marcus Johnson', 'male'],
    ['Sofia Ramirez', 'female'], ['Ethan Nguyen', 'male'], ['Aaliyah Brooks', 'female'], ['Jacob Miller', 'male'],
    ['Isabella Garcia', 'female'], ['Noah Kim', 'male'], ['Chloe Williams', 'female'], ['Andre Davis', 'male'],
    ['Emily Chen', 'female'], ['Luis Hernandez', 'male'], ['Hannah Wilson', 'female'], ['Tyler Anderson', 'male'],
    ['Jasmine Moore', 'female'], ['Kevin Tran', 'male'], ['Olivia Martinez', 'female'], ['Brandon Lee', 'male'],
    ['Riley Parker', 'nonbinary'], ['Gabriela Lopez', 'female'], ['Jordan Taylor', 'male'], ['Ava Robinson', 'female'],
    ['Samuel Okafor', 'male'], ['Natalie Scott', 'female'], ['Diego Flores', 'male'], ['Madison Clark', 'female'],
    ['Ryan Mitchell', 'male'], ['Leah Adams', 'female'], ['Christian Reyes', 'male'], ['Zoe Bennett', 'female'],
    ['Avery Collins', 'nonbinary'], ['Mia Sanchez', 'female'], ['Caleb Turner', 'male'], ['Grace Rivera', 'female'],
];
$count = max(1, min(count($people), (int)($_POST['count'] ?? 36)));
$cities = ['Houston', 'Houston', 'Houston', 'Dallas', 'Dallas', 'Austin', 'Austin', 'San Antonio'];
$jobs = ['Registered nurse', 'Software engineer', 'Grad student at UH', 'Marketing coordinator', 'Teacher', 'Accountant', 'Barista & artist',
    'Medical resident', 'Sales associate', 'UX designer', 'Paralegal', 'Physical therapist', 'Data analyst', 'Chef', 'Real estate agent',
    'Mechanical engineer', 'Student at UT Austin', 'Flight attendant', 'Personal trainer', 'Social worker', 'Pharmacy tech', 'Project manager'];
$interestPool = ['hiking', 'cooking', 'gaming', 'live music', 'yoga', 'running', 'reading', 'coffee', 'movies', 'photography', 'basketball',
    'brunch', 'thrifting', 'travel', 'dogs', 'cats', 'art', 'gym', 'soccer', 'board games', 'podcasts', 'baking', 'concerts', 'church'];
$bios = [
    "Moving for a new job and looking for a clean, chill roommate. I work days, cook a lot, and I'm happy to share groceries.",
    "Easygoing and respectful. I like a tidy common area, quiet weeknights, and the occasional movie night. Looking to split a 2BR.",
    "I'm relocating and would love a roommate who's friendly but also values their own space. Non-smoker, no drama.",
    "Night owl, but quiet about it. Usually at the gym after work. Looking for someone reliable with rent and bills.",
    "Grad student, mostly studying or at the library. Looking for a roommate near campus or the medical center.",
    "Love having people over for game nights now and then, but I'm also fine keeping it low-key. Pet friendly!",
    "Early riser, pretty organized, love to cook. Ideally looking for someone who wants a long-term roommate situation.",
    "New to the city and hoping to find a roommate who can show me around. I'm clean, respectful and easy to talk to.",
    "Work hybrid, so I'm home a couple days a week. Keep things quiet during the day. Weekends I'm usually out exploring.",
    "My lease is up soon and I'd love to find someone to go in on a nicer place with. Open to either finding one together or joining your place.",
];
$postTexts = [
    "Anyone else looking at {p}? Hoping to find someone to split a 2BR with — move-in around {m}.",
    "Just toured {p} and loved it. Looking for a roommate! Budget around {b}.",
    "Has anyone lived at {p}? How's management and parking?",
    "Looking for a roommate in {c}! I'm clean, quiet on weeknights, and pay on time. Message me 🙂",
    "I have a room opening up {m}. Prefer someone who's tidy and non-smoking. DM me!",
    "Splitting rent at {p} would make it so doable. Anyone interested in teaming up?",
    "First time using this — hi everyone! Looking for something in {c} around {b}.",
    "Pro tip: ask the leasing office about look-and-lease specials. Saved me a lot last time.",
];
$comments = ["I'm interested! Sent you a friend request.", "Same here, looking around the same dates.", "That place is great, the gym is really nice.",
    "Following!", "What's your move-in timeline?", "Messaged you 👋", "Good luck! Lots of people looking in that area.", "Love that area."];

// A few popular properties per city so demo members overlap (like real renters do).
$pool = [];
foreach (array_unique($cities) as $c) {
    $pool[$c] = array_map('intval', array_column(all("SELECT id FROM properties WHERE status = 'approved' AND city = ? AND (image IS NOT NULL OR image_url IS NOT NULL) ORDER BY id DESC LIMIT 8", [$c]), 'id'));
}

$created = [];
foreach (array_slice($people, 0, $count) as $i => [$name, $gender]) {
    $first = strtolower(explode(' ', $name)[0]);
    $last = strtolower(explode(' ', $name)[1]);
    $username = substr($first . '_' . substr($last, 0, 1) . mt_rand(10, 99), 0, 30);
    if (val('SELECT 1 FROM users WHERE username = ?', [$username])) continue;
    $city = $pick($cities);
    $min = 100 * mt_rand(6, 12);
    $max = $min + 100 * mt_rand(3, 8);
    $ints = $interestPool; shuffle($ints);
    $daysAgo = mt_rand(1, 60);
    q("INSERT INTO users (email, username, password_hash, name, is_demo, gender, birth_year, occupation, city, budget_min, budget_max, move_in_date, lease_months,
        looking_for, cleanliness, sleep_schedule, smoking, pets, guests, work_from_home, gender_pref, interests, bio, last_seen, created_at)
        VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        $username . '@demo.invalid', $username, password_hash(bin2hex(random_bytes(16)), PASSWORD_DEFAULT), $name, $gender,
        (int)date('Y') - mt_rand(21, 36), $pick($jobs), $city, $min, $max,
        date('Y-m-d', strtotime('+' . mt_rand(10, 120) . ' days')), $pick([6, 12, 12, 12, 15]),
        $pick(['need_place', 'need_place', 'have_place', 'either', 'either']), mt_rand(2, 5), $pick(['early', 'normal', 'normal', 'night']),
        $pick(['no', 'no', 'no', 'no', 'outside']), $pick(['none', 'have', 'ok', 'ok', 'no_pets']), $pick(['rarely', 'sometimes', 'sometimes', 'often']),
        mt_rand(0, 2) === 0 ? 1 : 0, mt_rand(0, 3) === 0 ? ($gender === 'nonbinary' ? 'any' : $gender) : 'any',
        implode(', ', array_slice($ints, 0, mt_rand(3, 5))), $pick($bios),
        date('Y-m-d H:i:s', time() - mt_rand(60, 86400 * 5)), date('Y-m-d H:i:s', time() - 86400 * $daysAgo),
    ]);
    $id = (int)db()->lastInsertId();
    $props = $pool[$city] ?? [];
    shuffle($props);
    foreach (array_slice($props, 0, mt_rand(1, 3)) as $pid) {
        q('INSERT IGNORE INTO user_properties (user_id, property_id) VALUES (?, ?)', [$id, $pid]);
    }
    $created[] = ['id' => $id, 'city' => $city, 'min' => $min, 'max' => $max, 'props' => array_slice($props, 0, 1), 'days' => $daysAgo];
}

// Posts, comments, likes, friendships.
$posts = 0;
foreach ($created as $c) {
    if (mt_rand(0, 100) > 65) continue;
    $pid = $c['props'][0] ?? null;
    $pname = $pid ? val('SELECT name FROM properties WHERE id = ?', [$pid]) : $c['city'];
    $text = strtr($pick($postTexts), ['{p}' => $pname, '{c}' => $c['city'], '{b}' => '$' . number_format($c['max']), '{m}' => date('F', strtotime('+' . mt_rand(1, 3) . ' month'))]);
    $at = date('Y-m-d H:i:s', time() - mt_rand(3600, 86400 * min(30, $c['days'])));
    q('INSERT INTO posts (user_id, property_id, body, created_at) VALUES (?, ?, ?, ?)', [$c['id'], $pid, $text, $at]);
    $postId = (int)db()->lastInsertId();
    $posts++;
    foreach (array_rand($created, 4) as $k) {
        $o = $created[$k]['id'];
        if ($o === $c['id']) continue;
        if (mt_rand(0, 1)) q('INSERT IGNORE INTO post_likes (post_id, user_id, created_at) VALUES (?, ?, ?)', [$postId, $o, $at]);
        if (mt_rand(0, 3) === 0) q('INSERT INTO comments (post_id, user_id, body, created_at) VALUES (?, ?, ?, DATE_ADD(?, INTERVAL ? MINUTE))', [$postId, $o, $pick($comments), $at, mt_rand(5, 600)]);
    }
}
$friends = 0;
foreach ($created as $a) {
    foreach (array_rand($created, 3) as $k) {
        $b = $created[$k];
        if ($b['id'] === $a['id'] || $b['city'] !== $a['city']) continue;
        if (val('SELECT 1 FROM friendships WHERE (requester_id = ? AND addressee_id = ?) OR (requester_id = ? AND addressee_id = ?)', [$a['id'], $b['id'], $b['id'], $a['id']])) continue;
        q("INSERT INTO friendships (requester_id, addressee_id, status) VALUES (?, ?, 'accepted')", [$a['id'], $b['id']]);
        $friends++;
    }
}
echo json_encode(['ok' => true, 'users' => count($created), 'posts' => $posts, 'friendships' => $friends, 'pools' => array_map('count', $pool)], JSON_PRETTY_PRINT);
