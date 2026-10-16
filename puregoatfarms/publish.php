<?php
/**
 * One-off importer for puregoatfarms.com. Uploaded next to wp-load.php,
 * run once over HTTPS, and removed again (it deletes itself and its payload
 * after a successful live run).
 *
 *   https://puregoatfarms.com/pgf-publish.php?token=TOKEN&dry=1   report only
 *   https://puregoatfarms.com/pgf-publish.php?token=TOKEN          publish
 *
 * Reads pgf-payload.json (see build_posts.py) and pgf-img/<slug>.webp.
 *  - Creates each post (or updates it if the slug already exists) with its
 *    categories, Yoast meta description / focus keyword / primary category,
 *    and a featured image.
 *  - Splices the contextual links into the two existing posts. An edit is
 *    applied only when its search string occurs exactly once and its
 *    replacement is not already present, and the result is verified byte
 *    for byte before it is kept; otherwise the original content is restored.
 *
 * It runs as the admin user so WordPress does not pass the content through
 * kses, which would strip the <style>/<script> calculators out of the two
 * existing posts when they are re-saved.
 */

define('PGF_TOKEN', '__TOKEN__');

if (!isset($_GET['token']) || !is_string($_GET['token']) || !hash_equals(PGF_TOKEN, $_GET['token'])) {
    http_response_code(404);
    exit;
}

ignore_user_abort(true);
set_time_limit(300);
require __DIR__ . '/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';

header('Content-Type: application/json; charset=utf-8');
$dry = !empty($_GET['dry']);
$report = ['dry_run' => $dry, 'posts' => [], 'edits' => [], 'errors' => []];

$admins = get_users(['role' => 'administrator', 'number' => 1, 'orderby' => 'ID', 'order' => 'ASC']);
if (!$admins) {
    $report['errors'][] = 'no administrator user found';
    echo json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}
$admin = $admins[0];
wp_set_current_user($admin->ID);
$report['run_as'] = $admin->user_login;
if (!current_user_can('unfiltered_html')) {
    $report['errors'][] = 'admin lacks unfiltered_html; refusing to re-save posts through kses';
    echo json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}

$payloadFile = __DIR__ . '/pgf-payload.json';
$payload = json_decode((string) file_get_contents($payloadFile), true);
if (!is_array($payload) || empty($payload['posts'])) {
    $report['errors'][] = 'payload missing or unreadable';
    echo json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    exit;
}

