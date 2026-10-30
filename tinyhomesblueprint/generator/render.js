// Renders stills with headless Chromium: 3D views from the site's own viewer, and PNG
// copies of the SVG drawings. Files are served straight from disk through request
// interception, so no web server is needed.
//
//   node generator/render.js build/render-jobs.json
//
// Each job: { type: "3d", model, out, width, height, view: {theta, phi, zoom}, roof }
//        or { type: "svg", svg, out, width }
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const TYPES = { '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.html': 'text/html' };

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('page error:', e.message));
  await page.route('http://thb.local/**', route => {
    const url = new URL(route.request().url());
    if (url.pathname === '/__harness.html') {
      return route.fulfill({ contentType: 'text/html', body: '<!doctype html><html><body style="margin:0"><div id="v"><canvas></canvas></div></body></html>' });
    }
    const file = url.pathname.startsWith('/__abs/') ? decodeURIComponent(url.pathname.slice(6)) : path.join(SITE, url.pathname);
    if (!fs.existsSync(file)) return route.fulfill({ status: 404, body: '' });
    route.fulfill({ contentType: TYPES[path.extname(file)] || 'application/octet-stream', body: fs.readFileSync(file) });
  });
  let n = 0;
  for (const job of jobs) {
    fs.mkdirSync(path.dirname(job.out), { recursive: true });
    if (job.type === '3d') {
      await page.setViewportSize({ width: job.width, height: job.height });
      await page.goto('http://thb.local/__harness.html');
      await page.evaluate(async ({ job }) => {
        const el = document.getElementById('v');
        el.style.width = job.width + 'px';
        el.dataset.model = job.model;
        el.dataset.height = job.height;
        const { mount } = await import('/assets/js/plan-3d.js');
        const v = await mount(el);
        v.view(job.view || {});
        v.roof(job.roof !== false);
      }, { job });
      await page.waitForTimeout(150);
      await page.locator('canvas').screenshot({ path: job.out });
    } else {
      const svg = fs.readFileSync(job.svg, 'utf8');
      const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
      const w = job.width, h = Math.round(w * (+m[2]) / (+m[1]));
      await page.setViewportSize({ width: w, height: h });
      await page.setContent(`<html><body style="margin:0">${svg.replace(/width="[\d.]+" height="[\d.]+"/, `width="${w}" height="${h}"`)}</body></html>`);
      await page.locator('svg').first().screenshot({ path: job.out });
    }
    n++;
  }
  await browser.close();
  console.log(`rendered ${n} images`);
})().catch(e => { console.error(e); process.exit(1); });
