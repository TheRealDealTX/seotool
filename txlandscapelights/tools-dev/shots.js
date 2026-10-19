const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + __dirname + '/og.html'); await p.waitForTimeout(1500);
  await p.screenshot({ path: __dirname + '/../src/assets/img/og-image.png' });
  const l = await b.newPage({ viewport: { width: 512, height: 512 } });
  await l.goto('file://' + __dirname + '/logo.html');
  await l.screenshot({ path: __dirname + '/logo-512.png', omitBackground: true });
  await b.close();
})();
