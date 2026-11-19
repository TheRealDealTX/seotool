<?php
declare(strict_types=1);
defined('M1S') || exit;

function admin_meta(string $title): array
{
    return ['title' => $title . ' · Admin', 'robots' => 'noindex, nofollow', 'body_class' => 'page-admin'];
}

function admin_dashboard(): void
{
    require_mod();
    $stats = [
        'Members' => (int)val('SELECT COUNT(*) FROM users'),
        'New members (7d)' => (int)val('SELECT COUNT(*) FROM users WHERE created_at > ?', [gmdate('Y-m-d H:i:s', time() - 604800)]),
        'Forum posts' => (int)val('SELECT COUNT(*) FROM threads WHERE removed = 0 AND status = \'live\''),
        'Comments' => (int)val('SELECT COUNT(*) FROM comments WHERE removed = 0 AND deleted = 0 AND status = \'live\''),
        'Articles' => (int)val("SELECT COUNT(*) FROM articles WHERE status = 'published'"),
        'Open reports' => (int)val('SELECT COUNT(*) FROM reports WHERE resolved_at IS NULL'),
    ];
    $recentThreads = all(THREAD_SELECT . ' ORDER BY t.created_at DESC LIMIT 10');
    $recentComments = all('SELECT c.*, u.username FROM comments c LEFT JOIN users u ON u.id = c.user_id ORDER BY c.created_at DESC LIMIT 10');
    render('admin/dashboard', compact('stats', 'recentThreads', 'recentComments'), admin_meta('Dashboard'));
}

function admin_articles(): void
{
    require_admin();
    $articles = all(ARTICLE_SELECT . ' ORDER BY a.published_at DESC');
    render('admin/articles', compact('articles'), admin_meta('Articles'));
}

function admin_article_edit(string $id): void
{
    $u = require_admin();
    $a = $id === 'new' ? null : (one('SELECT * FROM articles WHERE id = ?', [(int)$id]) ?? not_found());
    if (is_post()) {
        $title = trim(input('title'));
        $slug = slugify(input('slug') ?: $title, 100);
        $row = [
            'title' => $title,
            'slug' => $slug,
            'seo_title' => mb_substr(trim(input('seo_title')), 0, 120) ?: null,
            'meta_description' => mb_substr(trim(input('meta_description')), 0, 200) ?: null,
            'body_html' => (string)($_POST['body_html'] ?? ''),
            'topic_id' => (int)input('topic_id') ?: null,
            'status' => input('status') === 'draft' ? 'draft' : 'published',
            'image_alt' => trim(input('image_alt')) ?: null,
            'image_credit' => mb_substr(trim(input('image_credit')), 0, 300) ?: null,
            'image_credit_url' => preg_match('#^https?://#', trim(input('image_credit_url'))) ? mb_substr(trim(input('image_credit_url')), 0, 500) : null,
            'updated_at' => now(),
        ];
        $pub = input('published_at');
        $row['published_at'] = $pub && strtotime($pub) ? gmdate('Y-m-d H:i:s', strtotime($pub . ' UTC')) : ($a['published_at'] ?? now());
        $text = trim(preg_replace('/\s+/u', ' ', html_entity_decode(strip_tags($row['body_html']), ENT_QUOTES)));
        $row['excerpt'] = excerpt($text, 260);
        $row['reading_minutes'] = max(1, (int)round(str_word_count($text) / 230));
        $errors = [];
        if (mb_strlen($title) < 5) $errors[] = 'Title is too short.';
        if (one('SELECT id FROM articles WHERE slug = ? AND id <> ?', [$slug, $a['id'] ?? 0])) $errors[] = 'Another article already uses that URL slug.';
        if (!empty($_FILES['image']) && ($_FILES['image']['error'] ?? 4) !== UPLOAD_ERR_NO_FILE) {
            $img = store_upload_image($_FILES['image']);
            if (is_string($img)) $errors[] = $img;
            else [$row['image'], $row['image_w'], $row['image_h']] = $img;
        }
        if ($errors) {
            foreach ($errors as $err) flash('error', $err);
            redirect('/admin/articles/' . ($a['id'] ?? 'new') . '/');
        }
        if ($a) {
            update('articles', $row, 'id = :id', ['id' => $a['id']]);
            $aid = (int)$a['id'];
        } else {
            $row['author_id'] = $u['id'];
            $aid = insert('articles', $row);
        }
        flash('ok', 'Article saved.');
        redirect('/admin/articles/' . $aid . '/');
    }
    render('admin/article_edit', ['a' => $a, 'topics' => topics()], admin_meta($a ? 'Edit article' : 'New article'));
}

function admin_article_delete(string $id): void
{
    require_admin();
    $a = one('SELECT * FROM articles WHERE id = ?', [(int)$id]) ?? not_found();
    q('DELETE FROM comments WHERE target_type = ? AND target_id = ?', ['article', $a['id']]);
    q('DELETE FROM votes WHERE target_type = ? AND target_id = ?', ['article', $a['id']]);
    q('DELETE FROM articles WHERE id = ?', [$a['id']]);
    flash('ok', 'Article deleted. Consider whether its URL should redirect somewhere.');
    redirect('/admin/articles/');
}

