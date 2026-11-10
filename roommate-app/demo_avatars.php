<?php
// One-time: give demo members illustrated profile pictures. POST token=<setup_token>  (action=selfdestruct to remove)
declare(strict_types=1);
header('Content-Type: application/json');
$config = @include __DIR__ . '/app/config.php';
$token = $_POST['token'] ?? '';
if (!is_array($config) || empty($config['setup_token']) || !is_string($token) || !hash_equals($config['setup_token'], $token)) {
    http_response_code(403); exit(json_encode(['error' => 'forbidden']));
}
$_SERVER['REQUEST_METHOD'] = 'GET';
require __DIR__ . '/app/bootstrap.php';
if (($_POST['action'] ?? '') === 'selfdestruct') exit(json_encode(['ok' => @unlink(__FILE__)]));
set_time_limit(300);

$base = 'https://api.dicebear.com/9.x/avataaars/png?size=256&backgroundType=solid&backgroundColor=e7eef4,f6f1d9,dde5ea,e6f4e8'
    . '&mouth=smile,default,twinkle&eyes=default,happy,wink&eyebrows=default,defaultNatural,raisedExcited'
    . '&hairColor=a55728,2c1b18,b58143,d6b370,724133,4a312c,c93305&accessoriesProbability=15';
$styles = [
    'female' => '&top=bigHair,bob,curly,curvy,longButNotTooLong,miaWallace,straight01,straight02,straightAndStrand,hijab,fro&facialHairProbability=0',
    'male' => '&top=shortFlat,shortCurly,shortWaved,shortRound,theCaesar,theCaesarAndSidePart,dreads01,frizzle,shaggy,fro&facialHairProbability=35',
    'other' => '&top=bob,shaggy,shortCurly,curly,frizzle,shaggyMullet,fro&facialHairProbability=0',
];
$done = []; $failed = [];
foreach (all("SELECT id, username, gender, avatar FROM users WHERE is_demo = 1") as $u) {
    $style = $styles[$u['gender']] ?? $styles['other'];
    $png = @file_get_contents($base . $style . '&seed=' . rawurlencode($u['username']), false, stream_context_create(['http' => ['timeout' => 20]]));
    $img = $png ? @imagecreatefromstring($png) : false;
    if (!$img) { $failed[] = $u['username']; continue; }
    $out = imagecreatetruecolor(256, 256);
    imagefill($out, 0, 0, imagecolorallocate($out, 255, 255, 255));
    imagecopy($out, $img, 0, 0, 0, 0, 256, 256);
    $name = bin2hex(random_bytes(12)) . '.jpg';
    @mkdir(APP_ROOT . '/uploads/avatars', 0755, true);
    imagejpeg($out, APP_ROOT . '/uploads/avatars/' . $name, 88);
    delete_upload('avatars', $u['avatar']);
    q('UPDATE users SET avatar = ? WHERE id = ?', [$name, $u['id']]);
    $done[] = $u['username'];
}
echo json_encode(['ok' => !$failed, 'updated' => count($done), 'failed' => $failed], JSON_PRETTY_PRINT);
