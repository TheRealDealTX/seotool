<?php
// Photo uploads from the admin: validate, resize, save as WebP under /media/p/{id}/.
defined('HA_ROOT') || exit;

final class Images
{
    private const MAX_SIDE = 1800;

    /** @return string|null public path of the saved image */
    public static function saveUpload(array $file, int $propertyId, string $prefix = 'photo'): ?string
    {
        if (($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || !is_uploaded_file($file['tmp_name'])) {
            return null;
        }
        $info = @getimagesize($file['tmp_name']);
        if (!$info || !in_array($info[2], [IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_WEBP, IMAGETYPE_GIF], true)) {
            return null;
        }
        $src = match ($info[2]) {
            IMAGETYPE_JPEG => @imagecreatefromjpeg($file['tmp_name']),
            IMAGETYPE_PNG  => @imagecreatefrompng($file['tmp_name']),
            IMAGETYPE_WEBP => @imagecreatefromwebp($file['tmp_name']),
            IMAGETYPE_GIF  => @imagecreatefromgif($file['tmp_name']),
        };
        if (!$src) {
            return null;
        }
        if ($info[2] === IMAGETYPE_JPEG && function_exists('exif_read_data')) {
            $o = (@exif_read_data($file['tmp_name'])['Orientation'] ?? 1);
            $src = match ((int) $o) { 3 => imagerotate($src, 180, 0), 6 => imagerotate($src, -90, 0), 8 => imagerotate($src, 90, 0), default => $src };
        }
        [$w, $h] = [imagesx($src), imagesy($src)];
        $scale = min(1, self::MAX_SIDE / max($w, $h));
        if ($scale < 1) {
            $dst = imagecreatetruecolor((int) round($w * $scale), (int) round($h * $scale));
            imagealphablending($dst, false);
            imagesavealpha($dst, true);
            imagecopyresampled($dst, $src, 0, 0, 0, 0, imagesx($dst), imagesy($dst), $w, $h);
            imagedestroy($src);
            $src = $dst;
        }
        $dir = HA_ROOT . "/media/p/$propertyId";
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        $name = $prefix . '-' . bin2hex(random_bytes(5));
        if (function_exists('imagewebp')) {
            $rel = "/media/p/$propertyId/$name.webp";
            imagewebp($src, HA_ROOT . $rel, 82);
        } else {
            $rel = "/media/p/$propertyId/$name.jpg";
            imagejpeg($src, HA_ROOT . $rel, 85);
        }
        imagedestroy($src);
        return $rel;
    }

    /** Normalize $_FILES['x'] (multiple) into a list of single-file arrays. */
    public static function files(string $field): array
    {
        $f = $_FILES[$field] ?? null;
        if (!$f || !is_array($f['name'])) {
            return $f ? [$f] : [];
        }
        $out = [];
        foreach ($f['name'] as $i => $_) {
            $out[$i] = ['name' => $f['name'][$i], 'type' => $f['type'][$i], 'tmp_name' => $f['tmp_name'][$i], 'error' => $f['error'][$i], 'size' => $f['size'][$i]];
        }
        return $out;
    }

    public static function removeDir(int $propertyId): void
    {
        $dir = HA_ROOT . "/media/p/$propertyId";
        foreach (glob("$dir/*") ?: [] as $f) {
            @unlink($f);
        }
        @rmdir($dir);
    }
}