function admin_reports(): void
{
    $u = require_mod();
    if (is_post()) {
        $r = one('SELECT * FROM reports WHERE id = ?', [(int)input('id')]) ?? not_found();
        $action = input('action');
        if ($action === 'remove') {
            $table = $r['target_type'] === 'thread' ? 'threads' : 'comments';
            q("UPDATE $table SET removed = 1 WHERE id = ?", [$r['target_id']]);
            if ($r['target_type'] === 'comment') {
                $c = one('SELECT * FROM comments WHERE id = ?', [$r['target_id']]);
                if ($c) refresh_comment_count($c['target_type'], (int)$c['target_id']);
            }
        }
        q('UPDATE reports SET resolved_by = ?, resolved_at = ? WHERE target_type = ? AND target_id = ? AND resolved_at IS NULL',
            [$u['id'], now(), $r['target_type'], $r['target_id']]);
        flash('ok', $action === 'remove' ? 'Content removed and reports closed.' : 'Reports dismissed.');
        redirect('/admin/reports/');
    }
    $reports = all('SELECT r.*, u.username AS reporter FROM reports r LEFT JOIN users u ON u.id = r.user_id WHERE r.resolved_at IS NULL ORDER BY r.created_at DESC LIMIT 200');
    foreach ($reports as &$r) {
        if ($r['target_type'] === 'thread') {
            $t = find_thread((int)$r['target_id']);
            $r['preview'] = $t ? $t['title'] : '[gone]';
            $r['link'] = $t ? thread_url($t) : null;
            $r['author'] = $t['username'] ?? null;
        } else {
            $c = one('SELECT c.*, u.username FROM comments c LEFT JOIN users u ON u.id = c.user_id WHERE c.id = ?', [$r['target_id']]);
            $tgt = $c ? comment_target($c['target_type'], (int)$c['target_id']) : null;
            $r['preview'] = $c ? excerpt($c['body'], 200) : '[gone]';
            $r['link'] = $tgt ? $tgt['url'] . '#c' . $c['id'] : null;
            $r['author'] = $c['username'] ?? null;
        }
    }
    unset($r);
    render('admin/reports', compact('reports'), admin_meta('Reports'));
}

