// Screenshot + layout checks. Usage: node tools/shots.js <baseURL> <outDir> [paths...]
const { chromium, devices } = require('playwright');
const fs = require('fs');
const base = process.argv[2] || 'http://127.0.0.1:8090';
const out = process.argv[3] || 'shots';
const paths = process.argv.slice(4).length ? process.argv.slice(4) : ['/', '/appraisal-representation/hail-roof-damage-appraisal/', '/across-north-dakota/fargo/', '/claim-planning-tools/roof-snow-load-estimator/'];
fs.mkdirSync(out, { recursive: true });

async function scrollAll(page) {
  // Real wheel events so lazy images and reveal observers fire.
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h + 1200; y += 500) { await page.mouse.wheel(0, 500); await page.waitForTimeout(90); }
  await page.waitForTimeout(600);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(400);
}

(async () => {
  const browser = await chromium.launch();
  const configs = [
    { name: 'desktop', ctx: { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 } },
    { name: 'mobile', ctx: { ...devices['iPhone 13'] } },
  ];
  for (const c of configs) {
    const ctx = await browser.newContext(c.ctx);
    for (const p of paths) {
      const page = await ctx.newPage();
      const errs = [];
      page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      page.on('pageerror', e => errs.push(String(e)));
      const res = await page.goto(base + p, { waitUntil: 'networkidle' });
      await scrollAll(page);
      const info = await page.evaluate(() => ({
        sw: document.documentElement.scrollWidth, vw: window.innerWidth,
        broken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src),
        wide: [...document.querySelectorAll('body *')].filter(el => el.getBoundingClientRect().right > window.innerWidth + 1 && getComputedStyle(el).position !== 'fixed').slice(0, 5).map(el => el.tagName + '.' + el.className),
      }));
      const slug = (p === '/' ? 'home' : p.replace(/\//g, '_').replace(/^_|_$/g, ''));
      await page.screenshot({ path: `${out}/${c.name}-${slug}.png`, fullPage: true });
      console.log(c.name, p, res.status(), 'scrollW', info.sw, 'vw', info.vw, 'broken', info.broken.length, info.broken.slice(0, 3).join(' '), 'wide', info.wide.join(','), 'errors', errs.join(' | '));
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
})();
