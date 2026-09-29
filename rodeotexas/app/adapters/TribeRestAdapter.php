<?php
declare(strict_types=1);

namespace RT\Adapters;

/**
 * WordPress "The Events Calendar" public REST API.
 *   GET {base_url}/wp-json/tribe/events/v1/events?start_date=…&per_page=50&page=N
 *
 * Config:
 *   base_url   "https://example.org"                     (required)
 *   days_ahead 400                                        (window to request)
 *   + common keys from Adapter (require_keywords, default_venue, …)
 */
final class TribeRestAdapter extends Adapter
{
    public static function describe(): string
    {
        return 'WordPress “The Events Calendar” REST API (/wp-json/tribe/events/v1/events)';
    }

    public function fetch(): array
    {
        $base = rtrim((string) ($this->config['base_url'] ?? ''), '/');
        if ($base === '') {
            throw new \RuntimeException('base_url missing in source config');
        }
        $from = gmdate('Y-m-d', time() - 86400 * 2);
        $to = gmdate('Y-m-d', time() + 86400 * (int) ($this->config['days_ahead'] ?? 400));
        $out = [];
        $page = 1;
        $maxPages = (int) ($this->config['max_pages'] ?? 20);
        do {
            $url = $base . '/wp-json/tribe/events/v1/events?' . http_build_query([
                'start_date' => $from . ' 00:00:00', 'end_date' => $to . ' 23:59:59', 'per_page' => 50, 'page' => $page,
            ]);
            $r = $this->http($url, ['headers' => ['Accept: application/json']]);
            if ($r['status'] === 404 && $page > 1) {
                break;   // TEC returns 404 past the last page
            }
            if ($r['status'] !== 200) {
                throw new \RuntimeException("HTTP {$r['status']} from {$url}");
            }
            $data = json_decode($r['body'], true);
            if (!is_array($data) || !isset($data['events']) || !is_array($data['events'])) {
                throw new \RuntimeException('Unexpected response (no events array) from ' . $url);
            }
            foreach ($data['events'] as $e) {
                $rec = $this->map($e);
                if ($rec !== null) {
                    $out[] = $rec;
                }
            }
            $totalPages = (int) ($data['total_pages'] ?? 1);
            $page++;
        } while ($page <= $totalPages && $page <= $maxPages);
        return $out;
    }

    private function map(array $e): ?array
    {
        if (empty($e['id']) || empty($e['start_date'])) {
            return null;
        }
        $rawTitle = html_entity_decode((string) ($e['title'] ?? ''), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $status = $this->explicitStatus($rawTitle, $e['event_status'] ?? ($e['tribe_events_status'] ?? null));
        $title = $this->cleanTitle($this->stripStatusPrefix($rawTitle));
        if ($title === '') {
            return null;
        }
        $tz = (string) ($e['timezone'] ?? '') ?: null;
        $v = is_array($e['venue'] ?? null) ? $e['venue'] : [];
        $venue = $this->venue([
            'name' => $v['venue'] ?? null,
            'address' => $v['address'] ?? null,
            'city' => $v['city'] ?? null,
            'state' => $v['state'] ?? ($v['stateprovince'] ?? ($v['province'] ?? null)),
            'postal_code' => $v['zip'] ?? null,
            'country' => $v['country'] ?? null,
            'lat' => isset($v['geo_lat']) && $v['geo_lat'] !== '' ? (float) $v['geo_lat'] : null,
            'lng' => isset($v['geo_lng']) && $v['geo_lng'] !== '' ? (float) $v['geo_lng'] : null,
        ]);
        $org = null;
        if (!empty($e['organizer'][0]) && is_array($e['organizer'][0])) {
            $o = $e['organizer'][0];
            $org = [
                'name' => html_entity_decode((string) ($o['organizer'] ?? ''), ENT_QUOTES | ENT_HTML5, 'UTF-8') ?: null,
                'website' => $o['website'] ?? null,
                'email' => isset($o['email']) ? html_entity_decode((string) $o['email'], ENT_QUOTES | ENT_HTML5, 'UTF-8') : null,
                'phone' => $o['phone'] ?? null,
            ];
        }
        $allDay = !empty($e['all_day']);
        $perfs = [];
        if (!$allDay) {
            $s = substr((string) $e['start_date'], 0, 19);
            $en = !empty($e['end_date']) ? substr((string) $e['end_date'], 0, 19) : null;
            if ($en !== null && substr($en, 0, 10) === substr($s, 0, 10)) {
                $perfs[] = ['start' => $s, 'end' => $en, 'label' => null];
            } else {
                // Multi-day entry with one start/end pair: only the first start time is a stated fact.
                $perfs[] = ['start' => $s, 'end' => null, 'label' => 'Start time listed by source'];
            }
        }
        $cats = [];
        foreach ((array) ($e['categories'] ?? []) as $c) {
            if (!empty($c['name'])) {
                $cats[] = html_entity_decode((string) $c['name'], ENT_QUOTES | ENT_HTML5, 'UTF-8');
            }
        }
        $cost = trim(html_entity_decode(strip_tags((string) ($e['cost'] ?? '')), ENT_QUOTES | ENT_HTML5, 'UTF-8'));
        $website = trim((string) ($e['website'] ?? ''));
        return [
            'uid' => 'tec-' . $e['id'],   // WordPress post ID: stable even if the date changes
            'title' => $title,
            'description' => $this->plain($e['description'] ?? null),
            'start_date' => substr((string) $e['start_date'], 0, 10),
            'end_date' => substr((string) ($e['end_date'] ?? $e['start_date']), 0, 10),
            'timezone' => $tz,
            'performances' => $perfs,
            'venue' => $venue,
            'organizer' => $org,
            'official_url' => $website !== '' ? $website : null,
            'ticket_url' => null,          // TEC has no dedicated ticket field; never guess
            'price_text' => $cost !== '' ? $cost : null,
            'image_url' => is_array($e['image'] ?? null) ? ($e['image']['url'] ?? null) : null,
            'source_url' => $e['url'] ?? null,
            'status' => $status,
            'categories' => $cats,
            'association' => null,
            'level' => null,
        ];
    }
}
