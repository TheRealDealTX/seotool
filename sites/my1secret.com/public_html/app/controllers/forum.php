<?php
declare(strict_types=1);
defined('M1S') || exit;

const SORTS = ['hot' => 'Hot', 'new' => 'New', 'top' => 'Top', 'comments' => 'Most discussed'];
const PERIODS = ['day' => 'Today', 'week' => 'This week', 'month' => 'This month', 'year' => 'This year', 'all' => 'All time'];

function sort_params(): array
{
    $sort = $_GET['sort'] ?? 'hot';
    $sort = isset(SORTS[$sort]) ? $sort : 'hot';
    $t = $_GET['t'] ?? 'all';
    $t = isset(PERIODS[$t]) ? $t : 'all';
    return [$sort, $t];
}

function forum_index(): void
{
    [$sort, $t] = sort_params();
    $page = page_num();
    [$threads, $hasNext] = thread_list(null, $sort, $page, 25, $t);
    $counts = [];
    foreach (all('SELECT community_id, COUNT(*) n FROM threads WHERE removed = 0 AND status = \'live\' GROUP BY community_id') as $r) {
        $counts[(int)$r['community_id']] = (int)$r['n'];
    }
    render('forum_list', [
        'community' => null, 'threads' => $threads, 'hasNext' => $hasNext, 'page' => $page,
        'sort' => $sort, 't' => $t, 'votes' => my_votes('thread', array_column($threads, 'id')), 'counts' => $counts,
    ], [
        'title' => 'Community Forum: Renting, Home, Insurance & Texas Talk',
        'description' => 'Join the My 1 Secret forum: ask questions and share tips on renting, small-space living, insurance claims, Texas living and life hacks.',
        'robots' => ($sort !== 'hot' || $page > 1) ? 'noindex, follow' : null,
        'canonical' => abs_url('/forum/') . ($page > 1 && $sort === 'hot' ? '?page=' . $page : ''),
        'jsonld' => [breadcrumb_schema([['Forum', '/forum/']]), ['@type' => 'CollectionPage', 'name' => 'My 1 Secret Community Forum', 'url' => abs_url('/forum/')]],
        'breadcrumbs' => [['Forum', null]],
    ]);
}

