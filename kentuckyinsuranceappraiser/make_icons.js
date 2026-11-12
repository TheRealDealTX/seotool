// Renders the brand mark to favicon.svg, PNG icons, a multi-size favicon.ico and the 1200x630 OG image.
// usage: node make_icons.js <og-photo.jpg>   (uses the preinstalled Playwright Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const S = path.join(__dirname, "static");
const BLUE = "#0033A0", CORAL = "#FF6B4A";
const inner = `<path d="M9.5 24.5L24 11.5l14.5 13" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M15.5 30.5h17M15.5 37h9.5" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/><circle cx="32.5" cy="37" r="3.3" fill="${CORAL}"/>`;
const bold = `<path d="M7.5 26L24 11l16.5 15" fill="none" stroke="#fff" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 36.5h13" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="35" cy="36.5" r="4.8" fill="${CORAL}"/>`;
const svg = (body, rx = 11, scale = 1) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="${rx}" fill="${BLUE}"/><g transform="translate(${24 - 24 * scale} ${24 - 24 * scale}) scale(${scale})">${body}</g></svg>`;
function ico(pngs) { // pngs: [{size, buf}]
  const head = Buffer.alloc(6 + 16 * pngs.length); head.writeUInt16LE(0, 0); head.writeUInt16LE(1, 2); head.writeUInt16LE(pngs.length, 4);
  let off = head.length; const bufs = [];
  pngs.forEach((p, i) => { const e = 6 + 16 * i; head.writeUInt8(p.size % 256, e); head.writeUInt8(p.size % 256, e + 1); head.writeUInt8(0, e + 2); head.writeUInt8(0, e + 3);
    head.writeUInt16LE(1, e + 4); head.writeUInt16LE(32, e + 6); head.writeUInt32LE(p.buf.length, e + 8); head.writeUInt32LE(off, e + 12); off += p.buf.length; bufs.push(p.buf); });
  return Buffer.concat([head, ...bufs]);
}
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  const render = async (markup, size) => {
    await page.setViewportSize({ width: size, height: size });
    await page.setContent(`<html><body style="margin:0;background:transparent">${markup.replace("<svg ", `<svg width="${size}" height="${size}" `)}</body></html>`);
    return page.screenshot({ omitBackground: true, clip: { x: 0, y: 0, width: size, height: size } });
  };
  fs.writeFileSync(path.join(S, "favicon.svg"), svg(inner));
  fs.writeFileSync(path.join(S, "assets/img/mark.svg"), svg(inner));
  const small = [];
  for (const s of [16, 32, 48]) small.push({ size: s, buf: await render(svg(bold, s <= 16 ? 3 : 8), s) });
  fs.writeFileSync(path.join(S, "favicon.ico"), ico(small));
  fs.writeFileSync(path.join(S, "favicon-32x32.png"), small[1].buf);
  fs.writeFileSync(path.join(S, "favicon-96x96.png"), await render(svg(inner), 96));
  fs.writeFileSync(path.join(S, "apple-touch-icon.png"), await render(svg(inner, 0, 0.8), 180));
  fs.writeFileSync(path.join(S, "favicon-192.png"), await render(svg(inner, 0, 0.66), 192));
  fs.writeFileSync(path.join(S, "favicon-512.png"), await render(svg(inner, 0, 0.66), 512));
  // OG image
  const photo = fs.readFileSync(process.argv[2]).toString("base64");
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@500;600&family=Sora:wght@700;800&display=block"></head>
  <body style="margin:0;width:1200px;height:630px;position:relative;overflow:hidden;font-family:'Hanken Grotesk',sans-serif">
  <img src="data:image/jpeg;base64,${photo}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(100deg,rgba(0,14,51,.95) 0%,rgba(0,26,87,.86) 48%,rgba(0,51,160,.35) 100%)"></div>
  <div style="position:absolute;left:72px;top:70px;right:300px;color:#fff">
   <div style="display:flex;align-items:center;gap:18px">${svg(inner).replace("<svg ", '<svg width="72" height="72" ')}<span style="font:700 26px Sora;letter-spacing:-.02em">Kentucky Insurance Appraiser</span></div>
   <div style="margin-top:56px;font:800 64px/1.08 Sora;letter-spacing:-.03em">Independent appraisal for claims that came up <span style="color:${CORAL}">short</span></div>
   <div style="margin-top:28px;font:500 26px 'Hanken Grotesk';color:#dfe7ff">Estimate review · Party appraiser · Umpire · All 120 counties</div>
   <div style="margin-top:34px;display:inline-block;padding:12px 24px;border-radius:999px;background:${CORAL};color:#2a0b02;font:600 24px 'Hanken Grotesk'">(844) 537-1427 · kentuckyinsuranceappraiser.com</div>
  </div></body></html>`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(S, "assets/img/og-image.jpg"), type: "jpeg", quality: 86 });
  await browser.close();
  console.log("icons + og image written");
})();
