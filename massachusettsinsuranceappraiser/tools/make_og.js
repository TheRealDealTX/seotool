// Renders static/assets/img/og-image.jpg (1200x630) from a site photo + the brand mark, using the site fonts.
// Usage: node tools/make_og.js   (needs the preinstalled Playwright + Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(root, "static/assets/img/photos/boston-charles.webp")).toString("base64");
const mark = fs.readFileSync(path.join(root, "static/assets/img/mark.svg"), "utf8");
const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">
<style>body{margin:0;width:1200px;height:630px;font-family:"Plus Jakarta Sans",sans-serif;overflow:hidden}
.bg{position:absolute;inset:0;background:url(${photo}) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(100deg,rgba(14,17,24,.96) 0%,rgba(32,39,52,.86) 55%,rgba(32,39,52,.35) 100%)}
.in{position:absolute;left:80px;top:74px;right:80px;color:#e9edf4}
.mk svg{width:96px;height:96px}
.k{font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#f2a785;font-size:22px;margin-top:34px}
h1{font-family:"DM Serif Display",serif;font-weight:400;font-size:84px;line-height:1.02;margin:14px 0 22px;color:#fff;max-width:900px}
p{font-size:29px;margin:0;color:#dfe5ee}.t{display:inline-block;margin-top:34px;background:#e07a4f;color:#12161f;font-weight:800;font-size:28px;padding:14px 28px;border-radius:999px}
.bar{position:absolute;left:0;bottom:0;height:12px;width:100%;background:linear-gradient(90deg,#e07a4f 0 34%,#202734 34%)}</style></head>
<body><div class="bg"></div><div class="sh"></div><div class="in"><div class="mk">${mark}</div><div class="k">Independent claim appraisal</div><h1>Massachusetts Insurance Appraiser</h1><p>Disputed property claims in all 14 counties</p><span class="t">(844) 537-1427</span></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, "static/assets/img/og-image.jpg"), type: "jpeg", quality: 85 });
  await b.close();
  console.log("og-image.jpg written");
})();
