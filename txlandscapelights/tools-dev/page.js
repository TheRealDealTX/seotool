const { chromium } = require('playwright');
(async () => {
  const [,, url, out, w, full] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true, viewport: { width: +w || 1360, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: out, fullPage: full !== '0' });
  console.log('errors:', JSON.stringify(errs));
  console.log('hscroll:', await p.evaluate(() => document.documentElement.scrollWidth - innerWidth));
  await b.close();
})();
