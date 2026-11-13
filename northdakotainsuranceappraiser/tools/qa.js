// Interactive QA: drawer, logo hover, tool math. Usage: node tools/qa.js <baseURL>
const { chromium, devices } = require('playwright');
const base = process.argv[2] || 'http://127.0.0.1:8091';
const T = '/claim-planning-tools/';
let fails = 0;
const ok = (cond, msg) => { console.log((cond ? 'PASS ' : 'FAIL ') + msg); if (!cond) fails++; };
const near = (a, b, tol = 0.6) => Math.abs(a - b) <= tol;
const money = s => parseFloat(String(s).replace(/[^0-9.\-−]/g, '').replace('−', '-'));

(async () => {
  const browser = await chromium.launch();

  // ---------- mobile drawer ----------
  const m = await browser.newContext({ ...devices['iPhone 13'] });
  const p = await m.newPage();
  await p.goto(base + '/', { waitUntil: 'networkidle' });
  const drawerState = () => p.evaluate(() => {
    const d = document.querySelector('#drawer');
    const r = d.getBoundingClientRect();
    return { open: document.body.classList.contains('drawer-open'), inert: d.hasAttribute('inert'), hidden: d.getAttribute('aria-hidden'),
      lock: getComputedStyle(document.body).overflow, vis: getComputedStyle(d).visibility, shadow: getComputedStyle(d).boxShadow, left: Math.round(r.left), exp: document.querySelector('.burger').getAttribute('aria-expanded') };
  });
  let s = await drawerState();
  ok(!s.open && s.inert && s.hidden === 'true' && s.vis === 'hidden' && s.shadow === 'none', `drawer closed state: inert, aria-hidden, hidden, no shadow (${JSON.stringify(s)})`);
  await p.click('.burger');
  await p.waitForTimeout(450);
  s = await drawerState();
  ok(s.open && !s.inert && s.hidden === 'false' && s.lock === 'hidden' && s.vis === 'visible' && s.shadow !== 'none' && s.left < 390 && s.exp === 'true', `drawer opens with scroll lock + shadow (${JSON.stringify(s)})`);
  // expand Locations accordion and tap a link
  await p.click('#drawer .acc-btn:has-text("Locations")');
  await p.waitForTimeout(400);
  const accOpen = await p.getAttribute('#drawer .acc-btn:has-text("Locations")', 'aria-expanded');
  ok(accOpen === 'true', 'accordion section expands');
  const linkVisible = await p.isVisible('#drawer a[href="/across-north-dakota/minot/"]');
  ok(linkVisible, 'accordion link visible after expand');
  await Promise.all([p.waitForNavigation(), p.click('#drawer a[href="/across-north-dakota/minot/"]')]);
  ok(p.url() === base + '/across-north-dakota/minot/', 'drawer link lands on ' + p.url());
  // close three ways
  for (const how of ['x', 'overlay', 'escape']) {
    await p.click('.burger'); await p.waitForTimeout(400);
    if (how === 'x') await p.click('.drawer-close');
    if (how === 'overlay') await p.mouse.click(15, 400);
    if (how === 'escape') await p.keyboard.press('Escape');
    await p.waitForTimeout(450);
    s = await drawerState();
    ok(!s.open && s.inert && s.lock !== 'hidden' && s.vis === 'hidden', `drawer closes via ${how}`);
  }
  await m.close();

  // ---------- desktop: logo hover ----------
  const d = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const q = await d.newPage();
  await q.goto(base + '/across-north-dakota/fargo/', { waitUntil: 'networkidle' });
  for (const sel of ['.head .brand', '.foot .brand']) {
    if (sel.startsWith('.foot')) await q.locator(sel).scrollIntoViewIfNeeded();
    else { await q.mouse.wheel(0, 600); await q.waitForTimeout(400); }
    const get = () => q.evaluate(x => { const el = document.querySelector(x); const cs = getComputedStyle(el); const b = el.querySelector('b'); return cs.color + '|' + getComputedStyle(b).color + '|' + cs.textDecorationLine + '|' + getComputedStyle(b).textDecorationLine; }, sel);
    await q.mouse.move(5, 5);
    const before = await get();
    await q.hover(sel); await q.waitForTimeout(300);
    const after = await get();
    ok(before === after && !after.includes('underline'), `${sel} unchanged on hover (${before} -> ${after})`);
  }
  // drawer brand (mobile) hover check via forced state is covered by CSS rule; check computed color
  // ---------- tools ----------
  const fill = async (sel, v) => { await q.fill(sel, String(v)); await q.dispatchEvent(sel, 'input'); };
  const txt = sel => q.textContent(sel);

  await q.goto(base + T + 'award-break-even-calculator/', { waitUntil: 'networkidle' });
  await fill('#g-ins', 20000); await fill('#g-own', 30000);
  await q.$eval('#g-land', el => { el.value = 50; el.dispatchEvent(new Event('input', { bubbles: true })); });
  await q.selectOption('#g-ft', 'flat'); await fill('#g-fee', 2000); await fill('#g-ump', 3000);
  // gap 10000, award 25000, gain 5000, cost 2000+1500=3500, net 1500, break-even 35%
  ok(money(await txt('[data-o=gap]')) === 10000 && money(await txt('[data-o=award]')) === 25000 && money(await txt('[data-o=cost]')) === 3500 && money(await txt('[data-o=net]')) === 1500, 'gap estimator flat-fee math');
  ok((await txt('[data-o=breakeven]')).startsWith('35%'), 'break-even = 35% of gap: ' + await txt('[data-o=breakeven]'));
  await q.selectOption('#g-ft', 'pct'); await fill('#g-fee', 20);
  // cost = 5000*0.2 + 1500 = 2500, net 2500, BE = 1500/(10000*0.8)=18.75 -> 19%
  ok(money(await txt('[data-o=net]')) === 2500 && (await txt('[data-o=breakeven]')).startsWith('19%'), 'gap estimator percent-fee math');

  await q.goto(base + T + 'two-check-payout-calculator/', { waitUntil: 'networkidle' });
  // defaults: 21400 (11/30), 9600 (14/40), 2300 (5/10), ded 1500, cap 80%
  const dep = 21400 * 11 / 30 + 9600 * 14 / 40 + 2300 * 0.5;
  const rcv = 21400 + 9600 + 2300, acv = rcv - dep;
  ok(near(money(await txt('[data-o=rcv]')), rcv, 1) && near(money(await txt('[data-o=acv]')), acv, 1) && near(money(await txt('[data-o=first]')), acv - 1500, 1) && near(money(await txt('[data-o=total]')), rcv - 1500, 1), `payout calculator RCV ${rcv} ACV ${acv.toFixed(0)}`);
  await q.click('[data-add]'); await q.waitForTimeout(100);
  ok((await q.$$('.items-table tbody tr')).length === 4, 'add line item');

  await q.goto(base + T + 'roof-area-ice-barrier-calculator/', { waitUntil: 'networkidle' });
  // 52x30, oh 16in -> (52+2.667)*(30+2.667)=1785.8; 5/12 mult 1.0833 -> 1934.6 sf, 19.35 sq
  const foot = (52 + 32 / 12) * (30 + 32 / 12), mult = Math.sqrt(1 + (5 / 12) ** 2);
  ok(near(parseFloat(await txt('[data-o=sq]')), foot * mult / 100, 0.01) && (await txt('[data-o=mult]')) === mult.toFixed(3), `roof squares ${(foot * mult / 100).toFixed(2)}`);
  // ice barrier: (16+24)*1.0833=43.3in -> 2 courses; eaves 2*(52+2.667)=109.3 -> 219 lf
  ok((await txt('[data-o=courses]')).startsWith('2 courses') && money(await txt('[data-o=icelf]')) === Math.round(2 * (52 + 32 / 12) * 2), 'ice-barrier courses/lf: ' + await txt('[data-o=courses]') + ' / ' + await txt('[data-o=icelf]'));

  await q.goto(base + T + 'hail-deductible-dollar-converter/', { waitUntil: 'networkidle' });
  await fill('#w-a', 340000); await q.selectOption('#w-p', '2'); await fill('#w-f', 1500); await fill('#w-l', 18700);
  ok(money(await txt('[data-o=pd]')) === 6800 && money(await txt('[data-o=pdpay]')) === 11900 && money(await txt('[data-o=flatpay]')) === 17200 && money(await txt('[data-o=diff]')) === 5300, 'percentage deductible math');

  await q.goto(base + T + 'policy-clock-freeze-up-planner/', { waitUntil: 'networkidle' });
  await q.fill('#t-d', '2026-07-01'); await q.dispatchEvent('#t-d', 'change');
  const items = await q.$$eval('[data-o=timeline] li', l => l.map(x => x.textContent));
  ok(items.length === 6 && items[0].includes('Jul 3, 2026') && items.some(t => t.includes('Jul 1, 2027')) && items.some(t => t.includes('Jun 30, 2028')) && items.some(t => t.includes('Nov 28, 2026')), 'timeline dates (6 items): ' + items.map(t => t.slice(0, 22)).join(' / '));
  const [dl] = await Promise.all([q.waitForEvent('download'), q.click('[data-ics]')]);
  const fs = require('fs'); const pth = await dl.path(); const ics = fs.readFileSync(pth, 'utf8');
  ok(dl.suggestedFilename() === 'north-dakota-claim-timeline.ics' && ics.includes('BEGIN:VCALENDAR') && (ics.match(/BEGIN:VEVENT/g) || []).length === 6 && ics.includes('DTSTART;VALUE=DATE:20260703'), '.ics export with 6 events');

  await q.goto(base + T + 'claim-file-strength-test/', { waitUntil: 'networkidle' });
  const lis = await q.$$('.quiz li');
  for (let i = 0; i < lis.length; i++) await (await lis[i].$(i < 3 ? '.yes' : '.no')).click();
  // weights first three = 3+3+3 = 9 of total 25 -> 36%
  ok((await txt('[data-o=score]')).trim() === '36' && (await q.$$('[data-o=todo] li')).length === 9, 'readiness score 36 with 9 to-dos: ' + await txt('[data-o=score]'));

  await q.goto(base + T + 'snow-ice-roof-weight-estimator/', { waitUntil: 'networkidle' });
  await fill('#s-d', 24); await q.selectOption('#s-t', '20'); await fill('#s-i', 2); await fill('#s-a', 1500); await fill('#s-c', 40);
  // snow 2ft*20=40, ice 2/12*57=9.5 -> 49.5 psf; 74,250 lb; 124%
  ok((await txt('[data-o=psf]')).startsWith('49.5') && money(await txt('[data-o=lbs]')) >= 74250 && (await txt('[data-o=share]')) === '124%', 'snow load math: ' + await txt('[data-o=psf]') + ' ' + await txt('[data-o=lbs]') + ' ' + await txt('[data-o=share]'));

  // home mini gap check
  await q.goto(base + '/', { waitUntil: 'networkidle' });
  ok(money(await txt('#gap-check [data-o=gap]')) === 12600, 'home gap check default gap 12,600');
  // glossary filter
  await q.goto(base + '/appraisal-terms-a-z/', { waitUntil: 'networkidle' });
  await q.fill('#gloss-filter', 'umpire'); await q.dispatchEvent('#gloss-filter', 'input');
  const vis = await q.$$eval('.glossary dt', l => l.filter(x => !x.hidden).length);
  await q.fill('#gloss-filter', 'zzzzqq'); await q.dispatchEvent('#gloss-filter', 'input');
  ok(vis > 0 && await q.isVisible('.gloss-none'), `glossary filter (${vis} hits for umpire; no-match message shown)`);
  // region tabs
  await q.goto(base + '/', { waitUntil: 'networkidle' });
  await q.click('#tab-badlands');
  ok(await q.isVisible('#panel-badlands') && !(await q.isVisible('#panel-redriver')), 'region tabs switch panels');

  await browser.close();
  console.log(fails ? `${fails} FAILED` : 'ALL PASS');
  process.exit(fails ? 1 : 0);
})();
