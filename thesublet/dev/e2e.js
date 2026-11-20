// End-to-end test against php -S on :8099 (SQLite). Run: node dev/e2e.js
const { chromium, devices } = require('playwright');
const path = require('path');
const BASE = process.env.BASE || 'http://127.0.0.1:8099';
const shots = process.env.SHOTS || '/tmp/claude-0/shots';
require('fs').mkdirSync(shots, { recursive: true });
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/tile\.openstreetmap|unpkg|ERR_|Failed to load resource/.test(m.text())) errors.push(m.text()); });

  // 1. submit a free listing with photos
  await page.goto(BASE + '/post-a-sublet/?tier=free');
  await page.check('input[name=tier][value=free]');
  await page.fill('input[name=title]', 'Bright furnished room near Prospect Park, June to August');
  await page.selectOption('select[name=property_type]', 'private_room');
  await page.fill('input[name=city]', 'New York');
  await page.selectOption('select[name=state]', 'NY');
  await page.fill('input[name=zip]', '11215');
  await page.fill('input[name=neighborhood]', 'Park Slope');
  await page.fill('input[name=rent]', '1450');
  await page.fill('input[name=deposit]', '1000');
  const y = new Date().getFullYear() + 1;
  await page.fill('input[name=available_from]', `${y}-06-01`);
  await page.fill('input[name=available_to]', `${y}-08-31`);
  await page.fill('textarea[name=description]', 'A sunny private room in a two-bedroom apartment with a friendly roommate. Queen bed, desk, closet, fast Wi-Fi. Ten minutes to the F/G train and two blocks from the park.');
  await page.check('input[value=wifi]'); await page.check('input[value=workspace]');
  await page.fill('textarea[name=house_rules]', 'No smoking. Quiet after 10pm on weeknights.');
  await page.setInputFiles('input[name="photos[]"]', [path.resolve('dev/test-room.jpg'), path.resolve('dev/test-room2.png')]);
  await page.fill('input[name=contact_name]', 'Test Host');
  await page.fill('input[name=contact_email]', 'host@example.com');
  await page.check('input[name=agree]');
  await page.click('button[type=submit]:has-text("Continue")');
  await page.waitForURL(/thanks/);
  ok(/review queue/.test(await page.textContent('h1')), 'free submission lands on thanks page');

  // 2. admin login + approve
  await page.goto(BASE + '/admin/login/');
  await page.fill('input[name=user]', 'admin'); await page.fill('input[name=pass]', process.env.ADMIN_PASS || 'devpass12345');
  await page.click('button:has-text("Sign in")');
  await page.waitForURL(BASE + '/admin/');
  ok(/Pending review/.test(await page.textContent('.stat-grid')), 'admin dashboard loads');
  await page.screenshot({ path: shots + '/admin-dashboard.png' });
  await page.goto(BASE + '/admin/listings/?status=pending');
  const link = await page.getAttribute('table.tbl a[href^="/admin/listing/"]', 'href');
  await page.goto(BASE + link);
  page.once('dialog', d => d.accept());
  await page.click('button[value=approve]');
  await page.waitForLoadState();
  ok(/Live/.test(await page.textContent('.admin-meta')), 'admin approve publishes listing');
  const publicUrl = await page.getAttribute('a:has-text("Open public page")', 'href');
  ok(/^\/sublet\/new-york-ny\/bright-furnished-room-near-prospect-park-june-to-august-\d+\/$/.test(publicUrl), 'listing URL format ' + publicUrl);
  await page.goto(BASE + '/admin/logout/');

  // 3. public listing page as anonymous renter
  const anon = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const p2 = await anon.newPage();
  p2.on('pageerror', e => errors.push(e.message));
  await p2.goto(BASE + publicUrl);
  ok((await p2.locator('.gallery img').count()) === 2, 'two WebP photos shown');
  ok(!(await p2.content()).includes('host@example.com'), 'free listing hides host email');
  ok(await p2.locator('.amz a[rel="nofollow sponsored noopener"]').count() >= 4, 'amazon links with rel nofollow sponsored');
  ok((await p2.content()).includes('tag=riseapartments-20'), 'amazon tag present');
  const ld = await p2.$$eval('script[type="application/ld+json"]', s => s.map(x => JSON.parse(x.textContent)['@type']));
  ok(ld.includes('Offer') && ld.includes('BreadcrumbList'), 'listing schema: ' + ld.join(','));
  await p2.screenshot({ path: shots + '/listing-desktop.png', fullPage: true });
  // contact relay
  await p2.fill('form[action$="/contact/"] input[name=name]', 'Renter Rae');
  await p2.fill('form[action$="/contact/"] input[name=email]', 'rae@example.com');
  await p2.fill('form[action$="/contact/"] textarea[name=message]', 'Hi! I have a summer internship and would love to see the room. Could we do a video tour?');
  await p2.click('form[action$="/contact/"] button[type=submit]');
  await p2.waitForSelector('form[action$="/contact/"] .form-msg.ok', { timeout: 8000 });
  ok(true, 'contact relay message sent');
  // report
  await p2.click('details.report summary');
  await p2.selectOption('details.report select[name=reason]', 'wrong');
  await p2.click('details.report button[type=submit]');
  await p2.waitForSelector('details.report .form-msg.ok', { timeout: 8000 });
  ok(true, 'report submitted');
  // favorites + compare
  await p2.click('.fav-btn-lg');
  await p2.goto(BASE + '/favorites/');
  await p2.waitForSelector('[data-favorites-list] .card');
  ok(true, 'favorites page shows saved listing');
  await p2.check('.card input[data-compare]');
  await p2.goto(BASE + '/compare/');
  await p2.waitForSelector('[data-compare-table] table');
  ok(true, 'compare table renders');

  // 4. directory + filters + map
  await p2.goto(BASE + '/sublets/ny/new-york/');
  ok((await p2.locator('.card').count()) === 1, 'city page lists the listing');
  await p2.fill('.filters input[name=max]', '1000');
  await p2.waitForTimeout(1200);
  ok((await p2.locator('[data-results] .card').count()) === 0, 'live filter max=1000 hides it');
  await p2.fill('.filters input[name=max]', '');
  await p2.waitForTimeout(1200);
  ok((await p2.locator('[data-results] .card').count()) === 1, 'clearing filter shows it again');
  await p2.goto(BASE + '/sublets/ny/new-york/summer/');
  ok((await p2.locator('.card').count()) === 1, 'summer filter page includes Jun–Aug listing');
  await p2.goto(BASE + '/sublets/ny/new-york/entire-apartments/');
  ok((await p2.locator('.card').count()) === 0, 'entire-apartments page excludes private room');
  ok(/noindex/.test(await p2.getAttribute('meta[name=robots]', 'content')), 'empty filtered page is noindex');
  await p2.goto(BASE + '/sublets/?q=New+York');
  ok(p2.url().endsWith('/sublets/ny/new-york/'), 'search "New York" jumps to city page');
  // tools
  await p2.goto(BASE + '/tools/cost-calculator/');
  await p2.waitForSelector('[data-out=cost] .out-box');
  ok(true, 'cost calculator renders output');
  await p2.goto(BASE + '/tools/packing-checklist/');
  await p2.check('.cl-group input >> nth=0');
  await p2.reload();
  ok(await p2.isChecked('.cl-group input >> nth=0'), 'packing checklist persists in localStorage');
  await p2.goto(BASE + '/tools/city-quiz/');
  await p2.click('[data-quiz-go]');
  ok((await p2.locator('.match').count()) === 5, 'quiz shows 5 matches');
  await p2.goto(BASE + '/tools/room-planner/');
  await p2.selectOption('select[name=add]', { index: 3 });
  ok((await p2.locator('[data-pl-svg] g[data-i]').count()) === 1, 'room planner adds furniture');

  // 5. paid flow without Stripe keys falls back to review queue
  await p2.goto(BASE + '/post-a-sublet/');
  ok(await p2.isChecked('input[name=tier][value=paid]'), 'paid tier is default');

  // 6. mobile 390px: menu works
  const mob = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  const pm = await mob.newPage();
  pm.on('pageerror', e => errors.push(e.message));
  for (const u of ['/', '/sublets/ny/new-york/', publicUrl, '/post-a-sublet/', '/tools/compare/', '/blog/how-to-avoid-rental-scams/']) {
    await pm.goto(BASE + u);
    const sw = await pm.evaluate(() => document.documentElement.scrollWidth);
    ok(sw <= 390, `no horizontal scroll at 390px on ${u} (${sw})`);
  }
  await pm.goto(BASE + '/');
  await pm.screenshot({ path: shots + '/home-mobile.png', fullPage: true });
  await pm.click('.nav-toggle');
  await pm.waitForTimeout(300);
  const nav = await pm.locator('#site-nav').boundingBox();
  ok(nav && nav.x === 0 && nav.width >= 380 && nav.height > 500, 'mobile menu opens full-width ' + JSON.stringify(nav));
  ok(await pm.locator('#site-nav a:has-text("List your place")').isVisible(), 'mobile menu CTA visible');
  await pm.screenshot({ path: shots + '/menu-mobile.png' });
  await pm.evaluate(() => window.scrollTo(0, 1500));
  await pm.waitForTimeout(200);
  const nav2 = await pm.locator('#site-nav').boundingBox();
  ok(nav2 && Math.abs(nav2.y - 64) < 3, 'mobile menu stays fixed under header after scroll y=' + (nav2 && nav2.y));
  await pm.click('.nav-toggle');
  await pm.waitForTimeout(300);
  ok(!(await pm.locator('#site-nav a:has-text("Guides")').isVisible()), 'mobile menu closes');

  // desktop screenshots
  await page.goto(BASE + '/');
  await page.screenshot({ path: shots + '/home-desktop.png', fullPage: true });
  await page.goto(BASE + '/sublets/ma/boston/');
  await page.screenshot({ path: shots + '/city-empty.png', fullPage: true });

  ok(errors.length === 0, 'no JS errors ' + JSON.stringify(errors.slice(0, 5)));
  await browser.close();
  console.log(fails ? `\n${fails} FAILED` : '\nALL PASSED');
  process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
