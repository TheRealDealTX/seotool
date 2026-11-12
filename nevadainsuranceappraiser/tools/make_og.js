// Renders static/assets/img/og-image.jpg (1200x630) from a site photo + the brand mark, using the site fonts.
// Usage: node tools/make_og.js   (uses the preinstalled Playwright + Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(root, "static/assets/img/photos/desert-storm-basin.webp")).toString("base64");
const mark = fs.readFileSync(path.join(root, "static/assets/img/mark.svg"), "utf8");
const html = `<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,750&family=Figtree:wght@500;700&display=swap" rel="stylesheet">
<style>body{margin:0;width:1200px;height:630px;font-family:Figtree,sans-serif;overflow:hidden;background:#211a0b}
.bg{position:absolute;inset:0;background:url(${photo}) center/cover}
.sh{position:absolute;inset:0;background:linear-gradient(100deg,rgba(23,17,6,.95) 0%,rgba(23,17,6,.82) 55%,rgba(23,17,6,.3) 100%)}
.in{position:absolute;left:80px;top:78px;right:80px;color:#fbf3dc}
.mk svg{width:96px;height:96px}
h1{font-family:"Bricolage Grotesque",sans-serif;font-weight:750;font-size:78px;line-height:1;margin:34px 0 20px;color:#fff;max-width:920px;letter-spacing:-1px}
h1 span{color:#e2b13c}
p{font-size:29px;margin:0;color:#efe6cf}
.k{display:inline-block;margin-top:34px;background:#e2b13c;color:#211a0b;font-weight:700;font-size:28px;padding:14px 26px;border-radius:999px}
.bar{position:absolute;left:0;right:0;bottom:0;height:12px;background:#e2b13c}</style></head>
<body><div class="bg"></div><div class="sh"></div><div class="in"><div class="mk">${mark}</div><h1>Nevada <span>Insurance</span><br>Appraiser</h1><p>Independent appraisal for disputed property claims · statewide</p><span class="k">(844) 537-1427</span></div><div class="bar"></div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await p.setContent(html, { waitUntil: "networkidle" });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(root, "static/assets/img/og-image.jpg"), type: "jpeg", quality: 85 });
  await b.close();
  console.log("og-image.jpg written");
})();
