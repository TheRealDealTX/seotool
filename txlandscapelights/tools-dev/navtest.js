const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  await p.addInitScript(() => sessionStorage.setItem('tll-pop', '1'));
  await p.goto(process.argv[2]);
  const open = () => p.evaluate(() => document.body.classList.contains('nav-open'));
  await p.tap('.burger'); await p.waitForTimeout(400); const a = await open();
  await p.tap('.drawer__x'); await p.waitForTimeout(400); const b1 = await open();
  await p.tap('.burger'); await p.waitForTimeout(400); await p.keyboard.press('Escape'); const c = await open();
  const d = false;
  await p.tap('.burger'); await p.waitForTimeout(400); await Promise.all([p.waitForNavigation(), p.tap('.drawer__nav > a[href="/blog/"]')]);
  console.log({ opened: a, closedByX: !b1, closedByEsc: !c, scrim: !d, navigatedTo: new URL(p.url()).pathname, overflow: await p.evaluate(() => document.body.style.overflow) });
  await b.close();
})();
