// Playwright QA: screenshots, overflow, lazy images, console errors, tool math, mobile drawer, logo hover.
// usage: node tools/qa.js http://127.0.0.1:8080 <screenshot-dir>
const { chromium, devices } = require("playwright");
const fs = require("fs");
const BASE = process.argv[2] || "http://127.0.0.1:8080";
const OUT = process.argv[3] || "/tmp/qa";
fs.mkdirSync(OUT, { recursive: true });
const fails = [];
const ok = (cond, msg) => { if (!cond) fails.push(msg); console.log((cond ? "PASS " : "FAIL ") + msg); };
const near = (a, b, tol = 1) => Math.abs(a - b) <= tol;
const money = (s) => parseFloat(String(s).replace(/[^0-9.\-−]/g, "").replace("−", "-"));

async function wheelThrough(page) {
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h + 1000; y += 600) { await page.mouse.wheel(0, 600); await page.waitForTimeout(60); }
  await page.waitForTimeout(500);
}

(async () => {
  const browser = await chromium.launch();
  const urls = fs.readFileSync(__dirname + "/../public/sitemap.xml", "utf8").match(/<loc>[^<]+/g).map((l) => l.slice(5).replace("https://oregoninsuranceappraiser.com", ""));

  // ---- every page at phone width: no horizontal scroll, no console errors, all images load
  const ctxM = await browser.newContext({ ...devices["iPhone 13"] });
  for (const u of urls.concat(["/404.html"])) {
    const p = await ctxM.newPage();
    const errs = [];
    p.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
    p.on("pageerror", (e) => errs.push(String(e)));
    await p.goto(BASE + u, { waitUntil: "load" });
    await wheelThrough(p);
    const r = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, vw: window.innerWidth,
      bad: [...document.images].filter((i) => !i.complete || i.naturalWidth === 0).map((i) => i.src) }));
    ok(r.sw <= r.vw, `${u} no horizontal scroll at ${r.vw}px (scrollWidth ${r.sw})`);
    ok(r.bad.length === 0, `${u} all images loaded ${r.bad.join(" ")}`);
    ok(errs.length === 0, `${u} no console errors ${errs.join(" | ")}`);
    await p.close();
  }

  // ---- screenshots
  const shots = { home: "/", service: "/property-appraisals/wildfire-loss-appraisal/", location: "/appraisal-near-you/portland/", tool: "/oregon-claim-calculators/appraisal-payoff-estimator/" };
  const ctxD = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  for (const [k, u] of Object.entries(shots)) {
    for (const [name, ctx] of [["desktop", ctxD], ["mobile", ctxM]]) {
      const p = await ctx.newPage();
      await p.goto(BASE + u, { waitUntil: "load" });
      await wheelThrough(p);
      await p.evaluate(() => window.scrollTo(0, 0)); await p.waitForTimeout(400);
      await p.screenshot({ path: `${OUT}/${k}-${name}.png`, fullPage: true });
      if (name === "desktop") { const sw = await p.evaluate(() => document.documentElement.scrollWidth); ok(sw <= 1440, `${u} desktop no overflow (${sw})`); }
      await p.close();
    }
  }

  // ---- tool math
  const p = await ctxD.newPage();
  const fill = async (sel, v) => { await p.fill(sel, String(v)); await p.dispatchEvent(sel, "input"); };
  const txt = async (sel) => (await p.textContent(sel)).trim();
  await p.goto(BASE + "/oregon-claim-calculators/appraisal-payoff-estimator/");
  await fill("#g-ins", 20000); await fill("#g-own", 30000);
  await p.fill("#g-land", "50"); await p.dispatchEvent("#g-land", "input");
  await p.selectOption("#g-ft", "flat"); await fill("#g-fee", 2000); await fill("#g-ump", 3000);
  // gap 10000, gain 5000, cost 2000+1500 = 3500, net 1500; lo 3000-3500=-500, mid 5500-3500=2000, hi 8000-3500=4500
  ok(money(await txt("[data-o=gap]")) === 10000, "payoff: gap 10,000");
  ok(money(await txt("[data-o=net]")) === 1500, "payoff: net 1,500 at 50%");
  ok(money(await txt("[data-o=lo]")) === -500 && money(await txt("[data-o=mid]")) === 2000 && money(await txt("[data-o=hi]")) === 4500, "payoff: 30/55/80% scenarios");
  await p.selectOption("#g-ft", "pct"); await fill("#g-fee", 10);
  ok(money(await txt("[data-o=net]")) === 3000, "payoff: percent fee (5000 - 500 - 1500 = 3000)");

  await p.goto(BASE + "/oregon-claim-calculators/depreciation-holdback-tracker/");
  // rows: 21400 12/30, 6200 8/20, 3100 5/10 → dep = 8560 + 2480 + 1550 = 12590; rcv 30700; acv 18110; first 15610; total 28200; held 12590
  ok(money(await txt("[data-o=dep]")) === 12590, "dep: depreciation 12,590");
  ok(money(await txt("[data-o=first]")) === 15610 && money(await txt("[data-o=held]")) === 12590 && money(await txt("[data-o=total]")) === 28200, "dep: first / holdback / total");
  await p.selectOption("#d-dl", "no"); // materials only at 45% labor → dep × 0.55 = 6924.5
  ok(near(money(await txt("[data-o=dep]")), 6925), "dep: labor not depreciated (≈6,925)");
  await p.check("[name=nonrec]");
  ok(money(await txt("[data-o=held]")) === 0, "dep: ACV-only policy holds back nothing");

  await p.goto(BASE + "/oregon-claim-calculators/roof-pitch-squares-converter/");
  await fill("#r-l", 50); await fill("#r-w", 30); await fill("#r-oh", 0);
  await p.selectOption("#r-p", "12"); await p.selectOption("#r-wst", "10"); await fill("#r-c", 20);
  // 1500 sq ft × 1.41421 = 2121.3 → 21.21 sq; with 10% waste 23.33; bundles ceil(70.004)=71; vs 20 → +3.33
  ok((await txt("[data-o=sq]")) === "21.21", "roof: 21.21 squares at 12/12");
  ok((await txt("[data-o=deg]")) === "45.0°", "roof: 12/12 = 45°");
  ok((await txt("[data-o=bundles]")) === "71", "roof: 71 bundles (70.004 rounded up)");
  ok((await txt("[data-o=cmp]")).startsWith("+3.33"), "roof: +3.33 squares vs insurer");

  await p.goto(BASE + "/oregon-claim-calculators/percentage-deductible-checker/");
  await p.selectOption("#w-t", "eq");
  ok((await p.inputValue("#w-p")) === "10", "deduct: earthquake preset to 10%");
  await fill("#w-a", 400000); await fill("#w-l", 60000); await fill("#w-f", 1000);
  ok(money(await txt("[data-o=pd]")) === 40000 && money(await txt("[data-o=pdpay]")) === 20000 && money(await txt("[data-o=diff]")) === 39000, "deduct: 10% of 400k, pays 20k, 39k extra");

  await p.goto(BASE + "/oregon-claim-calculators/claim-calendar-builder/");
  await p.fill("#t-d", "2026-01-10"); await p.dispatchEvent("#t-d", "input");
  await p.fill("#t-a", "2026-03-01"); await p.dispatchEvent("#t-a", "input");
  const items = await p.$$eval("[data-o=timeline] li", (l) => l.map((x) => x.textContent));
  ok(items.length === 6, "dates: six milestones with demand date");
  ok(items.some((t) => t.includes("Jan 10, 2028") && t.includes("file suit")), "dates: suit date two years out (Jan 10, 2028)");
  ok(items.some((t) => t.includes("Mar 21, 2026") && t.includes("Name your appraiser")), "dates: appraiser named 20 days after demand");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("[data-ics]")]);
  const ics = fs.readFileSync(await dl.path(), "utf8");
  ok(ics.startsWith("BEGIN:VCALENDAR") && (ics.match(/BEGIN:VEVENT/g) || []).length === 6 && ics.includes("DTSTART;VALUE=DATE:20280110"), "dates: .ics export with 6 events");

  await p.goto(BASE + "/oregon-claim-calculators/appraisal-readiness-checkup/");
  const qs = await p.$$(".quiz li");
  for (let i = 0; i < qs.length; i++) await (await qs[i].$(i < 6 ? ".yes" : ".no")).click();
  // weights: first six yes = 3+3+3+2+2+2 = 15 of 24 → 63
  ok((await txt("[data-o=score]")) === "63", "ready: score 63 with first six yes");
  ok((await p.$$("[data-o=todo] li")).length === 6, "ready: six to-do items");

  await p.goto(BASE + "/oregon-claim-calculators/wildfire-contents-estimator/");
  // defaults: 3*9000+2*2200+16000+2*11000+6000+7000+12000+5000 = 99400, typical ×1 ; 7 yrs → 42% ; covC 210000
  ok(money(await txt("[data-o=rcv]")) === 99400, "contents: default total 99,400");
  ok(near(money(await txt("[data-o=acv]")), 57652), "contents: ACV at 42% depreciation");
  await p.selectOption("#c-lvl", "1.9"); await fill("#c-c", 150000);
  ok(near(money(await txt("[data-o=short]")), 188860 - 150000), "contents: shortfall vs limit");

  await p.goto(BASE + "/insurance-claim-dictionary/");
  await fill("#gloss-filter", "umpire");
  const vis = await p.$$eval(".glossary dt", (d) => d.filter((x) => !x.hidden).length);
  ok(vis >= 1 && vis < 10, `glossary search narrows results (${vis})`);
  const total = await p.$$eval(".glossary dt", (d) => d.length);
  ok(total >= 35, `glossary has ${total} terms`);

  // ---- logo hover: header + footer brand must not change color
  await p.goto(BASE + "/property-appraisals/");
  for (const sel of [".head .brand", ".foot .brand"]) {
    await p.locator(sel).scrollIntoViewIfNeeded();
    const before = await p.$eval(sel, (a) => [getComputedStyle(a).color, getComputedStyle(a.querySelector("b")).color, getComputedStyle(a).textDecorationLine]);
    await p.hover(sel); await p.waitForTimeout(400);
    const after = await p.$eval(sel, (a) => [getComputedStyle(a).color, getComputedStyle(a.querySelector("b")).color, getComputedStyle(a).textDecorationLine]);
    ok(JSON.stringify(before) === JSON.stringify(after), `${sel} unchanged on hover ${JSON.stringify(after)}`);
  }

  // ---- mobile drawer end to end
  const m = await ctxM.newPage();
  await m.goto(BASE + "/");
  const st = () => m.evaluate(() => ({ open: document.body.classList.contains("drawer-open"), lock: getComputedStyle(document.body).overflow, inert: document.getElementById("drawer").hasAttribute("inert"), aria: document.getElementById("drawer").getAttribute("aria-hidden"), vis: getComputedStyle(document.getElementById("drawer")).visibility, shadow: getComputedStyle(document.getElementById("drawer")).boxShadow }));
  let s0 = await st();
  ok(!s0.open && s0.inert && s0.aria === "true" && s0.vis === "hidden" && s0.shadow === "none", "drawer closed: inert, hidden, no shadow");
  await m.click(".burger"); await m.waitForTimeout(500);
  let s1 = await st();
  ok(s1.open && !s1.inert && s1.aria === "false" && s1.lock === "hidden" && s1.vis === "visible", "drawer opens with scroll lock");
  const box = await m.$eval("#drawer", (d) => { const r = d.getBoundingClientRect(); return [r.left, r.width]; });
  ok(box[0] >= -1, `drawer on screen while header is sticky (left ${box[0]})`);
  await m.click("#drawer .acc-btn >> nth=1"); await m.waitForTimeout(400);
  ok((await m.getAttribute("#drawer .acc-btn >> nth=1", "aria-expanded")) === "true", "drawer accordion expands");
  await Promise.all([m.waitForURL("**/appraisal-near-you/bend/"), m.click("#drawer a[href='/appraisal-near-you/bend/']")]);
  ok(m.url().endsWith("/appraisal-near-you/bend/"), "drawer link navigates to Bend");
  await m.click(".burger"); await m.waitForTimeout(400); await m.click(".drawer-close"); await m.waitForTimeout(400);
  ok(!(await st()).open, "drawer closes with ×");
  await m.click(".burger"); await m.waitForTimeout(400); await m.mouse.click(380, 400); await m.waitForTimeout(400);
  ok(!(await st()).open, "drawer closes on overlay tap");
  await m.click(".burger"); await m.waitForTimeout(400); await m.keyboard.press("Escape"); await m.waitForTimeout(400);
  const s2 = await st();
  ok(!s2.open && s2.inert && s2.lock !== "hidden", "drawer closes with Escape and unlocks scroll");
  await m.screenshot({ path: `${OUT}/drawer-closed.png` });
  await m.click(".burger"); await m.waitForTimeout(500); await m.screenshot({ path: `${OUT}/drawer-open.png` });

  // ---- no-JS rendering keeps content visible
  const nj = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1440, height: 900 } });
  const q = await nj.newPage(); await q.goto(BASE + "/");
  const hidden = await q.$$eval(".rv", (els) => els.filter((e) => getComputedStyle(e).opacity === "0").length);
  ok(hidden === 0, `no-JS: reveal elements visible (${hidden} hidden)`);

  await browser.close();
  console.log(fails.length ? `\n${fails.length} FAILURES` : "\nALL PASS");
  process.exit(fails.length ? 1 : 0);
})();
