// Renders static/assets/img/og-image.jpg (1200x630) from a site photo + the brand mark, using the site fonts.
// Usage: node tools/make_og.js   (needs the preinstalled Playwright + Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(root, "static/assets/img/photos/hero-supercell.webp")).toString("base64");
const mark = fs.readFileSync(path.join(root, "static/assets/img/mark.svg"), "utf8");
const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&family=Source+Sans+3:wght@600;700&display=swap" rel="stylesheet">
<style>body{margin:0;width:1200px;height:630px;font-family:'Source Sans 3',sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background:url(${photo}) center 40%/cover}
.sh{position:absolute;inset:0;background:linear-gradient(95deg,rgba(30,14,5,.95) 0%,rgba(30,14,5,.8) 50%,rgba(30,14,5,.2) 100%)}
.in{position:absolute;left:80px;top:76px;right:80px;color:#f6e3d4}
.mk svg{width:100px;height:100px}
h1{font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:104px;line-height:.95;margin:30px 0 18px;color:#fff;max-width:900px;text-transform:uppercase}
p{font-size:29px;margin:0;color:#f6e3d4}.k{display:inline-block;margin-top:34px;background:#d4621a;color:#2a1206;font-weight:700;font-size:28px;padding:14px 26px;border-radius:999px}
.bar{position:absolute;left:0;right:0;bottom:0;height:12px;background:#d4621a}</style></head>
<body><div class="bg"></div><div class="sh"></div><div class="in"><div class="mk">${mark}</div><h1>Wyoming Insurance Appraiser</h1><p>Independent appraisal for disputed hail, wind, snow &amp; fire claims · all 23 counties</p><span class="k">(844) 537-1427</span></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, "static/assets/img/og-image.jpg"), type: "jpeg", quality: 85 });
  await b.close();
  console.log("og-image.jpg written");
})();
