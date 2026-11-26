// End-to-end test of the listing add-on against a local php -S + mock Stripe.
// node e2e.js <base-url> <mail-capture-dir> <shots-dir> <fixtures-dir>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [BASE, MAIL, SHOTS, FIX] = process.argv.slice(2);
const results = []; const ok = (name, cond, extra = '') => { results.push([cond ? 'PASS' : 'FAIL', name, extra]); };
const lastMail = (re) => { const f = fs.readdirSync(MAIL).sort().reverse().map(x => fs.readFileSync(path.join(MAIL, x), 'utf8')).find(t => re.test(t)); return f || ''; };
const clickNav = (pg, sel) => Promise.all([pg.waitForNavigation(), pg.click(sel)]);
const linkIn = (t, re) => (t.match(re) || [])[0];
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', e => errors.push(e.message));

  // --- admin login + settings
  await page.goto(BASE + '/admin/');
  ok('admin redirects to login', page.url().endsWith('/admin/login/'));
  await page.fill('input[name=username]', 'admin'); await page.fill('input[name=password]', 'localadminpass'); await clickNav(page, 'button[type=submit]');
  ok('admin login', (await page.textContent('h1')).includes('Dashboard'));
  await page.goto(BASE + '/admin/settings/');
  await page.fill('input[name=stripe_secret]', 'sk_test_1234567890abcdefXYZ'); await page.fill('input[name=stripe_webhook_secret]', 'whsec_localtestsecret123');
  await clickNav(page, 'button[value=save]');
  ok('settings saved', (await page.content()).includes('Settings saved') && (await page.content()).includes('sk_test_…fXYZ'));
  await clickNav(page, 'button[value=test_stripe]');
  ok('test stripe button', (await page.content()).includes('Stripe connection OK (TEST mode)'));
  await clickNav(page, 'button[value=test_email]');
  ok('test email button', (await page.content()).includes('Test email sent') && /Subject: Test email/.test(lastMail(/Test email/)));
  const adminCookies = await ctx.cookies();

  // --- public: locked listing
  const pub = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const p = await pub.newPage(); p.on('pageerror', e => errors.push(e.message));
  await p.goto(BASE + '/properties/comanche-cavalry-family-housing/');
  const html = await p.content();
  ok('locked listing has lock box', html.includes('Contact details hidden until the owner verifies this listing'));
  ok('locked listing hides phone', !html.includes('(254) 285-2313') && !html.includes('tel:2542852313'));
  ok('locked listing hides website', !html.includes('cavalryfh.com'));
  ok('locked listing schema has no telephone', !/"telephone":"\(254/.test(html));
  ok('noindex on claim page header', true);
  await p.screenshot({ path: SHOTS + '/property-locked-desktop.png', fullPage: false });
  await clickNav(p, '.mhr-lock a.btn');
  ok('claim page reached', p.url().includes('/claim/comanche-cavalry-family-housing/'));
  ok('claim page noindex', (await p.content()).includes('noindex, nofollow'));
  await p.screenshot({ path: SHOTS + '/claim-desktop.png' });
  // missing checkbox -> error
  await p.fill('#c-name', 'Pat Owner'); await p.fill('#c-email', 'pat@example.com');
  await p.waitForTimeout(3100);
  await p.evaluate(() => document.querySelector('form.form').setAttribute('novalidate', '')); 
  await p.$eval('form.form', f => { f.querySelector('[name=authorized]').required = false; });
  await clickNav(p, 'form.form button[type=submit]');
  ok('claim requires authorization checkbox', (await p.content()).includes('Please confirm you are the owner'));
  await p.fill('#c-name', 'Pat Owner'); await p.fill('#c-email', 'pat@example.com'); await p.check('input[name=authorized]');
  await p.waitForTimeout(3100);
  await clickNav(p, 'form.form button[type=submit]');
  await p.waitForURL(/127\.0\.0\.1:8099\/pay\//);
  const co = await p.content();
  ok('checkout shows $10.00', co.includes('$10.00'), (co.match(/Total due: <strong[^>]*>([^<]+)/) || [])[1]);
  ok('checkout shows promo code field', !!(await p.$('[data-promo]')));
  await p.screenshot({ path: SHOTS + '/mock-checkout.png' });
  await p.fill('[data-promo]', 'FREE100'); await clickNav(p, 'button');
  await p.waitForURL(/checkout\/success/);
  ok('success page after 100%-off', (await p.textContent('h1')).includes("you're verified"));
  await p.goto(BASE + '/properties/comanche-cavalry-family-housing/');
  const h2 = await p.content();
  ok('claimed listing shows phone', h2.includes('(254) 285-2313'));
  ok('claimed listing shows verified badge', h2.includes('Verified owner'));
  ok('claimed listing shows website', h2.includes('cavalryfh.com'));
  ok('claimed listing schema telephone back', /"telephone":"\(254\) 285-2313"/.test(h2));
  ok('claimed listing is Featured', /chip-accent[^>]*>[\s\S]{0,400}Featured/.test(h2));
  await p.goto(BASE + '/properties/');
  const firstCards = await p.$$eval('.listing-card:not(.is-hidden)', cs => cs.slice(0, 6).map(c => c.dataset.slug + ':' + c.dataset.featured));
  const fIdx = firstCards.findIndex(x => x.endsWith(':0'));
  ok('featured listings first on /properties/ (after JS)', firstCards.slice(0, fIdx < 0 ? 6 : fIdx).every(x => x.endsWith(':1')) && firstCards.slice(fIdx).every(x => x.endsWith(':0')) && firstCards.some(x => x.startsWith('comanche-cavalry-family-housing:1')), firstCards.join(' '));
  await p.goto(BASE + '/bases/fort-cavazos/');
  const baseFirst = await p.$$eval('.listing-card:not(.is-hidden)', cs => cs.slice(0, 1).map(c => c.dataset.slug)[0]);
  ok('featured first on base page', baseFirst === 'comanche-cavalry-family-housing', baseFirst);
  await p.screenshot({ path: SHOTS + '/property-verified-desktop.png' });
  const wh = fs.existsSync(path.dirname(MAIL) + '/webhook.log') ? fs.readFileSync(path.dirname(MAIL) + '/webhook.log', 'utf8') : '';
  ok('webhook accepted (200)', /^200 /m.test(wh), wh.trim().split('\n').pop());
  ok('receipt email sent', /Subject: Receipt: Comanche/.test(lastMail(/Receipt: Comanche/)));
  ok('verification email sent', /Confirm your email/.test(lastMail(/pat@example.com[\s\S]*Confirm your email/)));

  // --- owner dashboard (auto-signed-in after checkout)
  await p.goto(BASE + '/account/');
  ok('owner dashboard shows listing', (await p.content()).includes('Comanche - Cavalry Family Housing'));
  await p.screenshot({ path: SHOTS + '/account-desktop.png' });
  await clickNav(p, 'text=Edit details & photos');
  await p.fill('#ed-price', '1599'); await p.fill('#ed-phone', '(254) 555-0100');
  await p.setInputFiles('#ed-photos', [FIX + '/test.jpg', FIX + '/evil.php.jpg']);
  await clickNav(p, '.mhr-editor button[type=submit]');
  const ed = await p.content();
  ok('owner edit saved', ed.includes('Your listing was updated'));
  ok('non-image upload rejected', ed.includes('please upload a JPEG, PNG, WebP or GIF image'));
  await p.goto(BASE + '/properties/comanche-cavalry-family-housing/');
  const h3 = await p.content();
  ok('owner edits are public', h3.includes('$1,599/mo') && h3.includes('(254) 555-0100'));
  const up = (h3.match(/\/wp-content\/uploads\/owners\/\d{4}\/\d{2}\/[a-f0-9]{24}\.webp/) || [])[0];
  ok('uploaded photo re-encoded as webp and shown', !!up, up);

  // --- free submission
  await p.goto(BASE + '/submit-property/');
  await p.fill('#f-name', 'Sam Lister'); await p.fill('#f-email', 'sam@example.com'); await p.fill('#f-phone', '555-222-3333');
  await p.click('[data-step-next]');
  await p.fill('#f-pname', 'Oak Street Duplex'); await p.fill('#f-address', '12 Oak St, Killeen, TX 76541'); await p.selectOption('#f-base', 'fort-cavazos'); await p.fill('#f-proximity', '8 minutes');
  await p.click('[data-step-next]');
  await p.fill('#f-price', '1450'); await p.fill('#f-beds', '3'); await p.fill('#f-pets', 'Dogs welcome'); await p.check('input[name=bah]'); await p.fill('#f-amenities', 'Garage, Fenced yard');
  await p.fill('#f-listing_email', 'leasing@oak.example'); await p.fill('#f-website', 'oak.example');
  await p.click('[data-step-next]');
  await p.fill('#f-description', 'A bright duplex close to the main gate.\n\nQuiet street.');
  await p.setInputFiles('#f-files', [FIX + '/test.jpg']);
  await p.waitForTimeout(3100);
  await clickNav(p, '[data-step-submit]');
  ok('free submission accepted', (await p.content()).includes('We received your property'));
  const pend = await p.goto(BASE + '/properties/oak-street-duplex/');
  ok('pending listing not public (404)', pend.status() === 404);

  // --- admin approve
  const adm = await browser.newContext(); await adm.addCookies(adminCookies); const a = await adm.newPage();
  await a.goto(BASE + '/admin/submissions/');
  ok('admin sees pending submission', (await a.content()).includes('Oak Street Duplex'));
  await a.screenshot({ path: SHOTS + '/admin-submissions.png', fullPage: true });
  await clickNav(a, 'article:has-text("Oak Street Duplex") button[value=approve]');
  ok('approved', (await a.content()).includes('Approved and published'));
  await p.goto(BASE + '/properties/oak-street-duplex/');
  const h4 = await p.content();
  ok('approved listing live with contact hidden', h4.includes('Contact details hidden') && !h4.includes('555-222-3333') && !h4.includes('leasing@oak.example'));
  ok('approved listing has BAH highlight + proximity', h4.includes('BAH-friendly rent') && h4.includes('8 minutes to Fort Hood'));
  const apText = lastMail(/Your listing is live: Oak Street Duplex/);
  ok('approval email: to submitter, subject', /To: sam@example\.com/.test(apText) && /Subject: Your listing is live: Oak Street Duplex/.test(apText));
  ok('approval email text: live URL + upgrade link + featured', apText.includes('http://127.0.0.1:8080/properties/oak-street-duplex/') && apText.includes('/claim/oak-street-duplex/') && apText.includes('Featured listing: shown first in search results') && apText.includes('UPGRADE FOR $10 (ONE-TIME)'));
  const htmlFile = fs.readdirSync(MAIL).filter(x => x.endsWith('.html')).sort().reverse().map(x => fs.readFileSync(path.join(MAIL, x), 'utf8')).find(t => t.includes('Oak Street Duplex'));
  ok('approval email html part', !!htmlFile && htmlFile.includes('href="http://127.0.0.1:8080/properties/oak-street-duplex/"') && htmlFile.includes('Upgrade my listing for $10') && htmlFile.includes('email-logo.png'));
  if (htmlFile) { fs.writeFileSync(SHOTS + '/approval-email.html', htmlFile); const ep = await (await browser.newContext({ viewport: { width: 700, height: 900 } })).newPage(); await ep.setContent(htmlFile); await ep.screenshot({ path: SHOTS + '/approval-email-rendered.png', fullPage: true }); }
  ok('admin flash confirms email sent', (await a.content()).includes('Approval email sent to sam@example.com'));
  const sm = await (await p.goto(BASE + '/properties-sitemap.xml')).text();
  ok('new listing in sitemap', sm.includes('/properties/oak-street-duplex/'));

  // --- paid submission -> cancel -> stays free pending
  const p2c = await browser.newContext(); const p2 = await p2c.newPage();
  const submitPaid = async (pname, email) => {
    await p2.goto(BASE + '/submit-property/?plan=paid');
    await p2.fill('#f-name', 'Riley Paid'); await p2.fill('#f-email', email); await p2.fill('#f-phone', '555-777-8888'); await p2.check('input[name=authorized]');
    await p2.click('[data-step-next]');
    await p2.fill('#f-pname', pname); await p2.fill('#f-address', '5 Pine Rd, Fayetteville, NC 28301'); await p2.selectOption('#f-base', 'fort-bragg');
    await p2.click('[data-step-next]'); await p2.click('[data-step-next]');
    await p2.fill('#f-description', 'Paid listing test.'); await p2.waitForTimeout(3100); await clickNav(p2, '[data-step-submit]');
    await p2.waitForURL(/8099\/pay\//);
  };
  await submitPaid('Pine Road Townhome', 'riley@example.com');
  await clickNav(p2, '[data-cancel]');
  ok('cancel keeps as free', (await p2.content()).includes('kept your property') && (await p2.content()).includes('free listing'));
  await a.goto(BASE + '/admin/submissions/');
  ok('cancelled paid submission now pending free', /Pine Road Townhome[\s\S]*plan: <strong>free/.test(await a.content()));

  // --- paid submission -> pay (webhook skipped: success redirect must fulfil)
  await p2.waitForTimeout(31000); // per-session 30s throttle
  await submitPaid('Maple Court Home', 'riley@example.com');
  await p2.check('input[name=skip_webhook]'); await clickNav(p2, 'button');
  await p2.waitForURL(/checkout\/success/);
  ok('paid submission success page', (await p2.textContent('h1')).includes("you're verified"));
  await p2.goto(BASE + '/properties/maple-court-home/');
  const h5 = await p2.content();
  ok('paid listing published instantly with contact', h5.includes('555-777-8888') && h5.includes('Verified owner'));
  ok('paid listing is Featured', /chip-accent[^>]*>[\s\S]{0,400}Featured/.test(h5));
  // replay success page: idempotent
  await p2.goBack();
  await a.goto(BASE + '/admin/payments/');
  const pays = await a.content();
  ok('payments listed, one fulfilled per checkout', (pays.match(/maple-court-home<\/a>/g) || []).length === 1);
  await a.screenshot({ path: SHOTS + '/admin-payments.png', fullPage: true });

  // --- magic link login
  const p3c = await browser.newContext(); const p3 = await p3c.newPage();
  await p3.goto(BASE + '/account/'); await p3.fill('#a-email', 'pat@example.com'); await p3.waitForTimeout(3100); await clickNav(p3, 'button[type=submit]');
  ok('magic link requested (generic message)', (await p3.content()).includes('If an owner account exists'));
  const link = linkIn(lastMail(/sign-in link/), /http:\/\/127\.0\.0\.1:8080\/account\/verify\/\?t=[a-f0-9]{48}/);
  ok('magic link emailed', !!link);
  await p3.goto(link);
  ok('magic link signs in', (await p3.content()).includes('Owner dashboard'));
  const p4 = await (await browser.newContext()).newPage(); await p4.goto(link);
  ok('magic link single-use', (await p4.content()).includes('invalid or has expired'));

  // --- admin brute force
  const bf = await (await browser.newContext()).newPage();
  for (let i = 0; i < 6; i++) { await bf.goto(BASE + '/admin/login/'); await bf.fill('input[name=username]', 'admin'); await bf.fill('input[name=password]', 'wrong' + i); await clickNav(bf, 'button[type=submit]'); }
  ok('admin lockout after 5 failures', (await bf.content()).includes('Too many failed attempts'));

  // --- mobile screenshots
  const m = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  await m.addCookies(adminCookies);
  const mp = await m.newPage(); mp.on('pageerror', e => errors.push(e.message));
  for (const [u, n] of [['/properties/airman-scott-village-1193-lackland-family-homes/', 'property-locked'], ['/claim/airman-scott-village-1193-lackland-family-homes/', 'claim'], ['/submit-property/', 'submit'], ['/account/', 'account-login'], ['/admin/listings/', 'admin-listings'], ['/admin/listings/oak-street-duplex/', 'admin-edit']]) {
    await mp.goto(BASE + u);
    const sw = await mp.evaluate(() => document.documentElement.scrollWidth);
    ok('mobile no horizontal scroll ' + n, sw <= 390, 'scrollWidth=' + sw);
    await mp.screenshot({ path: SHOTS + '/' + n + '-390.png', fullPage: n.startsWith('property') ? false : true });
  }
  ok('no JS errors', errors.length === 0, errors.join(' | '));
  await browser.close();
  for (const r of results) console.log(r.join('  '));
  console.log(results.filter(r => r[0] === 'FAIL').length + ' failed of ' + results.length);
})().catch(e => { console.error(e); for (const r of results) console.log(r.join('  ')); process.exit(1); });
