<?php
declare(strict_types=1);

namespace RT\Adapters;

use RT\Dates;

/**
 * schema.org Event JSON-LD embedded in organizer web pages.
 *
 * Config (one of):
 *   urls          ["https://…/event-page/", …]            explicit pages
 *   sitemap_url   "https://…/event-sitemap.xml"            discover pages from a sitemap
 *   url_pattern   "rodeo"                                  regex filter for sitemap URLs
 *   max_pages     40
 *   timezone      "America/Chicago"   used when a date has no offset
 *   + common keys from Adapter
 */
final class JsonLdAdapter extends Adapter
{
    private const EVENT_TYPES = ['Event', 'SportsEvent', 'Festival', 'MusicEvent', 'ExhibitionEvent', 'SocialEvent'];

    public static function describe(): string
    {
        return 'schema.org Event JSON-LD on organizer pages (explicit URLs or sitemap discovery)';
    }

    public function fetch(): array
    {
        $urls = (array) ($this->config['urls'] ?? []);
        if (!empty($this->config['sitemap_url'])) {
            $urls = array_merge($urls, $this->fromSitemap((string) $this->config['sitemap_url']));
        }
        $urls = array_slice(array_values(array_unique($urls)), 0, (int) ($this->config['max_pages'] ?? 40));
        if (!$urls) {
            throw new \RuntimeException('No pages to read (configure urls or sitemap_url)');
        }
        $out = [];
        $failures = 0;
        foreach ($urls as $u) {
            try {
                $r = $this->http($u, ['headers' => ['Accept: text/html']]);
            } catch (\RuntimeException $e) {
                $failures++;
                $this->log('warning', $e->getMessage());
                continue;
            }
            if ($r['status'] !== 200) {
                $failures++;
                $this->log('warning', "HTTP {$r['status']} for {$u}");
                continue;
            }
            foreach ($this->parseHtml($r['body'], $u) as $rec) {
                $out[] = $rec;
            }
        }
        if ($failures > 0 && $failures === count($urls)) {
            throw new \RuntimeException('Every page failed to load');
        }
        return $out;
    }

    private function fromSitemap(string $url): array
    {
        $r = $this->http($url, ['headers' => ['Accept: application/xml, text/xml']]);
        if ($r['status'] !== 200) {
            throw new \RuntimeException("Sitemap HTTP {$r['status']}: {$url}");
        }
        preg_match_all('~<loc>\s*([^<\s]+)\s*</loc>~i', $r['body'], $m);
        $pat = (string) ($this->config['url_pattern'] ?? '');
        $urls = [];
        foreach ($m[1] as $loc) {
            $loc = html_entity_decode($loc, ENT_QUOTES | ENT_XML1, 'UTF-8');
            if ($pat === '' || preg_match('~' . str_replace('~', '\~', $pat) . '~i', $loc)) {
                $urls[] = $loc;
            }
        }
        return $urls;
    }

    /** Extract normalized records from one HTML page (public for tests). */
    public function parseHtml(string $html, string $pageUrl): array
    {
        preg_match_all('~<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>~is', $html, $m);
        $events = [];
        foreach ($m[1] as $json) {
            $data = json_decode(html_entity_decode(trim($json), ENT_QUOTES | ENT_HTML5, 'UTF-8'), true);
            if ($data === null) {
                $data = json_decode(trim($json), true);
            }
            if (is_array($data)) {
                $this->collect($data, $events);
            }
        }
        $out = [];
        foreach ($events as $ev) {
            $rec = $this->map($ev, $pageUrl);
            if ($rec) {
                $out[] = $rec;
            }
        }
        return $out;
    }

    private function collect(array $node, array &$events): void
    {
        $type = $node['@type'] ?? null;
        $types = is_array($type) ? $type : [$type];
        if (array_intersect($types, self::EVENT_TYPES)) {
            $events[] = $node;
            return;
        }
        foreach (['@graph', 'itemListElement', 'item', 'subEvent'] as $k) {
            if (isset($node[$k]) && is_array($node[$k])) {
                $this->collect($node[$k], $events);
            }
        }
        if (array_is_list($node)) {
            foreach ($node as $child) {
                if (is_array($child)) {
                    $this->collect($child, $events);
                }
            }
        }
    }

