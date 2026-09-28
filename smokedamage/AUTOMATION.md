# SmokeDamage.com — weekly automation runbook

Two scheduled Claude Code routines run this site's recurring work. Each run
starts from a fresh session with this repository, the Hostinger connector and
(when connected) the Semrush connector. Source of truth is branch
`claude/trusting-dirac-awejbw`, directory `smokedamage/`.

Always read `CONTENT-SPEC.md` and `research/compliance.md` first. Never
fabricate facts, statistics, SEMrush numbers, events, laws, testimonials or
case studies. When in doubt, save as draft rather than publish.

## Common steps (both jobs)

1. `cd smokedamage && pip install -q pillow` (only needed if images change).
2. **Pull admin requests.** Get file-browser credentials with Hostinger
   `agency-hosting_files_generate-upload-url` for website `qpuHSMS5T`, then:
   ```sh
   B=${SD_FB_URL%/tus}
   curl -sS -H "X-Auth: $SD_FB_AUTH" -H "X-Auth-Rest: $SD_FB_REST" "$B/raw/.h5g/sd-private/requests.json"
   curl -sS -H "X-Auth: $SD_FB_AUTH" -H "X-Auth-Rest: $SD_FB_REST" "$B/raw/.h5g/sd-private/keyword-imports.json"
   ```
   Apply every `pending` request:
   - `seo_metadata` → edit `title:` / `description:` in the page's front matter
     (find the file via `source` in `private/site-manifest.json`). Description ≤150 chars.
   - `site_settings` → edit `siteconfig.py` (verify an address against the TDI record
     in `research/compliance.md` before changing `licensed_address`).
   - `publish_event` / `publish_blog` → set `status: published` (or delete the
     draft on `reject`) after re-checking it passes the publishing check below.
   Then write `requests.json` back with each handled request's `status` set to
   `done` (or `rejected`) and a short `result`, uploading it with the TUS
   `upload` function from `deploy.sh` to `.h5g/sd-private/requests.json`.
3. Do the job-specific work below.
4. Update `content/automation-status.json`
   (`last_event_scan`, `next_event_scan`, `last_blog_generated`,
   `next_blog_generation`, `semrush_connected`, `notes`).
5. `python3 build.py && python3 validate.py` — must report 0 errors.
6. `./deploy.sh` with the credentials, then Hostinger `agency-hosting_cache_clear-website` for `qpuHSMS5T`.
7. Spot-check the changed URLs on https://smokedamage.com (HTTP 200), commit
   with a clear message and push to `claude/trusting-dirac-awejbw`.

## Weekly event scan (Mondays)

Window: from `last_scan` in `content/events/_scan-log.json` to today.

Search official sources first: Texas A&M Forest Service (tfsweb.tamu.edu,
Texas Wildfire Incidents), InciWeb, Texas State Fire Marshal, TCEQ, county
emergency management, city fire departments, NWS; reputable local news only to
confirm.

Create an event only when it is in Texas and meets the criteria: significant
wildfire (structures lost, evacuations or large acreage), large commercial or
industrial fire, multi-building structure fire, explosion with fire/smoke
damage, or another verified event reasonably likely to produce property
smoke/fire claims. Never for "smoke smelled" or air-quality-only events.

- Compare against existing `content/events/*.md` (no duplicates; update an
  existing page's facts and `last_updated` if the event is ongoing).
- Confirm basic facts from ≥1 authoritative source; prefer 2 independent
  sources for material details. Omit anything unverified (acreage, structure
  counts, cause). Where sources conflict, use the agency figure and say so.
- File format: see an existing event file. Required sections: What happened;
  Official incident information; Property Insurance Considerations After a
  Smoke or Fire Event (general, no coverage claims, state that proximity does
  not mean a covered claim); `:::cta If Your Texas Property Was Affected by
  Smoke or Fire, Request a Free Claim Review.`; `:::sources`.
- Uncertain but possibly qualifying → `status: draft` (admin can approve).
- If nothing qualifies, publish nothing. Record the scan (window, created,
  rejected with reasons, sources checked) in `_scan-log.json`.
- Consider adding significant verified events to `content/history/timeline.json`.

## Weekly article (Wednesdays)

1. Keyword choice: if the Semrush connector works, pull US keyword ideas
   (phrase match / related) for smoke damage, smoke insurance claims, fire
   claims, soot claims, contents claims, public adjusting, insurance claim
   problems and Texas property insurance claims; prefer Texas relevance and
   commercial/problem-solving intent. Also consider admin-imported keywords
   (`priority` first) and `content/keyword-queue.csv` (`queued` rows, best first).
   Record only numbers returned by Semrush or present in the CSV — never estimate.
2. Cannibalization: grep `content/` for the intent; skip topics an existing
   page already targets (link to it instead).
3. Write `content/blog/<slug>.md` per `CONTENT-SPEC.md`: 1,800–2,800 words (usefulness
   first), author Joseph Dittman, SEO title ~50–60 chars, description ≤150
   chars with the keyword, keyword in first paragraph / an H2 / FAQ, 1–2 CTAs,
   FAQ block, 5+ internal links, image key from the spec, `:::sources` for any
   law/regulation/official info (Texas law only from `research/compliance.md`
   or newly verified official sources added there).
4. **Publishing check** — all must pass or save with `status: draft` and
   `check: <reason>`: no fabricated statistics, case studies or testimonials;
   no unsupported legal advice; no promised results or guaranteed coverage; no
   competitor defamation; no copied text; no duplicate site content; no
   incorrect Texas law; no broken internal links; title, description, author,
   image + alt, CTA present; FAQ only where appropriate; `validate.py` clean.
5. Mark the keyword `published` (slug in notes) in `content/keyword-queue.csv`.
