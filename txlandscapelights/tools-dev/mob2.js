const { chromium } = require('playwright');
(async () => {
  const [,, url, out, ...sels] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true, viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  let i = 0;
  for (const s of ['body', ...sels]) {
    if (s !== 'body') await p.evaluate(s => document.querySelector(s).scrollIntoView(), s);
    await p.waitForTimeout(2500); await p.screenshot({ path: `${out}${i++}.png` });
  }
  await b.close();
})();
