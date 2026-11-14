// Render the logo mark into favicon files (run once; outputs go to static/).
//   node tools/make_icons.js      (needs Playwright + Chromium; Pillow builds the multi-size .ico)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const S = path.join(__dirname, "..", "static");
const NAVY = "#003776", YEL = "#FFE835";
// Full mark (header, footer, favicon.svg): rounded tile, sun, twin-peak roofline, level line.
const MARK = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="11" fill="${NAVY}"/><circle cx="35" cy="13" r="3.2" fill="${YEL}"/><path d="M8 33.5L18.5 18l6.5 8.5 4.8-6.2L40 33.5" fill="none" stroke="${YEL}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 39.5h22" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>`;
// Bolder version for 16-48px: thicker strokes, no sun.
const BOLD = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="9" fill="${NAVY}"/><path d="M6 33L18 15.5l7 9.5 5-6.5L42 33" fill="none" stroke="${YEL}" stroke-width="6.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 41h24" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>`;
// Full-bleed square (apple-touch, maskable): no rounded corners, artwork inside the safe zone.
const bleed = (k) => { const o = 24 * (1 - k); return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" fill="${NAVY}"/><g transform="translate(${o} ${o}) scale(${k})"><circle cx="35" cy="13" r="3.2" fill="${YEL}"/><path d="M8 33.5L18.5 18l6.5 8.5 4.8-6.2L40 33.5" fill="none" stroke="${YEL}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 39.5h22" stroke="#fff" stroke-width="3" stroke-linecap="round"/></g></svg>`; };
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  const render = async (svg, px, out, opaque) => {
    await pg.setViewportSize({ width: px, height: px });
    await pg.setContent(`<html><body style="margin:0;background:transparent">${svg.replace("<svg ", `<svg width="${px}" height="${px}" `)}</body></html>`);
    await pg.screenshot({ path: out, omitBackground: !opaque, clip: { x: 0, y: 0, width: px, height: px } });
  };
  fs.writeFileSync(path.join(S, "favicon.svg"), MARK);
  fs.mkdirSync(path.join(S, "assets/img"), { recursive: true });
  fs.writeFileSync(path.join(S, "assets/img/mark.svg"), MARK);
  await render(MARK, 96, path.join(S, "favicon-96x96.png"));
  await render(bleed(0.74), 180, path.join(S, "apple-touch-icon.png"), true);
  await render(bleed(0.66), 192, path.join(S, "favicon-192.png"), true);
  await render(bleed(0.66), 512, path.join(S, "favicon-512.png"), true);
  const tmp = fs.mkdtempSync("/tmp/ico-");
  for (const s of [16, 32, 48]) await render(BOLD, s, path.join(tmp, `${s}.png`));
  await b.close();
  execFileSync("python3", ["-c", `from PIL import Image
ims=[Image.open('${tmp}/%d.png'%s).convert('RGBA') for s in (16,32,48)]
ims[2].save('${path.join(S, "favicon.ico")}',format='ICO',sizes=[(16,16),(32,32),(48,48)],append_images=ims[:2])`]);
  console.log("icons written");
})();
