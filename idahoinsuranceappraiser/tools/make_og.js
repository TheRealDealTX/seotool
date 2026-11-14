// Compose the 1200x630 Open Graph image from a site photo (run once):  node tools/make_og.js
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const S = path.join(__dirname, "..", "static");
const photo = "data:image/webp;base64," + fs.readFileSync(path.join(S, "assets/img/photos/hero.webp")).toString("base64");
const mark = fs.readFileSync(path.join(S, "favicon.svg"), "utf8").replace("<svg ", '<svg width="96" height="96" ');
const html = `<html><head><link href="https://fonts.googleapis.com/css2?family=Chivo:wght@800;900&family=Be+Vietnam+Pro:wght@500;600&display=swap" rel="stylesheet">
<style>body{margin:0}.c{position:relative;width:1200px;height:630px;overflow:hidden;font-family:'Be Vietnam Pro',sans-serif;color:#fff}
.c img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.c:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(100deg,rgba(0,22,52,.95) 0%,rgba(0,34,80,.85) 50%,rgba(0,34,80,.3) 100%)}
.in{position:absolute;z-index:2;left:72px;top:70px;right:72px}
.k{font:600 22px 'Be Vietnam Pro';letter-spacing:.14em;text-transform:uppercase;color:#FFE835;margin:28px 0 18px}
h1{font:900 76px/1.02 Chivo;margin:0;letter-spacing:-.01em;max-width:760px}
h1 span{background:linear-gradient(transparent 62%,rgba(255,232,53,.95) 62%,rgba(255,232,53,.95) 92%,transparent 92%)}
p{font:500 28px/1.4 'Be Vietnam Pro';margin:26px 0 0;max-width:680px;color:rgba(255,255,255,.92)}
.bar{position:absolute;z-index:2;left:0;right:0;bottom:0;height:16px;background:repeating-linear-gradient(-45deg,#FFE835 0 20px,#003776 20px 40px)}
.tel{position:absolute;z-index:2;right:72px;bottom:56px;font:800 30px Chivo;color:#FFE835}</style></head>
<body><div class="c"><img class="bg" src="${photo}"><div class="in">${mark}<div class="k">Independent property claim appraisal</div>
<h1><span>Idaho Insurance</span> <span>Appraiser</span></h1><p>Independent valuations for underpaid hail, wildfire, snow-load, wind and water claims, statewide.</p></div>
<div class="tel">(844) 537-1427</div><div class="bar"></div></div></body></html>`;
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await pg.setContent(html, { waitUntil: "networkidle" });
  await pg.screenshot({ path: path.join(S, "assets/img/og-image.jpg"), type: "jpeg", quality: 86 });
  await b.close(); console.log("og-image.jpg written");
})();
