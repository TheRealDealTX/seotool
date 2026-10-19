const { chromium } = require('playwright');
(async () => {
  const [,, url, out] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true, viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 });
  await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.screenshot({ path: out + '0.png' });
  await p.tap('.burger'); await p.waitForTimeout(700);
  await p.screenshot({ path: out + '1.png' });
  await p.tap('.drawer details summary'); await p.waitForTimeout(500);
  await p.screenshot({ path: out + '2.png' });
  await p.evaluate(() => scrollTo(0, 900)); await p.tap('.burger').catch(()=>{}); await p.waitForTimeout(300);
  console.log(await p.evaluate(() => { const d = document.querySelector('#drawer'), h = document.querySelector('.hdr'); return { drawerTop: d.getBoundingClientRect().top, z: getComputedStyle(d).zIndex, hdrZ: getComputedStyle(h).zIndex, hdrBottom: h.getBoundingClientRect().bottom, ubar: document.querySelector('.ubar').getBoundingClientRect().height }; }));
  await b.close();
})();
