<?php
declare(strict_types=1);
defined('M1S') || exit;

const M1S_TAGLINE = 'Real-life secrets for renters, homeowners and Texans';
const M1S_DEFAULT_DESC = 'A blog and forum for renters, homeowners and Texans: apartment living tips, small-space ideas, insurance claim help and advice from real people.';

function org_schema(): array
{
    return [
        '@type' => 'Organization',
        '@id'   => abs_url('/#organization'),
        'name'  => cfg('site_name'),
        'url'   => abs_url('/'),
        'logo'  => ['@type' => 'ImageObject', 'url' => abs_url('/assets/img/my1secret-icon-512.png'), 'width' => 512, 'height' => 512],
    ];
}

function website_schema(): array
{
    return [
        '@type' => 'WebSite',
        '@id'   => abs_url('/#website'),
        'name'  => cfg('site_name'),
        'url'   => abs_url('/'),
        'description' => M1S_DEFAULT_DESC,
        'publisher' => ['@id' => abs_url('/#organization')],
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => ['@type' => 'EntryPoint', 'urlTemplate' => abs_url('/search/?q={search_term_string}')],
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

/** $crumbs = [[name, path], ...] (home is added automatically) */
function breadcrumb_schema(array $crumbs): array
{
    $items = [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => abs_url('/')]];
    foreach ($crumbs as $i => [$name, $path]) {
        $item = ['@type' => 'ListItem', 'position' => $i + 2, 'name' => $name];
        if ($path) {
            $item['item'] = abs_url($path);
        }
        $items[] = $item;
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function person_schema(?string $username, ?string $displayName = null): array
{
    if (!$username) {
        return ['@type' => 'Person', 'name' => '[deleted]'];
    }
    return ['@type' => 'Person', 'name' => $displayName ?: $username, 'url' => abs_url(user_url($username))];
}

function interaction_stats(int $likes, int $comments): array
{
    return [
        ['@type' => 'InteractionCounter', 'interactionType' => 'https://schema.org/LikeAction', 'userInteractionCount' => max(0, $likes)],
        ['@type' => 'InteractionCounter', 'interactionType' => 'https://schema.org/CommentAction', 'userInteractionCount' => $comments],
    ];
}

/** Nested Comment items for DiscussionForumPosting / BlogPosting (capped for page weight). */
function comments_schema(array $tree, int &$budget = 30): array
{
    $out = [];
    foreach ($tree as $c) {
        if ($budget-- <= 0) {
            break;
        }
        if ($c['removed'] || $c['deleted']) {
            continue;
        }
        $item = [
            '@type' => 'Comment',
            'url' => abs_url($c['_url']),
            'text' => excerpt(md_plain($c['body']), 500),
            'datePublished' => iso_date($c['created_at']),
            'author' => $c['username'] ? person_schema($c['username'], $c['display_name'] ?? null) : ['@type' => 'Person', 'name' => $c['guest_name'] ?: '[deleted]'],
            'interactionStatistic' => ['@type' => 'InteractionCounter', 'interactionType' => 'https://schema.org/LikeAction', 'userInteractionCount' => max(0, (int)$c['upvotes'])],
        ];
        if (!empty($c['children'])) {
            $kids = comments_schema($c['children'], $budget);
            if ($kids) {
                $item['comment'] = $kids;
            }
        }
        $out[] = $item;
    }
    return $out;
}

function jsonld_tag(array $nodes): string
{
    $doc = ['@context' => 'https://schema.org', '@graph' => array_values($nodes)];
    $json = json_encode($doc, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP);
    return '<script type="application/ld+json">' . $json . '</script>';
}

/** Title for <title>: adds " | My 1 Secret" only when the result stays within ~60 characters (Google truncates past ~580px). */
function full_title(?string $title): string
{
    $brand = cfg('site_name');
    if (!$title) {
        return $brand . ': Tips for Renters, Homeowners & Texans';
    }
    $withBrand = $title . ' | ' . $brand;
    if (mb_strlen($withBrand) > 60 || str_contains($title, $brand)) {
        return $title;
    }
    return $withBrand;
}

/** Canonical for the current request: path only, plus ?page=N when N > 1. */
function current_canonical(): string
{
    $path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
    $p = page_num();
    return abs_url($path) . ($p > 1 ? '?page=' . $p : '');
}
