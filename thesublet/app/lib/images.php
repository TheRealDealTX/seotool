<?php defined('APP') || exit;

const MAX_PHOTOS = 12;

/**
 * Re-encode an uploaded image to WebP (max 1600px, strips metadata/EXIF incl. GPS).
 * Returns [binary, w, h] or throws.
 */
function photo_reencode(string $tmpPath): array
{
    if (!function_exists('imagewebp')) throw new RuntimeException('Image processing is unavailable on this server.');
    $info = @getimagesize($tmpPath);
    if (!$info) throw new RuntimeException('That file is not an image.');
    [$w, $h, $type] = $info;
    if ($w * $h > 40_000_000) throw new RuntimeException('Image dimensions are too large.');
    $src = match ($type) {
        IMAGETYPE_JPEG => @imagecreatefromjpeg($tmpPath),
        IMAGETYPE_PNG => @imagecreatefrompng($tmpPath),
        IMAGETYPE_WEBP => @imagecreatefromwebp($tmpPath),
        IMAGETYPE_GIF => @imagecreatefromgif($tmpPath),
        default => false,
    };
    if (!$src) throw new RuntimeException('Unsupported image type. Use JPG, PNG, WebP or GIF.');

    if ($type === IMAGETYPE_JPEG && function_exists('exif_read_data')) {
        $exif = @exif_read_data($tmpPath);
        $o = (int)($exif['Orientation'] ?? 1);
        if (in_array($o, [3, 6, 8], true)) {
            $src = imagerotate($src, [3 => 180, 6 => -90, 8 => 90][$o], 0);
            $w = imagesx($src); $h = imagesy($src);
        }
    }
    $max = 1600;
    $scale = min(1, $max / max($w, $h));
    $nw = max(1, (int)round($w * $scale)); $nh = max(1, (int)round($h * $scale));
    $dst = imagecreatetruecolor($nw, $nh);
    imagealphablending($dst, false);
    imagesavealpha($dst, true);
    imagefill($dst, 0, 0, imagecolorallocatealpha($dst, 255, 255, 255, 127));
    imagecopyresampled($dst, $src, 0, 0, 0, 0, $nw, $nh, $w, $h);
    ob_start();
    imagewebp($dst, null, 80);
    $bin = (string)ob_get_clean();
    imagedestroy($src); imagedestroy($dst);
    if ($bin === '') throw new RuntimeException('Could not convert image.');
    return [$bin, $nw, $nh];
}

/** Handle $_FILES[$field] (multiple). Returns [savedCount, errors[]]. */
function photos_save_uploads(int $listingId, string $field = 'photos'): array
{
    $saved = 0; $errors = [];
    if (empty($_FILES[$field]) || !is_array($_FILES[$field]['name'])) return [0, []];
    $existing = (int)val('SELECT COUNT(*) FROM photos WHERE listing_id = ?', [$listingId]);
    $sort = (int)val('SELECT COALESCE(MAX(sort), 0) FROM photos WHERE listing_id = ?', [$listingId]);
    foreach ($_FILES[$field]['name'] as $i => $name) {
        $errCode = $_FILES[$field]['error'][$i];
        if ($errCode === UPLOAD_ERR_NO_FILE) continue;
        if ($existing + $saved >= MAX_PHOTOS) { $errors[] = 'Photo limit reached (' . MAX_PHOTOS . ').'; break; }
        if ($errCode !== UPLOAD_ERR_OK) { $errors[] = e($name) . ': upload failed (file too large?).'; continue; }
        if ($_FILES[$field]['size'][$i] > 15 * 1024 * 1024) { $errors[] = e($name) . ': larger than 15 MB.'; continue; }
        try {
            [$bin, $w, $h] = photo_reencode($_FILES[$field]['tmp_name'][$i]);
            $st = db()->prepare('INSERT INTO photos (listing_id, data, width, height, sort, created_at) VALUES (?, ?, ?, ?, ?, ?)');
            $st->bindValue(1, $listingId, PDO::PARAM_INT);
            $st->bindValue(2, $bin, PDO::PARAM_LOB);
            $st->bindValue(3, $w, PDO::PARAM_INT);
            $st->bindValue(4, $h, PDO::PARAM_INT);
            $st->bindValue(5, ++$sort, PDO::PARAM_INT);
            $st->bindValue(6, now());
            $st->execute();
            $saved++;
        } catch (Throwable $e) {
            $errors[] = e($name) . ': ' . $e->getMessage();
        }
    }
    return [$saved, $errors];
}

/** Public URL of an uploaded photo. No image extension: Hostinger's nginx answers *.webp/*.jpg itself and never reaches PHP. */
function photo_src(int $id): string
{
    return '/photo/' . $id . '/';
}

function serve_photo(int $id): never
{
    $p = row('SELECT p.data, p.created_at, l.status FROM photos p JOIN listings l ON l.id = p.listing_id WHERE p.id = ?', [$id]);
    if (!$p) { http_response_code(404); exit; }
    $etag = '"p' . $id . '-' . strlen($p['data']) . '"';
    header('Content-Type: image/webp');
    header('Cache-Control: public, max-age=2592000, immutable');
    header('ETag: ' . $etag);
    if (($_SERVER['HTTP_IF_NONE_MATCH'] ?? '') === $etag) { http_response_code(304); exit; }
    header('Content-Length: ' . strlen($p['data']));
    echo $p['data'];
    exit;
}
