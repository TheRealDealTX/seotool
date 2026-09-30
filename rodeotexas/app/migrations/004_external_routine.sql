-- Source for events found by the external weekly routine's research step.
-- Never auto-published: every record lands in the review queue as a draft.
SET @now = UTC_TIMESTAMP();
INSERT IGNORE INTO sources (slug, name, adapter, config, homepage, access_status, access_note, enabled, auto_publish, daily_check, created_at, updated_at) VALUES
('weekly-research', 'Weekly research (official organizer sites)', 'push', '{"require_keywords":["rodeo","bull riding","roping","barrel","bronc","ranch rodeo"],"exclude_acts":true}', NULL, 'active',
 'Events found each week by the external routine on OFFICIAL organizer, venue or association pages whose terms allow it. Each record carries its source URL. Always held for admin review (auto-publish off).',
 0, 0, 0, @now, @now);