    private function map(array $ev, string $pageUrl): ?array
    {
        $raw = html_entity_decode((string) ($ev['name'] ?? ''), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $start = (string) ($ev['startDate'] ?? '');
        if ($raw === '' || $start === '') {
            return null;
        }
        $defTz = (string) ($this->config['timezone'] ?? 'America/Chicago');
        $hasTime = (bool) preg_match('/T\d{2}:\d{2}/', $start);
        $sLocal = $hasTime ? Dates::toLocal($start, $defTz, $defTz) : substr($start, 0, 10);
        $endRaw = (string) ($ev['endDate'] ?? '');
        $eLocal = $endRaw !== '' ? (preg_match('/T\d{2}:\d{2}/', $endRaw) ? Dates::toLocal($endRaw, $defTz, $defTz) : substr($endRaw, 0, 10)) : null;
        if (!$sLocal || !preg_match('/^\d{4}-\d{2}-\d{2}/', $sLocal)) {
            return null;
        }
        $sDate = substr($sLocal, 0, 10);
        $eDate = $eLocal ? substr($eLocal, 0, 10) : $sDate;
        if ($eDate < $sDate) {
            $eDate = $sDate;
        }
        if ($eDate < gmdate('Y-m-d', time() - 86400 * 2)) {
            return null;
        }
        // Midnight-to-midnight or 00:00 starts are day-level, not real show times.
        $perfs = [];
        if ($hasTime && substr($sLocal, 11, 5) !== '00:00') {
            $sameDay = $eDate === $sDate;
            $perfs[] = ['start' => $sLocal, 'end' => ($sameDay && $eLocal && strlen($eLocal) > 10) ? $eLocal : null,
                'label' => $sameDay ? null : 'Start time listed by source'];
        }
        $loc = $ev['location'] ?? [];
        if (is_array($loc) && array_is_list($loc)) {
            $loc = $loc[0] ?? [];
        }
        $addr = is_array($loc) ? ($loc['address'] ?? []) : [];
        if (is_string($addr)) {
            $addr = (new IcalAdapter(['config' => '{}']))->parseLocation($addr);
            $addr = ['streetAddress' => $addr['address'], 'addressLocality' => $addr['city'], 'addressRegion' => $addr['state'], 'postalCode' => $addr['postal_code']];
        }
        $geo = is_array($loc) ? ($loc['geo'] ?? []) : [];
        $venue = $this->venue([
            'name' => is_array($loc) ? ($loc['name'] ?? null) : (is_string($loc) ? $loc : null),
            'address' => $addr['streetAddress'] ?? null,
            'city' => $addr['addressLocality'] ?? null,
            'state' => $addr['addressRegion'] ?? null,
            'postal_code' => isset($addr['postalCode']) ? (string) $addr['postalCode'] : null,
            'country' => is_array($addr['addressCountry'] ?? null) ? ($addr['addressCountry']['name'] ?? null) : ($addr['addressCountry'] ?? null),
            'lat' => isset($geo['latitude']) ? (float) $geo['latitude'] : null,
            'lng' => isset($geo['longitude']) ? (float) $geo['longitude'] : null,
        ]);
        $offers = $ev['offers'] ?? null;
        if (is_array($offers) && array_is_list($offers)) {
            $offers = $offers[0] ?? null;
        }
        $price = null;
        if (is_array($offers) && isset($offers['price']) && $offers['price'] !== '') {
            $price = (is_numeric($offers['price']) ? '$' . rtrim(rtrim(number_format((float) $offers['price'], 2), '0'), '.') : (string) $offers['price']);
            if (isset($offers['highPrice'])) {
                $price .= '–$' . $offers['highPrice'];
            }
        } elseif (is_array($offers) && isset($offers['lowPrice'])) {
            $price = '$' . $offers['lowPrice'] . (isset($offers['highPrice']) ? '–$' . $offers['highPrice'] : '');
        }
        $org = $ev['organizer'] ?? null;
        if (is_array($org) && array_is_list($org)) {
            $org = $org[0] ?? null;
        }
        $image = $ev['image'] ?? null;
        if (is_array($image)) {
            $image = array_is_list($image) ? ($image[0] ?? null) : ($image['url'] ?? null);
            if (is_array($image)) {
                $image = $image['url'] ?? null;
            }
        }
        $statusField = is_string($ev['eventStatus'] ?? null) ? $ev['eventStatus'] : null;
        $status = $this->explicitStatus($raw, $statusField ? str_replace(['https://schema.org/', 'http://schema.org/', 'Event'], '', $statusField) : null);
        if ($statusField && str_contains($statusField, 'Rescheduled')) {
            $status = 'scheduled';   // rescheduled = new dates are in the record
        }
        $url = (string) ($ev['url'] ?? $pageUrl);
        return [
            'uid' => (string) ($ev['@id'] ?? ($url . '#' . $sDate)),
            'title' => $this->cleanTitle($this->stripStatusPrefix($raw)),
            'description' => $this->plain(is_string($ev['description'] ?? null) ? $ev['description'] : null),
            'start_date' => $sDate,
            'end_date' => $eDate,
            'timezone' => null,
            'performances' => $perfs,
            'venue' => $venue,
            'organizer' => is_array($org) ? ['name' => $org['name'] ?? null, 'website' => $org['url'] ?? null, 'email' => $org['email'] ?? null, 'phone' => $org['telephone'] ?? null] : null,
            'official_url' => null,
            'ticket_url' => is_array($offers) && !empty($offers['url']) ? (string) $offers['url'] : null,
            'price_text' => $price,
            'image_url' => is_string($image) ? $image : null,
            'source_url' => $url,
            'status' => $status,
            'categories' => [],
            'association' => null,
            'level' => null,
        ];
    }
}
