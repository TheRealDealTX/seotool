<?php
// Photo uploads. Only JPEG, PNG, WebP and GIF are accepted, detected from the
// file's contents (not its name or the browser's type). Every image is decoded
// with GD, resized to at most 1600px and re-encoded as WebP (JPEG if this PHP
// lacks WebP) under a random name, so nothing the user sent is stored as-is.

const MHR_MAX_UPLOAD = 10 * 1024 * 1024;
const MHR_MAX_PHOTOS = 20;

function mhr_upload_dir() { return dirname(APP) . '/wp-content/uploads/owners'; }

// Process $_FILES[$field] (multiple). Returns [images, errors].
function mhr_handle_uploads($field, $alt_base, $limit) {
    $out = []; $err = [];
    if (empty($_FILES[$field]) || !is_array($_FILES[$field]['name'])) return [$out, $err];
    $f = $_FILES[$field];
    $n = count($f['name']);
    for ($i = 0; $i < $n; $i++) {
        if ($f['error'][$i] === UPLOAD_ERR_NO_FILE) continue;
        $name = mb_substr(basename((string)$f['name'][$i]), 0, 80);
        if (count($out) >= $limit) { $err[] = "Only $limit more photo(s) can be added; the rest were skipped."; break; }
        if ($f['error'][$i] !== UPLOAD_ERR_OK) { $err[] = "$name: upload failed."; continue; }
        if ($f['size'][$i] > MHR_MAX_UPLOAD) { $err[] = "$name: photos must be under 10 MB."; continue; }
        $img = mhr_store_image($f['tmp_name'][$i], $alt_base . ' photo ' . (count($out) + 1), $e);
        if ($img) $out[] = $img; else $err[] = "$name: $e";
    }
    return [$out, $err];
}

function mhr_store_image($tmp, $alt, &$error = null) {
    if (!is_uploaded_file($tmp) && !mhr_cfg('dev')) { $error = 'invalid upload.'; return null; }
    $info = @getimagesize($tmp);
    $types = [IMAGETYPE_JPEG => 'imagecreatefromjpeg', IMAGETYPE_PNG => 'imagecreatefrompng', IMAGETYPE_WEBP => 'imagecreatefromwebp', IMAGETYPE_GIF => 'imagecreatefromgif'];
    if (!$info || !isset($types[$info[2]])) { $error = 'please upload a JPEG, PNG, WebP or GIF image.'; return null; }
    [$w, $h] = $info;
    if ($w < 200 || $h < 150) { $error = 'image is too small (minimum 200×150).'; return null; }
    if ($w * $h > 40000000) { $error = 'image dimensions are too large.'; return null; }
    $src = @$types[$info[2]]($tmp);
    if (!$src) { $error = 'the image could not be read.'; return null; }
    if ($info[2] === IMAGETYPE_JPEG && function_exists('exif_read_data')) $src = mhr_exif_rotate($src, $tmp, $w, $h);

    $scale = min(1, 1600 / max($w, $h));
    $nw = max(1, (int)round($w * $scale)); $nh = max(1, (int)round($h * $scale));
    $dst = imagecreatetruecolor($nw, $nh);
    imagefill($dst, 0, 0, imagecolorallocate($dst, 255, 255, 255));
    imagecopyresampled($dst, $src, 0, 0, 0, 0, $nw, $nh, $w, $h);
    imagedestroy($src);

    $sub = gmdate('Y/m');
    $dir = mhr_upload_dir() . '/' . $sub;
    if (!is_dir($dir) && !mkdir($dir, 0755, true)) { $error = 'storage is not writable.'; return null; }
    $webp = function_exists('imagewebp');
    $file = bin2hex(random_bytes(12)) . ($webp ? '.webp' : '.jpg');
    $ok = $webp ? imagewebp($dst, "$dir/$file", 82) : imagejpeg($dst, "$dir/$file", 85);
    imagedestroy($dst);
    if (!$ok) { $error = 'the image could not be saved.'; return null; }
    @chmod("$dir/$file", 0644);
    return ['src' => "/wp-content/uploads/owners/$sub/$file", 'alt' => mb_substr($alt, 0, 150), 'w' => $nw, 'h' => $nh];
}

function mhr_exif_rotate($img, $file, &$w, &$h) {
    $exif = @exif_read_data($file);
    $deg = [3 => 180, 6 => -90, 8 => 90][$exif['Orientation'] ?? 1] ?? 0;
    if (!$deg) return $img;
    $r = imagerotate($img, $deg, 0);
    if (!$r) return $img;
    imagedestroy($img);
    if ($deg !== 180) [$w, $h] = [$h, $w];
    return $r;
}

// Delete a stored owner photo (only files under uploads/owners).
function mhr_delete_image($src) {
    if (!preg_match('#^/wp-content/uploads/owners/\d{4}/\d{2}/[a-f0-9]{24}\.(webp|jpg)$#', $src)) return;
    $f = dirname(APP) . $src;
    if (is_file($f)) @unlink($f);
}
