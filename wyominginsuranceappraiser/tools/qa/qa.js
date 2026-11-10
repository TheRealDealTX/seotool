// Visual + layout QA. Usage: node qa.js <baseURL> <outdir>
const { chromium, devices } = require("playwright");
const base = process.argv[2] || "http://127.0.0.1:8765";
const out = process.argv[3] || process.cwd() + "/shots";
require("fs").mkdirSync(out, { recursive: true });
const pages = ["/", "/what-we-appraise/hail-roof-claim-disputes/", "/where-we-work/cheyenne/", "/free-calculators/hail-test-square-scorer/",
  "/what-we-appraise/", "/where-we-work/", "/free-calculators/", "/claim-guides/", "/claim-terms/", "/appraisal-step-by-step/", "/talk-to-us/", "/photo-credits/", "/appraisal-answers/", "/nope/"];
(async () => {
  const b = await chromium.launch();
  const ctxs = { desk: { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }, mob: { ...devices["iPhone 13"] } };
  let problems = 0;
  for (const [name, opt] of Object.entries(ctxs)) {
    const ctx = await b.newContext(opt);
    for (const p of pages) {
      const pg = await ctx.newPage();
      const errs = [];
      pg.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
      pg.on("pageerror", e => errs.push("pageerror " + e.message));
      pg.on("requestfailed", r => errs.push("reqfail " + r.url()));
      const resp = await pg.goto(base + p, { waitUntil: "networkidle" });
      // scroll through to trigger lazy images + reveals
      const H = await pg.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < H; y += 450) { await pg.mouse.wheel(0, 450); await pg.waitForTimeout(90); }
      await pg.evaluate(async () => { await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 8000); }))); });
      await pg.evaluate(() => window.scrollTo(0, 0)); await pg.waitForTimeout(500);
      const r = await pg.evaluate(() => {
        const imgs = [...document.images];
        const broken = imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.currentSrc || i.src);
        const sw = document.documentElement.scrollWidth, vw = window.innerWidth;
        const wide = sw > vw ? [...document.querySelectorAll("body *")].filter(el => el.getBoundingClientRect().right > vw + 1 && getComputedStyle(el).position !== "fixed").slice(0, 6).map(el => el.tagName + "." + el.className) : [];
        return { sw, vw, broken, n: imgs.length, wide };
      });
      const flag = r.sw !== r.vw || r.broken.length || errs.filter(e => !/404|favicon/.test(e) || p !== "/nope/").length;
      if (flag) problems++;
      console.log(`${name} ${resp.status()} ${p} imgs=${r.n} broken=${r.broken.length} scrollW=${r.sw}/${r.vw}${r.wide.length ? " WIDE:" + r.wide.join(",") : ""}${errs.length ? " ERR:" + errs.join(" | ") : ""}`);
      if (["/", "/what-we-appraise/hail-roof-claim-disputes/", "/where-we-work/cheyenne/", "/free-calculators/hail-test-square-scorer/"].includes(p)) {
        const f = `${out}/${name}${p.replace(/\//g, "_") || "_home"}.png`;
        await pg.screenshot({ path: f, fullPage: true });
      }
      await pg.close();
    }
    await ctx.close();
  }
  await b.close();
  console.log("problem pages:", problems);
})();