function community_page(string $slug): void
{
    $c = find_community($slug) ?? not_found();
    [$sort, $t] = sort_params();
    $page = page_num();
    [$threads, $hasNext] = thread_list((int)$c['id'], $sort, $page, 25, $t);
    $total = (int)val('SELECT COUNT(*) FROM threads WHERE community_id = ? AND removed = 0 AND status = \'live\'', [$c['id']]);
    $topicSlug = array_search($c['slug'], ['renting' => 'renting', 'home-design' => 'small-space-living', 'insurance-claims' => 'insurance-claims', 'texas-living' => 'texas', 'lifestyle' => 'lifestyle'], true);
    $articles = [];
    if ($topicSlug) {
        $tid = (int)val('SELECT id FROM topics WHERE slug = ?', [$topicSlug]);
        [$articles] = article_list($tid, 1, 4);
    }
    $postings = [];
    foreach (array_slice($threads, 0, 10) as $th) {
        $postings[] = ['@type' => 'ListItem', 'position' => count($postings) + 1, 'url' => abs_url(thread_url($th)), 'name' => $th['title']];
    }
    render('forum_list', [
        'community' => $c, 'threads' => $threads, 'hasNext' => $hasNext, 'page' => $page, 'total' => $total,
        'sort' => $sort, 't' => $t, 'votes' => my_votes('thread', array_column($threads, 'id')), 'articles' => $articles, 'topicSlug' => $topicSlug,
    ], [
        'title' => $c['title'] . ($page > 1 ? " (Page $page)" : ''),
        'description' => $c['description'],
        'robots' => ($sort !== 'hot' || $page > 1) ? 'noindex, follow' : null,
        'canonical' => abs_url(community_url($c)) . ($page > 1 && $sort === 'hot' ? '?page=' . $page : ''),
        'jsonld' => [
            breadcrumb_schema([['Forum', '/forum/'], [$c['name'], community_url($c)]]),
            ['@type' => 'CollectionPage', 'name' => $c['title'], 'description' => $c['description'], 'url' => abs_url(community_url($c)),
             'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $postings]],
        ],
        'breadcrumbs' => [['Forum', '/forum/'], [$c['name'], null]],
    ]);
}

function thread_page(string $cslug, string $id, string $slug): void
{
    $t = find_thread((int)$id) ?? not_found();
    if ($t['status'] !== 'live' && !is_mod()) {
        not_found();
    }
    $url = thread_url($t);
    if ($t['community_slug'] !== $cslug || $t['slug'] !== $slug) {
        redirect($url, 301);
    }
    if ($t['removed'] && !is_mod()) {
        render('error', ['code' => 410, 'heading' => 'This post was removed',
            'message' => 'A moderator removed this post for breaking the community guidelines.'],
            ['title' => 'Post removed', 'robots' => 'noindex, follow'], 410);
    }
    $sort = in_array($_GET['sort'] ?? '', ['new', 'old'], true) ? $_GET['sort'] : 'best';
    $tree = comment_tree('thread', (int)$t['id'], $url, $sort);
    $commentVotes = my_votes('comment', flatten_ids($tree));
    $myVote = my_votes('thread', [(int)$t['id']])[(int)$t['id']] ?? 0;
    $c = find_community($t['community_slug']);
    $more = all(THREAD_SELECT . ' WHERE t.removed = 0 AND t.status = \'live\' AND t.community_id = ? AND t.id <> ? ORDER BY t.hot DESC LIMIT 5', [$t['community_id'], $t['id']]);

    $text = $t['deleted'] ? '' : md_plain((string)$t['body']);
    $budget = 40;
    $posting = [
        '@type' => 'DiscussionForumPosting',
        '@id' => abs_url($url) . '#post',
        'headline' => $t['title'],
        'url' => abs_url($url),
        'mainEntityOfPage' => abs_url($url),
        'datePublished' => iso_date($t['created_at']),
        'author' => $t['deleted'] ? ['@type' => 'Person', 'name' => '[deleted]'] : ($t['username'] ? person_schema($t['username'], $t['display_name']) : ['@type' => 'Person', 'name' => $t['guest_name'] ?: '[deleted]']),
        'interactionStatistic' => interaction_stats((int)$t['upvotes'], (int)$t['comment_count']),
        'isPartOf' => ['@type' => 'WebPage', 'name' => $c['title'], 'url' => abs_url(community_url($c))],
    ];
    if ($text !== '') {
        $posting['text'] = excerpt($text, 2000);
    }
    if ($t['edited_at']) {
        $posting['dateModified'] = iso_date($t['edited_at']);
    }
    if ($t['image']) {
        $posting['image'] = abs_url($t['image']);
    }
    if ($t['link_url']) {
        $posting['sharedContent'] = ['@type' => 'WebPage', 'url' => $t['link_url']];
    }
    if ($tree) {
        $posting['comment'] = comments_schema($tree, $budget);
    }
    $desc = $text !== '' ? excerpt($text, 145) : excerpt($t['title'] . ' Discussion in ' . $c['name'] . ' on My 1 Secret.', 145);

    render('thread', compact('t', 'tree', 'commentVotes', 'myVote', 'c', 'more', 'sort'), [
        'title' => mb_strlen($t['title']) <= 45 ? $t['title'] . ' : ' . $c['name'] : $t['title'],
        'description' => $desc,
        'canonical' => abs_url($url),
        'robots' => thread_indexable($t) ? null : 'noindex, follow',
        'image' => $t['image'] ? abs_url($t['image']) : null,
        'type' => 'article',
        'jsonld' => [$posting, breadcrumb_schema([['Forum', '/forum/'], [$c['name'], community_url($c)], [$t['title'], null]])],
        'breadcrumbs' => [['Forum', '/forum/'], [$c['name'], community_url($c)]],
    ]);
}

/* ---------- posting rules ---------- */

/** Light spam rules for brand-new accounts. Returns an error message or null. */
function posting_blocked(array $u, string $text, string $kind): ?string
{
    if ((int)$u['banned']) {
        return 'Your account is suspended.';
    }
    $ageHours = (time() - strtotime($u['created_at'] . ' UTC')) / 3600;
    $newbie = !is_mod($u) && $ageHours < 48 && (int)$u['karma'] < 5;
    if ($newbie && md_link_count($text) > 1) {
        return 'New accounts can include one link per ' . $kind . '. Join a few conversations first and the limit lifts.';
    }
    $limits = $kind === 'post' ? [$newbie ? 3 : 10, 3600] : [$newbie ? 15 : 60, 3600];
    if (!throttle($kind, $limits[0], $limits[1], 'u' . $u['id'])) {
        return 'You are posting very quickly. Take a short break and try again.';
    }
    return null;
}

function submit_page(): void
{
    $u = current_user();   // guests may post with a name + email
    $cslug = input('community', $_GET['c'] ?? '');
    $errors = [];
    if (is_post()) {
        $c = find_community($cslug);
        $title = trim(preg_replace('/\s+/u', ' ', input('title')));
        $body = rtrim(input('body'));
        $link = input('link_url');
        if (!$c) $errors[] = 'Choose a community.';
        if (mb_strlen($title) < 8) $errors[] = 'Give your post a descriptive title (at least 8 characters).';
        if (mb_strlen($title) > 300) $errors[] = 'Titles can be up to 300 characters.';
        if (mb_strlen($body) > 40000) $errors[] = 'The post is too long (40,000 characters max).';
        if ($link !== '' && (!filter_var($link, FILTER_VALIDATE_URL) || !preg_match('#^https?://#i', $link))) $errors[] = 'The link must start with http:// or https://';
        if ($title !== '' && preg_match('/^[^a-z]*$/', $title) && preg_match('/[A-Z]{12,}/', $title)) $errors[] = 'Please do not write the title in all caps.';
        $guestName = $guestEmail = null;
        if (!$u && !$errors) {
            [$guestName, $guestEmail, $gerr] = guest_from_post('post');
            if ($gerr) $errors[] = $gerr;
            elseif (md_link_count($body . ' ' . $link) > 1) $errors[] = 'Posts without an account can include one link. Create a free account to share more.';
        }
        $img = null;
        if (!$errors && $u && !empty($_FILES['image'])) {
            $r = store_upload_image($_FILES['image']);
            if (is_string($r) && $r !== 'none') $errors[] = $r;
            if (is_array($r)) $img = $r;
        }
        if (!$errors && $u && ($msg = posting_blocked($u, $body . ' ' . $link, 'post'))) $errors[] = $msg;
        if (!$errors && one('SELECT id FROM threads WHERE ' . ($u ? 'user_id = ?' : 'guest_email = ?') . ' AND title = ? AND created_at > ?',
                [$u ? $u['id'] : $guestEmail, $title, gmdate('Y-m-d H:i:s', time() - 86400)])) {
            $errors[] = 'You already posted this.';
        }
        if (!$errors) {
            $live = $u || guest_is_trusted($guestEmail);
            $id = insert('threads', [
                'community_id' => $c['id'], 'user_id' => $u['id'] ?? null, 'guest_name' => $guestName, 'guest_email' => $guestEmail,
                'status' => $live ? 'live' : 'pending', 'title' => $title, 'slug' => slugify($title),
                'body' => $body, 'body_html' => md($body), 'link_url' => $link ?: null,
                'image' => $img[0] ?? null, 'image_w' => $img[1] ?? null, 'image_h' => $img[2] ?? null,
                'score' => 1, 'upvotes' => 1, 'hot' => hot_score(1, now()), 'created_at' => now(), 'last_activity_at' => now(),
            ]);
            if ($u) {
                insert('votes', ['user_id' => $u['id'], 'target_type' => 'thread', 'target_id' => $id, 'value' => 1, 'created_at' => now()]);
                redirect(thread_url(find_thread($id)));
            }
            guest_remember($guestName, $guestEmail);
            if ($live) {
                redirect(thread_url(find_thread($id)));
            }
            guest_send_confirmation('thread', $id, $guestName, $guestEmail, $title);
            guest_gc();
            redirect('/confirm/sent/?e=' . rawurlencode(guest_mask($guestEmail)));
        }
        remember_input(['title', 'body', 'link_url', 'community', 'guest_name', 'guest_email']);
        foreach ($errors as $err) flash('error', $err);
        redirect('/submit/' . ($cslug ? '?c=' . rawurlencode($cslug) : ''));
    }
    render('submit', ['communities' => communities(), 'selected' => old('community', $cslug), 'thread' => null], [
        'title' => 'Create a post', 'robots' => 'noindex',
    ]);
}

function thread_edit(string $cslug, string $id, string $slug): void
{
    $u = require_login();
    $t = find_thread((int)$id) ?? not_found();
    if ((int)$t['user_id'] !== (int)$u['id'] && !is_mod($u)) {
        forbidden();
    }
    if ($t['deleted']) {
        not_found();
    }
    if (is_post()) {
        $title = trim(preg_replace('/\s+/u', ' ', input('title')));
        $body = rtrim(input('body'));
        $link = input('link_url');
        $err = null;
        if (mb_strlen($title) < 8 || mb_strlen($title) > 300) $err = 'Titles must be 8 to 300 characters.';
        elseif (mb_strlen($body) > 40000) $err = 'The post is too long.';
        elseif ($link !== '' && (!filter_var($link, FILTER_VALIDATE_URL) || !preg_match('#^https?://#i', $link))) $err = 'The link must start with http:// or https://';
        elseif (!is_mod($u) && (time() - strtotime($u['created_at'] . ' UTC')) < 172800 && (int)$u['karma'] < 5 && md_link_count($body . ' ' . $link) > 1) $err = 'New accounts can include one link per post.';
        if ($err) {
            flash('error', $err);
            redirect(thread_url($t) . 'edit/');
        }
        $row = ['title' => $title, 'body' => $body, 'body_html' => md($body), 'link_url' => $link ?: null, 'edited_at' => now()];
        if ($title !== $t['title']) {
            $row['slug'] = slugify($title);
        }
        if (input('remove_image') === '1') {
            $row['image'] = null;
        }
        update('threads', $row, 'id = :id', ['id' => $t['id']]);
        flash('ok', 'Post updated.');
        redirect(thread_url(find_thread((int)$t['id'])));
    }
    render('submit', ['communities' => communities(), 'selected' => $t['community_slug'], 'thread' => $t], [
        'title' => 'Edit post', 'robots' => 'noindex',
    ]);
}

function thread_delete(string $id): void
{
    $u = require_login();
    $t = find_thread((int)$id) ?? not_found();
    if ((int)$t['user_id'] !== (int)$u['id']) {
        forbidden();
    }
    update('threads', ['deleted' => 1, 'body' => '', 'body_html' => '', 'link_url' => null, 'image' => null, 'edited_at' => now()], 'id = :id', ['id' => $t['id']]);
    flash('ok', 'Your post was deleted.');
    redirect(community_url($t['community_slug']));
}

function thread_mod(string $id): void
{
    $u = require_mod();
    $t = find_thread((int)$id) ?? not_found();
    $action = input('action');
    $map = ['pin' => ['pinned' => 1], 'unpin' => ['pinned' => 0], 'lock' => ['locked' => 1], 'unlock' => ['locked' => 0],
        'remove' => ['removed' => 1], 'restore' => ['removed' => 0]];
    if (!isset($map[$action])) {
        back();
    }
    update('threads', $map[$action], 'id = :id', ['id' => $t['id']]);
    if ($action === 'remove' || $action === 'restore') {
        q('UPDATE reports SET resolved_by = ?, resolved_at = ? WHERE target_type = ? AND target_id = ? AND resolved_at IS NULL', [$u['id'], now(), 'thread', $t['id']]);
    }
    flash('ok', 'Post ' . ($action === 'remove' ? 'removed' : $action . 'ed') . '.');
    back(thread_url($t));
}

/* ---------- comments ---------- */

function comment_target(string $type, int $id): ?array
{
    if ($type === 'thread') {
        $t = find_thread($id);
        return $t ? ['row' => $t, 'url' => thread_url($t), 'locked' => (int)$t['locked'] || (int)$t['removed'] || (int)$t['deleted']] : null;
    }
    if ($type === 'article') {
        $a = one("SELECT * FROM articles WHERE id = ? AND status = 'published'", [$id]);
        return $a ? ['row' => $a, 'url' => article_url($a), 'locked' => false] : null;
    }
    return null;
}

function comment_create(): void
{
    $u = current_user();   // guests may comment with a name + email
    $type = input('target_type');
    $target = comment_target($type, (int)input('target_id')) ?? not_found();
    $body = rtrim(input('body'));
    $parentId = (int)input('parent_id') ?: null;
    $back = $target['url'];
    $err = null;
    if ($target['locked'] && !($u && is_mod($u))) $err = 'This conversation is locked.';
    elseif (mb_strlen(trim($body)) < 2) $err = 'Write a comment first.';
    elseif (mb_strlen($body) > 10000) $err = 'Comments can be up to 10,000 characters.';
    $depth = 0;
    if (!$err && $parentId) {
        $parent = one('SELECT * FROM comments WHERE id = ? AND target_type = ? AND target_id = ?', [$parentId, $type, $target['row']['id']]);
        if (!$parent) {
            $err = 'The comment you replied to is gone.';
        } else {
            $depth = min((int)$parent['depth'] + 1, 12);
        }
    }
    $guestName = $guestEmail = null;
    if (!$err && !$u) {
        [$guestName, $guestEmail, $err] = guest_from_post('comment');
        if (!$err && md_link_count($body) > 1) {
            $err = 'Comments without an account can include one link. Create a free account to share more.';
        }
    }
    if (!$err && $u) {
        $err = posting_blocked($u, $body, 'comment');
    }
    if ($err) {
        if (wants_json()) json_out(['error' => $err], 422);
        remember_input(['body', 'guest_name', 'guest_email']);
        flash('error', $err);
        redirect($back . ($parentId ? '?reply=' . $parentId . '#c' . $parentId : '#comment-form'));
    }
    $live = $u || guest_is_trusted($guestEmail);
    $cid = insert('comments', [
        'target_type' => $type, 'target_id' => $target['row']['id'], 'parent_id' => $parentId, 'user_id' => $u['id'] ?? null,
        'guest_name' => $guestName, 'guest_email' => $guestEmail, 'status' => $live ? 'live' : 'pending',
        'body' => $body, 'body_html' => md($body, false), 'depth' => $depth, 'score' => 1, 'upvotes' => 1, 'created_at' => now(),
    ]);
    if ($u) {
        insert('votes', ['user_id' => $u['id'], 'target_type' => 'comment', 'target_id' => $cid, 'value' => 1, 'created_at' => now()]);
    } else {
        guest_remember($guestName, $guestEmail);
    }
    if (!$live) {
        guest_send_confirmation('comment', $cid, $guestName, $guestEmail, excerpt($body, 120));
        guest_gc();
        redirect('/confirm/sent/?e=' . rawurlencode(guest_mask($guestEmail)) . '&back=' . rawurlencode($back));
    }
    comment_published($type, (int)$target['row']['id']);
    redirect($back . '#c' . $cid);
}

function comment_published(string $type, int $targetId): void
{
    refresh_comment_count($type, $targetId);
    if ($type === 'thread') {
        q('UPDATE threads SET last_activity_at = ? WHERE id = ?', [now(), $targetId]);
    }
}

/** /confirm/?id=&t= : publish a pending guest contribution and trust this browser. */
function guest_confirm(): void
{
    $row = one('SELECT * FROM guest_tokens WHERE id = ?', [(int)input('id')]);
    if (!$row || !hash_equals($row['token_hash'], hash('sha256', input('t'))) || strtotime($row['created_at'] . ' UTC') < time() - 86400 * 7) {
        render('error', ['code' => 400, 'heading' => 'That link has expired',
            'message' => 'Confirmation links work for 7 days. Please post again and use the new link we email you.'],
            ['title' => 'Link expired', 'robots' => 'noindex'], 400);
    }
    $table = $row['target_type'] === 'thread' ? 'threads' : 'comments';
    $item = one("SELECT * FROM $table WHERE id = ?", [$row['target_id']]);
    if (!$item) {
        not_found('That post no longer exists.');
    }
    $email = strtolower($row['email']);
    if (one('SELECT email FROM guests WHERE email = ?', [$email])) {
        q('UPDATE guests SET verified_at = COALESCE(verified_at, ?), name = ? WHERE email = ?', [now(), $item['guest_name'], $email]);
    } else {
        insert('guests', ['email' => $email, 'name' => (string)$item['guest_name'], 'verified_at' => now(), 'banned' => 0, 'created_at' => now()]);
    }
    if ((int)one('SELECT banned FROM guests WHERE email = ?', [$email])['banned'] === 1) {
        forbidden('This email address cannot post here.');
    }
    // publish every pending contribution from this address, not just the one clicked
    $now = now();
    foreach (all("SELECT id FROM threads WHERE guest_email = ? AND status = 'pending'", [$email]) as $t) {
        q("UPDATE threads SET status = 'live', created_at = ?, last_activity_at = ?, hot = ? WHERE id = ?", [$now, $now, hot_score(1, $now), $t['id']]);
    }
    foreach (all("SELECT * FROM comments WHERE guest_email = ? AND status = 'pending'", [$email]) as $c) {
        q("UPDATE comments SET status = 'live' WHERE id = ?", [$c['id']]);
        comment_published($c['target_type'], (int)$c['target_id']);
    }
    q('UPDATE guest_tokens SET used_at = ? WHERE id = ?', [$now, $row['id']]);
    guest_cookie_set((string)$item['guest_name'], $email, true);
    flash('ok', 'Thanks, ' . $item['guest_name'] . '! You are confirmed and your post is live. Next time it publishes instantly.');
    if ($row['target_type'] === 'thread') {
        redirect(thread_url(find_thread((int)$item['id'])));
    }
    $t = comment_target($item['target_type'], (int)$item['target_id']);
    redirect(($t ? $t['url'] : '/') . '#c' . $item['id']);
}

function guest_confirm_sent(): void
{
    render('confirm_sent', ['email' => mb_substr(input('e'), 0, 200), 'back' => safe_next(input('back'), '/forum/')],
        ['title' => 'Check your email', 'robots' => 'noindex']);
}

function comment_edit(string $id): void
{
    $u = require_login();
    $c = one('SELECT * FROM comments WHERE id = ?', [(int)$id]) ?? not_found();
    $target = comment_target($c['target_type'], (int)$c['target_id']) ?? not_found();
    if ((int)$c['user_id'] !== (int)$u['id'] || $c['deleted'] || $c['removed']) {
        forbidden();
    }
    $body = rtrim(input('body'));
    if (mb_strlen(trim($body)) < 2 || mb_strlen($body) > 10000) {
        flash('error', 'Comments must be 2 to 10,000 characters.');
        redirect($target['url'] . '#c' . $c['id']);
    }
    update('comments', ['body' => $body, 'body_html' => md($body, false), 'edited_at' => now()], 'id = :id', ['id' => $c['id']]);
    redirect($target['url'] . '#c' . $c['id']);
}

function comment_delete(string $id): void
{
    $u = require_login();
    $c = one('SELECT * FROM comments WHERE id = ?', [(int)$id]) ?? not_found();
    $target = comment_target($c['target_type'], (int)$c['target_id']) ?? not_found();
    if ((int)$c['user_id'] !== (int)$u['id']) {
        forbidden();
    }
    update('comments', ['deleted' => 1, 'body' => '', 'body_html' => '', 'edited_at' => now()], 'id = :id', ['id' => $c['id']]);
    refresh_comment_count($c['target_type'], (int)$c['target_id']);
    flash('ok', 'Comment deleted.');
    redirect($target['url'] . '#comments');
}

function comment_mod(string $id): void
{
    $u = require_mod();
    $c = one('SELECT * FROM comments WHERE id = ?', [(int)$id]) ?? not_found();
    $target = comment_target($c['target_type'], (int)$c['target_id']);
    $action = input('action');
    if (!in_array($action, ['remove', 'restore'], true)) {
        back();
    }
    update('comments', ['removed' => $action === 'remove' ? 1 : 0], 'id = :id', ['id' => $c['id']]);
    q('UPDATE reports SET resolved_by = ?, resolved_at = ? WHERE target_type = ? AND target_id = ? AND resolved_at IS NULL', [$u['id'], now(), 'comment', $c['id']]);
    refresh_comment_count($c['target_type'], (int)$c['target_id']);
    flash('ok', 'Comment ' . ($action === 'remove' ? 'removed' : 'restored') . '.');
    back($target ? $target['url'] : '/');
}

/* ---------- votes & reports ---------- */

function vote_action(): void
{
    $u = require_login();
    $type = input('type');
    $id = (int)input('id');
    $value = (int)input('value');
    if (!isset(M1S_VOTE_TYPES[$type]) || !in_array($value, [-1, 0, 1], true)) {
        wants_json() ? json_out(['error' => 'Bad request'], 400) : back();
    }
    if ((int)$u['banned']) {
        forbidden();
    }
    if (!throttle('vote', 400, 3600, 'u' . $u['id'])) {
        wants_json() ? json_out(['error' => 'Slow down a little.'], 429) : back();
    }
    try {
        $r = cast_vote((int)$u['id'], $type, $id, $value);
    } catch (RuntimeException $e) {
        wants_json() ? json_out(['error' => 'Not found'], 404) : back();
    }
    wants_json() ? json_out($r) : back();
}

function report_action(): void
{
    $u = require_login();
    $type = input('type');
    $id = (int)input('id');
    if (!in_array($type, ['thread', 'comment'], true)) {
        not_found();
    }
    $row = one('SELECT * FROM ' . M1S_VOTE_TYPES[$type] . ' WHERE id = ?', [$id]) ?? not_found();
    if (is_post()) {
        $reason = input('reason');
        $detail = mb_substr(input('detail'), 0, 400);
        $reasons = ['Spam or advertising', 'Harassment or hate', 'Personal information', 'Misinformation that could cause harm', 'Off-topic', 'Something else'];
        if (!in_array($reason, $reasons, true)) {
            flash('error', 'Pick a reason.');
            redirect('/report/?type=' . $type . '&id=' . $id);
        }
        if (throttle('report', 20, 3600, 'u' . $u['id']) && !one('SELECT id FROM reports WHERE user_id = ? AND target_type = ? AND target_id = ?', [$u['id'], $type, $id])) {
            insert('reports', ['user_id' => $u['id'], 'target_type' => $type, 'target_id' => $id,
                'reason' => $reason . ($detail !== '' ? ': ' . $detail : ''), 'created_at' => now()]);
        }
        flash('ok', 'Thanks. A moderator will review it.');
        $t = comment_target($type === 'thread' ? 'thread' : $row['target_type'], $type === 'thread' ? $id : (int)$row['target_id']);
        redirect($t ? $t['url'] : '/');
    }
    render('report', ['type' => $type, 'id' => $id, 'row' => $row], ['title' => 'Report', 'robots' => 'noindex']);
}
