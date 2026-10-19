const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--proxy-server=https=' + process.env.HTTPS_PROXY.replace(/^https?:\/\//, '')] });
  const p = await b.newPage({ ignoreHTTPSErrors: true });
  p.on('requestfailed', r => console.log('FAIL', r.url().slice(0, 90), r.failure().errorText));
  p.on('response', r => r.url().includes('open-meteo') && console.log('RESP', r.status()));
  await p.goto(process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } });
  await p.waitForTimeout(4000);
  console.log(await p.evaluate(() => ({
    reveal: [...document.querySelectorAll('[data-reveal]')].map(e => e.className + ':' + e.classList.contains('is-in')).join(' | '),
    temp: document.querySelector('[data-w=temp]')?.textContent, cond: document.querySelector('[data-w=cond]')?.textContent,
    map: document.querySelector('.txmap svg')?.getBoundingClientRect().height,
  })));
  await b.close();
})();
