// Renders social share images (1200x630 PNG) and app icons with the
// preinstalled Chromium. Run after build.py, then run build.py again:
//   python3 build.py && node render_og.mjs && python3 build.py
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const require = createRequire(import.meta.url);
let pw;
try { pw = require("playwright"); } catch { pw = require("/opt/node-tools/node_modules/playwright"); }
const ROOT = path.dirname(fileURLToPath(import.meta.url));
const items = JSON.parse(fs.readFileSync(path.join(ROOT, ".og.json"), "utf8"));
const ogDir = path.join(ROOT, "assets", "og");
fs.mkdirSync(ogDir, { recursive: true });
const fontCss = "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,800,100&family=Plus+Jakarta+Sans:wght@700&display=block";
const browser = await pw.chromium.launch({ executablePath: fs.existsSync("/opt/pw-browsers/chromium") ? undefined : undefined });
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
for (const it of items) {
  const ph = path.join(ROOT, "assets", "photos", it.cover + "-1600.webp");
  const svg = fs.existsSync(ph)
    ? `<img src="data:image/webp;base64,${fs.readFileSync(ph).toString("base64")}" style="width:1200px;height:750px;object-fit:cover">`
    : fs.readFileSync(path.join(ROOT, "public", "assets", "covers", it.cover + ".svg"), "utf8");
  await page.setContent(`<!doctype html><html><head><link rel="stylesheet" href="${fontCss}"><style>
    body{margin:0;width:1200px;height:630px;overflow:hidden;position:relative;font-family:"Plus Jakarta Sans",sans-serif}
    .bg{position:absolute;inset:0}.bg svg{width:1200px;height:750px;margin-top:-60px}
    .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,14,30,.82),rgba(20,14,30,.35) 60%,rgba(20,14,30,.05))}
    .t{position:absolute;left:70px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;color:#fff}
    .l{font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:22px;opacity:.9;margin-bottom:18px}
    h1{font-family:Fraunces,serif;font-variation-settings:"SOFT" 100;font-size:64px;line-height:1.05;margin:0;letter-spacing:-.02em}
    .b{position:absolute;left:70px;bottom:44px;display:flex;align-items:center;gap:12px;color:#fff;font-family:Fraunces,serif;font-size:34px;font-weight:800}
    .b svg{width:44px;height:44px}</style></head><body>
    <div class="bg">${svg}</div><div class="shade"></div>
    <div class="t"><div class="l">${it.label}</div><h1>${it.title}</h1></div>
    <div class="b"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#ff5a4e"/><path d="M21 7l-9 15h7l-2 11 10-16h-7z" fill="#fff"/></svg>HotsBuzz</div>
    </body></html>`, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(ogDir, it.file + ".jpg"), type: "jpeg", quality: 84 });
}
const icon = fs.readFileSync(path.join(ROOT, "static", "favicon.svg"), "utf8");
// Icons are rendered once (pass --icons to redo). Then turn favicon-48.png into favicon.ico:
//   convert favicon-48.png -define icon:auto-resize=48,32,16 favicon.ico && rm favicon-48.png
const icons = process.argv.includes("--icons") ? [["apple-touch-icon.png", 180, 14], ["web-app-manifest-192x192.png", 192, 0], ["web-app-manifest-512x512.png", 512, 0], ["favicon-48.png", 48, 0]] : [];
for (const [name, size, pad] of icons) {
  await page.setViewportSize({ width: size, height: size });
  await page.setContent(`<body style="margin:0;background:${pad ? "#fff8ef" : "transparent"}"><div style="padding:${pad}px;width:${size - 2 * pad}px;height:${size - 2 * pad}px">${icon.replace("<svg ", '<svg width="100%" height="100%" ')}</div></body>`);
  await page.screenshot({ path: path.join(ROOT, "static", name), omitBackground: !pad });
}
await browser.close();
console.log(`rendered ${items.length} social images + icons`);
