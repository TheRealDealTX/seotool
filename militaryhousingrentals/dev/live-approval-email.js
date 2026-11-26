// Live check of the approval email: submit a free test listing as the site
// mailbox, approve it in admin (sends the email), then permanently remove it.
// node live-approval-email.js <base> <secrets.json> <test.jpg> <to-email>
const { chromium } = require('playwright'); const fs = require('fs');
const [BASE, SEC, IMG, TO] = process.argv.slice(2); const sec = JSON.parse(fs.readFileSync(SEC));
(async () => {
  const b = await chromium.launch();
  const u = await (await b.newContext()).newPage();
  const nav = (pg, sel) => Promise.all([pg.waitForNavigation(), pg.click(sel)]);
  await u.goto(BASE + '/submit-property/');
  await u.fill('#f-name', 'Site Owner'); await u.fill('#f-email', TO); await u.fill('#f-phone', '555-010-0000'); await u.click('[data-step-next]');
  await u.fill('#f-pname', 'ZZ Approval Email Test'); await u.fill('#f-address', '1 Test Way, Killeen, TX 76541'); await u.selectOption('#f-base', 'fort-cavazos'); await u.click('[data-step-next]');
  await u.click('[data-step-next]');
  await u.fill('#f-description', 'Automated test of the approval email. This listing is removed right after.');
  await u.waitForTimeout(3200); await nav(u, '[data-step-submit]');
  console.log('submitted:', (await u.content()).includes('We received your property'));
  const a = await (await b.newContext()).newPage();
  await a.goto(BASE + '/admin/login/'); await a.fill('input[name=username]', sec.admin_user); await a.fill('input[name=password]', sec.admin_pass); await nav(a, 'button[type=submit]');
  await a.goto(BASE + '/admin/submissions/');
  await nav(a, 'article:has-text("ZZ Approval Email Test") button[value=approve]');
  const flash = (await a.textContent('.notice')).trim();
  console.log('admin flash:', flash);
  const r = await u.goto(BASE + '/properties/zz-approval-email-test/'); console.log('listing live:', r.status());
  await a.goto(BASE + '/admin/listings/zz-approval-email-test/');
  await a.check('.mhr-danger input[name=confirm]'); await nav(a, '.mhr-danger button[value=purge]');
  console.log('purged:', (await a.content()).includes('Permanently deleted'));
  console.log('gone:', (await u.goto(BASE + '/properties/zz-approval-email-test/')).status());
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
