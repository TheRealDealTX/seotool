<?php
defined('M1S') || exit;

/** Up/down vote widget. $type: thread|comment|article */
function vote_box(string $type, int $id, int $score, int $myVote, bool $upOnly = false, string $class = ''): string
{
    $login = !current_user();
    $h = '<div class="vote ' . e($class) . '" data-vote data-type="' . e($type) . '" data-id="' . $id . '" data-my="' . $myVote . '">';
    $btn = function (int $val, string $label, string $icon) use ($type, $id, $myVote, $login) {
        $on = $myVote === $val;
        if ($login) {
            return '<a class="vote-btn ' . ($val > 0 ? 'up' : 'down') . '" href="/login/?next=' . e(rawurlencode($_SERVER['REQUEST_URI'] ?? '/')) . '" aria-label="' . e($label) . ' (log in)" rel="nofollow">' . $icon . '</a>';
        }
        return '<form method="post" action="/vote/">' . csrf_field()
            . '<input type="hidden" name="type" value="' . e($type) . '"><input type="hidden" name="id" value="' . $id . '">'
            . '<input type="hidden" name="value" value="' . ($on ? 0 : $val) . '">'
            . '<button type="submit" class="vote-btn ' . ($val > 0 ? 'up' : 'down') . ($on ? ' on' : '') . '" aria-pressed="' . ($on ? 'true' : 'false') . '" aria-label="' . e($label) . '" data-val="' . $val . '">' . $icon . '</button></form>';
    };
    $h .= $btn(1, $type === 'article' ? 'Helpful' : 'Upvote', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3l7 8h-4.5v6h-5v-6H3z"/></svg>');
    $h .= '<span class="vote-score" aria-label="Score">' . number_format($score) . '</span>';
    if (!$upOnly) {
        $h .= $btn(-1, 'Downvote', '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 17l-7-8h4.5V3h5v6H17z"/></svg>');
    }
    return $h . '</div>';
}

function community_chip(array $row): string
{
    $slug = $row['community_slug'] ?? $row['slug'];
    $name = $row['community_name'] ?? $row['name'];
    $color = $row['community_color'] ?? $row['color'] ?? '#1f8fcf';
    return '<a class="chip" style="--c:' . e($color) . '" href="' . e(community_url($slug)) . '">' . e($name) . '</a>';
}

/** One row in a thread feed. */
function thread_row(array $t, int $myVote, bool $showCommunity = true): string
{
    $url = thread_url($t);
    $h = '<article class="thread-row' . ($t['pinned'] ? ' pinned' : '') . '">';
    $h .= vote_box('thread', (int)$t['id'], (int)$t['score'], $myVote);
    $h .= '<div class="thread-main">';
    $h .= '<div class="meta">';
    if ($showCommunity) {
        $h .= community_chip($t) . ' · ';
    }
    $h .= ($t['deleted'] ? '<span class="muted">[deleted]</span>' : user_label($t)) . ' · <time datetime="' . e(iso_date($t['created_at'])) . '">' . e(time_ago($t['created_at'])) . '</time>';
    if ($t['pinned']) $h .= ' <span class="badge badge-pin">pinned</span>';
    if ($t['locked']) $h .= ' <span class="badge">locked</span>';
    if ($t['removed']) $h .= ' <span class="badge badge-danger">removed</span>';
    $h .= '</div>';
    $h .= '<h3 class="thread-title"><a href="' . e($url) . '">' . e($t['title']) . '</a></h3>';
    if ($t['link_url']) {
        $host = parse_url($t['link_url'], PHP_URL_HOST);
        $h .= '<a class="link-host" href="' . e($t['link_url']) . '" rel="nofollow ugc noopener" target="_blank">' . e(preg_replace('/^www\./', '', (string)$host)) . ' ↗</a>';
    }
    if (!$t['deleted'] && trim((string)$t['body']) !== '') {
        $h .= '<p class="thread-snippet">' . e(excerpt(md_plain((string)$t['body']), 180)) . '</p>';
    }
    $h .= '<div class="thread-actions"><a href="' . e($url) . '#comments">💬 ' . plural((int)$t['comment_count'], 'comment') . '</a></div>';
    $h .= '</div>';
    if ($t['image']) {
        $h .= '<a class="thread-thumb" href="' . e($url) . '" tabindex="-1" aria-hidden="true"><img src="' . e($t['image']) . '" alt="" loading="lazy" width="96" height="72"></a>';
    }
    return $h . '</article>';
}

function article_card(array $a, string $size = 'md'): string
{
    $url = article_url($a);
    $h = '<article class="card article-card card-' . e($size) . '">';
    if ($a['image']) {
        $h .= '<a class="card-img" href="' . e($url) . '" tabindex="-1" aria-hidden="true"><img src="' . e($a['image']) . '" alt="" loading="' . ($size === 'lg' ? 'eager' : 'lazy') . '" width="' . (int)$a['image_w'] . '" height="' . (int)$a['image_h'] . '"></a>';
    } else {
        $h .= '<a class="card-img card-img-empty" href="' . e($url) . '" tabindex="-1" aria-hidden="true"><span>' . e(mb_substr($a['topic_name'] ?? 'M', 0, 1)) . '</span></a>';
    }
    $h .= '<div class="card-body">';
    if (!empty($a['topic_slug'])) {
        $h .= '<a class="eyebrow" href="' . e(topic_url($a['topic_slug'])) . '">' . e($a['topic_name']) . '</a>';
    }
    $tag = $size === 'lg' ? 'h2' : 'h3';
    $h .= "<$tag class=\"card-title\"><a href=\"" . e($url) . '">' . e($a['title']) . "</a></$tag>";
    if ($size !== 'sm') {
        $h .= '<p>' . e(excerpt($a['meta_description'] ?: $a['excerpt'], $size === 'lg' ? 220 : 130)) . '</p>';
    }
    $h .= '<div class="meta"><time datetime="' . e(iso_date($a['published_at'])) . '">' . e(nice_date($a['published_at'])) . '</time> · ' . (int)$a['reading_minutes'] . ' min read'
        . ((int)$a['comment_count'] ? ' · ' . plural((int)$a['comment_count'], 'comment') : '') . '</div>';
    return $h . '</div></article>';
}

/** Comment form (top-level or reply). Members post directly; guests add a name + email. */
function comment_form(string $type, int $targetId, ?int $parentId = null, bool $locked = false): string
{
    if ($locked) {
        return '<p class="notice">This conversation is locked. New comments are turned off.</p>';
    }
    $guest = !current_user();
    $id = $parentId ? 'reply-' . $parentId : 'comment-form';
    $h = '<form class="comment-form" id="' . $id . '" method="post" action="/comment/">' . member_csrf_field()
        . '<input type="hidden" name="target_type" value="' . e($type) . '"><input type="hidden" name="target_id" value="' . $targetId . '">';
    if ($parentId) {
        $h .= '<input type="hidden" name="parent_id" value="' . $parentId . '">';
    }
    $h .= '<label class="sr-only" for="body-' . $id . '">' . ($parentId ? 'Your reply' : 'Your comment') . '</label>'
        . '<textarea id="body-' . $id . '" name="body" rows="' . ($parentId ? 3 : 4) . '" maxlength="10000" required placeholder="' . ($parentId ? 'Write a reply…' : 'What are your thoughts?') . '">' . e($parentId ? '' : old('body')) . '</textarea>';
    if ($guest) {
        $h .= guest_fields((bool)$parentId);
    }
    $h .= '<div class="form-row"><span class="hint">Markdown: **bold**, *italic*, [link](https://…), - lists, &gt; quotes</span>'
        . ($parentId ? '<button type="button" class="btn btn-ghost btn-sm" data-cancel-reply>Cancel</button>' : '')
        . '<button class="btn btn-accent btn-sm" type="submit">' . ($parentId ? 'Reply' : 'Comment') . '</button></div></form>';
    return $h;
}

/** Recursive comment tree. */
function comment_tree_html(array $tree, array $votes, string $type, int $targetId, bool $locked, int $replyTo = 0): string
{
    $me = current_user();
    $h = '<ol class="comments">';
    foreach ($tree as $c) {
        $id = (int)$c['id'];
        $dead = $c['removed'] || $c['deleted'];
        $h .= '<li class="comment" id="c' . $id . '"><div class="comment-inner">';
        $h .= '<div class="comment-head">'
            . ($dead ? '<span class="muted">[' . ($c['removed'] ? 'removed' : 'deleted') . ']</span>' : user_label($c))
            . ' · <a class="muted" href="#c' . $id . '"><time datetime="' . e(iso_date($c['created_at'])) . '">' . e(time_ago($c['created_at'])) . '</time></a>'
            . ($c['edited_at'] && !$dead ? ' <span class="muted" title="Edited ' . e(nice_date($c['edited_at'])) . '">· edited</span>' : '')
            . ' <button type="button" class="collapse" data-collapse aria-expanded="true" aria-label="Collapse thread">[–]</button></div>';
        $h .= '<div class="comment-body prose-sm">' . ($dead ? '<p class="muted">' . ($c['removed'] ? 'Removed by a moderator.' : 'This comment was deleted.') . '</p>' : $c['body_html']) . '</div>';
        if (!$dead) {
            $h .= '<div class="comment-actions">' . vote_box('comment', $id, (int)$c['score'], $votes[$id] ?? 0, false, 'vote-inline');
            if (!$locked) {
                $h .= '<a href="?reply=' . $id . '#c' . $id . '" class="action" data-reply="' . $id . '" rel="nofollow">Reply</a>';
            }
            if ($me) {
                if ((int)$c['user_id'] === (int)$me['id']) {
                    $h .= '<details class="inline-edit"><summary class="action">Edit</summary><form method="post" action="/comment/' . $id . '/edit/">' . csrf_field()
                        . '<textarea name="body" rows="3" maxlength="10000" aria-label="Edit comment">' . e($c['body']) . '</textarea><button class="btn btn-sm btn-accent">Save</button></form></details>'
                        . '<form method="post" action="/comment/' . $id . '/delete/" data-confirm="Delete this comment?">' . csrf_field() . '<button class="action linklike">Delete</button></form>';
                } else {
                    $h .= '<a class="action" href="/report/?type=comment&amp;id=' . $id . '" rel="nofollow">Report</a>';
                }
                if (is_mod($me)) {
                    $h .= '<form method="post" action="/comment/' . $id . '/mod/">' . csrf_field() . '<input type="hidden" name="action" value="remove"><button class="action linklike danger">Remove</button></form>';
                }
            }
            $h .= '</div>';
            if (!$locked) {
                $h .= '<div class="reply-slot" data-reply-slot="' . $id . '"' . ($replyTo === $id ? '' : ' hidden') . '>' . comment_form($type, $targetId, $id) . '</div>';
            }
        } elseif ($me && is_mod($me) && $c['removed']) {
            $h .= '<div class="comment-actions"><form method="post" action="/comment/' . $id . '/mod/">' . csrf_field() . '<input type="hidden" name="action" value="restore"><button class="action linklike">Restore</button></form></div>';
        }
        $h .= '</div>';
        if ($c['children']) {
            $h .= comment_tree_html($c['children'], $votes, $type, $targetId, $locked, $replyTo);
        }
        $h .= '</li>';
    }
    return $h . '</ol>';
}

function comment_section(array $tree, array $votes, string $type, int $targetId, int $count, bool $locked, string $sort): string
{
    $replyTo = (int)($_GET['reply'] ?? 0);
    $h = '<section class="comments-section" id="comments" aria-labelledby="comments-h">';
    $h .= '<div class="section-head"><h2 id="comments-h">' . plural($count, 'comment') . '</h2>';
    if ($count > 1) {
        $h .= '<nav class="sort-tabs small" aria-label="Sort comments">';
        foreach (['best' => 'Best', 'new' => 'Newest', 'old' => 'Oldest'] as $k => $label) {
            $h .= '<a rel="nofollow" href="' . ($k === 'best' ? '?' : '?sort=' . $k) . '#comments"' . ($sort === $k ? ' aria-current="true"' : '') . '>' . $label . '</a>';
        }
        $h .= '</nav>';
    }
    $h .= '</div>';
    $h .= comment_form($type, $targetId, null, $locked);
    if ($tree) {
        $h .= comment_tree_html($tree, $votes, $type, $targetId, $locked, $replyTo);
    } elseif (!$locked) {
        $h .= '<p class="empty">No comments yet. Be the first to share your take.</p>';
    }
    return $h . '</section>';
}

function sort_tabs(string $base, string $sort, string $t): string
{
    $h = '<nav class="sort-tabs" aria-label="Sort posts">';
    foreach (SORTS as $k => $label) {
        $href = $k === 'hot' ? $base : $base . '?sort=' . $k;
        $h .= '<a href="' . e($href) . '"' . ($sort === $k ? ' aria-current="true"' : '') . ($k !== 'hot' ? ' rel="nofollow"' : '') . '>' . $label . '</a>';
    }
    if ($sort === 'top') {
        $h .= '<span class="period">';
        foreach (PERIODS as $k => $label) {
            $h .= '<a rel="nofollow" href="' . e($base . '?sort=top&t=' . $k) . '"' . ($t === $k ? ' aria-current="true"' : '') . '>' . $label . '</a>';
        }
        $h .= '</span>';
    }
    return $h . '</nav>';
}

function communities_widget(?string $active = null, array $counts = []): string
{
    $h = '<section class="widget"><h2>Communities</h2><ul class="community-list">';
    foreach (communities() as $c) {
        $h .= '<li><a href="' . e(community_url($c)) . '"' . ($active === $c['slug'] ? ' aria-current="page"' : '') . '><span class="cdot" style="--c:' . e($c['color']) . '"></span>' . e($c['name'])
            . (isset($counts[(int)$c['id']]) ? ' <span class="muted">' . number_format($counts[(int)$c['id']]) . '</span>' : '') . '</a></li>';
    }
    return $h . '</ul><a class="btn btn-accent btn-block" href="/submit/' . ($active ? '?c=' . e($active) : '') . '">Create a post</a></section>';
}

function topics_widget(?string $active = null): string
{
    $h = '<section class="widget"><h2>Blog topics</h2><ul class="topic-list">';
    foreach (topics() as $t) {
        $h .= '<li><a href="' . e(topic_url($t)) . '"' . ($active === $t['slug'] ? ' aria-current="page"' : '') . '>' . e($t['name']) . ' <span class="muted">' . (int)$t['article_count'] . '</span></a></li>';
    }
    return $h . '</ul></section>';
}
