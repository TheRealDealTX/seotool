<?php
/**
 * Generates the site's raster images with PHP GD (run once; outputs are committed):
 *   public_html/assets/img/og-default.png   1200×630 social sharing image
 *   public_html/assets/img/logo-512.png     square logo (schema.org publisher logo)
 *   public_html/assets/img/apple-touch-icon.png 180×180
 *   public_html/favicon.ico                 32×32 PNG-in-ICO
 *
 *   php tools/make-images.php /path/to/ZillaSlab-Bold.ttf
 */
declare(strict_types=1);

$font = $argv[1] ?? '';
if (!is_file($font)) {
    fwrite(STDERR, "Usage: php tools/make-images.php ZillaSlab-Bold.ttf\n");
    exit(1);
}
$out = dirname(__DIR__) . '/public_html';

function rgb($im, string $hex): int
{
    return imagecolorallocate($im, hexdec(substr($hex, 1, 2)), hexdec(substr($hex, 3, 2)), hexdec(substr($hex, 5, 2)));
}

function badge(int $size): GdImage
{
    $s = $size * 4; // supersample
    $im = imagecreatetruecolor($s, $s);
    imagesavealpha($im, true);
    imagefill($im, 0, 0, imagecolorallocatealpha($im, 0, 0, 0, 127));
    imagefilledellipse($im, $s / 2, $s / 2, $s - 2, $s - 2, rgb($im, '#7a3b1b'));
    $gold = rgb($im, '#e9c77b');
    imagesetthickness($im, max(2, (int) ($s * 0.03)));
    for ($a = 0; $a < 360; $a += 12) {
        imagearc($im, (int) ($s / 2), (int) ($s / 2), (int) ($s * 0.78), (int) ($s * 0.78), $a, $a + 7, $gold);
    }
    $pts = [];
    for ($i = 0; $i < 10; $i++) {
        $rad = $i % 2 === 0 ? $s * 0.3 : $s * 0.3 * 0.42;
        $ang = -M_PI / 2 + $i * M_PI / 5;
        $pts[] = (int) round($s / 2 + $rad * cos($ang));
        $pts[] = (int) round($s / 2 + 4 + $rad * sin($ang));
    }
    imagefilledpolygon($im, $pts, rgb($im, '#f4e6c8'));
    $dst = imagecreatetruecolor($size, $size);
    imagesavealpha($dst, true);
    imagefill($dst, 0, 0, imagecolorallocatealpha($dst, 0, 0, 0, 127));
    imagecopyresampled($dst, $im, 0, 0, 0, 0, $size, $size, $s, $s);
    return $dst;
}

@mkdir($out . '/assets/img', 0755, true);
imagepng(badge(512), $out . '/assets/img/logo-512.png', 9);
imagepng(badge(180), $out . '/assets/img/apple-touch-icon.png', 9);
imagepng(badge(192), $out . '/assets/img/icon-192.png', 9);

// favicon.ico (single 32×32 PNG image inside an ICO container)
ob_start();
imagepng(badge(32));
$png = (string) ob_get_clean();
$ico = pack('vvv', 0, 1, 1) . pack('CCCCvvVV', 32, 32, 0, 0, 1, 32, strlen($png), 22) . $png;
file_put_contents($out . '/favicon.ico', $ico);

// Social image
$w = 1200; $h = 630;
$im = imagecreatetruecolor($w, $h);
for ($y = 0; $y < $h; $y++) {
    $t = $y / $h;
    $r = (int) (58 + (176 - 58) * $t); $g = (int) (27 + (67 - 27) * $t); $b = (int) (12 + (27 - 12) * $t);
    imageline($im, 0, $y, $w, $y, imagecolorallocate($im, $r, $g, $b));
}
$logo = badge(220);
imagecopy($im, $logo, 90, 205, 0, 0, 220, 220);
$white = rgb($im, '#ffffff'); $gold = rgb($im, '#e3b95f'); $cream = rgb($im, '#f6e8d2');
imagettftext($im, 92, 0, 350, 330, $white, $font, 'Rodeo Texas');
imagettftext($im, 36, 0, 354, 400, $gold, $font, 'Find upcoming rodeos across Texas');
imagettftext($im, 26, 0, 354, 450, $cream, $font, 'Dates · venues · show times · official links');
for ($x = 0; $x < $w; $x += 22) {
    imagefilledrectangle($im, $x + 14, $h - 18, $x + 21, $h - 8, imagecolorallocatealpha($im, 255, 255, 255, 90));
}
imagepng($im, $out . '/assets/img/og-default.png', 9);
echo "Images written.\n";
