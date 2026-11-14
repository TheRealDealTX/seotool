// Browser QA: node tools/qa.js <baseUrl> <outDir>
// Screenshots, horizontal overflow, lazy images, calculator math, mobile drawer, logo hover, console errors.
const { chromium, devices } = require("playwright");
const fs = require("fs");
const base = (process.argv[2] || "http://127.0.0.1:8080").replace(/\/$/, "");
const out = process.argv[3] || "qa-out";
fs.mkdirSync(out, { recursive: true });
const PAGES = {
  home: "/",
  service: "/appraiser-services/hail-roof-damage-appraiser/",
  location: "/cities-we-serve/rapid-city-appraiser/",
  tool: "/policyholder-calculators/appraisal-payoff-estimator/",
};
const ALL = ["/", "/appraiser-services/", "/cities-we-serve/", "/policyholder-calculators/", "/storm-claim-articles/", "/insurance-appraisal-glossary/",
  "/appraisal-questions-answered/", "/inside-the-appraisal-process/", "/get-a-claim-review/", "/company-profile/", "/page-map/",
  ...["appraisal-payoff-estimator", "depreciation-recovery-calculator", "roof-slope-factor-calculator", "hail-percentage-deductible-calculator",
      "appraisal-calendar-builder", "claim-file-readiness-grader", "coinsurance-penalty-calculator"].map(s => "/policyholder-calculators/" + s + "/"),
  "/appraiser-services/black-hills-wildfire-claim-appraiser/", "/cities-we-serve/sioux-falls-appraiser/", "/storm-claim-articles/who-to-call-appraiser-adjuster-or-attorney/"];
const results = { errors: [], notes: [] };
const fail = (m) => { results.errors.push(m); console.log("FAIL", m); };
const ok = (m) => { results.notes.push(m); console.log("ok  ", m); };
const near = (a, b, tol = 1) => Math.abs(a - b) <= tol;

async function wheelToBottom(page) {
  await page.mouse.move(200, 300);
  for (let i = 0; i < 120; i++) {
    await page.mouse.wheel(0, 700);
    await page.waitForTimeout(60);
    const done = await page.evaluate(() => window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4);
    if (done) break;
  }
  await page.waitForTimeout(800);
}

