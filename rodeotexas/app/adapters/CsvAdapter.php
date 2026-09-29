<?php
declare(strict_types=1);

namespace RT\Adapters;

use RT\Dates;

/**
 * Manual CSV import — the fallback for sources that require permission,
 * credentials or paid access (e.g. PRORODEO schedule data you are licensed
 * to use, association schedules sent by e-mail, spreadsheets from organizers).
 *
 * The file is uploaded in Admin → Sources → (source) → Upload CSV, or passed on
 * the command line:  php app/bin/import.php --source=<slug> --file=path.csv
 *
 * Columns (header row required; order does not matter; only title,
 * start_date and city are mandatory). See docs/csv-template.csv.
 *   source_uid, title, start_date, end_date, performances, venue_name, address,
 *   city, state, postal_code, official_url, ticket_url, price, organizer_name,
 *   organizer_website, organizer_email, organizer_phone, association, level,
 *   event_type, status, description, source_url
 *
 * performances: "2026-10-03 19:30; 2026-10-04 14:00 Matinee" (local venue time)
 */
final class CsvAdapter extends Adapter
{
    private ?string $file = null;

    public static function describe(): string
    {
        return 'Manual CSV upload (fallback for sources awaiting permission)';
    }

    public function setFile(string $path): void
    {
        $this->file = $path;
    }

    public function fetch(): array
    {
        if ($this->file === null || !is_file($this->file)) {
            throw new \RuntimeException('No CSV file supplied for this manual source');
        }
        $fh = fopen($this->file, 'rb');
        if (!$fh) {
            throw new \RuntimeException('Cannot open CSV file');
        }
        $bom = fread($fh, 3);
        if ($bom !== "\xEF\xBB\xBF") {
            rewind($fh);
        }
        $header = fgetcsv($fh, 0, ',', '"', '\\');
        if (!$header) {
            throw new \RuntimeException('CSV is empty');
        }
        $header = array_map(static fn($h) => strtolower(trim((string) $h)), $header);
        foreach (['title', 'start_date'] as $req) {
            if (!in_array($req, $header, true)) {
                throw new \RuntimeException("CSV missing required column: {$req}");
            }
        }
        $out = [];
        $line = 1;
        while (($row = fgetcsv($fh, 0, ',', '"', '\\')) !== false) {
            $line++;
            if ($row === [null] || count(array_filter($row, static fn($x) => trim((string) $x) !== '')) === 0) {
                continue;
            }
            $r = [];
            foreach ($header as $i => $h) {
                $r[$h] = isset($row[$i]) ? trim((string) $row[$i]) : '';
            }
            $rec = $this->map($r, $line);
            if ($rec) {
                $out[] = $rec;
            }
        }
        fclose($fh);
        return $out;
    }

    private function map(array $r, int $line): ?array
    {
        $g = static fn(string $k): ?string => (isset($r[$k]) && $r[$k] !== '') ? $r[$k] : null;
        $start = valid_date($g('start_date'));
        if (!$start || !$g('title')) {
            $this->log('warning', "CSV line {$line}: missing/invalid title or start_date — skipped");
            return null;
        }
        $end = valid_date($g('end_date')) ?? $start;
        $tz = 'America/Chicago';
        $perfs = [];
        foreach (array_filter(array_map('trim', explode(';', (string) $g('performances')))) as $p) {
            if (preg_match('/^(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})\s*(am|pm)?\s*(.*)$/i', $p, $m)) {
                $h = (int) $m[2];
                if (!empty($m[4])) {
                    $h = $h % 12 + (strtolower($m[4]) === 'pm' ? 12 : 0);
                }
                $perfs[] = ['start' => sprintf('%s %02d:%s:00', $m[1], $h, $m[3]), 'end' => null, 'label' => trim($m[5]) ?: null];
            } else {
                $this->log('warning', "CSV line {$line}: could not read performance \"{$p}\"");
            }
        }
        $status = $g('status') ? $this->explicitStatus('', $g('status')) : null;
        $title = $this->cleanTitle((string) $g('title'));
        $uid = $g('source_uid') ?? ('csv-' . sha1(strtolower($title) . '|' . $start . '|' . strtolower((string) $g('city'))));
        $org = $g('organizer_name') ? ['name' => $g('organizer_name'), 'website' => $g('organizer_website'), 'email' => $g('organizer_email'), 'phone' => $g('organizer_phone')] : null;
        return [
            'uid' => $uid,
            'title' => $title,
            'description' => $g('description'),
            'start_date' => $start,
            'end_date' => $end >= $start ? $end : $start,
            'timezone' => null,
            'performances' => $perfs,
            'venue' => $this->venue(['name' => $g('venue_name'), 'address' => $g('address'), 'city' => $g('city'), 'state' => $g('state'), 'postal_code' => $g('postal_code')]),
            'organizer' => $org,
            'official_url' => $g('official_url'),
            'ticket_url' => $g('ticket_url'),
            'price_text' => $g('price'),
            'image_url' => null,
            'source_url' => $g('source_url'),
            'status' => $status,
            'categories' => array_filter([$g('event_type')]),
            'association' => $g('association') ? strtolower($g('association')) : null,
            'level' => in_array($g('level'), levels(), true) ? $g('level') : null,
        ];
    }
}
