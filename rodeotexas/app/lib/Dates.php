<?php
declare(strict_types=1);

namespace RT;

use DateTimeImmutable;
use DateTimeZone;

/**
 * Date formatting and status computation in the venue's own time zone.
 * Stored event dates are local calendar dates; performance times are local
 * wall-clock times in events.timezone (America/Chicago or America/Denver).
 */
final class Dates
{
    /** Overridable "now" for tests. */
    public static ?string $now = null;

    public static function now(string $tz = 'America/Chicago'): DateTimeImmutable
    {
        return (new DateTimeImmutable(self::$now ?? 'now', new DateTimeZone('UTC')))
            ->setTimezone(new DateTimeZone($tz));
    }

    public static function today(string $tz = 'America/Chicago'): string
    {
        return self::now($tz)->format('Y-m-d');
    }

    /**
     * @return array{key:string,label:string}
     * key: upcoming | ongoing | completed | postponed | canceled
     */
    public static function status(array $ev): array
    {
        if (($ev['status'] ?? '') === 'canceled') {
            return ['key' => 'canceled', 'label' => 'Canceled'];
        }
        if (($ev['status'] ?? '') === 'postponed') {
            return ['key' => 'postponed', 'label' => 'Postponed'];
        }
        $today = self::today($ev['timezone'] ?? 'America/Chicago');
        if ($today < $ev['start_date']) {
            return ['key' => 'upcoming', 'label' => 'Upcoming'];
        }
        if ($today <= $ev['end_date']) {
            return ['key' => 'ongoing', 'label' => 'Happening now'];
        }
        return ['key' => 'completed', 'label' => 'Completed'];
    }

    /** "Sat, Oct 3, 2026" or "Oct 2–4, 2026" or "Dec 30, 2026 – Jan 2, 2027" */
    public static function range(string $start, string $end, bool $weekday = false): string
    {
        $s = new DateTimeImmutable($start);
        $e = new DateTimeImmutable($end);
        if ($start === $end) {
            return $s->format($weekday ? 'D, M j, Y' : 'M j, Y');
        }
        if ($s->format('Y') !== $e->format('Y')) {
            return $s->format('M j, Y') . ' – ' . $e->format('M j, Y');
        }
        if ($s->format('m') !== $e->format('m')) {
            return $s->format('M j') . ' – ' . $e->format('M j, Y');
        }
        return $s->format('M j') . '–' . $e->format('j, Y');
    }

    /** Local wall-clock time with zone abbreviation: "7:30 PM CDT". */
    public static function time(string $localDateTime, string $tz): string
    {
        $d = new DateTimeImmutable($localDateTime, new DateTimeZone($tz));
        return $d->format('g:i A T');
    }

    /** ISO 8601 with the venue's UTC offset (for schema.org). */
    public static function iso(string $localDateTime, string $tz): string
    {
        return (new DateTimeImmutable($localDateTime, new DateTimeZone($tz)))->format('c');
    }

    /** Convert local wall-clock time to UTC "Ymd\THis\Z" (for iCalendar). */
    public static function icsUtc(string $localDateTime, string $tz): string
    {
        return (new DateTimeImmutable($localDateTime, new DateTimeZone($tz)))
            ->setTimezone(new DateTimeZone('UTC'))->format('Ymd\THis\Z');
    }

    /** Parse any source timestamp into local wall-clock "Y-m-d H:i:s" for $tz. */
    public static function toLocal(string $value, string $tz, ?string $sourceTz = null): ?string
    {
        try {
            $hasOffset = (bool) preg_match('/(Z|[+-]\d{2}:?\d{2})$/', trim($value));
            $d = $hasOffset
                ? new DateTimeImmutable($value)
                : new DateTimeImmutable($value, new DateTimeZone($sourceTz ?: $tz));
            return $d->setTimezone(new DateTimeZone($tz))->format('Y-m-d H:i:s');
        } catch (\Exception $e) {
            return null;
        }
    }

    /** This weekend (Fri–Sun) relative to today in Central time. */
    public static function weekend(): array
    {
        $t = self::now();
        $dow = (int) $t->format('N');          // 1 Mon … 7 Sun
        if ($dow >= 5) {
            $fri = $t->modify('-' . ($dow - 5) . ' days');
        } else {
            $fri = $t->modify('+' . (5 - $dow) . ' days');
        }
        $from = $dow >= 5 ? $t : $fri;          // don't include days already past
        return [$from->format('Y-m-d'), $fri->modify('+2 days')->format('Y-m-d')];
    }

    public static function thisMonth(): array
    {
        $t = self::now();
        return [$t->format('Y-m-d'), $t->format('Y-m-t')];
    }
}
