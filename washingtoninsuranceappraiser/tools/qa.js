// Functional QA: every calculator's math, the mobile drawer end to end, logo hover color, overflow and image loading.
// node tools/qa.js <baseURL>
const { chromium, devices } = require("playwright");
const fs = require("fs");
const base = process.argv[2] || "http://127.0.0.1:8099";
let fails = 0;
const ok = (cond, msg) => { console.log((cond ? "PASS " : "FAIL ") + msg); if (!cond) fails++; };
const T = "/free-claim-calculators/";
const money = n => "$" + Math.round(n).toLocaleString("en-US");

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, acceptDownloads: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  const txt = async (sel) => (await page.locator(sel).first().textContent()).trim();

  // 1. Appraisal payoff: 23,600 vs 38,900, 55%, flat 3,000 + half of 3,600
  await page.goto(base + T + "appraisal-payoff-calculator/");
  const gap = 38900 - 23600, award = 23600 + gap * 0.55, gain = award - 23600;
  ok(await txt("[data-o=gap]") === money(gap), "payoff: dispute " + money(gap));
  ok(await txt("[data-o=award]") === money(award), "payoff: award " + money(award) + " (got " + await txt("[data-o=award]") + ")");
  ok(await txt("[data-o=cost]") === money(4800), "payoff: cost $4,800");
  ok(await txt("[data-o=net]") === money(gain - 4800), "payoff: net " + money(gain - 4800));
  ok(await txt("[data-o=pct]") === "65%", "payoff: gap 65%");
  await page.selectOption("[name=feetype]", "pct"); await page.fill("[name=fee]", "10");
  ok(await txt("[data-o=cost]") === money(gain * 0.1 + 1800), "payoff: 10% fee + half umpire = " + money(gain * 0.1 + 1800) + " (got " + await txt("[data-o=cost]") + ")");

  // 2. Holdback: rows (21000,11,30) (2800,5,10) (2600,7,12), cap 80%, deductible 1,500
  await page.goto(base + T + "replacement-cost-holdback-calculator/");
  const rows = [[21000, 11, 30], [2800, 5, 10], [2600, 7, 12]];
  const rcv = rows.reduce((s, r) => s + r[0], 0), dep = rows.reduce((s, r) => s + Math.min(0.8, r[1] / r[2]) * r[0], 0);
  const first = rcv - dep - 1500;
  ok(await txt("[data-o=rcv]") === money(rcv), "holdback: RCV " + money(rcv));
  ok(await txt("[data-o=dep]") === money(dep), "holdback: depreciation " + money(dep) + " (got " + await txt("[data-o=dep]") + ")");
  ok(await txt("[data-o=first]") === money(first), "holdback: first check " + money(first));
  ok(await txt("[data-o=held]") === money(dep), "holdback: held back " + money(dep));
  ok(await txt("[data-o=total]") === money(rcv - 1500), "holdback: total " + money(rcv - 1500));
  await page.check("[name=nonrec]");
  ok(await txt("[data-o=total]") === money(first) && await txt("[data-o=held]") === "$0", "holdback: ACV-only total = first check, held $0");
  await page.click("[data-add]");
  ok(await page.locator("[data-tool=dep] tbody tr").count() === 4, "holdback: add row");
  await page.locator("[data-tool=dep] tbody tr .x").last().click();
  ok(await page.locator("[data-tool=dep] tbody tr").count() === 3, "holdback: remove row");

  // 3. Roof: 52x30 footprint, 18in overhang, 8/12, 12% waste
  await page.goto(base + T + "roof-pitch-squares-calculator/");
  const foot = (52 + 3) * (30 + 3), mult = Math.sqrt(1 + (8 / 12) ** 2), sq = foot * mult / 100, order = sq * 1.12;
  ok(await txt("[data-o=mult]") === mult.toFixed(3), "roof: 8/12 multiplier " + mult.toFixed(3));
  ok(await txt("[data-o=sq]") === sq.toFixed(2), "roof: squares " + sq.toFixed(2) + " (got " + await txt("[data-o=sq]") + ")");
  ok(await txt("[data-o=order]") === (Math.ceil(order * 3) / 3).toFixed(2), "roof: order with waste " + (Math.ceil(order * 3) / 3).toFixed(2));
  ok(await txt("[data-o=bundles]") === String(Math.ceil(order * 3)), "roof: bundles " + Math.ceil(order * 3));
  await page.click("text=I know the footprint area");
  await page.fill("[name=area]", "2000"); await page.selectOption("[name=pitch]", "12");
  ok(await txt("[data-o=sq]") === "28.28", "roof: area mode 2000 @ 12/12 = 28.28");
  await page.fill("[name=price]", "600");
  ok(await txt("[data-o=cost]") === money(28.2843 * 1.12 * 600), "roof: cost at $600/sq");

  // 4. Percentage deductible: 520,000 x 10% vs $68,000 loss
  await page.goto(base + T + "percentage-deductible-calculator/");
  ok(await txt("[data-o=pd]") === "$52,000", "deductible: 10% = $52,000");
  ok(await txt("[data-o=pdpay]") === "$16,000", "deductible: pays $16,000");
  ok(await txt("[data-o=flatpay]") === "$67,000", "deductible: flat pays $67,000");
  ok(await txt("[data-o=diff]") === "$51,000", "deductible: extra $51,000");
  await page.selectOption("[name=pct]", "2");
  ok(await txt("[data-o=pd]") === "$10,400", "deductible: 2% wind/hail = $10,400");
  await page.fill("[name=loss]", "8000");
  ok((await txt("[data-o=below]")).includes("entirely within"), "deductible: loss below deductible message");

  // 5. Timeline planner + .ics
  await page.goto(base + T + "claim-timeline-planner/");
  await page.fill("[name=dol]", "2026-11-19");
  await page.dispatchEvent("[name=dol]", "change");
  const items = await page.locator("[data-o=timeline] li").allTextContents();
  ok(items.length === 5, "timeline: 5 milestones");
  ok(items.some(t => t.includes("Nov 19, 2027")), "timeline: suit limitation 365 days -> Nov 19, 2027");
  ok(items.some(t => t.includes("May 18, 2027")), "timeline: depreciation 180 days -> May 18, 2027");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("[data-ics]")]);
  const ics = fs.readFileSync(await dl.path(), "utf8");
  ok(dl.suggestedFilename() === "washington-claim-timeline.ics" && (ics.match(/BEGIN:VEVENT/g) || []).length === 5 && ics.includes("DTSTART;VALUE=DATE:20271119"), "timeline: .ics with 5 events");

  // 6. Readiness quiz
  await page.goto(base + T + "appraisal-readiness-quiz/");
  for (const b of await page.locator(".quiz .yes").all()) await b.click();
  ok(await txt("[data-o=score]") === "100", "quiz: all yes = 100");
  for (const b of await page.locator(".quiz .no").all()) await b.click();
  ok(await txt("[data-o=score]") === "0" && await page.locator("[data-o=todo] li").count() === 12, "quiz: all no = 0 with 12 to-dos");
  await page.click("[data-reset]");
  ok(await txt("[data-o=score]") === "–", "quiz: reset");

  // 7. Wildfire coverage check: 2200 x 325, 10% code, 35,000 debris; A 560,000 +25% ERC, 10% O&L; contents 50% vs 260,000
  await page.goto(base + T + "wildfire-total-loss-coverage-check/");
  const base_ = 2200 * 325, need = base_ * 1.1 + 35000, have = 560000 * 1.25 + 56000;
  ok(await txt("[data-o=need]") === money(need), "wildfire: rebuild " + money(need));
  ok(await txt("[data-o=have]") === money(have), "wildfire: available " + money(have));
  ok(await txt("[data-o=short]") === money(need - have) && (await txt("[data-o=gaplabel]")).includes("shortfall"), "wildfire: shortfall " + money(need - have));
  ok((await txt("[data-o=cgap]")).startsWith("$280,000") && (await txt("[data-o=cgap]")).includes("covered"), "wildfire: contents limit $280,000 covers $260,000");
  await page.selectOption("[name=erc]", "50");
  ok((await txt("[data-o=gaplabel]")).includes("cushion"), "wildfire: 50% ERC flips to cushion");

  // home mini gap check
  await page.goto(base + "/");
  ok(await txt("[data-tool=gap] [data-o=gap]") === "$15,300", "home: quick gap check works");
  ok(await txt("[data-tool=gap] [data-o=award]") === "$31,250", "home: quick gap award at 50%");

  // logo hover: color and underline must not change (header + footer)
  await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(300);
  for (const sel of [".site-head .brand", ".site-foot .brand"]) {
    const el = page.locator(sel).first();
    await el.scrollIntoViewIfNeeded(); await page.mouse.move(5, 5); await page.waitForTimeout(300);
    const read = () => el.evaluate(n => [getComputedStyle(n).color, getComputedStyle(n.querySelector("b")).color, getComputedStyle(n.querySelector(".brand-t span")).color, getComputedStyle(n).textDecorationLine, getComputedStyle(n.querySelector("b")).textDecorationLine].join("|"));
    const before = await read();
    await el.hover(); await page.waitForTimeout(400);
    const after = await read();
    ok(before === after, `logo hover unchanged ${sel} (${before} -> ${after})`);
  }
  ok(errs.length === 0, "no console/page errors on desktop " + errs.join(" | "));

  // mobile drawer end to end
  const m = await browser.newContext({ ...devices["iPhone 13"] });
  const mp = await m.newPage();
  mp.on("pageerror", e => errs.push(String(e)));
  await mp.goto(base + "/");
  const open = async () => { await mp.click(".burger"); await mp.waitForTimeout(500); };
  const isOpen = () => mp.evaluate(() => document.body.classList.contains("drawer-open") && !document.getElementById("drawer").hasAttribute("inert") && document.getElementById("drawer").getAttribute("aria-hidden") === "false" && getComputedStyle(document.body).overflow === "hidden" && document.querySelector(".burger").getAttribute("aria-expanded") === "true");
  const isClosed = () => mp.evaluate(() => { const d = document.getElementById("drawer"); return !document.body.classList.contains("drawer-open") && d.hasAttribute("inert") && d.getAttribute("aria-hidden") === "true" && getComputedStyle(d).visibility === "hidden" && getComputedStyle(d).boxShadow === "none"; });
  ok(await isClosed(), "drawer: closed, hidden and shadowless on load");
  ok(await mp.evaluate(() => { const d = document.getElementById("drawer"); return !document.querySelector(".site-head").contains(d); }), "drawer: lives outside the sticky header");
  await open(); ok(await isOpen(), "drawer: opens with scroll lock, inert removed, aria updated");
  await mp.click(".drawer-x"); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with ×");
  await open(); await mp.mouse.click(20, 400); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with overlay tap");
  await open(); await mp.keyboard.press("Escape"); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with Escape");
  await open();
  await mp.click(".acc-btn >> text=Cities"); await mp.waitForTimeout(450);
  ok(await mp.getAttribute(".acc-btn >> text=Cities", "aria-expanded") === "true", "drawer: accordion expands");
  await Promise.all([mp.waitForURL("**/cities-we-serve/bellingham/"), mp.click("#drawer a[href='/cities-we-serve/bellingham/']")]);
  ok(mp.url().endsWith("/cities-we-serve/bellingham/"), "drawer: link lands on " + mp.url());
  ok(await isClosed(), "drawer: closed after navigating");
  ok(await mp.evaluate(() => document.documentElement.scrollWidth === window.innerWidth), "mobile: no horizontal scroll on location page");
  ok(await mp.locator(".call-bar").isVisible(), "mobile: call bar visible");
  ok(errs.length === 0, "no page errors " + errs.join(" | "));
  await browser.close();
  console.log(fails ? `${fails} FAILED` : "ALL PASSED");
  process.exit(fails ? 1 : 0);
})();
