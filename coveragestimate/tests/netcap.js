const { chromium } = require('playwright');
const fs = require('fs');
const urls = fs.readFileSync('urls.txt','utf8').trim().split('\n').concat(['https://coveragestimate.com/this-page-does-not-exist-ce404/','https://coveragestimate.com/category/general/']);
(async () => {
  const b = await chromium.launch(); const seen = new Set(); const other = new Set();
  for (const u of urls) for (const vp of [{width:1280,height:900},{width:390,height:844}]) {
    const p = await b.newPage({viewport:vp});
    p.on('request', r => { const x = new URL(r.url()); if (x.hostname.endsWith('coveragestimate.com')) { if (!/\.html?$|\/$/.test(x.pathname) || x.pathname.startsWith('/wp-')) seen.add(x.pathname + (x.pathname.includes('admin-ajax')?' ['+r.method()+']':'')); } else other.add(x.hostname); });
    try {
      await p.goto(u, {waitUntil:'networkidle', timeout:60000});
      const H = await p.evaluate(()=>document.body.scrollHeight);
      for (let y=0;y<H;y+=500){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(50); }
      await p.waitForTimeout(800);
      if (vp.width<500) { const t = await p.$('.elementor-menu-toggle'); if (t) { await t.click().catch(()=>{}); await p.waitForTimeout(400);} }
      else { const m = await p.$('.elementor-nav-menu a.has-submenu'); if (m) { await m.hover().catch(()=>{}); await p.waitForTimeout(400);} }
    } catch(e) { console.error('ERR', u, e.message); }
    await p.close();
  }
  fs.writeFileSync('netcap.txt', [...seen].sort().join('\n'));
  console.log('same-origin assets', seen.size, '\nexternal hosts:', [...other].join(', '));
  await b.close();
})();
