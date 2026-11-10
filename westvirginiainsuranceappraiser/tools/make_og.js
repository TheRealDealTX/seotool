// Renders static/assets/img/og-image.jpg (1200x630) from a site photo + the brand mark, using the site fonts.
// Usage: node tools/make_og.js   (needs the preinstalled Playwright + Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(root, "static/assets/img/photos/gorge-overlook.webp")).toString("base64");
const mark = fs.readFileSync(path.join(root, "static/assets/img/mark.svg"), "utf8");
const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@700&family=Public+Sans:wght@600;700&display=swap" rel="stylesheet">
<style>body{margin:0;width:1200px;height:630px;font-family:"Public Sans",sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background:url(${photo}) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(100deg,rgba(8,24,5,.96) 0%,rgba(13,38,9,.86) 52%,rgba(13,38,9,.35) 100%)}
.in{position:absolute;left:80px;top:70px;right:80px;color:#e6eee1}
.mk svg{width:96px;height:96px}
h1{font-family:"Zilla Slab",serif;font-weight:700;font-size:86px;line-height:.98;margin:30px 0 22px;color:#fff;max-width:800px}
p{font-size:30px;margin:0;color:#d7e4d0}.k{display:inline-block;margin-top:32px;background:#b8336a;color:#fff;font-weight:700;font-size:28px;padding:14px 28px;border-radius:999px}
.bar{position:absolute;left:0;bottom:0;height:14px;width:100%;background:linear-gradient(90deg,#15370d,#b8336a)}</style></head>
<body><div class="bg"></div><div class="sh"></div><div class="in"><div class="mk">${mark}</div><h1>West Virginia Insurance Appraiser</h1><p>Independent appraisal for disputed property claims · all 55 counties</p><span class="k">(844) 537-1427</span></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, "static/assets/img/og-image.jpg"), type: "jpeg", quality: 85 });
  await b.close();
  console.log("og-image.jpg written");
})();
