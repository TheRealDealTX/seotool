<?php
// Roommate compatibility scoring.

/**
 * Score how well two renters fit, 0–100, with the reasons behind it.
 * $sharedProps = number of apartment properties both are interested in.
 */
function match_score(array $a, array $b, int $sharedProps = 0): array
{
    $points = 0;
    $max = 0;
    $reasons = [];

    // Shared property interest — the strongest signal.
    $max += 30;
    if ($sharedProps > 0) {
        $points += min(30, 22 + 4 * $sharedProps);
        $reasons[] = $sharedProps === 1 ? 'Same apartment property' : "$sharedProps properties in common";
    }

    // Budget overlap.
    $max += 15;
    $aMin = (int)($a['budget_min'] ?: 0); $aMax = (int)($a['budget_max'] ?: 100000);
    $bMin = (int)($b['budget_min'] ?: 0); $bMax = (int)($b['budget_max'] ?: 100000);
    if (($a['budget_min'] || $a['budget_max']) && ($b['budget_min'] || $b['budget_max'])) {
        if ($aMin <= $bMax && $bMin <= $aMax) {
            $points += 15;
            $reasons[] = 'Budgets overlap';
        } elseif (min(abs($aMin - $bMax), abs($bMin - $aMax)) <= 200) {
            $points += 7;
        }
    } else {
        $points += 7;
    }

    // Same city.
    $max += 8;
    if ($a['city'] && $b['city'] && strcasecmp(trim($a['city']), trim($b['city'])) === 0) {
        $points += 8;
        $reasons[] = 'Both in ' . $b['city'];
    }

    // Move-in timing.
    $max += 8;
    if ($a['move_in_date'] && $b['move_in_date']) {
        $days = abs(strtotime($a['move_in_date']) - strtotime($b['move_in_date'])) / 86400;
        if ($days <= 30) { $points += 8; $reasons[] = 'Similar move-in dates'; }
        elseif ($days <= 60) { $points += 4; }
    } else {
        $points += 4;
    }

    // Need / have a place complement.
    $max += 6;
    $lf = [$a['looking_for'], $b['looking_for']];
    sort($lf);
    if ($lf === ['have_place', 'need_place']) { $points += 6; $reasons[] = 'One has a place, one needs one'; }
    elseif (in_array('either', $lf, true) || $lf[0] === 'need_place') { $points += 4; }

    // Cleanliness.
    $max += 10;
    $diff = abs((int)$a['cleanliness'] - (int)$b['cleanliness']);
    $points += max(0, 10 - $diff * 3);
    if ($diff === 0) $reasons[] = 'Same cleanliness standards';

    // Sleep schedule.
    $max += 7;
    if ($a['sleep_schedule'] === $b['sleep_schedule']) { $points += 7; $reasons[] = 'Matching sleep schedules'; }
    elseif ($a['sleep_schedule'] === 'normal' || $b['sleep_schedule'] === 'normal') { $points += 3; }

    // Smoking.
    $max += 7;
    if ($a['smoking'] === $b['smoking']) { $points += 7; if ($a['smoking'] === 'no') $reasons[] = 'Both non-smokers'; }
    elseif ($a['smoking'] !== 'yes' && $b['smoking'] !== 'yes') { $points += 4; }

    // Pets.
    $max += 5;
    $petClash = ($a['pets'] === 'have' && $b['pets'] === 'no_pets') || ($b['pets'] === 'have' && $a['pets'] === 'no_pets');
    if (!$petClash) $points += 5;

    // Guests.
    $max += 4;
    $g = ['rarely' => 0, 'sometimes' => 1, 'often' => 2];
    $points += max(0, 4 - 2 * abs($g[$a['guests']] - $g[$b['guests']]));

    $score = (int)round($points / $max * 100);

    // Gender preferences are a dealbreaker either way.
    $prefOk = fn($pref, $gender) => $pref === 'any' || $pref === $gender;
    if (!$prefOk($a['gender_pref'], $b['gender']) || !$prefOk($b['gender_pref'], $a['gender'])) {
        $score = (int)round($score * 0.4);
    }
    if ($petClash) $reasons[] = 'Pet preferences differ';

    // Shared interests.
    $ia = array_filter(array_map(fn($s) => strtolower(trim($s)), explode(',', (string)$a['interests'])));
    $ib = array_filter(array_map(fn($s) => strtolower(trim($s)), explode(',', (string)$b['interests'])));
    $common = array_values(array_intersect($ia, $ib));
    if ($common) {
        $score = min(100, $score + min(6, 2 * count($common)));
        $reasons[] = 'Both into ' . implode(', ', array_slice($common, 0, 3));
    }

    return ['score' => max(1, min(100, $score)), 'reasons' => $reasons];
}

function score_class(int $s): string
{
    return $s >= 75 ? 'great' : ($s >= 55 ? 'good' : 'fair');
}

/** Shared property counts between $me and many users: [user_id => count]. */
function shared_property_counts(int $me): array
{
    $rows = all('SELECT up2.user_id, COUNT(*) AS n FROM user_properties up1
        JOIN user_properties up2 ON up2.property_id = up1.property_id AND up2.user_id <> up1.user_id
        WHERE up1.user_id = ? GROUP BY up2.user_id', [$me]);
    $out = [];
    foreach ($rows as $r) $out[(int)$r['user_id']] = (int)$r['n'];
    return $out;
}
