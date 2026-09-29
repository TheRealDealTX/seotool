<?php
declare(strict_types=1);

namespace RT;

/**
 * Title comparison used to detect duplicates across sources while keeping
 * genuinely distinct competitions apart.
 *
 * "Gladewater Round-Up Rodeo" and "Gladewater Round-up Breakaway" share a
 * base name but differ in a *discriminator* (breakaway), so they are two
 * events that belong to the same group — never merged.
 */
final class Matcher
{
    /** Words that make a competition distinct from its parent rodeo. */
    public const DISCRIMINATORS = [
        'breakaway', 'barrel', 'barrels', 'steer', 'bull', 'bulls', 'bullriding', 'xtreme', 'extreme', 'bronc',
        'broncs', 'bareback', 'roping', 'team', 'tiedown', 'youth', 'junior', 'jr', 'ranch', 'legacy', 'finals',
        'qualifier', 'rookie', 'bulldogging', 'kickoff', 'slack', 'permit', 'gb', 'sr', 'queen', 'pageant',
        'high', 'school', 'college', 'match', 'shootout', 'invitational', 'wrestling',
    ];

    private const STOP = ['the', 'and', 'of', 'a', 'at', 'in', 'annual', 'presented', 'by', 'pro', 'prca', 'rodeo',
        'prorodeo', 'championship', 'championships', 'tx', 'texas', 'inc', 'association', 'assn', 'cowboys', 'fair'];

    /** Canonical tokens (lowercase, no years/ordinals/punctuation). */
    public static function tokens(string $title): array
    {
        $t = html_entity_decode($title, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $t = strtolower($t);
        $t = str_replace(['round-up', 'round up', 'x-treme', 'tie-down', 'bull riding', 'steer roping', 'legacy sr'],
            ['roundup', 'roundup', 'xtreme', 'tiedown', 'bullriding', 'steer roping', 'legacy steer roping'], $t);
        $t = preg_replace('/\b(19|20)\d{2}\b/', ' ', $t) ?? $t;           // years
        $t = preg_replace('/\b\d+(st|nd|rd|th)\b/', ' ', $t) ?? $t;       // ordinals
        $t = preg_replace('/[^a-z0-9]+/', ' ', $t) ?? $t;
        $out = [];
        foreach (explode(' ', $t) as $w) {
            if ($w === '' || in_array($w, self::STOP, true)) {
                continue;
            }
            if ($w === 'mt') { $w = 'mount'; }
            if ($w === 'xbulls') { $out[] = 'xtreme'; $w = 'bulls'; }
            $out[] = $w;
        }
        return array_values(array_unique($out));
    }

    /** @return array{0:string[],1:string[]} [base tokens, discriminator tokens] */
    public static function split(string $title): array
    {
        $base = []; $disc = [];
        foreach (self::tokens($title) as $w) {
            if (in_array($w, self::DISCRIMINATORS, true)) {
                // Normalise synonyms so "bull"/"bulls"/"bullriding" compare equal.
                $w = ['bulls' => 'bull', 'bullriding' => 'bull', 'barrels' => 'barrel', 'broncs' => 'bronc', 'extreme' => 'xtreme', 'jr' => 'junior', 'sr' => 'steer'][$w] ?? $w;
                $disc[$w] = true;
            } else {
                $base[] = $w;
            }
        }
        $disc = array_keys($disc);
        sort($disc);
        return [$base, $disc];
    }

    public static function jaccard(array $a, array $b): float
    {
        if (!$a && !$b) {
            return 1.0;
        }
        $i = count(array_intersect($a, $b));
        $u = count(array_unique(array_merge($a, $b)));
        return $u ? $i / $u : 0.0;
    }

    /**
     * Compare two titles.
     * @return string 'same' | 'related' | 'different'
     */
    public static function compare(string $t1, string $t2): string
    {
        [$b1, $d1] = self::split($t1);
        [$b2, $d2] = self::split($t2);
        $sim = self::jaccard($b1, $b2);
        $contained = $b1 && $b2 && (!array_diff($b1, $b2) || !array_diff($b2, $b1));
        $baseSimilar = $sim >= 0.5 || $contained;
        if (!$baseSimilar) {
            return 'different';
        }
        return $d1 === $d2 ? 'same' : 'related';
    }

    public static function normCity(?string $city): string
    {
        $c = strtolower(trim((string) $city));
        $c = preg_replace('/^(mt\.?|mount)\s+/', 'mount ', $c) ?? $c;
        $c = preg_replace('/^(ft\.?|fort)\s+/', 'fort ', $c) ?? $c;
        return preg_replace('/[^a-z ]/', '', $c) ?? $c;
    }

    public static function datesOverlap(string $s1, string $e1, string $s2, string $e2, int $slackDays = 1): bool
    {
        $a1 = strtotime($s1 . ' -' . $slackDays . ' day');
        $b1 = strtotime($e1 . ' +' . $slackDays . ' day');
        return strtotime($s2) <= $b1 && strtotime($e2) >= $a1;
    }
}
