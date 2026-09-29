<?php
declare(strict_types=1);

namespace RT;

/**
 * Stores public form entries in the review queue and notifies the administrator.
 * Nothing submitted by visitors is published automatically.
 */
final class Submissions
{
    public static function store(string $kind, string $summary, array $payload, ?string $name, ?string $email, ?int $eventId = null): int
    {
        $id = Db::insert('review_items', [
            'kind' => $kind, 'status' => 'open', 'event_id' => $eventId, 'summary' => mb_substr($summary, 0, 255),
            'payload' => json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'submitter_name' => $name, 'submitter_email' => $email, 'ip_hash' => ip_hash(), 'created_at' => now_utc(),
        ]);
        $labels = ['submission' => 'New event submission', 'correction' => 'Correction report', 'contact' => 'Contact message'];
        $body = ($labels[$kind] ?? $kind) . ": {$summary}\n\n";
        foreach ($payload as $k => $v) {
            if ($v === null || $v === '' || $v === []) {
                continue;
            }
            $body .= str_pad(ucfirst(str_replace('_', ' ', (string) $k)) . ':', 22) . (is_array($v) ? json_encode($v) : $v) . "\n";
        }
        $body .= "\nFrom: " . ($name ?: '(no name)') . ' <' . ($email ?: 'no e-mail') . ">\n";
        $body .= "\nReview it here: " . abs_url('/admin/?page=review&id=' . $id) . "\n";
        Mailer::toAdmin(($labels[$kind] ?? 'Form') . ': ' . $summary, $body, $email);
        return $id;
    }
}
