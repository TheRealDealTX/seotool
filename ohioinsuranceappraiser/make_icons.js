// Renders the brand mark to favicon.svg, PNG icons, a multi-size favicon.ico, the maskable icons and the 1200x630 OG image.
// usage: node make_icons.js <og-photo.jpg|webp>   (uses the preinstalled Playwright Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const S = path.join(__dirname, "static");
const RED = "#C12637", TEAL = "#7FD8CF";
// Inspection lens with a roof line inside and a teal handle (matches mark() in build.py).
const inner = `<circle cx="21" cy="20.5" r="10.5" fill="none" stroke="#fff" stroke-width="3.6"/><path d="M15.2 22.6l5.8-5 5.8 5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><path d="M29 28.6l8 8" stroke="${TEAL}" stroke-width="5" stroke-linecap="round"/>`;
// Bolder version for 16-48px: thicker ring, no inner roof detail lost to blur.
const bold = `<circle cx="20.5" cy="20" r="11" fill="none" stroke="#fff" stroke-width="6"/><path d="M14.5 22.5l6-5.2 6 5.2" fill="none" stroke="#fff" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M29.5 29.5l9 9" stroke="${TEAL}" stroke-width="7.5" stroke-linecap="round"/>`;
const svg = (body, rx = 12, scale = 1) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="${rx}" fill="${RED}"/><g transform="translate(${24 - 24 * scale} ${24 - 24 * scale}) scale(${scale})">${body}</g></svg>`;
function ico(pngs) {
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
  for (const f of ["favicon-32x32.png"]) { try { fs.unlinkSync(path.join(S, f)); } catch (e) {} }
  fs.writeFileSync(path.join(S, "favicon.svg"), svg(inner));
  fs.mkdirSync(path.join(S, "assets/img"), { recursive: true });
  fs.writeFileSync(path.join(S, "assets/img/mark.svg"), svg(inner));
  const small = [];
  for (const s of [16, 32, 48]) small.push({ size: s, buf: await render(svg(bold, s <= 16 ? 4 : 9), s) });
  fs.writeFileSync(path.join(S, "favicon.ico"), ico(small));
  fs.writeFileSync(path.join(S, "favicon-96x96.png"), await render(svg(inner), 96));
  fs.writeFileSync(path.join(S, "apple-touch-icon.png"), await render(svg(inner, 0, 0.82), 180));   // full bleed
  fs.writeFileSync(path.join(S, "favicon-192.png"), await render(svg(inner, 0, 0.64), 192));         // maskable safe zone
  fs.writeFileSync(path.join(S, "favicon-512.png"), await render(svg(inner, 0, 0.64), 512));
  const photo = fs.readFileSync(process.argv[2]).toString("base64");
  const mime = process.argv[2].endsWith(".webp") ? "image/webp" : "image/jpeg";
  await page.setViewportSize({ width: 1200, height: 630 });
  await page.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@500;600&family=Red+Hat+Display:wght@800;900&display=block"></head>
  <body style="margin:0;width:1200px;height:630px;position:relative;overflow:hidden;font-family:'Albert Sans',sans-serif">
  <img src="data:${mime};base64,${photo}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(100deg,rgba(38,7,12,.96) 0%,rgba(74,13,22,.88) 50%,rgba(38,7,12,.3) 100%)"></div>
  <div style="position:absolute;left:0;top:0;bottom:0;width:14px;background:${RED}"></div>
  <div style="position:absolute;left:78px;top:66px;right:280px;color:#fff">
   <div style="display:flex;align-items:center;gap:18px">${svg(inner).replace("<svg ", '<svg width="74" height="74" ')}<span style="font:900 30px 'Red Hat Display';letter-spacing:-.01em">Ohio Insurance <span style="color:#ff9aa5">Appraiser</span></span></div>
   <div style="margin-top:50px;font:900 62px/1.07 'Red Hat Display';letter-spacing:-.025em">An independent second number for an underpaid claim</div>
   <div style="margin-top:26px;font:500 26px 'Albert Sans';color:#f3dcdf">Appraisal · Estimate audits · Umpire work · All 88 counties</div>
   <div style="margin-top:32px;display:inline-block;padding:12px 24px;border-radius:999px;background:${RED};color:#fff;font:600 24px 'Albert Sans'">(844) 537-1427 · ohioinsuranceappraiser.com</div>
  </div></body></html>`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(S, "assets/img/og-image.jpg"), type: "jpeg", quality: 86 });
  await browser.close();
  console.log("icons + og image written");
})();
