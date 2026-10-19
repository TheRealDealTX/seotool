const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [360, 390, 430]) {
    const p = await b.newPage({ viewport: { width: w, height: 200 }, isMobile: true, deviceScaleFactor: 2 });
    await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
    await p.goto(process.argv[2]); await p.waitForTimeout(800);
    await p.screenshot({ path: `${process.argv[3]}${w}.png`, clip: { x: 0, y: 0, width: w, height: 110 } });
    console.log(w, await p.evaluate(() => document.documentElement.scrollWidth - innerWidth), await p.evaluate(() => document.querySelector('.hdr .wrap').getBoundingClientRect().height));
  }
  await b.close();
})();