// ---------------------------------------------------------------- new posts
foreach ($payload['posts'] as $p) {
    $r = ['slug' => $p['slug'], 'title' => $p['title']];
    $existing = get_page_by_path($p['slug'], OBJECT, 'post');
    $r['exists'] = $existing ? (int) $existing->ID : false;
    $imgFile = __DIR__ . '/pgf-img/' . $p['slug'] . '.webp';
    $r['image_file'] = is_readable($imgFile);
    $r['words'] = str_word_count(wp_strip_all_tags($p['content']));
    foreach ($p['categories'] as $cid) {
        if (!term_exists((int) $cid, 'category')) {
            $r['missing_category'][] = $cid;
        }
    }
    if ($dry) {
        $report['posts'][] = $r;
        continue;
    }

    $args = [
        'post_title'    => $p['title'],
        'post_name'     => $p['slug'],
        'post_content'  => $p['content'],
        'post_excerpt'  => $p['excerpt'],
        'post_status'   => 'publish',
        'post_type'     => 'post',
        'post_author'   => $admin->ID,
        'post_category' => array_map('intval', $p['categories']),
        'comment_status' => 'closed',
    ];
    if ($existing) {
        $args['ID'] = $existing->ID;
        $postId = wp_update_post(wp_slash($args), true);
    } else {
        $postId = wp_insert_post(wp_slash($args), true);
    }
    if (is_wp_error($postId)) {
        $r['error'] = $postId->get_error_message();
        $report['posts'][] = $r;
        continue;
    }
    $r['id'] = (int) $postId;
    $r['url'] = get_permalink($postId);

    update_post_meta($postId, '_yoast_wpseo_metadesc', $p['metadesc']);
    update_post_meta($postId, '_yoast_wpseo_focuskw', $p['focuskw']);
    update_post_meta($postId, '_yoast_wpseo_primary_category', (string) $p['primary_category']);

    if (!has_post_thumbnail($postId) && is_readable($imgFile)) {
        $bits = wp_upload_bits(basename($imgFile), null, (string) file_get_contents($imgFile));
        if (empty($bits['error'])) {
            $attId = wp_insert_attachment([
                'post_mime_type' => 'image/webp',
                'post_title'     => $p['image_title'],
                'post_content'   => '',
                'post_status'    => 'inherit',
            ], $bits['file'], $postId);
            if (!is_wp_error($attId)) {
                $meta = wp_generate_attachment_metadata($attId, $bits['file']);
                if (is_array($meta)) {
                    wp_update_attachment_metadata($attId, $meta);
                    $r['image_sizes'] = isset($meta['sizes']) ? array_keys($meta['sizes']) : [];
                }
                update_post_meta($attId, '_wp_attachment_image_alt', $p['image_title']);
                set_post_thumbnail($postId, $attId);
                $r['thumbnail'] = (int) $attId;
            } else {
                $r['image_error'] = $attId->get_error_message();
            }
        } else {
            $r['image_error'] = $bits['error'];
        }
    }
    $report['posts'][] = $r;
}

// ---------------------------------------------- links in the existing posts
global $wpdb;
foreach ($payload['edits'] as $e) {
    $post = get_post((int) $e['post_id']);
    $r = ['post' => (int) $e['post_id'], 'anchor' => mb_substr($e['search'], 0, 70)];
    if (!$post) {
        $r['status'] = 'post not found';
        $report['edits'][] = $r;
        continue;
    }
    $content = $post->post_content;
    if (strpos($content, $e['replace']) !== false) {
        $r['status'] = 'already applied';
        $report['edits'][] = $r;
        continue;
    }
    $count = substr_count($content, $e['search']);
    $r['matches'] = $count;
    if ($count !== 1) {
        $r['status'] = 'skipped: anchor must occur exactly once';
        $report['edits'][] = $r;
        continue;
    }
    if ($dry) {
        $r['status'] = 'would apply';
        $report['edits'][] = $r;
        continue;
    }
    $expected = str_replace($e['search'], $e['replace'], $content);
    $res = wp_update_post(wp_slash(['ID' => $post->ID, 'post_content' => $expected]), true);
    if (is_wp_error($res)) {
        $r['status'] = 'error: ' . $res->get_error_message();
        $report['edits'][] = $r;
        continue;
    }
    clean_post_cache($post->ID);
    $saved = get_post($post->ID)->post_content;
    if ($saved !== $expected) {
        // Something filtered the content on save. Put the original back, raw.
        $wpdb->update($wpdb->posts, ['post_content' => $content], ['ID' => $post->ID]);
        clean_post_cache($post->ID);
        $r['status'] = 'reverted: saved content differed from expected (' . strlen($saved) . ' vs ' . strlen($expected) . ' bytes)';
    } else {
        $r['status'] = 'applied';
    }
    $report['edits'][] = $r;
}

// ------------------------------------------------------------------ cleanup
if (!$dry && empty($report['errors'])) {
    $removed = [];
    foreach (glob(__DIR__ . '/pgf-img/*') ?: [] as $f) {
        if (@unlink($f)) $removed[] = basename($f);
    }
    @rmdir(__DIR__ . '/pgf-img');
    if (@unlink($payloadFile)) $removed[] = basename($payloadFile);
    if (@unlink(__FILE__)) $removed[] = basename(__FILE__);
    $report['removed'] = $removed;
}

echo json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