function admin_users(): void
{
    $me = require_mod();
    if (is_post() && in_array(input('action'), ['guest_ban', 'guest_unban'], true)) {
        $email = strtolower(input('email'));
        $ban = input('action') === 'guest_ban' ? 1 : 0;
        if (!one('SELECT email FROM guests WHERE email = ?', [$email])) {
            insert('guests', ['email' => $email, 'name' => (string)input('name'), 'verified_at' => null, 'banned' => $ban, 'created_at' => now()]);
        } else {
            q('UPDATE guests SET banned = ? WHERE email = ?', [$ban, $email]);
        }
        if ($ban) {
            q('UPDATE threads SET removed = 1 WHERE guest_email = ?', [$email]);
            foreach (all('SELECT id, target_type, target_id FROM comments WHERE guest_email = ?', [$email]) as $c) {
                q('UPDATE comments SET removed = 1 WHERE id = ?', [$c['id']]);
                refresh_comment_count($c['target_type'], (int)$c['target_id']);
            }
        }
        flash('ok', $ban ? 'Guest email banned and their posts removed.' : 'Guest email unbanned.');
        redirect('/admin/users/');
    }
    if (is_post()) {
        $target = one('SELECT * FROM users WHERE id = ?', [(int)input('id')]) ?? not_found();
        $action = input('action');
        if ((int)$target['id'] === (int)$me['id']) {
            flash('error', 'You cannot change your own account here.');
        } elseif (in_array($action, ['ban', 'unban'], true) && ($target['role'] === 'member' || is_admin($me))) {
            update('users', ['banned' => $action === 'ban' ? 1 : 0, 'session_epoch' => (int)$target['session_epoch'] + 1], 'id = :id', ['id' => $target['id']]);
            if ($action === 'ban' && input('purge') === '1') {
                q('UPDATE threads SET removed = 1 WHERE user_id = ?', [$target['id']]);
                q('UPDATE comments SET removed = 1 WHERE user_id = ?', [$target['id']]);
            }
            flash('ok', 'User ' . $target['username'] . ($action === 'ban' ? ' banned.' : ' unbanned.'));
        } elseif ($action === 'role' && is_admin($me) && in_array(input('role'), ['member', 'mod', 'admin'], true)) {
            update('users', ['role' => input('role')], 'id = :id', ['id' => $target['id']]);
            flash('ok', 'Role updated.');
        } else {
            flash('error', 'Not allowed.');
        }
        redirect('/admin/users/' . (input('q') !== '' ? '?q=' . rawurlencode(input('q')) : ''));
    }
    $qText = trim($_GET['q'] ?? '');
    $users = $qText !== ''
        ? all('SELECT * FROM users WHERE username LIKE ? OR email LIKE ? ORDER BY created_at DESC LIMIT 100', ["%$qText%", "%$qText%"])
        : all('SELECT * FROM users ORDER BY created_at DESC LIMIT 100');
    $guests = all("SELECT g.email, MAX(g.name) AS name, MAX(g.banned) AS banned, MAX(g.verified_at) AS verified_at,
        (SELECT COUNT(*) FROM threads t WHERE t.guest_email = g.email) + (SELECT COUNT(*) FROM comments c WHERE c.guest_email = g.email) AS posts
        FROM guests g GROUP BY g.email ORDER BY MAX(g.created_at) DESC LIMIT 200");
    render('admin/users', compact('users', 'qText', 'guests'), admin_meta('Users'));
}

function admin_communities(): void
{
    require_admin();
    if (is_post()) {
        $id = (int)input('id');
        $row = [
            'name' => trim(input('name')),
            'title' => trim(input('title')),
            'description' => trim(input('description')),
            'color' => preg_match('/^#[0-9a-f]{6}$/i', input('color')) ? input('color') : '#1f8fcf',
            'sort' => (int)input('sort'),
        ];
        if ($row['name'] === '' || $row['title'] === '' || $row['description'] === '') {
            flash('error', 'Name, SEO title and description are required.');
        } elseif ($id) {
            update('communities', $row, 'id = :id', ['id' => $id]);
            flash('ok', 'Community saved.');
        } else {
            $slug = slugify(input('slug') ?: $row['name'], 40);
            if (one('SELECT id FROM communities WHERE slug = ?', [$slug])) {
                flash('error', 'That URL is already used.');
            } else {
                insert('communities', $row + ['slug' => $slug, 'created_at' => now()]);
                flash('ok', 'Community created.');
            }
        }
        redirect('/admin/communities/');
    }
    render('admin/communities', ['communities' => communities()], admin_meta('Communities'));
}

function admin_topics(): void
{
    require_admin();
    if (is_post()) {
        $id = (int)input('id');
        $row = ['name' => trim(input('name')), 'seo_title' => trim(input('seo_title')), 'description' => trim(input('description')), 'sort' => (int)input('sort')];
        if ($row['name'] === '') {
            flash('error', 'Name is required.');
        } elseif ($id) {
            update('topics', $row, 'id = :id', ['id' => $id]);
            flash('ok', 'Topic saved.');
        } else {
            $slug = slugify(input('slug') ?: $row['name'], 60);
            if (one('SELECT id FROM topics WHERE slug = ?', [$slug])) {
                flash('error', 'That URL is already used.');
            } else {
                insert('topics', $row + ['slug' => $slug]);
                flash('ok', 'Topic created.');
            }
        }
        redirect('/admin/topics/');
    }
    render('admin/topics', ['topics' => topics()], admin_meta('Topics'));
}

function admin_products(): void
{
    require_admin();
    if (is_post()) {
        $id = (int)input('id');
        if (input('action') === 'delete' && $id) {
            q('DELETE FROM products WHERE id = ?', [$id]);
            flash('ok', 'Product deleted.');
            redirect('/admin/products/');
        }
        $row = [
            'name' => mb_substr(trim(input('name')), 0, 160),
            'blurb' => mb_substr(trim(input('blurb')), 0, 300) ?: null,
            'query' => mb_substr(trim(input('query')), 0, 200) ?: null,
            'url' => mb_substr(trim(input('url')), 0, 500) ?: null,
            'image' => preg_match('#^https://#', trim(input('image'))) ? mb_substr(trim(input('image')), 0, 500) : null,
            'tags' => implode(',', array_filter(array_map('trim', explode(',', strtolower(input('tags')))))),
            'sort' => (int)input('sort'),
            'active' => input('active') === '1' ? 1 : 0,
        ];
        if ($row['name'] === '') {
            flash('error', 'Name is required.');
        } elseif ($row['url'] && !preg_match('#^(https://(www\.)?amazon\.com/|[A-Z0-9]{10}$)#', $row['url'])) {
            flash('error', 'Link must be an amazon.com URL or a 10-character ASIN.');
        } elseif ($id) {
            update('products', $row, 'id = :id', ['id' => $id]);
            flash('ok', 'Product saved.');
        } else {
            insert('products', $row + ['created_at' => now()]);
            flash('ok', 'Product added.');
        }
        redirect('/admin/products/' . (input('f') !== '' ? '?f=' . rawurlencode(input('f')) : ''));
    }
    $f = trim($_GET['f'] ?? '');
    $products = $f !== ''
        ? all('SELECT * FROM products WHERE tags LIKE ? OR name LIKE ? ORDER BY tags, sort, id', ["%$f%", "%$f%"])
        : all('SELECT * FROM products ORDER BY tags, sort, id');
    render('admin/products', compact('products', 'f'), admin_meta('Amazon products'));
}
