-- Event sources as researched on 2026-09-29 (see docs/SOURCES.md for the evidence).
-- access_status: active = automated import allowed and working
--                awaiting_permission = terms of use forbid automated collection, or the site blocks bots;
--                                      use the manual CSV fallback until written permission is obtained
--                manual_only = no machine-readable feed; enter events by hand or CSV

SET @now = UTC_TIMESTAMP();

INSERT IGNORE INTO sources (slug, name, adapter, config, homepage, access_status, access_note, enabled, auto_publish, daily_check, created_at, updated_at) VALUES
('dickies-arena', 'Dickies Arena (Fort Worth)', 'tribe_rest',
 '{"base_url":"https://dickiesarena.com","require_keywords":["rodeo","pbr","bull riding","bulls","bronc","roping","barrel","fwssr","stock show"],"exclude_acts":true,"title_replace":{"FWSSR":"Fort Worth Stock Show & Rodeo"},"title_strip_regex":"^\\\\d{4}\\\\.\\\\d{1,2}\\\\.\\\\d{1,2}(?:-\\\\d{1,2}(?:\\\\.\\\\d{1,2})?)?(?:\\\\.\\\\d{2}\\\\.\\\\d{2})?\\\\s+","default_venue":{"name":"Dickies Arena","address":"1911 Montgomery St","city":"Fort Worth","state":"TX","postal_code":"76107"}}',
 'https://dickiesarena.com/', 'active',
 'Public WordPress “The Events Calendar” REST API. robots.txt allows all paths; no terms-of-use page (checked 2026-09-29). The feed omits the venue address, so the arena''s own address is set in default_venue. Only rodeo-related events are kept.',
 1, 1, 1, @now, @now),

('destination-bryan', 'Destination Bryan (Bryan–College Station)', 'jsonld',
 '{"sitemap_url":"https://www.destinationbryan.com/sitemaps-1-event-default-1-sitemap.xml","url_pattern":"rodeo","require_keywords":["rodeo","bull riding","roping","barrel"],"exclude_keywords":["concert","live music","band","dance"],"exclude_acts":true,"max_pages":25}',
 'https://www.destinationbryan.com/', 'active',
 'schema.org Event JSON-LD on each event page, discovered from the public event sitemap. robots.txt allows these paths; no terms-of-use page, privacy policy has no automated-access clause (checked 2026-09-29).',
 1, 1, 0, @now, @now),

('visit-stephenville', 'Visit Stephenville (Cowboy Capital of the World)', 'ical',
 '{"url":"https://www.visitstephenville.com/common/modules/iCalendar/iCalendar.aspx?catID=14&feed=calendar","require_keywords":["rodeo","bull riding","roping","barrel","ranch rodeo","bronc"],"exclude_acts":true,"unknown_location":"review"}',
 'https://www.visitstephenville.com/', 'active',
 'Public iCalendar feed (CivicPlus). The feed path is not disallowed by robots.txt; no automated-access clause found (checked 2026-09-29). Mostly non-rodeo community events, so a rodeo keyword filter is applied.',
 1, 1, 0, @now, @now),

('visit-mesquite', 'Visit Mesquite (City of Mesquite CVB)', 'tribe_rest',
 '{"base_url":"https://www.visitmesquitetx.com","require_keywords":["rodeo","bull riding","roping","barrel","bronc"],"unknown_location":"review","min_delay":10}',
 'https://www.visitmesquitetx.com/', 'active',
 'Public The Events Calendar REST API. robots.txt Crawl-delay 10 is honoured; no terms-of-use page (checked 2026-09-29). Venues are often blank, so records without a location go to review.',
 1, 1, 0, @now, @now),

('freeman-coliseum', 'Freeman Coliseum (San Antonio)', 'tribe_rest',
 '{"base_url":"https://freemancoliseum.com","require_keywords":["rodeo","bull riding","bulls","roping","barrel","bronc","stock show"],"default_venue":{"name":"Freeman Coliseum","address":"3201 E Houston St","city":"San Antonio","state":"TX","postal_code":"78219"}}',
 'https://freemancoliseum.com/', 'active',
 'Public The Events Calendar REST API. robots.txt disallows only /wp-admin/; no terms-of-use page (checked 2026-09-29). Feed lists venue name only; the coliseum''s own address is set in default_venue.',
 1, 1, 0, @now, @now),

('rodeohouston', 'Houston Livestock Show and Rodeo', 'tribe_rest',
 '{"base_url":"https://www.rodeohouston.com","require_keywords":["rodeo","bull riding","roping","barrel","bronc","calf scramble","mutton"],"min_delay":10}',
 'https://www.rodeohouston.com/', 'awaiting_permission',
 'A working public feed exists, but the terms of use (https://www.rodeohouston.com/terms-of-use/) prohibit “data mining, robots, or similar data gathering and extraction tools”. Disabled until written permission is obtained. Use manual entry/CSV meanwhile.',
 0, 1, 0, @now, @now),

('prorodeo', 'PRORODEO (PRCA) schedule', 'csv', '{}',
 'https://prorodeo.com/schedule', 'awaiting_permission',
 'prorodeo.com is protected by Incapsula bot protection (HTTP 403 for automated requests) and has no documented public API. Do not scrape. Request a data feed/licence from PRCA; meanwhile import rodeos you are permitted to list via CSV.',
 0, 1, 0, @now, @now),

('cowtown-coliseum', 'Cowtown Coliseum / Stockyards Championship Rodeo', 'jsonld',
 '{"urls":["https://www.cowtowncoliseum.com/"],"default_venue":{"name":"Cowtown Coliseum","address":"121 E Exchange Ave","city":"Fort Worth","state":"TX","postal_code":"76164"},"require_keywords":["rodeo","bull","bronc","roping","barrel"]}',
 'https://www.cowtowncoliseum.com/', 'awaiting_permission',
 'Homepage carries Event JSON-LD, but the operator''s terms (https://legendsglobal.com/terms-of-use/) prohibit systematic retrieval to compile a directory without written permission. Disabled until permission is granted.',
 0, 1, 0, @now, @now),

('ipra', 'IPRA schedule', 'csv', '{}', 'https://www.ipra-rodeo.com/schedule.php', 'manual_only',
 'HTML schedule only (no feed). Terms of reuse not published; ask IPRA for permission or a spreadsheet, then import via CSV.', 0, 1, 0, @now, @now),

('thsra', 'Texas High School Rodeo Association', 'csv', '{}', 'https://www.thsra.org/schedule-and-draw', 'manual_only',
 'Wix site without a machine-readable calendar. Import schedules via CSV.', 0, 1, 0, @now, @now),

('manual-csv', 'Manual CSV import', 'csv', '{}', NULL, 'manual_only',
 'General-purpose CSV upload for schedules you have permission to publish (organizer spreadsheets, association PDFs typed up, etc.).', 0, 1, 0, @now, @now),

('legacy-site', 'Previous RodeoTexas.org calendar', 'csv', '{}', 'https://rodeotexas.org/', 'manual_only',
 'Events carried over from the old WordPress site (2025–2026). Location from the event name; details were not re-verified.', 0, 0, 0, @now, @now);
