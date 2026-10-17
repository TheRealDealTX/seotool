# Content spec for organizedbyannefl.com modules

Business: "Organized by Anne" — professional home organizing in Fort Lauderdale, FL
(Broward County). Tagline/positioning carried over from the original site:
"Organizing with a touch of design" / "Create order in the chaos of life".
Contact: email info@organizedbyannefl.com only. NO phone number anywhere.

Voice: warm, practical, specific, design-minded. Use "we"/"our team" (brand voice),
never first-person "I'm Anne", and never invent a biography, years of experience,
certifications, client counts, awards, press mentions, testimonials or reviews.
No fabricated statistics or quoted studies. US spelling. No emojis.
Local color where natural and accurate: Fort Lauderdale neighborhoods (Las Olas,
Victoria Park, Coral Ridge, Rio Vista, Harbor Beach, Flagler Village), nearby
cities (Wilton Manors, Oakland Park, Lauderdale-by-the-Sea, Plantation, Weston,
Davie, Coral Springs, Hollywood, Pompano Beach), condos and high-rises, humidity,
hurricane season (June 1 – November 30), seasonal residents/snowbirds.

Body HTML: only <h2>, <h3>, <p>, <ul>, <ol>, <li>, <strong>, <em>, <a>, and these blocks:
  <div class="callout"><strong>Short title</strong><p>Text</p></div>
  <div class="tip"><strong>Pro tip</strong><p>Text</p></div>
  <table class="table"><thead>..</thead><tbody>..</tbody></table>
Do not use <h1> (the template adds it). Use straight ASCII quotes inside Python
strings carefully; prefer triple-quoted strings for body_html. Use &amp; for & in HTML.

Internal links (use these exact paths, no trailing slash):
  /services, /contact, /about, /blog, /tools, /service-area
  /services/home-organizing, /services/closet-organization,
  /services/kitchen-pantry-organization, /services/decluttering-downsizing,
  /services/move-in-unpacking, /services/home-office-organization,
  /services/laundry-bathroom-organization, /services/virtual-organizing
  /tools/organizing-time-estimator, /tools/declutter-decision-helper,
  /tools/30-day-declutter-challenge, /tools/closet-rod-calculator
  Blog slugs (/blog/<slug>):
  junk-drawer-organization-tips, under-bed-storage-ideas,
  homeschool-organization-small-spaces, organizing-mistakes-that-backfire,
  when-to-replace-household-items, refresh-your-space-for-under-10,
  hurricane-season-home-organization-florida, closet-organization-humid-climate,
  pantry-organization-ideas, room-by-room-decluttering-checklist,
  small-bathroom-organization-ideas, how-to-organize-a-home-office,
  how-much-does-a-professional-organizer-cost, seasonal-home-organization-snowbirds
Each body should contain 3-6 contextual internal links (at least one service, and a
tool where relevant).
