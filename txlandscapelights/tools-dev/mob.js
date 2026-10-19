const { chromium } = require('playwright');
(async () => {
  const [,, url, out] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true, viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForTimeout(5000);
  await p.screenshot({ path: out + '-pop.png' });
  console.log('popup open:', await p.evaluate(() => document.querySelector('#pop').classList.contains('is-open')));
  await p.click('.pop__x');
  const H = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += 500) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(80); }
  await p.waitForTimeout(1500);
  console.log('hscroll', await p.evaluate(() => document.documentElement.scrollWidth - innerWidth));
  const shots = [];
  for (let y = 0, i = 0; y < Math.min(H, 844 * 14); y += 844, i++) { await p.evaluate(y => scrollTo(0, y), y); await p.waitForTimeout(250); await p.screenshot({ path: `${out}-${i}.png` }); shots.push(i); }
  console.log(shots.length);
  await b.close();
})();
