<?php
/**
 * Automated tests (no framework needed). Uses a throwaway database.
 *
 *   RT_CONFIG=/path/to/test-config.php php tests/run.php
 *
 * The config must point at an EMPTY test database (it is wiped). The runner
 * starts a local fixture web server on 127.0.0.1:8099 (tests/fixtures/router.php).
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/app/bootstrap.php';
require RT_APP . '/bin/migrate.php';
require RT_APP . '/bin/seed-content.php';

use RT\Adapters\CsvAdapter;
use RT\Adapters\IcalAdapter;
use RT\Dates;
use RT\Db;
use RT\EventAdmin;
use RT\EventRepo;
use RT\Geo;
use RT\Http;
use RT\Ics;
use RT\Importer;
use RT\Matcher;
use RT\PublicForm;

putenv('RT_QUIET=1');
putenv('RT_SEND_MAIL_CLI=0');
if (!str_contains((string) cfg('db.name'), 'test')) {
    exit("Refusing to run: db.name must contain 'test'.\n");
}
$pass = 0; $fail = 0; $section = '';
function t(string $name, bool $ok, string $detail = ''): void
{
    global $pass, $fail, $section;
    if ($ok) { $pass++; echo "  ✔ {$name}\n"; }
    else { $fail++; echo "  ✘ {$name}" . ($detail !== '' ? " — {$detail}" : '') . "\n"; }
}
function section(string $s): void { echo "\n■ {$s}\n"; }

// ------------------------------------------------------------------ setup
$pdo = Db::pdo();
$pdo->exec('SET FOREIGN_KEY_CHECKS=0');
foreach ($pdo->query('SHOW TABLES')->fetchAll(PDO::FETCH_COLUMN) as $tbl) {
    $pdo->exec("DROP TABLE `{$tbl}`");
}
$pdo->exec('SET FOREIGN_KEY_CHECKS=1');
rt_migrate();
Db::q('UPDATE sources SET enabled = 0');       // never hit real sites from tests
$GLOBALS['RT_CONFIG']['geocoder']['enabled'] = false;
Http::$backoffBase = 0;                         // no sleeping between retries in tests

$fixtureRoot = __DIR__ . '/fixtures';
$server = proc_open(['php', '-S', '127.0.0.1:8099', $fixtureRoot . '/router.php'], [1 => ['file', '/dev/null', 'w'], 2 => ['file', '/dev/null', 'w']], $pipes);
usleep(600000);
register_shutdown_function(static function () use ($server) { proc_terminate($server); });
$F = 'http://127.0.0.1:8099';
$addSource = static function (string $slug, string $adapter, array $cfg, int $auto = 1) {
    $now = now_utc();
    $cfg += ['min_delay' => 0];
    return Db::insert('sources', ['slug' => $slug, 'name' => 'Test ' . $slug, 'adapter' => $adapter, 'config' => json_encode($cfg),
        'access_status' => 'active', 'enabled' => 1, 'auto_publish' => $auto, 'created_at' => $now, 'updated_at' => $now]);
};
$count = static fn(string $sql = 'SELECT COUNT(*) FROM events', array $p = []) => (int) Db::val($sql, $p);

// ------------------------------------------------------------------ pure units
section('Location & time zone rules');
t('TX state accepted', Geo::texasVerdict(['state' => 'Texas']) === 'yes');
t('Oklahoma rejected', Geo::texasVerdict(['state' => 'OK']) === 'no');
t('Texas ZIP without state accepted', Geo::texasVerdict(['postal_code' => '79901']) === 'yes');
t('El Paso 885xx ZIP accepted', Geo::isTexasZip('88510'));
t('Non-Texas ZIP rejected', Geo::texasVerdict(['postal_code' => '73942']) === 'no');
t('No location = unknown', Geo::texasVerdict(['city' => null]) === 'unknown');
t('El Paso County is Mountain Time', Geo::timezoneFor('El Paso County', -106.4) === 'America/Denver');
t('Hudspeth County is Mountain Time', Geo::timezoneFor('Hudspeth', null) === 'America/Denver');
t('Pecos (Reeves County) is Central', Geo::timezoneFor('Reeves County', -103.5) === 'America/Chicago');
t('Region: Fort Worth → North Texas', Geo::regionSlugFor(32.75, -97.33) === 'north-texas');
t('Region: Amarillo → Panhandle', Geo::regionSlugFor(35.2, -101.8) === 'panhandle-plains');
t('Region: El Paso → West Texas', Geo::regionSlugFor(31.76, -106.48) === 'west-texas');

section('Title matching (duplicates vs distinct competitions)');
t('Same rodeo, different punctuation/year', Matcher::compare('Gladewater Round-Up Rodeo 2026', 'Gladewater Round Up Rodeo') === 'same');
t('Breakaway is related, not the same', Matcher::compare('Gladewater Round-Up Rodeo', 'Gladewater Round-up Breakaway') === 'related');
t('Xtreme Bulls is related, not the same', Matcher::compare('Rodeo Austin', 'Rodeo Austin – Xtreme Bulls') === 'related');
t('Different towns are different', Matcher::compare('Coleman PRCA Rodeo', 'Crockett Lions Club PRCA Rodeo') === 'different');
t('"Mt." and "Mount" normalise', Matcher::normCity('Mt. Pleasant') === Matcher::normCity('Mount Pleasant'));

section('Dates, status and calendar time zones');
Dates::$now = '2026-10-03 17:00:00';   // Sat noon CDT
t('Ongoing status', Dates::status(['status' => 'scheduled', 'start_date' => '2026-10-02', 'end_date' => '2026-10-04', 'timezone' => 'America/Chicago'])['key'] === 'ongoing');
t('Completed status', Dates::status(['status' => 'scheduled', 'start_date' => '2026-09-02', 'end_date' => '2026-09-04', 'timezone' => 'America/Chicago'])['key'] === 'completed');
t('Canceled wins over dates', Dates::status(['status' => 'canceled', 'start_date' => '2026-12-02', 'end_date' => '2026-12-04', 'timezone' => 'America/Chicago'])['key'] === 'canceled');
[$wf, $wt] = Dates::weekend();
t('This weekend on a Saturday = Sat–Sun', $wf === '2026-10-03' && $wt === '2026-10-04', "$wf..$wt");
Dates::$now = '2026-09-29 15:00:00';   // Tuesday
[$wf, $wt] = Dates::weekend();
t('This weekend on a Tuesday = Fri–Sun', $wf === '2026-10-02' && $wt === '2026-10-04', "$wf..$wt");
[$mf, $mt] = Dates::thisMonth();
t('This month = today → month end', $mf === '2026-09-29' && $mt === '2026-09-30');
Dates::$now = null;
t('7:30 PM El Paso (MDT) = 01:30Z next day', Dates::icsUtc('2026-10-10 19:30:00', 'America/Denver') === '20261011T013000Z');
t('7:30 PM Fort Worth (CDT) = 00:30Z next day', Dates::icsUtc('2026-10-10 19:30:00', 'America/Chicago') === '20261011T003000Z');
t('After DST ends, Central is UTC-6', Dates::icsUtc('2026-11-14 19:30:00', 'America/Chicago') === '20261115T013000Z');
t('Mountain label shows MDT', str_ends_with(Dates::time('2026-10-10 19:30:00', 'America/Denver'), 'MDT'));
t('ISO offset for schema.org', Dates::iso('2026-12-05 19:00:00', 'America/Chicago') === '2026-12-05T19:00:00-06:00');

section('Robots.txt parsing');
$rb = Http::parseRobots("User-agent: *\nDisallow: /private\nCrawl-delay: 10\n\nUser-agent: Googlebot\nDisallow: /\n", 'RodeoTexasBot/1.0');
t('Generic group applies to our bot', $rb['disallow'] === ['/private'] && $rb['delay'] === 10.0);
$rb2 = Http::parseRobots("User-agent: RodeoTexasBot\nDisallow: /\n", 'RodeoTexasBot/1.0 (+x)');
t('Specific group for our bot wins', $rb2['disallow'] === ['/']);

section('iCalendar parser');
$ical = new IcalAdapter(['config' => '{}']);
$loc = $ical->parseLocation('Gladewater Rodeo Arena, 1 Arena Rd, Gladewater, TX 75647');
t('LOCATION parsed into venue parts', $loc['name'] === 'Gladewater Rodeo Arena' && $loc['city'] === 'Gladewater' && $loc['postal_code'] === '75647' && $loc['state'] === 'TX', json_encode($loc));
$recs = $ical->parse((string) file_get_contents($F . '/ics/feed.ics'));
$ep = array_values(array_filter($recs, static fn($r) => $r['uid'] === 'ics-elpaso-1'))[0] ?? null;
t('TZID America/Denver time kept as local 19:30', $ep && $ep['performances'][0]['start'] === $ep['start_date'] . ' 19:30:00' && $ep['timezone'] === 'America/Denver');
t('Folded DESCRIPTION unfolded', $ep && str_contains((string) $ep['description'], 'unfolding in the parser'));
$gl = array_values(array_filter($recs, static fn($r) => $r['uid'] === 'ics-glade-1'))[0] ?? null;
t('All-day DTEND is exclusive', $gl && $gl['end_date'] === date('Y-m-d', strtotime('+32 days')));

// ------------------------------------------------------------------ import integration
section('Import: first run');
$tec = $addSource('tec', 'tribe_rest', ['base_url' => $F . '/v1', 'require_keywords' => ['rodeo', 'breakaway', 'roping', 'bull']]);
$r1 = Importer::run('cli', 'weekly');
t('Run succeeded', $r1['status'] === 'success', $r1['message']);
t('Texas rodeos created (Gladewater x2, Big Spring, Stephenville)', $r1['stats']['created'] === 4, json_encode($r1['stats']));
t('Oklahoma event excluded by venue state', $r1['stats']['skipped_outside_texas'] === 1);
t('Golf tournament filtered as not rodeo-related', $r1['stats']['skipped_filter'] === 1);
t('Event with no location skipped, not guessed', $r1['stats']['skipped_no_location'] === 1);
t('Complete records auto-published', $count("SELECT COUNT(*) FROM events WHERE publish_state = 'published'") === 4);
$glade = Db::one("SELECT * FROM events WHERE title = 'Gladewater Round-Up Rodeo'");
$gladeBa = Db::one("SELECT * FROM events WHERE title = 'Gladewater Round-Up Breakaway'");
t('Breakaway kept as a separate event', $glade && $gladeBa && $glade['id'] !== $gladeBa['id']);
t('…and grouped with the rodeo', $glade && $gladeBa && $gladeBa['group_id'] !== null && Db::val('SELECT group_id FROM events WHERE id = ?', [$glade['id']]) == $gladeBa['group_id']);
t('Show time stored in venue local time', Db::val('SELECT starts_at FROM performances WHERE event_id = ?', [$glade['id']]) === $glade['start_date'] . ' 19:30:00');
t('Verification date recorded', $glade['last_verified_at'] !== null && $glade['source_label'] === 'Test tec');
t('Price carried over from source', $glade['price_text'] === '$15');

section('Import: repeat run is idempotent');
$before = $count();
$r2 = Importer::run('cli', 'weekly');
t('No new events on identical data', $count() === $before && $r2['stats']['created'] === 0);
t('All records reported unchanged', $r2['stats']['unchanged'] === 7, json_encode($r2['stats']));
t('No duplicate source records', $count('SELECT COUNT(*) FROM source_records') === 7);

section('Manual corrections are preserved');
$bigSpring = Db::one("SELECT * FROM events WHERE title LIKE 'Big Spring%'");
$input = ['title' => 'Gladewater Round-Up Rodeo — corrected by admin', 'start_date' => $glade['start_date'], 'end_date' => $glade['end_date'],
    'publish_state' => 'published', 'status' => 'scheduled', 'venue_id' => (string) $glade['venue_id'], 'official_url' => $glade['official_url'],
    'performances' => EventAdmin::perfsToText((int) $glade['id']), 'org_name' => 'Fixture Rodeo Assn', 'source_label' => $glade['source_label'],
    'source_url' => $glade['source_url'], 'price_text' => '$15', 'description' => $glade['description']];
[$sid, $errs] = EventAdmin::save((int) $glade['id'], $input, 1);
$locked = json_decode((string) Db::val('SELECT locked_fields FROM events WHERE id = ?', [$glade['id']]), true);
t('Admin edit saved and title locked', !$errs && in_array('title', $locked, true), json_encode($errs));

section('Import: source changes a week later');
Db::update('sources', ['config' => json_encode(['base_url' => $F . '/v2', 'require_keywords' => ['rodeo', 'breakaway', 'roping', 'bull'], 'min_delay' => 0])], 'id = :id', ['id' => $tec]);
$r3 = Importer::run('cli', 'weekly');
t('Run succeeded', $r3['status'] === 'success', $r3['message']);
t('Locked title NOT overwritten', Db::val('SELECT title FROM events WHERE id = ?', [$glade['id']]) === 'Gladewater Round-Up Rodeo — corrected by admin');
t('Conflict sent to review instead', $count("SELECT COUNT(*) FROM review_items WHERE kind = 'import_conflict' AND event_id = ?", [$glade['id']]) === 1);
$bs = Db::one('SELECT * FROM events WHERE id = ?', [$bigSpring['id']]);
t('Rescheduled dates applied to unlocked event', $bs['start_date'] === date('Y-m-d', strtotime('+57 days')), $bs['start_date']);
t('Date change logged in history', $count("SELECT COUNT(*) FROM event_history WHERE event_id = ? AND field = 'start_date'", [$bigSpring['id']]) === 1);
t('Explicit "CANCELED:" marks the event canceled', Db::val("SELECT status FROM events WHERE title = 'Stephenville PRCA Rodeo'") === 'canceled');
t('New event added', $count("SELECT COUNT(*) FROM events WHERE title = 'Texas Youth Rodeo Finals'") === 1);
t('Youth level detected from the title', Db::val("SELECT level FROM events WHERE title = 'Texas Youth Rodeo Finals'") === 'youth');
$r3b = Importer::run('cli', 'weekly');
t('Conflict not duplicated on re-run', $count("SELECT COUNT(*) FROM review_items WHERE kind = 'import_conflict' AND event_id = ?", [$glade['id']]) === 1 && $r3b['stats']['conflicts'] === 0);

section('Cross-source duplicates');
$ics = $addSource('ics', 'ical', ['url' => $F . '/ics/feed.ics', 'unknown_location' => 'review']);
$beforeIcs = $count();
$r4 = Importer::run('cli', 'single', [$ics]);
t('Same Gladewater rodeo from a second source matched, not duplicated', $r4['stats']['matched'] === 1, json_encode($r4['stats']));
t('Only the El Paso event is new', $count() === $beforeIcs + 1);
$elp = Db::one("SELECT e.*, v.timezone AS vtz FROM events e JOIN venues v ON v.id = e.venue_id WHERE e.title = 'Rodeo El Paso Test Night'");
t('El Paso venue in Mountain Time (by ZIP/longitude)', $elp && $elp['timezone'] === 'America/Denver', $elp['timezone'] ?? 'missing');
$ev = EventRepo::bySlug($elp['slug']);
$icsTxt = Ics::forEvent($ev, EventRepo::performances((int) $ev['id']));
$expect = Dates::icsUtc($elp['start_date'] . ' 19:30:00', 'America/Denver');
t('Calendar file uses correct UTC for Mountain Time', str_contains($icsTxt, 'DTSTART:' . $expect), $expect);
t('No invented end time? (source gave one: 22:00)', str_contains($icsTxt, 'DTEND:' . Dates::icsUtc($elp['start_date'] . ' 22:00:00', 'America/Denver')));
t('Unknown-location record routed to review', $count("SELECT COUNT(*) FROM review_items WHERE kind = 'import_ambiguous'") === 1);

section('Structured data (JSON-LD source)');
$ld = $addSource('ld', 'jsonld', ['urls' => [$F . '/ld/event.html']]);
$r5 = Importer::run('cli', 'single', [$ld]);
$pecos = Db::one("SELECT * FROM events WHERE title = 'Pecos Test Rodeo'");
t('JSON-LD event imported', (bool) $pecos, $r5['message']);
t('schema.org EventPostponed → postponed', $pecos && $pecos['status'] === 'postponed');
t('Offer URL stored but NOT marked verified', $pecos && $pecos['ticket_url'] === 'https://fixture.test/tickets' && (int) $pecos['ticket_url_verified'] === 0);

section('Failures leave data intact');
$snapshot = Db::val('SELECT MD5(GROUP_CONCAT(CONCAT_WS("|", id, title, start_date, end_date, status, publish_state) ORDER BY id)) FROM events');
$bad = $addSource('bad', 'tribe_rest', ['base_url' => $F . '/fail']);
$garbage = $addSource('garbage', 'tribe_rest', ['base_url' => $F . '/garbage']);
$r6 = Importer::run('cli', 'weekly');
t('Run reported as partial', $r6['status'] === 'partial', $r6['status']);
t('Two sources failed, others OK', $r6['stats']['sources_failed'] === 2 && $r6['stats']['sources_ok'] === 3, json_encode($r6['stats']));
t('Existing events untouched', Db::val('SELECT MD5(GROUP_CONCAT(CONCAT_WS("|", id, title, start_date, end_date, status, publish_state) ORDER BY id)) FROM events') === $snapshot);
t('Failure counted on the source', (int) Db::val('SELECT consecutive_failures FROM sources WHERE id = ?', [$bad]) === 1);
t('Error logged', $count("SELECT COUNT(*) FROM import_logs WHERE run_id = ? AND level = 'error'", [$r6['run_id']]) === 2);
Db::q('UPDATE sources SET enabled = 0 WHERE id IN (?, ?)', [$bad, $garbage]);

section('Disappearing events are not canceled or deleted');
$youth = (int) Db::val("SELECT id FROM events WHERE title = 'Texas Youth Rodeo Finals'");
Db::update('sources', ['config' => json_encode(['base_url' => $F . '/v1', 'require_keywords' => ['rodeo', 'breakaway'], 'min_delay' => 0])], 'id = :id', ['id' => $tec]);
Importer::run('cli', 'single', [$tec]);
$y = Db::one('SELECT status, publish_state FROM events WHERE id = ?', [$youth]);
t('Event missing from the feed is still scheduled & published', $y && $y['status'] === 'scheduled' && $y['publish_state'] === 'published');

section('Overlapping runs are prevented');
$fh = fopen(Importer::lockFile(), 'c');
flock($fh, LOCK_EX);
$r7 = Importer::run('cli', 'weekly');
flock($fh, LOCK_UN);
fclose($fh);
t('Second run refused while one holds the lock', $r7['status'] === 'locked');
t('isRunning() false after release', !Importer::isRunning());

section('Manual CSV fallback');
$csvFile = sys_get_temp_dir() . '/rt-test-' . getmypid() . '.csv';
file_put_contents($csvFile, "title,start_date,end_date,performances,venue_name,city,state,postal_code,official_url,association\n"
    . 'Test County PRCA Rodeo,' . date('Y-m-d', strtotime('+100 days')) . ',' . date('Y-m-d', strtotime('+101 days')) . ',"' . date('Y-m-d', strtotime('+100 days')) . ' 7:30 pm; ' . date('Y-m-d', strtotime('+101 days')) . ' 14:00 Matinee",Expo Arena,Lubbock,TX,79401,https://example.org/r,prca' . "\n"
    . 'Out Of State Rodeo,' . date('Y-m-d', strtotime('+100 days')) . ',,,Arena,Tulsa,OK,74101,https://example.org/o,' . "\n"
    . 'Broken row,not-a-date,,,,Austin,TX,,,' . "\n");
$csvSrc = (int) Db::val("SELECT id FROM sources WHERE slug = 'manual-csv'");
$r8 = Importer::run('manual', 'single', [$csvSrc], $csvFile);
t('CSV imported the Texas row only', $r8['stats']['created'] === 1 && $r8['stats']['skipped_outside_texas'] === 1, json_encode($r8['stats']));
$csvEv = Db::one("SELECT * FROM events WHERE title = 'Test County PRCA Rodeo'");
t('CSV performances parsed (7:30 pm → 19:30)', $csvEv && Db::val('SELECT MIN(starts_at) FROM performances WHERE event_id = ?', [$csvEv['id']]) === date('Y-m-d', strtotime('+100 days')) . ' 19:30:00');
t('CSV association applied', $csvEv && Db::val('SELECT abbr FROM associations WHERE id = ?', [$csvEv['association_id']]) === 'PRCA');
$r9 = Importer::run('manual', 'single', [$csvSrc], $csvFile);
t('Re-uploading the same CSV creates nothing', $r9['stats']['created'] === 0);
@unlink($csvFile);

// ------------------------------------------------------------------ search & filters
section('Search and filters');
$f = static fn(array $in) => EventRepo::search(EventRepo::filtersFrom($in));
t('Search by event name', $f(['q' => 'gladewater'])['total'] === 2);
t('Search by city', $f(['q' => 'Big Spring'])['total'] === 1);
t('Search by venue', $f(['q' => 'Rodeo Bowl'])['total'] === 1);
t('Search by exact ZIP', $f(['q' => '79720'])['total'] === 1);
$zip = $f(['q' => '79799']);
t('ZIP with no exact match falls back to ZIP area', $zip['total'] >= 1 && $zip['note'] !== null);
t('SQL wildcard characters are literal', $f(['q' => '%'])['total'] === 0 && $f(['q' => '_'])['total'] === 0);
t('Filter by association (Stephenville + CSV rodeo are PRCA)', $f(['association' => 'prca'])['total'] === 2);
t('Filter by level', $f(['level' => 'youth'])['total'] === 1);
t('Filter by type', $f(['type' => 'breakaway-roping'])['total'] === 1);
$bsNow = Db::one("SELECT start_date, end_date FROM events WHERE title LIKE 'Big Spring%'");
$dateF = $f(['from' => date('Y-m-d', strtotime($bsNow['end_date'] . ' -1 day')), 'to' => date('Y-m-d', strtotime($bsNow['end_date'] . ' +1 day'))]);
t('Date range filter (overlap)', $dateF['total'] === 1 && str_starts_with($dateF['rows'][0]['title'], 'Big Spring'));
t('Invalid filter values are ignored', EventRepo::filtersFrom(['region' => "x' OR 1=1 --", 'level' => 'pro', 'from' => '2026-13-45'])['region'] === null);
t('Past events excluded from upcoming list', $f([])['total'] === $count("SELECT COUNT(*) FROM events WHERE publish_state = 'published' AND end_date >= ?", [Dates::today()]));
t('Drafts never appear publicly', !array_filter($f([])['rows'], static fn($r) => $r['publish_state'] !== 'published'));

// ------------------------------------------------------------------ forms & auth
section('Public form protection');
$_SERVER['REMOTE_ADDR'] = '203.0.113.9';
$tok = PublicForm::token('submit');
t('Honeypot catches bots', PublicForm::check('submit', ['_ft' => $tok, PublicForm::HONEYPOT => 'http://spam'], 99) === 'spam');
t('Too-fast submission treated as spam', PublicForm::check('submit', ['_ft' => $tok], 99) === 'spam');
$old = (time() - 10) . '.' . hash_hmac('sha256', 'submit|' . (time() - 10), (string) cfg('app_secret'));
t('Valid token accepted', PublicForm::check('submit', ['_ft' => $old], 99) === null);
t('Tampered token rejected', PublicForm::check('submit', ['_ft' => (time() - 10) . '.' . str_repeat('a', 64)], 99) !== null);
t('Token for another form rejected', PublicForm::check('contact', ['_ft' => $old], 99) !== null);
for ($i = 0; $i < 3; $i++) { PublicForm::check('ratetest', ['_ft' => (time() - 10) . '.' . hash_hmac('sha256', 'ratetest|' . (time() - 10), (string) cfg('app_secret'))], 3); }
t('Rate limit kicks in', str_contains((string) PublicForm::check('ratetest', ['_ft' => (time() - 10) . '.' . hash_hmac('sha256', 'ratetest|' . (time() - 10), (string) cfg('app_secret'))], 3), 'short time'));

section('Admin authentication');
RT\Auth::createAdmin('owner@example.com', 'Owner', 'a-very-long-password-1');
$hash = (string) Db::val("SELECT password_hash FROM admins WHERE email = 'owner@example.com'");
t('Password stored as a hash', str_starts_with($hash, '$2y$') || str_starts_with($hash, '$argon2'));
$threw = false;
try { RT\Auth::createAdmin('x@example.com', 'X', 'short'); } catch (InvalidArgumentException $e) { $threw = true; }
t('Short passwords rejected', $threw);
$_SESSION = [];
for ($i = 0; $i < 5; $i++) { RT\Auth::attempt('owner@example.com', 'wrong-password'); }
t('Locked out after 5 failures', str_contains((string) RT\Auth::attempt('owner@example.com', 'a-very-long-password-1'), 'Too many'));

echo "\n{$pass} passed, {$fail} failed\n";
exit($fail ? 1 : 0);
