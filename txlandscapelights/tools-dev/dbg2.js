const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.goto(process.argv[2]);
  await p.evaluate(() => document.querySelector('.rail').scrollIntoView());
  await p.waitForTimeout(1500);
  console.log(await p.evaluate(() => { const r = document.querySelector('.rail'); const b = r.getBoundingClientRect(); return [r.className, b.top, b.height, b.width, innerHeight]; }));
  await b.close();
})();