(async () => {
  const browser = await chromium.launch();
  const consoleErrs = [];
  const watch = (page, label) => {
    page.on("console", (m) => { if (m.type() === "error") consoleErrs.push(label + ": " + m.text()); });
    page.on("pageerror", (e) => consoleErrs.push(label + ": " + e.message));
    page.on("response", (r) => { if (r.status() >= 400 && r.url().startsWith(base)) consoleErrs.push(label + ": HTTP " + r.status() + " " + r.url()); });
  };

  // 1. screenshots + overflow + lazy images, desktop and phone
  for (const [mode, ctxOpts] of [["desktop", { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 }], ["mobile", { ...devices["iPhone 13"] }]]) {
    const ctx = await browser.newContext(ctxOpts);
    for (const [name, path] of Object.entries(PAGES)) {
      const page = await ctx.newPage(); watch(page, mode + " " + path);
      await page.goto(base + path, { waitUntil: "networkidle" });
      await page.screenshot({ path: `${out}/${mode}-${name}-top.png` });
      await wheelToBottom(page);
      const imgs = await page.evaluate(() => Array.from(document.images).filter(i => i.offsetParent !== null && !(i.complete && i.naturalWidth > 0)).map(i => i.currentSrc || i.src));
      imgs.length ? fail(`${mode} ${path}: ${imgs.length} images not loaded ${imgs.slice(0, 3)}`) : ok(`${mode} ${path}: all images loaded`);
      const hidden = await page.evaluate(() => Array.from(document.querySelectorAll(".rv")).filter(e => getComputedStyle(e).opacity < 0.9).map(e => e.className + ":" + (e.textContent||"").trim().slice(0,30)));
      hidden.length ? fail(`${mode} ${path}: ${hidden} reveal blocks still hidden after scrolling`) : ok(`${mode} ${path}: reveals done`);
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(300);
      await page.screenshot({ path: `${out}/${mode}-${name}-full.png`, fullPage: true });
      await page.close();
    }
    // overflow across many pages
    for (const path of ALL) {
      const page = await ctx.newPage(); watch(page, mode + " " + path);
      await page.goto(base + path, { waitUntil: "domcontentloaded" });
      const w = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
      w[0] > w[1] ? fail(`${mode} ${path}: scrollWidth ${w[0]} > viewport ${w[1]}`) : null;
      await page.close();
    }
    ok(`${mode}: overflow checked on ${ALL.length} pages`);
    await ctx.close();
  }

  // 2. calculator math
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage(); watch(page, "tools");
  const go = async (s) => page.goto(base + "/policyholder-calculators/" + s + "/", { waitUntil: "networkidle" });
  const txt = async (sel) => (await page.textContent(sel)).trim();
  const fill = async (sel, v) => { await page.fill(sel, String(v)); await page.dispatchEvent(sel, "input"); };

  await go("appraisal-payoff-estimator");
  await fill("#g-ins", 20000); await fill("#g-own", 30000); await page.fill("#g-land", "50"); await page.dispatchEvent("#g-land", "input");
  await page.selectOption("#g-ft", "flat"); await fill("#g-fee", 2000); await fill("#g-ump", 2000);
  // gap 10000, award 25000, gain 5000, cost 2000+1000=3000, net 2000, break-even 3000/10000=30%
  const pay = [await txt("[data-o=gap]"), await txt("[data-o=award]"), await txt("[data-o=cost]"), await txt("[data-o=net]"), await txt("[data-o=be]")];
  JSON.stringify(pay) === JSON.stringify(["$10,000", "$25,000", "$3,000", "$2,000", "30% of the gap"]) ? ok("payoff estimator math " + pay) : fail("payoff estimator " + pay);
  await page.selectOption("#g-ft", "pct"); await fill("#g-fee", 10);
  // cost = 500 + 1000 = 1500, net 3500, be = 1000/(10000*0.9)=11.1% -> 12%
  const pay2 = [await txt("[data-o=cost]"), await txt("[data-o=net]"), await txt("[data-o=be]")];
  JSON.stringify(pay2) === JSON.stringify(["$1,500", "$3,500", "12% of the gap"]) ? ok("payoff pct fee " + pay2) : fail("payoff pct fee " + pay2);

  await go("depreciation-recovery-calculator");
  // defaults: 16800 (11/30), 4200 (18/40), 3100 (7/12); deductible 2500; cap 80%
  const exp = (() => { const r = [[16800, 11, 30], [4200, 18, 40], [3100, 7, 12]]; let rcv = 0, dep = 0; r.forEach(([c, a, l]) => { rcv += c; dep += Math.min(.8, a / l) * c; }); const acv = rcv - dep; return { rcv, first: acv - 2500, held: rcv - 2500 - (acv - 2500), total: rcv - 2500 }; })();
  const m = (n) => "$" + Math.round(n).toLocaleString("en-US");
  const dep = [await txt("[data-o=rcv]"), await txt("[data-o=first]"), await txt("[data-o=held]"), await txt("[data-o=total]")];
  JSON.stringify(dep) === JSON.stringify([m(exp.rcv), m(exp.first), m(exp.held), m(exp.total)]) ? ok("depreciation math " + dep) : fail("depreciation " + dep + " vs " + [m(exp.rcv), m(exp.first), m(exp.held), m(exp.total)]);
  await page.check("[name=nonrec]");
  (await txt("[data-o=held]")) === "$0" ? ok("ACV-only holdback is $0") : fail("ACV-only holdback " + (await txt("[data-o=held]")));
  await page.click("[data-add]"); (await page.$$("tbody tr")).length === 4 ? ok("add row works") : fail("add row");

  await go("roof-slope-factor-calculator");
  // 64x30 with 16" overhang: (64+2.667)*(30+2.667)=2177.8; 7/12 factor 1.1577 -> 2521.2 sq ft -> 25.21 sq
  const roof = [await txt("[data-o=mult]"), await txt("[data-o=sq]")];
  const foot = (64 + 32 / 12) * (30 + 32 / 12), f = Math.sqrt(1 + (7 / 12) ** 2);
  JSON.stringify(roof) === JSON.stringify([f.toFixed(3), (foot * f / 100).toFixed(2)]) ? ok("roof math " + roof) : fail("roof " + roof);
  await page.selectOption("#r-p", "12"); (await txt("[data-o=mult]")) === "1.414" ? ok("12/12 slope factor 1.414") : fail("12/12 factor");

  await go("hail-percentage-deductible-calculator");
  // 340000 * 1% = 3400; loss 18900 -> pays 15500; flat 1500 -> 17400; extra 1900
  const ded = [await txt("[data-o=pd]"), await txt("[data-o=pdpay]"), await txt("[data-o=flatpay]"), await txt("[data-o=diff]")];
  JSON.stringify(ded) === JSON.stringify(["$3,400", "$15,500", "$17,400", "$1,900"]) ? ok("deductible math " + ded) : fail("deductible " + ded);
  await page.selectOption("#w-p", "5"); await fill("#w-l", 12000);
  (await txt("[data-o=pdpay]")) === "$0" ? ok("loss inside 5% deductible pays $0") : fail("inside deductible");
  (await page.$$("[data-o=ladder] tr")).length === 5 ? ok("deductible ladder rows") : fail("ladder");

  await go("appraisal-calendar-builder");
  await page.fill("#t-d", "2026-06-01"); await page.dispatchEvent("#t-d", "change");
  await page.fill("#t-dm", "2026-09-01"); await page.dispatchEvent("#t-dm", "change");
  const items = await page.$$eval("[data-o=timeline] li", (l) => l.map((x) => x.textContent));
  items.length === 6 && items.some(t => t.includes("Sep 21, 2026") && t.includes("Name your appraiser")) && items.some(t => t.includes("May 31, 2028")) ? ok("calendar: 6 milestones, appraiser + suit dates right") : fail("calendar " + JSON.stringify(items));
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("[data-ics]")]);
  const ics = fs.readFileSync(await dl.path(), "utf8");
  (ics.match(/BEGIN:VEVENT/g) || []).length === 6 && ics.includes("DTSTART;VALUE=DATE:20260921") && ics.startsWith("BEGIN:VCALENDAR") ? ok(".ics export: 6 events, " + dl.suggestedFilename()) : fail(".ics " + ics.slice(0, 200));

  await go("claim-file-readiness-grader");
  const yes = await page.$$(".quiz .yes");
  for (const b of yes) await b.click();
  (await txt("[data-o=grade]")) === "A" && (await txt("[data-o=score]")) === "100" ? ok("grader all-yes = A / 100") : fail("grader all yes");
  const no = await page.$$(".quiz .no"); await no[0].click(); await no[1].click(); await no[2].click();
  // total weight 24; minus 9 -> 15/24 = 62.5% -> 63 -> C
  (await txt("[data-o=score]")) === "63" && (await txt("[data-o=grade]")) === "C" && (await page.$$("[data-o=todo] li")).length === 3 ? ok("grader 3 key items missing = C / 63, 3 to-dos") : fail("grader partial " + (await txt("[data-o=score]")));

  await go("coinsurance-penalty-calculator");
  // 420000*80%=336000 required; 280000/336000=0.8333; 96000*0.8333=80000-5000=75000; full 91000; penalty 16000
  const co = [await txt("[data-o=req]"), await txt("[data-o=ratio]"), await txt("[data-o=pay]"), await txt("[data-o=full]"), await txt("[data-o=pen]")];
  JSON.stringify(co) === JSON.stringify(["$336,000", "83%", "$75,000", "$91,000", "$16,000"]) ? ok("coinsurance math " + co) : fail("coinsurance " + co);
  await fill("#c-l", 400000); (await txt("[data-o=pen]")) === "$0" ? ok("no penalty when insured to value") : fail("coinsurance full");

  // home mini gap check
  await page.goto(base + "/", { waitUntil: "networkidle" });
  (await txt("#check [data-o=gap]")) === "$11,700" ? ok("home quick gap check $11,700") : fail("home mini " + (await txt("#check [data-o=gap]")));

  // 3. logo hover: header (solid state) and footer
  await page.evaluate(() => window.scrollTo(0, 600)); await page.waitForTimeout(400);
  for (const sel of [".head .brand", ".foot .brand"]) {
    await page.locator(sel).scrollIntoViewIfNeeded();
    const before = await page.$eval(sel, (e) => [getComputedStyle(e).color, getComputedStyle(e).textDecorationLine, getComputedStyle(e.querySelector("b")).color]);
    await page.hover(sel); await page.waitForTimeout(350);
    const after = await page.$eval(sel, (e) => [getComputedStyle(e).color, getComputedStyle(e).textDecorationLine, getComputedStyle(e.querySelector("b")).color]);
    JSON.stringify(before) === JSON.stringify(after) ? ok(`${sel} unchanged on hover ${after}`) : fail(`${sel} hover changed ${before} -> ${after}`);
  }
  await ctx.close();

  // 4. mobile drawer end to end
  const mctx = await browser.newContext({ ...devices["iPhone 13"] });
  const mp = await mctx.newPage(); watch(mp, "drawer");
  await mp.goto(base + "/", { waitUntil: "networkidle" });
  const state = async () => mp.evaluate(() => ({ open: document.body.classList.contains("drawer-open"), lock: getComputedStyle(document.body).overflow, inert: document.getElementById("drawer").hasAttribute("inert"), hidden: document.getElementById("drawer").getAttribute("aria-hidden"), vis: getComputedStyle(document.getElementById("drawer")).visibility, shadow: getComputedStyle(document.getElementById("drawer")).boxShadow }));
  let s0 = await state();
  !s0.open && s0.inert && s0.vis === "hidden" && s0.shadow === "none" ? ok("drawer closed: inert, hidden, no shadow") : fail("drawer initial " + JSON.stringify(s0));
  const openIt = async () => { await mp.tap(".burger"); await mp.waitForTimeout(450); };
  await openIt(); let s1 = await state();
  s1.open && s1.lock === "hidden" && !s1.inert && s1.hidden === "false" && s1.vis === "visible" ? ok("drawer opens with scroll lock") : fail("drawer open " + JSON.stringify(s1));
  const box = await mp.$eval("#drawer", (d) => { const r = d.getBoundingClientRect(); return [r.left, r.right, window.innerWidth, r.top, r.bottom, window.innerHeight]; });
  box[1] <= box[2] + 1 && box[3] <= 0 && box[4] >= box[5] - 1 ? ok("drawer spans full viewport height " + box) : fail("drawer geometry " + box);
  await mp.screenshot({ path: `${out}/mobile-drawer-open.png` });
  await mp.tap(".drawer-x"); await mp.waitForTimeout(450); (await state()).open ? fail("× did not close") : ok("closes with ×");
  await openIt(); await mp.tap(".scrim", { position: { x: 20, y: 400 } }); await mp.waitForTimeout(450); (await state()).open ? fail("overlay did not close") : ok("closes on overlay tap");
  await openIt(); await mp.keyboard.press("Escape"); await mp.waitForTimeout(450); (await state()).open ? fail("Escape did not close") : ok("closes on Escape");
  await openIt(); await mp.tap("#drawer .acc-btn >> nth=2"); await mp.waitForTimeout(400);
  (await mp.getAttribute("#drawer .acc-btn >> nth=2", "aria-expanded")) === "true" ? ok("accordion expands") : fail("accordion");
  await mp.screenshot({ path: `${out}/mobile-drawer-accordion.png` });
  await Promise.all([mp.waitForURL("**/policyholder-calculators/coinsurance-penalty-calculator/"), mp.tap("#acc-2 a[href$='coinsurance-penalty-calculator/']")]);
  const s2 = await state();
  !s2.open && mp.url().endsWith("/policyholder-calculators/coinsurance-penalty-calculator/") ? ok("link tap navigates to " + mp.url().replace(base, "")) : fail("drawer link " + mp.url());
  const cb = await mp.$eval(".callbar", (e) => getComputedStyle(e).position + " " + getComputedStyle(e).display);
  cb.startsWith("fixed") ? ok("mobile call bar " + cb) : fail("call bar " + cb);
  await mctx.close();

  // 5. reduced motion + no-JS render
  const nj = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
  const np = await nj.newPage();
  await np.goto(base + "/", { waitUntil: "load" });
  const njHidden = await np.evaluate(() => Array.from(document.querySelectorAll(".rv, .region-panel")).filter(e => getComputedStyle(e).opacity < 0.9 || getComputedStyle(e).display === "none").length);
  njHidden ? fail("no-JS: " + njHidden + " blocks hidden") : ok("no-JS: all content visible");
  await np.screenshot({ path: `${out}/nojs-home.png`, fullPage: false });
  await nj.close();

  const uniq = [...new Set(consoleErrs)];
  uniq.length ? uniq.slice(0, 20).forEach(fail) : ok("no console errors or failed requests");
  await browser.close();
  fs.writeFileSync(`${out}/qa.json`, JSON.stringify(results, null, 1));
  console.log(`\n${results.notes.length} passed, ${results.errors.length} failed`);
  process.exit(results.errors.length ? 1 : 0);
})();
