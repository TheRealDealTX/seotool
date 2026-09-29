<?php
declare(strict_types=1);

namespace RT;

/**
 * Small HTML fragments shared by public templates. All dynamic values are
 * escaped with e().
 */
final class View
{
    public static function statusBadge(array $e): string
    {
        $s = Dates::status($e);
        return '<span class="badge badge--' . e($s['key']) . '">' . e($s['label']) . '</span>';
    }

    public static function dateBlock(array $e): string
    {
        $s = new \DateTimeImmutable($e['start_date']);
        $multi = $e['start_date'] !== $e['end_date'];
        return '<div class="date-block" aria-hidden="true"><span class="date-block__m">' . e($s->format('M')) . '</span>'
            . '<span class="date-block__d">' . e($s->format('j')) . ($multi ? '<small>+</small>' : '') . '</span>'
            . '<span class="date-block__y">' . e($s->format('Y')) . '</span></div>';
    }

    public static function place(array $e): string
    {
        $parts = array_filter([$e['venue_name'] ?? null, ($e['city'] ?? null) ? $e['city'] . ', TX' : null]);
        return $parts ? implode(' · ', $parts) : 'Location not listed';
    }

    public static function eventCard(array $e, bool $compact = false): string
    {
        $url = '/rodeos/' . rawurlencode($e['slug']) . '/';
        $time = '';
        if (!empty($e['first_perf'])) {
            $time = ' · starts ' . Dates::time($e['first_perf'], $e['timezone']) . ((int) $e['perf_count'] > 1 ? ' +' . ((int) $e['perf_count'] - 1) . ' more' : '');
        }
        $tags = '';
        if (!empty($e['assoc_abbr'])) {
            $tags .= '<span class="tag tag--assoc" title="' . e($e['assoc_name']) . '">' . e($e['assoc_abbr']) . '</span>';
        }
        if (!empty($e['type_name'])) {
            $tags .= '<span class="tag">' . e($e['type_name']) . '</span>';
        }
        if (!empty($e['level'])) {
            $tags .= '<span class="tag tag--level">' . e(level_label($e['level'])) . '</span>';
        }
        if (!empty($e['region_name']) && !$compact) {
            $tags .= '<span class="tag tag--region">' . e($e['region_name']) . '</span>';
        }
        $fav = '<button type="button" class="fav-btn" data-fav="' . e($e['slug']) . '" data-title="' . e($e['title']) . '" data-date="' . e($e['start_date']) . '" aria-pressed="false" aria-label="Save ' . e($e['title']) . ' to favorites"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg></button>';
        return '<article class="event-card' . ($compact ? ' event-card--compact' : '') . '">'
            . self::dateBlock($e)
            . '<div class="event-card__body">'
            . '<h3 class="event-card__title"><a href="' . e($url) . '">' . e($e['title']) . '</a></h3>'
            . '<p class="event-card__meta"><time datetime="' . e($e['start_date']) . '">' . e(Dates::range($e['start_date'], $e['end_date'])) . '</time>' . e($time) . '</p>'
            . '<p class="event-card__place">' . e(self::place($e)) . '</p>'
            . '<div class="event-card__tags">' . self::statusBadge($e) . $tags . '</div>'
            . '</div>' . $fav . '</article>';
    }

    public static function pagination(int $page, int $pages, array $filters, string $base): string
    {
        if ($pages <= 1) {
            return '';
        }
        $link = static function (int $p) use ($filters, $base): string {
            $q = array_filter(array_merge(self::filterQuery($filters), ['page' => $p > 1 ? $p : null]), static fn($v) => $v !== null && $v !== '');
            return $base . ($q ? '?' . http_build_query($q) : '');
        };
        $h = '<nav class="pager" aria-label="Pages">';
        if ($page > 1) {
            $h .= '<a rel="prev" href="' . e($link($page - 1)) . '">‹ Previous</a>';
        }
        $h .= '<span class="pager__info">Page ' . $page . ' of ' . $pages . '</span>';
        if ($page < $pages) {
            $h .= '<a rel="next" href="' . e($link($page + 1)) . '">Next ›</a>';
        }
        return $h . '</nav>';
    }

    /** Filter array → query params (drops defaults). */
    public static function filterQuery(array $f): array
    {
        $q = [];
        foreach (['q', 'region', 'association', 'type', 'level', 'when'] as $k) {
            if (!empty($f[$k])) {
                $q[$k] = $f[$k];
            }
        }
        if (empty($f['when'])) {
            foreach (['from', 'to'] as $k) {
                if (!empty($f[$k])) {
                    $q[$k] = $f[$k];
                }
            }
        }
        if (($f['view'] ?? 'list') !== 'list') {
            $q['view'] = $f['view'];
        }
        return $q;
    }

    public static function mapsLink(array $e): ?string
    {
        if (!$e['city']) {
            return null;
        }
        $dest = implode(', ', array_filter([$e['venue_name'], $e['venue_address'], $e['city'] . ', TX', $e['postal_code']]));
        return 'https://www.google.com/maps/dir/?api=1&destination=' . rawurlencode($dest);
    }
}
