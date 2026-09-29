<?php
declare(strict_types=1);

namespace RT\Adapters;

use RT\Dates;

/**
 * iCalendar (.ics) feeds — Google Calendar public ICS, CivicPlus, The Events
 * Calendar (?ical=1), etc.
 *
 * Config:
 *   url            feed URL (required)
 *   timezone       zone for floating times (default America/Chicago)
 *   + common keys from Adapter
 *
 * LOCATION is free text; we extract "City, TX 7xxxx" style addresses. When a
 * location cannot be parsed, the venue is left empty (the importer then routes
 * the record to review or skips it — it never guesses).
 */
final class IcalAdapter extends Adapter
{
    public static function describe(): string
    {
        return 'iCalendar feed (.ics)';
    }

    public function fetch(): array
    {
        $url = (string) ($this->config['url'] ?? '');
        if ($url === '') {
            throw new \RuntimeException('url missing in source config');
        }
        $r = $this->http($url, ['headers' => ['Accept: text/calendar, */*;q=0.5']]);
        if ($r['status'] !== 200) {
            throw new \RuntimeException("HTTP {$r['status']} from {$url}");
        }
        if (stripos($r['body'], 'BEGIN:VCALENDAR') === false) {
            throw new \RuntimeException('Response is not an iCalendar document: ' . $url);
        }
        return $this->parse($r['body']);
    }

    /** Parse ICS text into normalized records (public for tests). */
    public function parse(string $ics): array
    {
        $defaultTz = (string) ($this->config['timezone'] ?? 'America/Chicago');
        $calTz = null;
        if (preg_match('/^X-WR-TIMEZONE:(.+)$/mi', $ics, $m)) {
            $calTz = trim($m[1]);
        }
        // Unfold continuation lines (RFC 5545 §3.1).
        $ics = preg_replace("/\r?\n[ \t]/", '', str_replace("\r\n", "\n", $ics)) ?? $ics;
        $today = gmdate('Y-m-d', time() - 86400 * 2);
        $out = [];
        if (!preg_match_all('/BEGIN:VEVENT\n(.*?)\nEND:VEVENT/s', $ics, $blocks)) {
            return [];
        }
        foreach ($blocks[1] as $block) {
            $p = [];
            foreach (explode("\n", $block) as $line) {
                if (!preg_match('/^([A-Z0-9-]+)((?:;[^:]*)?):(.*)$/', $line, $mm)) {
                    continue;
                }
                $name = $mm[1];
                $params = [];
                foreach (array_filter(explode(';', ltrim($mm[2], ';'))) as $kv) {
                    [$k, $v] = array_pad(explode('=', $kv, 2), 2, '');
                    $params[strtoupper($k)] = trim($v, '"');
                }
                $p[$name] ??= ['value' => $this->unescape($mm[3]), 'params' => $params];
            }
            if (empty($p['DTSTART'])) {
                continue;
            }
            $tz = $p['DTSTART']['params']['TZID'] ?? $calTz ?? $defaultTz;
            try { new \DateTimeZone($tz); } catch (\Exception $e) { $tz = $defaultTz; }
            [$sDate, $sTime] = $this->dt($p['DTSTART'], $tz);
            [$eDate, $eTime] = isset($p['DTEND']) ? $this->dt($p['DTEND'], $tz) : [$sDate, null];
            if ($sDate === null) {
                continue;
            }
            $allDay = $sTime === null;
            if ($allDay && isset($p['DTEND']) && $eDate !== null && $eDate > $sDate) {
                $eDate = date('Y-m-d', strtotime($eDate . ' -1 day'));   // DTEND is exclusive for all-day events
            }
            $eDate = ($eDate !== null && $eDate >= $sDate) ? $eDate : $sDate;
            if ($eDate < $today) {
                continue;
            }
            $raw = (string) ($p['SUMMARY']['value'] ?? '');
            $status = $this->explicitStatus($raw, $p['STATUS']['value'] ?? null);
            if (($p['STATUS']['value'] ?? '') === 'TENTATIVE') {
                $status = null;
            }
            $title = $this->cleanTitle($this->stripStatusPrefix($raw));
            if ($title === '') {
                continue;
            }
            $venue = $this->parseLocation((string) ($p['LOCATION']['value'] ?? ''));
            if (isset($p['GEO']) && preg_match('/^(-?[\d.]+);(-?[\d.]+)$/', $p['GEO']['value'], $g)) {
                $venue['lat'] = (float) $g[1];
                $venue['lng'] = (float) $g[2];
            }
            $uid = (string) ($p['UID']['value'] ?? '');
            if (isset($p['RECURRENCE-ID'])) {
                $uid .= '#' . $p['RECURRENCE-ID']['value'];
            }
            if ($uid === '') {
                $uid = 'ics-' . sha1($title . '|' . $sDate);
            }
            $url = trim((string) ($p['URL']['value'] ?? ''));
            $out[] = [
                'uid' => $uid,
                'title' => $title,
                'description' => $this->plain($p['DESCRIPTION']['value'] ?? null),
                'start_date' => $sDate,
                'end_date' => $eDate,
                'timezone' => $tz,
                'performances' => $allDay ? [] : [[
                    'start' => $sDate . ' ' . $sTime,
                    'end' => ($eTime !== null && $eDate !== null) ? $eDate . ' ' . $eTime : null,
                    'label' => null,
                ]],
                'venue' => $this->venue($venue),
                'organizer' => null,
                'official_url' => null,
                'ticket_url' => null,
                'price_text' => null,
                'image_url' => null,
                'source_url' => $url !== '' ? $url : null,
                'status' => $status,
                'categories' => array_filter(array_map('trim', explode(',', (string) ($p['CATEGORIES']['value'] ?? '')))),
                'association' => null,
                'level' => null,
            ];
        }
        return $out;
    }

