<?php
/**
 * Fake source websites for the import tests (served by `php -S` from tests/run.php).
 *   /v1/wp-json/tribe/events/v1/events   The Events Calendar feed, version 1
 *   /v2/wp-json/tribe/events/v1/events   same feed a week later (changes, one removal, one cancellation)
 *   /fail/wp-json/...                    HTTP 500 (source outage)
 *   /garbage/wp-json/...                 200 with non-JSON body
 *   /ics/feed.ics                        iCalendar feed (El Paso Mountain Time, duplicate of a TEC event)
 *   /ld/event.html                       page with schema.org Event JSON-LD
 * Dates are relative to today so the fixtures never go stale.
 */
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$d = static fn(int $days, string $fmt = 'Y-m-d') => date($fmt, strtotime("+{$days} days"));

if ($path === '/robots.txt') {
    header('Content-Type: text/plain');
    echo "User-agent: *\nDisallow: /private/\n";
    return true;
}

$venue = static fn($name, $city, $state, $zip, $addr = '1 Arena Rd') => ['venue' => $name, 'address' => $addr, 'city' => $city, 'state' => $state, 'zip' => $zip, 'country' => 'United States'];
$ev = static function (int $id, string $title, int $startDays, int $endDays, array $venue, array $extra = []) use ($d) {
    return array_merge([
        'id' => $id, 'title' => $title, 'description' => '<p>' . $title . ' description</p>', 'url' => 'https://fixture.test/event/' . $id . '/',
        'start_date' => $d($startDays) . ' 19:30:00', 'end_date' => $d($endDays) . ' 22:00:00', 'all_day' => false, 'timezone' => 'America/Chicago',
        'website' => 'https://fixture.test/official/' . $id, 'cost' => '$15', 'venue' => $venue, 'organizer' => [['organizer' => 'Fixture Rodeo Assn', 'website' => 'https://fixture.test/', 'email' => '', 'phone' => '555-0100']],
        'categories' => [], 'image' => false,
    ], $extra);
};

if (preg_match('#^/(v1|v2)/wp-json/tribe/events/v1/events$#', $path, $m)) {
    header('Content-Type: application/json');
    $v = $m[1];
    $events = [
        $ev(101, 'Gladewater Round-Up Rodeo', 30, 32, $venue('Gladewater Rodeo Arena', 'Gladewater', 'TX', '75647')),
        $ev(102, 'Gladewater Round-Up Breakaway', 30, 32, $venue('Gladewater Rodeo Arena', 'Gladewater', 'TX', '75647')),
        $ev(103, 'Guymon Pioneer Days Rodeo', 30, 32, $venue('Henry Hughes Arena', 'Guymon', 'OK', '73942')),
        $ev(104, 'Committee Golf Tournament', 40, 40, $venue('Golf Club', 'Houston', 'TX', '77002')),
        $ev(105, 'Big Spring Cowboy Reunion & Rodeo', 50, 52, $venue('Rodeo Bowl', 'Big Spring', 'TX', '79720')),
        $ev(106, 'Mystery Ranch Rodeo', 60, 60, []),
        $ev(107, 'Stephenville PRCA Rodeo', 70, 71, $venue('Lone Star Arena', 'Stephenville', 'TX', '76401')),
    ];
    if ($v === 'v2') {
        // Big Spring moved one week later, Stephenville explicitly canceled, Mystery removed, a new youth rodeo added.
        $events[4] = $ev(105, 'Big Spring Cowboy Reunion & Rodeo', 57, 59, $venue('Rodeo Bowl', 'Big Spring', 'TX', '79720'));
        $events[6] = $ev(107, 'CANCELED: Stephenville PRCA Rodeo', 70, 71, $venue('Lone Star Arena', 'Stephenville', 'TX', '76401'));
        $events[0]['title'] = 'Gladewater Round-Up Rodeo (source title changed)';
        unset($events[5]);
        $events[] = $ev(108, 'Texas Youth Rodeo Finals', 80, 81, $venue('Brazos Expo', 'Bryan', 'TX', '77807'));
    }
    echo json_encode(['events' => array_values($events), 'total' => count($events), 'total_pages' => 1]);
    return true;
}
if (str_starts_with($path, '/fail/')) {
    http_response_code(500);
    echo 'Internal Server Error';
    return true;
}
if (str_starts_with($path, '/garbage/')) {
    header('Content-Type: text/html');
    echo '<html>Maintenance</html>';
    return true;
}
if ($path === '/ics/feed.ics') {
    header('Content-Type: text/calendar');
    $s = $d(30, 'Ymd');
    $e = $d(33, 'Ymd');
    $ep = $d(45, 'Ymd');
    echo "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//fixture//EN\r\nX-WR-TIMEZONE:America/Chicago\r\n"
        . "BEGIN:VEVENT\r\nUID:ics-glade-1\r\nSUMMARY:Gladewater Round Up Rodeo\r\nDTSTART;VALUE=DATE:{$s}\r\nDTEND;VALUE=DATE:{$e}\r\nLOCATION:Gladewater Rodeo Arena\\, 1 Arena Rd\\, Gladewater\\, TX 75647\r\nURL:https://fixture.test/ics/glade\r\nEND:VEVENT\r\n"
        . "BEGIN:VEVENT\r\nUID:ics-elpaso-1\r\nSUMMARY:Rodeo El Paso Test Night\r\nDTSTART;TZID=America/Denver:{$ep}T193000\r\nDTEND;TZID=America/Denver:{$ep}T220000\r\nLOCATION:Coliseum\\, 4100 E Paisano Dr\\, El Paso\\, TX 79905\r\nURL:https://fixture.test/ics/elpaso\r\n"
        . "DESCRIPTION:A long description line that is folded across two lines to test RFC 5545 unfolding in the\r\n  parser.\r\nEND:VEVENT\r\n"
        . "BEGIN:VEVENT\r\nUID:ics-nowhere\r\nSUMMARY:Somewhere Rodeo\r\nDTSTART;VALUE=DATE:{$ep}\r\nLOCATION:TBA\r\nEND:VEVENT\r\n"
        . "END:VCALENDAR\r\n";
    return true;
}
if ($path === '/ld/event.html') {
    header('Content-Type: text/html');
    $ld = ['@context' => 'https://schema.org', '@graph' => [[
        '@type' => 'SportsEvent', '@id' => 'https://fixture.test/ld#ev1', 'name' => 'Pecos Test Rodeo',
        'startDate' => $d(90) . 'T20:00:00-05:00', 'endDate' => $d(90) . 'T22:30:00-05:00',
        'eventStatus' => 'https://schema.org/EventPostponed',
        'location' => ['@type' => 'Place', 'name' => 'Buck Jackson Arena', 'address' => ['@type' => 'PostalAddress', 'streetAddress' => '1 Rodeo Dr', 'addressLocality' => 'Pecos', 'addressRegion' => 'TX', 'postalCode' => '79772']],
        'offers' => ['@type' => 'Offer', 'url' => 'https://fixture.test/tickets', 'price' => '20', 'priceCurrency' => 'USD'],
    ]]];
    echo '<html><head><script type="application/ld+json">' . json_encode($ld) . '</script></head><body>x</body></html>';
    return true;
}
http_response_code(404);
echo 'not found';
return true;
