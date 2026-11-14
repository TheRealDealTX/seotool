// Screenshots for visual review: node tools/shots.js <baseURL> <outDir> [scale]
// Scrolls with real wheel events so lazy images and reveal animations trigger, then captures full pages.
const { chromium, devices } = require("playwright");
const base = process.argv[2] || "http://127.0.0.1:8099", out = process.argv[3] || ".", scale = +(process.argv[4] || 1);
const PAGES = { home: "/", service: "/insurance-appraisal-services/wildfire-ash-claim-appraisal/", location: "/cities-we-serve/spokane/", tool: "/free-claim-calculators/wildfire-total-loss-coverage-check/" };
async function wheelThrough(page) {
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h + 1200; y += 500) { await page.mouse.wheel(0, 500); await page.waitForTimeout(110); }
  await page.waitForTimeout(700);
}
(async () => {
  const browser = await chromium.launch();
  const sets = [["desktop", { viewport: { width: 1440, height: 900 }, deviceScaleFactor: scale }], ["mobile", { ...devices["iPhone 13"] }]];
  for (const [name, opts] of sets) {
    const ctx = await browser.newContext(opts); const page = await ctx.newPage();
    const errs = []; page.on("pageerror", e => errs.push(e.message)); page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
    for (const [k, p] of Object.entries(PAGES)) {
      await page.goto(base + p, { waitUntil: "networkidle" });
      await page.mouse.move(200, 300);
      await wheelThrough(page);
      const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, vw: window.innerWidth,
        broken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src) }));
      console.log(name, k, "scrollWidth", r.sw, "viewport", r.vw, r.sw === r.vw ? "OK" : "OVERFLOW", "broken imgs", r.broken.length, r.broken.slice(0, 3).join(" "));
      await page.screenshot({ path: `${out}/${name}-${k}.png`, fullPage: true });
    }
    console.log(name, "console/page errors:", errs.length ? errs.join(" | ") : "none");
    await ctx.close();
  }
  await browser.close();
})();
