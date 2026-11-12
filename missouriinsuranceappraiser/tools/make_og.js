// Renders static/assets/img/og-image.jpg (1200x630) from a site photo + the brand mark, using the site fonts.
// Usage: node tools/make_og.js   (needs the preinstalled Playwright + Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(root, "static/assets/img/photos/storm-before-hail.webp")).toString("base64");
const mark = fs.readFileSync(path.join(root, "static/assets/img/mark.svg"), "utf8");
const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Figtree:wght@600;700&display=swap" rel="stylesheet">
<style>body{margin:0;width:1200px;height:630px;font-family:Figtree,sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background:url(${photo}) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(100deg,rgba(23,13,6,.95) 0%,rgba(42,26,14,.84) 55%,rgba(42,26,14,.4) 100%)}
.in{position:absolute;left:80px;top:80px;right:80px;color:#f6efe5}
.mk{width:96px;height:96px}.mk svg{width:96px;height:96px}
h1{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:76px;line-height:1.02;margin:34px 0 22px;color:#fff;max-width:900px}
p{font-size:28px;margin:0;color:#e9dccb}.k{display:inline-block;margin-top:34px;background:#1f7a80;color:#fff;font-weight:700;font-size:26px;padding:14px 22px;border-radius:6px}
.bar{position:absolute;left:0;right:0;bottom:0;height:12px;background:#5fc1c4}</style></head>
<body><div class="bg"></div><div class="sh"></div><div class="in"><div class="mk">${mark}</div><h1>Missouri Insurance Appraiser</h1><p>Independent appraisal for underpaid property claims · all 114 counties</p><span class="k">(844) 537-1427</span></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, "static/assets/img/og-image.jpg"), type: "jpeg", quality: 85 });
  await b.close();
  console.log("og-image.jpg written");
})();
