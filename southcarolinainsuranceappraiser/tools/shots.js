// Screenshot + layout checks. node tools/shots.js <baseURL> <outDir> [paths...]
// Scrolls with real wheel events so lazy images and reveals trigger, then reports
// scrollWidth vs viewport, broken images and console errors.
const { chromium, devices } = require("playwright");
const base = process.argv[2] || "http://127.0.0.1:8099";
const out = process.argv[3] || ".";
const paths = process.argv.slice(4).length ? process.argv.slice(4) : ["/", "/claim-dispute-services/hurricane-claim-appraisal/", "/locations-served/charleston/", "/free-claim-tools/wind-flood-damage-splitter/"];
(async () => {
  const browser = await chromium.launch();
  const profiles = [["desktop", { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }], ["mobile", { ...devices["iPhone 13"] }]];
  for (const [name, opts] of profiles) {
    const ctx = await browser.newContext(opts);
    for (const p of paths) {
      const page = await ctx.newPage();
      const errs = [];
      page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
      page.on("pageerror", e => errs.push(String(e)));
      const res = await page.goto(base + p, { waitUntil: "networkidle" });
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      if (name === "desktop") { for (let y = 0; y < h; y += 500) { await page.mouse.wheel(0, 500); await page.waitForTimeout(120); } }
      else { for (let y = 0; y < h; y += 500) { await page.evaluate(() => window.scrollBy(0, 500)); await page.waitForTimeout(120); } }
      await page.waitForTimeout(800);
      const info = await page.evaluate(() => ({
        sw: document.documentElement.scrollWidth, vw: window.innerWidth,
        bad: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src),
        wide: [...document.querySelectorAll("body *")].filter(el => el.getBoundingClientRect().right > window.innerWidth + 1 && !el.closest(".marquee,.storms,.drawer,.table-wrap,.hp")).slice(0, 5).map(el => el.tagName + "." + el.className),
      }));
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(300);
      const fn = `${out}/${name}${p.replace(/\//g, "_") || "_"}.png`;
      await page.screenshot({ path: fn, fullPage: true });
      console.log(name, res.status(), p, `sw=${info.sw} vw=${info.vw}`, info.bad.length ? "BADIMG " + info.bad.join(",") : "imgs ok", info.wide.length ? "WIDE " + info.wide.join(" ") : "", errs.length ? "ERR " + errs.join(" | ") : "");
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
})();
