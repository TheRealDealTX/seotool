// Live smoke test after deploy: admin login, free submission -> approve, claim
// page, then permanently removes the test listing through the admin panel.
// node live-smoke.js <base> <shots-dir> <secrets.json with admin_user/admin_pass> <test.jpg>
const { chromium } = require('playwright'); const fs = require('fs');
const [BASE, SHOTS, SEC, IMG] = process.argv.slice(2); const sec = JSON.parse(fs.readFileSync(SEC));
const R = []; const ok = (n, c, x = '') => R.push([c ? 'PASS' : 'FAIL', n, x]);
(async () => {
  const b = await chromium.launch(); const errs = [];
  const a = await (await b.newContext({ viewport: { width: 1280, height: 900 } })).newPage(); a.on('pageerror', e => errs.push(e.message));
  await a.goto(BASE + '/admin/login/'); await a.fill('input[name=username]', sec.admin_user); await a.fill('input[name=password]', sec.admin_pass); await a.click('button[type=submit]');
  ok('admin login', (await a.textContent('h1')).includes('Dashboard'));
  const dash = await a.content();
  ok('dashboard: Stripe keys missing warning', dash.includes("Stripe isn't set up yet"));
  ok('dashboard: SMTP password missing warning', dash.includes('SMTP password'));
  await a.screenshot({ path: SHOTS + '/live-admin-dashboard.png', fullPage: true });
  await a.goto(BASE + '/admin/messages/'); const msgs = (await a.$$('details.mhr-msg')).length; ok('old messages imported', msgs >= 18, msgs + ' messages');

  const u = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage(); u.on('pageerror', e => errs.push(e.message));
  await u.goto(BASE + '/submit-property/');
  await u.fill('#f-name', 'Claude Test'); await u.fill('#f-email', 'test-noreply@example.com'); await u.fill('#f-phone', '555-010-0000'); await u.click('[data-step-next]');
  await u.fill('#f-pname', 'ZZ Test Listing Delete Me'); await u.fill('#f-address', '1 Test Way, Killeen, TX 76541'); await u.selectOption('#f-base', 'fort-cavazos'); await u.click('[data-step-next]');
  await u.fill('#f-price', '1234'); await u.click('[data-step-next]');
  await u.fill('#f-description', 'Automated deployment test. This listing will be deleted.'); await u.setInputFiles('#f-files', [IMG]);
  await u.waitForTimeout(3200); await u.click('[data-step-submit]');
  ok('free submission', (await u.content()).includes('We received your property'));
  await a.goto(BASE + '/admin/submissions/');
  ok('pending visible to admin', (await a.content()).includes('ZZ Test Listing Delete Me'));
  await a.click('article:has-text("ZZ Test Listing Delete Me") button[value=approve]');
  ok('approve', (await a.content()).includes('Approved and published'));
  const r = await u.goto(BASE + '/properties/zz-test-listing-delete-me/'); const h = await u.content();
  ok('approved listing live, contact hidden', r.status() === 200 && h.includes('Contact details hidden') && !h.includes('555-010-0000'));
  ok('uploaded photo served', /\/wp-content\/uploads\/owners\/\d{4}\/\d{2}\/[a-f0-9]{24}\.webp/.test(h));
  await u.screenshot({ path: SHOTS + '/live-test-listing-390.png' });

  await u.goto(BASE + '/claim/zz-test-listing-delete-me/');
  await u.fill('#c-name', 'Claude Test'); await u.fill('#c-email', 'test-noreply@example.com'); await u.check('input[name=authorized]');
  await u.waitForTimeout(3200); await u.click('form.form button[type=submit]');
  const after = await u.content();
  if (after.includes('Online payments are not available')) ok('claim: payments not configured yet (expected before keys)', true);
  else ok('claim redirects to Stripe Checkout', u.url().startsWith('https://checkout.stripe.com/'), u.url());
  if (u.url().startsWith('https://checkout.stripe.com/')) {
    await u.waitForTimeout(4000); const t = await u.textContent('body');
    ok('Stripe page shows $10.00', t.includes('$10.00')); ok('Stripe page has promo code field', /promotion code/i.test(t));
    await u.screenshot({ path: SHOTS + '/live-stripe-checkout-390.png' });
  }

  await a.goto(BASE + '/admin/listings/zz-test-listing-delete-me/');
  await a.check('.mhr-danger input[name=confirm]'); await a.click('.mhr-danger button[value=purge]');
  ok('test listing purged', (await a.content()).includes('Permanently deleted'));
  const g = await u.goto(BASE + '/properties/zz-test-listing-delete-me/'); ok('test listing gone (404)', g.status() === 404);
  ok('no JS errors', errs.length === 0, errs.join('|'));
  await b.close(); R.forEach(x => console.log(x.join('  '))); console.log(R.filter(x => x[0] === 'FAIL').length + ' failed of ' + R.length);
})().catch(e => { console.error(e); R.forEach(x => console.log(x.join('  '))); });
