// Functional browser tests: navigation, form (JS path), calculator math, checklist, storm tools.
// Usage: NODE_PATH=$(npm root -g) node tools/test/functional.js   (server on BASE, default :8081)
const { chromium } = require('playwright');
const base = process.env.BASE || 'http://127.0.0.1:8081';
let failures = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS ' : 'FAIL ') + msg); if (!cond) failures++; };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));

  // Calculator math (pure function) against hand-checked cases.
  await page.goto(base + '/claim-calculator/');
  const cases = await page.evaluate(() => {
    const c = window.mpaCalc;
    return [
      c({ rcv: 24000, dep: 7200, depmode: 'amt', ded: 5000, prev: 0, noncov: 0, limit: 0, rc: true }),
      c({ rcv: 24000, dep: 30, depmode: 'pct', ded: 5000, prev: 4000, noncov: 2000, limit: 0, rc: true }),
      c({ rcv: 24000, dep: 7200, depmode: 'amt', ded: 5000, prev: 0, noncov: 0, limit: 0, rc: false }),
      c({ rcv: 300000, dep: 0, depmode: 'amt', ded: 5000, prev: 0, noncov: 0, limit: 250000, rc: true }),
      c({ rcv: 4000, dep: 1000, depmode: 'amt', ded: 5000, prev: 0, noncov: 0, limit: 0, rc: true }),
    ];
  });
  const [a, b, c, d, e] = cases;
  ok(a.acv === 16800 && a.initial === 11800 && a.recoverable === 7200 && a.total === 19000 && a.oop === 5000, 'calc: basic RC example');
  // covered 22000; dep 6600; acv 15400; initialGross 10400; maxPay 17000; recov 6600; initial net 6400; remaining 13000; oop 24000-17000=7000
  ok(b.rcv === 22000 && b.dep === 6600 && b.acv === 15400 && b.initial === 6400 && b.recoverable === 6600 && b.remaining === 13000 && b.total === 17000 && b.oop === 7000, 'calc: % depreciation, non-covered, prior payment');
  ok(c.total === 11800 && c.recoverable === 0 && c.oop === 12200, 'calc: ACV policy');
  ok(d.total === 250000 && d.oop === 50000, 'calc: policy limit cap');
  ok(e.total === 0 && e.oop === 4000 && e.warnings.length > 0, 'calc: deductible exceeds loss');
  // UI: example button fills results.
  await page.click('[data-example]');
  ok((await page.textContent('[data-out="total"]')) === '$19,000', 'calc UI: example shows $19,000 total');
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('[data-download]')]);
  ok(/claim-settlement-estimate\.txt$/.test(dl.suggestedFilename()), 'calc UI: report downloads');

  // Checklist.
  await page.goto(base + '/claim-documentation-checklist/');
  await page.click('[data-cat="hail"]');
  const total = await page.$$eval('[data-item]', els => els.length);
  await page.check('[data-item="photos"]');
  await page.check('[data-item="h-softmetal"]');
  const count = await page.textContent('[data-cl-count]');
  ok(count === `2 of ${total} complete`, 'checklist: progress ' + count);
  await page.check('[data-cl-save]');
  await page.reload();
  ok(await page.isChecked('[data-item="photos"]'), 'checklist: progress saved in localStorage when opted in');
  const [dl2] = await Promise.all([page.waitForEvent('download'), page.click('[data-cl-download]')]);
  ok(/checklist-hail\.txt$/.test(dl2.suggestedFilename()), 'checklist: download');
  page.once('dialog', dlg => dlg.accept());
  await page.click('[data-cl-reset]');
  ok((await page.textContent('[data-cl-count]')).startsWith('0 of'), 'checklist: reset');

  // Storm history filters.
  await page.goto(base + '/storm-history/', { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => /matching event/.test(document.querySelector('[data-count-label]').textContent), null, { timeout: 15000 });
  await page.selectOption('#f-type', 'hail');
  await page.selectOption('#f-hail', '2.75');
  await page.waitForTimeout(400);
  const lbl = await page.textContent('[data-count-label]');
  ok(/^12 matching/.test(lbl), 'storm history: baseball+ hail filter → ' + lbl);
  await page.fill('#f-loc', 'McAllen');
  await page.waitForTimeout(400);
  ok(/^1 matching/.test(await page.textContent('[data-count-label]')), 'storm history: location filter (McAllen 4.5" hail)');

  // Storm lookup.
  await page.goto(base + '/storm-lookup/', { waitUntil: 'domcontentloaded' });
  await page.fill('#l-where', '78504');
  await page.fill('#l-date', '2025-05-08');
  await page.click('[data-lookup] button[type="submit"]');
  await page.waitForFunction(() => /report/.test(document.querySelector('[data-lookup-results]').textContent), null, { timeout: 15000 });
  const res = await page.textContent('[data-lookup-results]');
  ok(/\d+ reports? within 5 miles of ZIP 78504/.test(res) && /Hail/.test(res), 'storm lookup: ZIP 78504 around May 8, 2025 finds hail');
  await page.fill('#l-where', 'Nowhereville');
  await page.click('[data-lookup] button[type="submit"]');
  ok(/Hidalgo County city/.test(await page.textContent('[data-lookup-status]')), 'storm lookup: unknown place message');

  // Form via JavaScript (requires the local SMTP sink).
  await page.goto(base + '/contact/');
  await page.click('button[type="submit"]');
  ok((await page.$$('.field.has-error')).length >= 6, 'form: client-side validation shows errors');
  await page.fill('[name="full_name"]', 'Browser Test');
  await page.fill('[name="phone"]', '(956) 555-0101');
  await page.fill('[name="email"]', 'browser@example.com');
  await page.fill('[name="location"]', 'Mission');
  await page.selectOption('[name="claim_type"]', 'Wind / storm damage');
  await page.selectOption('[name="claim_status"]', 'Claim underpaid / low offer');
  await page.fill('[name="message"]', 'Wind took shingles off after the storm.');
  await page.check('[name="privacy_ack"]');
  await page.waitForTimeout(3200);
  await page.click('button[type="submit"]');
  await page.waitForFunction(() => document.querySelector('.form-success') || !document.querySelector('button[type="submit"].is-loading'), null, { timeout: 25000 });
  await page.waitForTimeout(300);
  const done = (await page.textContent('form[data-claim-form] .form-success, form[data-claim-form] .form-status').catch(() => '')) || '';
  ok(/Thank you! Your Free Claim Review request has been received/.test(done), 'form: JS submission success message ' + done.slice(0, 200).replace(/\s+/g, ' '));

  // Mobile navigation.
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto(base + '/');
  await m.click('.nav-toggle');
  ok(await m.isVisible('#main-nav a[href="/about-us/"]'), 'mobile nav opens');
  await m.click('.nav-item.has-sub .sub-toggle');
  ok(await m.isVisible('a[href="/services/hail-damage-claims/"]'), 'mobile submenu opens');
  await m.keyboard.press('Escape');
  ok(!(await m.isVisible('#main-nav a[href="/about-us/"]')), 'mobile nav closes with Escape');
  ok(await m.isVisible('.mobile-bar-call'), 'sticky mobile call bar visible');

  ok(errors.length === 0, 'no JavaScript errors ' + errors.join(' | '));
  await browser.close();
  console.log(failures ? `\n${failures} FAILURE(S)` : '\nALL PASSED');
  process.exit(failures ? 1 : 0);
})();
