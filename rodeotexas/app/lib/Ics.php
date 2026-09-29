<?php
declare(strict_types=1);

namespace RT;

/**
 * Downloadable iCalendar file for an event.
 *  - with show times: one VEVENT per performance, in UTC (converted from the
 *    venue's own zone, so El Paso shows correctly in Mountain Time)
 *  - without show times: one all-day VEVENT spanning the event dates
 */
final class Ics
{
    public static function forEvent(array $e, array $perfs): string
    {
        $host = parse_url((string) cfg('base_url'), PHP_URL_HOST) ?: 'rodeotexas.org';
        $url = abs_url('/rodeos/' . $e['slug'] . '/');
        $loc = implode(', ', array_filter([$e['venue_name'], $e['venue_address'], $e['city'] ? $e['city'] . ', TX' : null, $e['postal_code']]));
        $desc = trim(($e['description'] ? excerpt($e['description'], 600) . "\n\n" : '') . 'Details and updates: ' . $url
            . ($e['official_url'] ? "\nOfficial site: " . $e['official_url'] : ''));
        $status = ['canceled' => 'CANCELLED', 'postponed' => 'TENTATIVE'][$e['status']] ?? 'CONFIRMED';
        $stamp = gmdate('Ymd\THis\Z');
        $lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//RodeoTexas.org//Event Directory//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH'];
        $events = [];
        if ($perfs) {
            foreach ($perfs as $p) {
                // No end time is invented: DTEND is only written when the organizer published one.
                $events[] = array_filter([
                    'UID' => 'event-' . $e['id'] . '-perf-' . $p['id'] . '@' . $host,
                    'DTSTART' => Dates::icsUtc($p['starts_at'], $e['timezone']),
                    'DTEND' => $p['ends_at'] ? Dates::icsUtc($p['ends_at'], $e['timezone']) : null,
                    'SUMMARY' => $e['title'] . ($p['label'] ? ' — ' . $p['label'] : ''),
                ]);
            }
        } else {
            $events[] = [
                'UID' => 'event-' . $e['id'] . '@' . $host,
                'DTSTART;VALUE=DATE' => str_replace('-', '', $e['start_date']),
                'DTEND;VALUE=DATE' => date('Ymd', strtotime($e['end_date'] . ' +1 day')),
                'SUMMARY' => $e['title'],
            ];
        }
        foreach ($events as $v) {
            $lines[] = 'BEGIN:VEVENT';
            foreach ($v as $k => $val) {
                $lines[] = $k . ':' . (str_starts_with($k, 'DT') ? $val : self::esc($val));
            }
            $lines[] = 'DTSTAMP:' . $stamp;
            $lines[] = 'STATUS:' . $status;
            if ($loc !== '') {
                $lines[] = 'LOCATION:' . self::esc($loc);
            }
            if ($e['lat'] !== null) {
                $lines[] = 'GEO:' . $e['lat'] . ';' . $e['lng'];
            }
            $lines[] = 'URL:' . $url;
            $lines[] = 'DESCRIPTION:' . self::esc($desc);
            $lines[] = 'END:VEVENT';
        }
        $lines[] = 'END:VCALENDAR';
        return implode("\r\n", array_map([self::class, 'fold'], $lines)) . "\r\n";
    }

    private static function esc(string $s): string
    {
        return str_replace(['\\', ';', ',', "\r\n", "\n"], ['\\\\', '\\;', '\\,', '\\n', '\\n'], $s);
    }

    /** Fold lines longer than 75 octets (RFC 5545 §3.1), UTF-8 safe. */
    private static function fold(string $line): string
    {
        if (strlen($line) <= 75) {
            return $line;
        }
        $out = '';
        $cur = '';
        foreach (mb_str_split($line) as $ch) {
            if (strlen($cur . $ch) > ($out === '' ? 75 : 74)) {
                $out .= ($out === '' ? '' : "\r\n ") . $cur;
                $cur = '';
            }
            $cur .= $ch;
        }
        return $out . "\r\n " . $cur;
    }
}