    /** @return array{0:?string,1:?string} [local date, local time or null for all-day] */
    private function dt(array $prop, string $tz): array
    {
        $v = trim($prop['value']);
        if (($prop['params']['VALUE'] ?? '') === 'DATE' || preg_match('/^\d{8}$/', $v)) {
            return [substr($v, 0, 4) . '-' . substr($v, 4, 2) . '-' . substr($v, 6, 2), null];
        }
        if (!preg_match('/^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})(Z?)$/', $v, $m)) {
            return [null, null];
        }
        $iso = "{$m[1]}-{$m[2]}-{$m[3]} {$m[4]}:{$m[5]}:{$m[6]}" . ($m[7] === 'Z' ? 'Z' : '');
        $local = Dates::toLocal($iso, $tz, $tz);
        return $local ? [substr($local, 0, 10), substr($local, 11)] : [null, null];
    }

    private function unescape(string $s): string
    {
        return str_replace(['\\n', '\\N', '\\,', '\\;', '\\\\'], ["\n", "\n", ',', ';', '\\'], $s);
    }

    /** "Arena Name, 123 Main St, Stephenville, TX 76401" → venue parts. Public for tests. */
    public function parseLocation(string $loc): array
    {
        $v = ['name' => null, 'address' => null, 'city' => null, 'state' => null, 'postal_code' => null, 'country' => null];
        $loc = trim(preg_replace('/\s+/', ' ', str_replace("\n", ', ', $loc)) ?? '');
        if ($loc === '') {
            return $v;
        }
        $loc = preg_replace('/,?\s*(USA|United States( of America)?)$/i', '', $loc) ?? $loc;
        // "..., City, TX 76401" or "... City TX 76401" or "..., City, Texas"
        if (preg_match('/^(.*?)[,\s]+([A-Za-z .\'-]+?),?\s+(TX|Texas|[A-Z]{2})\.?(?:\s+(\d{5})(?:-\d{4})?)?$/', $loc, $m)) {
            $v['state'] = strtoupper($m[3]) === 'TEXAS' ? 'TX' : strtoupper($m[3]);
            $v['postal_code'] = $m[4] ?? null ?: null;
            $parts = array_map('trim', explode(',', $m[1] . ', ' . $m[2]));
            $v['city'] = array_pop($parts) ?: null;
            if ($parts) {
                $first = $parts[0];
                if (preg_match('/^\d/', $first)) {
                    $v['address'] = implode(', ', $parts);
                } else {
                    $v['name'] = $first;
                    $v['address'] = count($parts) > 1 ? implode(', ', array_slice($parts, 1)) : null;
                }
            }
            // A city that begins with digits means our split was wrong; do not trust it.
            if ($v['city'] !== null && preg_match('/\d/', $v['city'])) {
                $v['city'] = null;
            }
        } else {
            $v['name'] = $loc;
        }
        return $v;
    }
}
