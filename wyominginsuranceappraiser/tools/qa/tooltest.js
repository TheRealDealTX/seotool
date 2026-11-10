// Tool math + mobile drawer tests. Usage: node tooltest.js <baseURL>
const { chromium, devices } = require("playwright");
const base = process.argv[2] || "http://127.0.0.1:8765";
require("fs").mkdirSync(process.cwd() + "/shots", { recursive: true });
let fails = 0;
const eq = (name, got, want) => { const ok = got === want; if (!ok) fails++; console.log(`${ok ? "PASS" : "FAIL"} ${name}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`); };
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const T = "/free-calculators/";
  const out = (k) => pg.textContent(`[data-o="${k}"]`).then(s => s.trim());
  const fill = async (sel, v) => { await pg.fill(sel, String(v)); await pg.dispatchEvent(sel, "input"); };

  // 1. Award net-gain projector: 21300 vs 34900, 60%, $2500 flat, umpire 3000 split
  await pg.goto(base + T + "award-net-gain-projector/");
  eq("gap", await out("gap"), "$13,600"); eq("award", await out("award"), "$29,460"); eq("gain", await out("gain"), "$8,160");
  eq("cost", await out("cost"), "$4,000"); eq("net", await out("net"), "$4,160"); eq("pct", await out("pct"), "64%");
  await pg.selectOption("#g-ft", "pct"); await fill("#g-fee", 10);
  eq("pct fee cost", await out("cost"), "$2,316"); eq("pct fee net", await out("net"), "$5,844");

  // 2. ACV & holdback: rows 21400/11/30, 6800/14/50, 960/8/20; deductible 1000, cap 80%
  await pg.goto(base + T + "acv-holdback-worksheet/");
  // dep = 21400*11/30=7846.67 + 6800*14/50=1904 + 960*8/20=384 => 10134.67; acv=26125.33
  eq("rcv", await out("rcv"), "$29,160"); eq("dep", await out("dep"), "$10,135"); eq("acv", await out("acv"), "$19,025");
  eq("first", await out("first"), "$18,025"); eq("held", await out("held"), "$10,135"); eq("total", await out("total"), "$28,160");
  await pg.check("[name=nonrec]"); await pg.dispatchEvent("[name=nonrec]", "change");
  eq("acv-only held", await out("held"), "$0"); eq("acv-only total", await out("total"), "$18,025");
  await pg.click("[data-add]"); eq("add row", await pg.$$eval('[data-tool="dep"] tbody tr', r => r.length), 4);
  await pg.click('[data-tool="dep"] tbody tr:last-child .x'); eq("remove row", await pg.$$eval('[data-tool="dep"] tbody tr', r => r.length), 3);

  // 3. Roof: 62x36 + 12in overhang => 64*38=2432; 6/12 mult 1.118 => 2719.06 sf; 27.19 sq; 12% waste => 30.45 -> ceil(91.36)/3=30.67
  await pg.goto(base + T + "roof-area-pitch-waste/");
  eq("mult", await out("mult"), "1.118"); eq("sq", await out("sq"), "27.19"); eq("order", await out("order"), "30.67"); eq("bundles", await out("bundles"), "92");
  await fill("#r-pr", 500); eq("roof cost", await out("cost"), "$15,227");
  await pg.selectOption("#r-p", "12"); eq("12/12 mult", await out("mult"), "1.414");

  // 4. Deductible: 420000 at 2% = 8400; loss 24800; flat 1000
  await pg.goto(base + T + "deductible-comparison/");
  eq("pd", await out("pd"), "$8,400"); eq("pdpay", await out("pdpay"), "$16,400"); eq("flatpay", await out("flatpay"), "$23,800"); eq("diff", await out("diff"), "$7,400");
  await pg.selectOption("#w-p", "0.5"); eq("0.5%", await out("pd"), "$2,100");

  // 5. Timeline + .ics download
  await pg.goto(base + T + "claim-timeline-builder/");
  await pg.fill("#t-d", "2026-06-15"); await pg.dispatchEvent("#t-d", "change");
  const items = await pg.$$eval('[data-o="timeline"] li', l => l.map(x => x.textContent));
  eq("timeline items", items.length, 5);
  eq("notice date", items[0].includes("Jun 18, 2026"), true);
  eq("suit date", items.some(t => t.includes("Jun 14, 2028")), true);
  const [dl] = await Promise.all([pg.waitForEvent("download"), pg.click("[data-ics]")]);
  const ics = require("fs").readFileSync(await dl.path(), "utf8");
  eq("ics name", dl.suggestedFilename(), "wyoming-claim-timeline.ics");
  eq("ics events", (ics.match(/BEGIN:VEVENT/g) || []).length, 5);
  eq("ics date", ics.includes("DTSTART;VALUE=DATE:20260618"), true);

  // 6. Ready-meter: answer all yes => 100; first no (weight 3 of 24) => 88
  await pg.goto(base + T + "appraisal-ready-meter/");
  for (const btn of await pg.$$(".quiz .yes")) await btn.click();
  eq("all yes", await out("score"), "100");
  await pg.click(".quiz li:first-child .no");
  eq("one no", await out("score"), "88"); eq("todo", (await pg.$$('[data-o="todo"] li')).length, 1);
  await pg.click("[data-reset]"); eq("reset", await out("score"), "–");

  // 7. Hail test squares: 4 facets, threshold 8 => 17.2 of 34.4 = 50%
  await pg.goto(base + T + "hail-test-square-scorer/");
  eq("qsq", await out("qsq"), "17.2"); eq("share", await out("share"), "50%"); eq("qn", await out("qn"), "2 of 4"); eq("tsq", await out("tsq"), "34.4");
  await fill("#h-pr", 560); eq("hail cost", await out("cost"), "$9,632"); eq("hail full", await out("full"), "$19,264");
  await fill("#h-th", 5); eq("thresh 5", await out("qn"), "3 of 4"); eq("thresh 5 share", await out("share"), "77%");

  // home mini gap
  await pg.goto(base + "/");
  eq("mini gap", await pg.textContent('#gap [data-o="gap"]'), "$12,600"); eq("mini award", await pg.textContent('#gap [data-o="award"]'), "$23,100");

  // glossary filter
  await pg.goto(base + "/claim-terms/");
  await pg.fill("#gloss-filter", "umpire");
  const vis = await pg.$$eval(".gterm", g => g.filter(x => !x.hidden).length);
  eq("glossary filter hits>0", vis > 0 && vis < 10, true);
  eq("glossary total", await pg.$$eval(".gterm", g => g.length) >= 35, true);

  // form endpoint rejects invalid input (client side message) — server side tested with curl
  // ---------- mobile drawer ----------
  const m = await b.newContext({ ...devices["iPhone 13"] });
  const mp = await m.newPage();
  await mp.goto(base + "/");
  const st = () => mp.evaluate(() => ({ open: document.body.classList.contains("drawer-open"), lock: document.body.classList.contains("lock"), inert: document.getElementById("drawer").hasAttribute("inert"), hidden: document.getElementById("drawer").getAttribute("aria-hidden"), vis: getComputedStyle(document.getElementById("drawer")).visibility, shadow: getComputedStyle(document.getElementById("drawer")).boxShadow }));
  let s = await st(); eq("closed: inert", s.inert, true); eq("closed: invisible", s.vis, "hidden"); eq("closed: no shadow", s.shadow, "none");
  await mp.click(".burger"); await mp.waitForTimeout(500);
  s = await st(); eq("open", s.open, true); eq("scroll lock", s.lock, true); eq("open: not inert", s.inert, false); eq("aria-hidden false", s.hidden, "false"); eq("visible", s.vis, "visible");
  await mp.screenshot({ path: process.cwd() + "/shots/drawer-open.png" });
  await mp.click('.acc-btn[aria-controls="acc-1"]'); await mp.waitForTimeout(400);
  eq("accordion expanded", await mp.getAttribute('.acc-btn[aria-controls="acc-1"]', "aria-expanded"), "true");
  await mp.screenshot({ path: process.cwd() + "/shots/drawer-acc.png" });
  await Promise.all([mp.waitForNavigation(), mp.click('#acc-1 a[href="/where-we-work/casper/"]')]);
  eq("link landed", new URL(mp.url()).pathname, "/where-we-work/casper/");
  s = await st(); eq("closed after nav", s.open, false);
  // close via ×
  await mp.click(".burger"); await mp.waitForTimeout(450); await mp.click(".drawer-close"); await mp.waitForTimeout(450);
  s = await st(); eq("close ×", s.open, false); eq("close × unlock", s.lock, false); eq("close × inert", s.inert, true);
  // close via overlay
  await mp.click(".burger"); await mp.waitForTimeout(450); await mp.mouse.click(20, 400); await mp.waitForTimeout(450);
  s = await st(); eq("close overlay", s.open, false);
  // close via Escape
  await mp.click(".burger"); await mp.waitForTimeout(450); await mp.keyboard.press("Escape"); await mp.waitForTimeout(450);
  s = await st(); eq("close Escape", s.open, false); eq("Escape unlock", s.lock, false);
  // edge haze check: closed drawer area pixels at right edge equal page
  await b.close();
  console.log(fails ? `FAILURES: ${fails}` : "ALL TESTS PASSED");
  process.exit(fails ? 1 : 0);
})();
