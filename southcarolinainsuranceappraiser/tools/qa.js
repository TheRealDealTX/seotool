// Functional QA: tool math, mobile drawer end to end, logo hover color.
// node tools/qa.js <baseURL>
const { chromium, devices } = require("playwright");
const base = process.argv[2] || "http://127.0.0.1:8099";
let fails = 0;
const ok = (cond, msg) => { console.log((cond ? "PASS " : "FAIL ") + msg); if (!cond) fails++; };
const T = "/free-claim-tools/";

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, acceptDownloads: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  const txt = async (sel) => (await page.locator(sel).first().textContent()).trim();

  await page.goto(base + T + "claim-gap-fee-estimator/");
  ok(await txt("[data-o=gap]") === "$15,300", "gap: dispute $15,300");
  ok(await txt("[data-o=award]") === "$32,015", "gap: award $32,015");
  ok(await txt("[data-o=cost]") === "$4,400", "gap: cost $4,400");
  ok(await txt("[data-o=net]") === "$4,015", "gap: net $4,015");
  ok(await txt("[data-o=pct]") === "65%", "gap: 65%");
  await page.selectOption("[name=feetype]", "pct"); await page.fill("[name=fee]", "10");
  ok(await txt("[data-o=cost]") === "$2,442", "gap: 10% fee + half umpire = $2,442 (got " + await txt("[data-o=cost]") + ")");

  await page.goto(base + T + "rcv-acv-holdback-calculator/");
  ok(await txt("[data-o=rcv]") === "$27,900", "dep: RCV $27,900");
  ok(await txt("[data-o=dep]") === "$15,087", "dep: depreciation $15,087");
  ok(await txt("[data-o=first]") === "$10,313", "dep: first check $10,313");
  ok(await txt("[data-o=held]") === "$15,087", "dep: holdback $15,087");
  ok(await txt("[data-o=total]") === "$25,400", "dep: total $25,400");
  await page.check("[name=nonrec]");
  ok(await txt("[data-o=total]") === "$10,313" && await txt("[data-o=held]") === "$0", "dep: ACV-only total $10,313, holdback $0");
  await page.click("[data-add]");
  ok(await page.locator("[data-tool=dep] tbody tr").count() === 4, "dep: add line");

  await page.goto(base + T + "roof-area-pitch-estimator/");
  ok(await txt("[data-o=mult]") === "1.158", "roof: 7/12 factor 1.158");
  ok(await txt("[data-o=sq]") === "25.75", "roof: 25.75 squares (got " + await txt("[data-o=sq]") + ")");
  ok(await txt("[data-o=order]") === "29.33", "roof: 29.33 with waste");
  ok(await txt("[data-o=bundles]") === "88", "roof: 88 bundles");
  await page.click("text=Footprint area");
  await page.fill("[name=area]", "2000"); await page.selectOption("[name=pitch]", "12");
  ok(await txt("[data-o=sq]") === "28.28", "roof: area mode 2000 @12/12 = 28.28");

  await page.goto(base + T + "hurricane-deductible-calculator/");
  ok(await txt("[data-o=pd]") === "$8,200", "deduct: $8,200");
  ok(await txt("[data-o=pdpay]") === "$18,200", "deduct: pays $18,200");
  ok(await txt("[data-o=flatpay]") === "$24,900", "deduct: flat pays $24,900");
  ok(await txt("[data-o=diff]") === "$6,700", "deduct: diff $6,700");

  await page.goto(base + T + "wind-flood-damage-splitter/");
  ok(await txt("[data-o=windpay]") === "$44,400", "split: wind pays $44,400");
  ok(await txt("[data-o=floodpay]") === "$38,200", "split: flood pays $38,200");
  ok(await txt("[data-o=own]") === "$13,400", "split: own $13,400");
  await page.check("[name=noflood]");
  ok(await txt("[data-o=own]") === "$51,600", "split: no flood -> own $51,600");

  await page.goto(base + T + "claim-timeline-builder/");
  await page.fill("[name=dol]", "2026-09-01");
  await page.dispatchEvent("[name=dol]", "change");
  const items = await page.locator("[data-o=timeline] li").allTextContents();
  ok(items.length === 5, "dates: 5 milestones");
  ok(items.some(t => t.includes("Aug 31, 2029")), "dates: suit reference 1,095 days -> Aug 31, 2029");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("[data-ics]")]);
  const fs = require("fs"); const p = await dl.path(); const ics = fs.readFileSync(p, "utf8");
  ok(dl.suggestedFilename() === "sc-claim-timeline.ics" && (ics.match(/BEGIN:VEVENT/g) || []).length === 5 && ics.includes("DTSTART;VALUE=DATE:20290831"), "dates: .ics with 5 events");

  await page.goto(base + T + "appraisal-readiness-checkup/");
  for (const b of await page.locator(".quiz .yes").all()) await b.click();
  ok(await txt("[data-o=score]") === "100", "ready: all yes = 100");
  for (const b of await page.locator(".quiz .no").all()) await b.click();
  ok(await txt("[data-o=score]") === "0" && await page.locator("[data-o=todo] li").count() === 12, "ready: all no = 0 with 12 to-dos");

  await page.goto(base + "/");
  ok(await txt("[data-tool=gap] [data-o=gap]") === "$15,300", "home mini gap check works");

  // logo hover: color must not change (header + footer)
  for (const sel of [".head .brand", ".foot .brand"]) {
    const el = page.locator(sel).first();
    await el.scrollIntoViewIfNeeded();
    const before = await el.evaluate(n => [getComputedStyle(n).color, getComputedStyle(n.querySelector("b")).color, getComputedStyle(n).textDecorationLine].join("|"));
    await el.hover(); await page.waitForTimeout(400);
    const after = await el.evaluate(n => [getComputedStyle(n).color, getComputedStyle(n.querySelector("b")).color, getComputedStyle(n).textDecorationLine].join("|"));
    ok(before === after, `logo hover unchanged ${sel} (${before} -> ${after})`);
  }
  ok(errs.length === 0, "no page errors on desktop " + errs.join(" | "));

  // mobile drawer end to end
  const m = await browser.newContext({ ...devices["iPhone 13"] });
  const mp = await m.newPage();
  mp.on("pageerror", e => errs.push(String(e)));
  await mp.goto(base + "/");
  const open = async () => { await mp.click(".burger"); await mp.waitForTimeout(500); };
  const isOpen = () => mp.evaluate(() => document.body.classList.contains("drawer-open") && !document.getElementById("drawer").hasAttribute("inert") && getComputedStyle(document.body).overflow === "hidden");
  const isClosed = () => mp.evaluate(() => !document.body.classList.contains("drawer-open") && document.getElementById("drawer").hasAttribute("inert") && document.getElementById("drawer").getAttribute("aria-hidden") === "true" && getComputedStyle(document.getElementById("drawer")).visibility === "hidden");
  ok(await isClosed(), "drawer: closed and hidden on load (no edge shadow)");
  ok(await mp.evaluate(() => getComputedStyle(document.getElementById("drawer")).boxShadow === "none"), "drawer: no shadow while closed");
  await open(); ok(await isOpen(), "drawer: opens with scroll lock + inert removed");
  await mp.click(".drawer-close"); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with ×");
  await open(); await mp.mouse.click(380, 400); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with overlay tap");
  await open(); await mp.keyboard.press("Escape"); await mp.waitForTimeout(500); ok(await isClosed(), "drawer: closes with Escape");
  await open();
  await mp.click(".acc-btn >> text=Locations"); await mp.waitForTimeout(450);
  ok(await mp.getAttribute(".acc-btn >> text=Locations", "aria-expanded") === "true", "drawer: accordion expands");
  await Promise.all([mp.waitForNavigation(), mp.click("#drawer a[href='/locations-served/beaufort/']")]);
  ok(mp.url().endsWith("/locations-served/beaufort/"), "drawer: link lands on " + mp.url());
  ok(await isClosed(), "drawer: closed after navigating");
  ok(await mp.evaluate(() => document.documentElement.scrollWidth === window.innerWidth), "mobile: no horizontal scroll on location page");
  ok(errs.length === 0, "no page errors " + errs.join(" | "));
  await browser.close();
  console.log(fails ? `${fails} FAILED` : "ALL PASSED");
  process.exit(fails ? 1 : 0);
})();
