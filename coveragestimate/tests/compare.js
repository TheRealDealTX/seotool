const { chromium } = require('playwright');
const fs = require('fs');
const paths = fs.readFileSync('urls.txt','utf8').trim().split('\n').map(u=>u.replace('https://coveragestimate.com',''));
const LOCAL = process.argv[2] || 'http://127.0.0.1:8765';
(async () => {
  const b = await chromium.launch(); const results = [];
  async function shot(base, path, w, tag, isLocal) {
    const ctx = await b.newContext({viewport:{width:w,height:900}, reducedMotion:'reduce'});
    const p = await ctx.newPage(); const bad = []; const liveHits = []; const errs = [];
    p.on('pageerror', e=>errs.push(e.message));
    p.on('response', r=>{ if (r.status()>=400 && !r.url().includes('google')) bad.push(r.status()+' '+r.url()); });
    p.on('request', r=>{ if (isLocal && /\/\/(www\.)?coveragestimate\.com/.test(r.url())) liveHits.push(r.url()); });
    await p.goto(base+path, {waitUntil:'networkidle', timeout:60000});
    await p.addStyleTag({content:'*,*::before,*::after{animation:none!important;transition:none!important}.marquee-track{transform:none!important}'});
    const H = await p.evaluate(()=>document.body.scrollHeight);
    for (let y=0;y<H;y+=400){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(40); }
    await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(1500);
    const f = 'cmp/'+(path.replace(/\//g,'_')||'_')+'_'+w+'_'+tag+'.png';
    await p.screenshot({path:f, fullPage:true});
    const title = await p.title(); await ctx.close();
    return {f, bad, liveHits, errs, title};
  }
  for (const path of paths) for (const w of [1280, 390]) {
    const a = await shot('https://coveragestimate.com', path, w, 'live', false);
    const l = await shot(LOCAL, path, w, 'local', true);
    results.push({path, w, live:a.f, local:l.f, titleMatch:a.title===l.title, localBad:l.bad, liveHits:l.liveHits, localErrs:l.errs, liveErrs:a.errs});
  }
  fs.writeFileSync('cmp/results.json', JSON.stringify(results,null,1)); await b.close();
})();
