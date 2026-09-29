<?php
declare(strict_types=1);

namespace RT;

/**
 * schema.org structured data. Only facts we actually have are emitted —
 * missing values are omitted, never filled with placeholders.
 */
final class Seo
{
    public static function website(): array
    {
        return [
            '@context' => 'https://schema.org',
            '@type' => 'WebSite',
            'name' => cfg('site_name', 'Rodeo Texas'),
            'url' => abs_url('/'),
            'potentialAction' => [
                '@type' => 'SearchAction',
                'target' => abs_url('/rodeos/') . '?q={search_term_string}',
                'query-input' => 'required name=search_term_string',
            ],
        ];
    }

    public static function breadcrumbs(array $items): array
    {
        $list = [];
        foreach (array_values($items) as $i => [$name, $url]) {
            $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($url)];
        }
        return ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $list];
    }

    /** Event markup. Returns null when essential facts (a Texas place) are missing. */
    public static function event(array $e, array $perfs): ?array
    {
        if (!$e['city'] || $e['is_legacy']) {
            return null;
        }
        $tz = $e['timezone'];
        $start = $e['start_date'];
        $end = $e['end_date'];
        if ($perfs) {
            $start = Dates::iso($perfs[0]['starts_at'], $tz);
            $lastPerf = end($perfs);
            $end = $lastPerf['ends_at'] ? Dates::iso($lastPerf['ends_at'], $tz) : $e['end_date'];
            if (count($perfs) === 1 && !$lastPerf['ends_at']) {
                $end = null;
            }
        }
        $address = array_filter([
            '@type' => 'PostalAddress',
            'streetAddress' => $e['venue_address'],
            'addressLocality' => $e['city'],
            'addressRegion' => 'TX',
            'postalCode' => $e['postal_code'],
            'addressCountry' => 'US',
        ]);
        $place = array_filter([
            '@type' => 'Place',
            'name' => $e['venue_name'] ?: $e['city'] . ', Texas',
            'address' => $address,
            'geo' => ($e['lat'] !== null && $e['location_precision'] === 'address')
                ? ['@type' => 'GeoCoordinates', 'latitude' => (float) $e['lat'], 'longitude' => (float) $e['lng']] : null,
        ]);
        $statusMap = ['canceled' => 'EventCancelled', 'postponed' => 'EventPostponed'];
        $data = [
            '@context' => 'https://schema.org',
            '@type' => 'Event',
            'name' => $e['title'],
            'startDate' => $start,
            'endDate' => $end,
            'eventStatus' => 'https://schema.org/' . ($statusMap[$e['status']] ?? 'EventScheduled'),
            'eventAttendanceMode' => 'https://schema.org/OfflineEventAttendanceMode',
            'location' => $place,
            'description' => $e['description'] ? excerpt($e['description'], 300) : null,
            'url' => abs_url('/rodeos/' . $e['slug'] . '/'),
            'image' => $e['image_url'] ?: null,
            'organizer' => $e['org_name'] ? array_filter(['@type' => 'Organization', 'name' => $e['org_name'], 'url' => $e['org_website']]) : null,
            'offers' => $e['ticket_url'] ? array_filter(['@type' => 'Offer', 'url' => $e['ticket_url']]) : null,
            'sameAs' => $e['official_url'] ?: null,
        ];
        return array_filter($data, static fn($v) => $v !== null && $v !== '' && $v !== []);
    }

    public static function article(array $a): array
    {
        return array_filter([
            '@context' => 'https://schema.org',
            '@type' => 'BlogPosting',
            'headline' => $a['title'],
            'description' => $a['meta_description'] ?: excerpt($a['excerpt'] ?? '', 160),
            'image' => $a['featured_image'] ? abs_url($a['featured_image']) : null,
            'datePublished' => $a['published_at'] ? gmdate('c', strtotime($a['published_at'] . ' UTC')) : null,
            'dateModified' => gmdate('c', strtotime($a['updated_at'] . ' UTC')),
            'mainEntityOfPage' => abs_url('/' . $a['slug'] . '/'),
            'author' => ['@type' => 'Organization', 'name' => cfg('site_name', 'Rodeo Texas'), 'url' => abs_url('/')],
            'publisher' => ['@type' => 'Organization', 'name' => cfg('site_name', 'Rodeo Texas'), 'logo' => ['@type' => 'ImageObject', 'url' => abs_url('/assets/img/logo-512.png')]],
        ]);
    }
}
