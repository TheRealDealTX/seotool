const { chromium } = require('playwright');
(async () => {
  const [,, url, prefix, w, ...sels] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true, viewport: { width: +w, height: 900 } });
  await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
  await p.goto(url, { waitUntil: 'networkidle' });
  let i = 0;
  for (const s of sels) {
    await p.evaluate(s => document.querySelector(s).scrollIntoView(), s);
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `${prefix}${i++}.png` });
  }
  await b.close();
})();
