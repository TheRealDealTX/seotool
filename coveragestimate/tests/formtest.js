const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const base = 'http://127.0.0.1:8765';
  for (const path of ['/contact/', '/']) {
    const p = await b.newPage({viewport:{width:1280,height:900}}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
    await p.goto(base+path, {waitUntil:'networkidle'});
    const form = p.locator('form.elementor-form').first();
    await form.locator('[name="form_fields[name]"]').fill('TEST Local Name');
    await form.locator('[name="form_fields[email]"]').fill('test@example.com');
    await form.locator('[name="form_fields[phone]"]').fill('8005550142');
    await form.locator('[name="form_fields[property]"]').fill('Test Condos');
    await form.locator('[name="form_fields[units]"]').fill('42');
    await form.locator('[name="form_fields[message]"]').fill('Line one\nLine two');
    const [resp] = await Promise.all([p.waitForResponse(r=>r.url().includes('admin-ajax.php')), form.locator('button[type=submit]').click()]);
    await p.waitForTimeout(800);
    console.log(path, resp.status(), (await resp.text()).slice(0,160), '| msg:', await form.locator('.elementor-message').first().textContent().catch(()=>'none'), '| errs', errs.length);
    await p.close();
  }
  // popup on a post page
  const p = await b.newPage({viewport:{width:1280,height:900}});
  await p.goto(base+'/condo-insurance-calculator/', {waitUntil:'networkidle'}); await p.waitForTimeout(1500);
  const modal = p.locator('.elementor-popup-modal'); console.log('popup visible:', await modal.isVisible());
  const f = modal.locator('form.elementor-form');
  await f.locator('[name="form_fields[name]"]').fill('TEST Popup'); await f.locator('[name="form_fields[email]"]').fill('popup@example.com');
  const [r2] = await Promise.all([p.waitForResponse(r=>r.url().includes('admin-ajax.php')), f.locator('button[type=submit]').click()]);
  console.log('popup submit', r2.status(), (await r2.text()).slice(0,200));
  await p.waitForTimeout(2500); console.log('popup visible after submit:', await modal.isVisible().catch(()=>false));
  // invalid server-side
  const r3 = await p.evaluate(async()=>{const fd=new FormData();fd.append('action','elementor_pro_forms_send_form');fd.append('form_id','2dfe24a');fd.append('form_fields[email]','bad');const r=await fetch('/wp-admin/admin-ajax.php',{method:'POST',body:fd});return r.text();});
  console.log('invalid:', r3);
  await b.close();
})();
