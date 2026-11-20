const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const BASE = 'http://127.0.0.1:8099';
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
const lastLink = () => { const m = fs.readFileSync('dev/mail.log', 'utf8').match(/http:\/\/127\.0\.0\.1:8099\/auth\/[a-f0-9]+\//g); return m && m[m.length - 1]; };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext(); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  // verified listing before email verification: contact hidden
  await p.goto(BASE + '/sublets/ma/boston/');
  const href = await p.getAttribute('.card-title a', 'href');
  await p.goto(BASE + href);
  ok(await p.locator('.badge-verified').count() > 0, 'verified badge shown');
  ok(!(await p.content()).includes('pat@example.com'), 'contact hidden until owner verifies email');
  ok(await p.locator('.g-empty a:has-text("Add Photos")').count() === 1, 'no-photo placeholder with Add Photos button');
  await p.click('.g-empty a:has-text("Add Photos")');
  ok(/\/manage\/\d+\//.test(p.url()), 'Add Photos goes to manage page');
  // login
  await p.goto(BASE + '/login/');
  await p.fill('input[name=email]', 'pat@example.com');
  await p.click('button[type=submit]');
  await p.waitForSelector('.flash-ok');
  const link = lastLink(); ok(!!link, 'magic link emailed ' + link);
  await p.goto(link);
  await p.click('button:has-text("Sign in")');
  await p.waitForURL(BASE + '/account/');
  ok(/Your listings/.test(await p.textContent('h1')), 'dashboard after magic link');
  // reused link fails
  const p2 = await (await b.newContext()).newPage(); await p2.goto(link);
  ok(/expired/.test(await p2.textContent('h1')), 'magic link is single-use');
  // edit + photo
  await p.click('a:has-text("Edit")');
  await p.fill('input[name=title]', 'Entire furnished 1BR in Back Bay — ideal for travel nurses');
  await p.setInputFiles('input[name="photos[]"]', [path.resolve('dev/test-room.jpg')]);
  await p.click('button:has-text("Save changes")');
  await p.waitForSelector('.flash-ok');
  ok(/Added 1 photo/.test(await p.textContent('.flash-ok')), 'owner edit saved with photo');
  // public page now shows contact
  await p.goto(BASE + '/account/');
  const pub = await p.getAttribute('.dash-item h2 a', 'href');
  const anon = await (await b.newContext()).newPage();
  await anon.goto(BASE + pub);
  ok((await anon.content()).includes('pat@example.com') && (await anon.content()).includes('617-555-0100'), 'verified + email-verified listing shows contact details');
  ok(await anon.locator('.gallery img').count() === 1, 'photo visible');
  // old slug redirects to canonical
  await anon.goto(BASE + pub.replace(/[a-z0-9-]+-(\d+)\/$/, 'old-slug-$1/'));
  ok(anon.url() === BASE + pub, 'old slug 301s to canonical');
  // mark rented
  await p.goto(BASE + '/account/');
  await p.click('button[value=rented]');
  await p.waitForSelector('.flash-ok');
  ok(/Rented/.test(await p.textContent('.dash-item')), 'marked rented');
  await p.click('button[value=activate]');
  await p.waitForSelector('.flash-ok');
  ok(/Live/.test(await p.textContent('.dash-item')), 're-activated');
  ok(errs.length === 0, 'no JS errors ' + errs.join('|'));
  await b.close(); console.log(fails ? fails + ' FAILED' : 'ALL PASSED'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
