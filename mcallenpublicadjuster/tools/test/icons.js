// Render the SVG logo mark to PNG icons with Playwright (Chromium).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const site = path.join(__dirname, '..', '..', 'site');
  const svg = fs.readFileSync(path.join(site, 'assets/img/logo-mark.svg'), 'utf8');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const [name, size, pad, bg] of [['apple-touch-icon.png', 180, 22, '#10243A'], ['assets/img/logo-mark.png', 512, 0, 'transparent'], ['assets/img/icon-192.png', 192, 20, '#10243A'], ['assets/img/icon-512.png', 512, 56, '#10243A'], ['favicon-48.png', 48, 0, 'transparent']]) {
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<html><body style="margin:0;background:${bg};display:grid;place-items:center;width:${size}px;height:${size}px">${svg.replace('width="48" height="48"', `width="${size - pad * 2}" height="${size - pad * 2}"`)}</body></html>`);
    await page.screenshot({ path: path.join(site, name), omitBackground: bg === 'transparent' });
  }
  await browser.close();
})();
