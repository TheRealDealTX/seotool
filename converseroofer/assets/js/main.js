(function(){
  var cfg = window.CR_CONFIG || {};

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function(){
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Mark active nav link
  var path = location.pathname.replace(/\/index\.html$/, '/');
  document.querySelectorAll('.nav a[href]').forEach(function(a){
    var href = a.getAttribute('href');
    if (!href || a.classList.contains('btn')) return;
    var target = new URL(href, location.href).pathname.replace(/\/index\.html$/, '/');
    if (target === path || (target !== '/' && path.indexOf(target.replace(/index\.html$/, '')) === 0 && target.length > 1)) {
      a.classList.add('active');
    }
  });

  // Year in footer
  document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });

  // Lead forms
  document.querySelectorAll('form[data-lead]').forEach(function(form){
    var msg = form.querySelector('.msg');
    var started = false;
    form.addEventListener('focusin', function(){ if (!started) { started = true; try { (window.CR_track || function(){})('form_start', { form: 'lead' }); } catch(_){} } });
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if (form.querySelector('.hp input') && form.querySelector('.hp input').value) return; // honeypot
      var data = {};
      new FormData(form).forEach(function(v,k){ data[k] = v; });
      data.page = location.href;
      data.submitted = new Date().toString();
      var btn = form.querySelector('button[type=submit]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      function ok(text){
        if (msg) { msg.className = 'msg'; msg.style.display = 'block'; msg.textContent = text; }
        form.reset();
        if (btn) { btn.disabled = false; btn.textContent = label; }
        try { (window.CR_track || function(){})('generate_lead', { source: 'website_form', storm: data.storm || '', insurance_contacted: data.insurance_contacted || '' }); } catch(_){}
      }
      function fail(text){
        if (msg) { msg.className = 'msg err'; msg.style.display = 'block'; msg.textContent = text; }
        if (btn) { btn.disabled = false; btn.textContent = label; }
      }

      if (cfg.formEndpoint) {
        fetch(cfg.formEndpoint, {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
          body: JSON.stringify(data)
        }).then(function(r){
          if (r.ok) ok('Thanks — we got it. Expect a call or text from ' + (cfg.phone||'us') + ' shortly.');
          else fail('Something went wrong sending the form. Please call or text ' + (cfg.phone||'us') + '.');
        }).catch(function(){
          fail('Something went wrong sending the form. Please call or text ' + (cfg.phone||'us') + '.');
        });
      } else {
        // No endpoint configured: hand the lead off as an email draft (if leadEmail is set) or a prefilled text message.
        var body = ['Free roof inspection request'].concat(['name','phone','address','storm','insurance_contacted','notes'].filter(function(k){ return data[k]; }).map(function(k){ return k + ': ' + data[k]; })).join('\n');
        if (cfg.leadEmail) {
          window.location.href = 'mailto:' + cfg.leadEmail + '?subject=' + encodeURIComponent('Free roof inspection request — ' + (data.name||'')) + '&body=' + encodeURIComponent(body);
          ok('Thanks — your email app should open with the details. If it did not, call or text ' + (cfg.phone||'us') + '.');
        } else {
          window.location.href = (cfg.smsHref || 'sms:') + '?&body=' + encodeURIComponent(body);
          ok('Thanks — your messaging app should open with the details ready to send to ' + (cfg.phone||'us') + '. If it did not, just call or text that number.');
        }
      }
    });
  });

  // Phone links from config
  document.querySelectorAll('[data-phone]').forEach(function(el){
    if (cfg.phone) el.textContent = cfg.phone;
    if (el.tagName === 'A' && cfg.phoneHref) el.href = cfg.phoneHref;
  });
})();
