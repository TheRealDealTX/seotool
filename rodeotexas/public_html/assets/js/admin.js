/* Admin behaviour (no inline scripts: the admin runs under a strict CSP). */
(function () {
  'use strict';
  // Confirm before destructive or long-running actions: <form data-confirm="…">
  document.addEventListener('submit', function (e) {
    var f = e.target;
    var msg = f.getAttribute('data-confirm');
    var btn = e.submitter;
    if (btn && btn.getAttribute('data-confirm')) { msg = btn.getAttribute('data-confirm'); }
    if (msg && !window.confirm(msg)) { e.preventDefault(); return; }
    // Prevent double submits of long imports.
    if (f.querySelector('input[name="action"][value="run_import"], input[name="action"][value="run"]')) {
      Array.prototype.forEach.call(f.querySelectorAll('button[type="submit"], button:not([type])'), function (b) {
        setTimeout(function () { b.disabled = true; b.textContent = 'Running… please wait'; }, 0);
      });
    }
  });
  // Live JSON check for source configuration.
  var cfg = document.getElementById('f_config');
  if (cfg) {
    cfg.addEventListener('input', function () {
      try { JSON.parse(cfg.value || '{}'); cfg.setCustomValidity(''); } catch (err) { cfg.setCustomValidity('Invalid JSON: ' + err.message); }
      cfg.reportValidity();
    });
  }
})();
