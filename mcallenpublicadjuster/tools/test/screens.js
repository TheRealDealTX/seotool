// Screenshot pages at desktop and mobile widths and report console errors.
// Usage: NODE_PATH=$(npm root -g) node tools/test/screens.js <outdir> [paths...]
const { chromium } = require('playwright');
const out = process.argv[2];
const paths = process.argv.slice(3);
const base = process.env.BASE || 'http://127.0.0.1:8081';
(async () => {
  const browser = await chromium.launch();
  for (const [label, vp] of [['desk', { width: 1366, height: 900 }], ['mob', { width: 390, height: 844 }]]) {
    const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    page.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
    for (const p of paths) {
      errs.length = 0;
      await page.goto(base + p, { waitUntil: 'networkidle' });
      // trigger reveal animations
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo({ top: y, behavior: 'instant' }); await new Promise(r => setTimeout(r, 50)); } window.scrollTo({ top: 0, behavior: 'instant' }); });
      await page.waitForTimeout(400);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
      const name = (p.replace(/[^a-z0-9]+/gi, '_') || 'home') + '-' + label + '.png';
      await page.screenshot({ path: out + '/' + name, fullPage: true });
      console.log(label, p, overflow ? 'HORIZONTAL-OVERFLOW' : '', errs.filter(e => !/tile.openstreetmap/.test(e)).join(' | '));
    }
    await ctx.close();
  }
  await browser.close();
})();
