// Renders the 1200x630 Open Graph image from a site photo (uses the preinstalled Playwright Chromium).
// usage: node tools/make_og.js static/assets/img/photos/<key>.webp
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const S = path.join(__dirname, "..", "static");
const mark = fs.readFileSync(path.join(S, "favicon.svg"), "utf8").replace("<svg ", '<svg width="76" height="76" ');
(async () => {
  const photo = fs.readFileSync(process.argv[2]).toString("base64");
  const mime = process.argv[2].endsWith(".webp") ? "image/webp" : "image/jpeg";
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await page.setContent(`<html><head><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gabarito:wght@700;800&family=Libre+Franklin:wght@500;600&display=block"></head>
  <body style="margin:0;width:1200px;height:630px;position:relative;overflow:hidden;font-family:'Libre Franklin',sans-serif">
  <img src="data:${mime};base64,${photo}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(100deg,rgba(0,42,28,.97) 0%,rgba(0,42,28,.9) 48%,rgba(0,67,44,.35) 100%)"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:16px;background:#FFD520"></div>
  <div style="position:absolute;left:76px;top:64px;right:250px;color:#fff">
    <div style="display:flex;align-items:center;gap:18px">${mark}<div style="line-height:1.05"><div style="font:800 34px 'Gabarito'">Washington</div><div style="font:600 18px 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;color:#FFD520;margin-top:4px">Insurance Appraiser</div></div></div>
    <div style="margin-top:48px;font:800 60px/1.06 'Gabarito';letter-spacing:-.02em">A second, <span style="color:#FFD520">independent</span> number for your property claim</div>
    <div style="margin-top:24px;font:500 25px 'Libre Franklin';color:#d7ebe2">Appraisal · Estimate review · Umpire services · All 39 counties</div>
    <div style="margin-top:30px;display:inline-block;padding:12px 24px;border-radius:999px;background:#FFD520;color:#002a1c;font:600 23px 'Libre Franklin'">(844) 537-1427 · washingtoninsuranceappraiser.com</div>
  </div></body></html>`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(S, "assets/img/og-image.jpg"), type: "jpeg", quality: 86 });
  await browser.close();
  console.log("og-image.jpg written");
})();
