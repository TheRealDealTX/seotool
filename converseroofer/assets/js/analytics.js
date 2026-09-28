/* Google Analytics 4 loader + call / text / lead tracking. Nothing loads until gaId is set in config.js. */
(function(){
  var cfg = window.CR_CONFIG || {};
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  window.gtag = gtag;
  if (cfg.gaId) {
    var s = document.createElement('script'); s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.gaId);
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', cfg.gaId, { send_page_view: true });
  }
  function page(){ return location.pathname.replace(/\/index\.html$/, '/') || '/'; }
  function track(name, params){
    try { gtag('event', name, Object.assign({ page_path: page() }, params || {})); } catch(_){}
  }
  document.addEventListener('click', function(e){
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('tel:') === 0) {
      track('call_click', { link_text: (a.textContent || '').trim().slice(0, 60), placement: a.closest('.call-bar') ? 'mobile_bar' : a.closest('.site-header') ? 'header' : a.closest('.cta-band') ? 'cta_band' : a.closest('.hero') ? 'hero' : 'body' });
      if (cfg.adsCallConversion) { try { gtag('event', 'conversion', { send_to: cfg.adsCallConversion }); } catch(_){} }
    } else if (href.indexOf('sms:') === 0) {
      track('text_click', { link_text: (a.textContent || '').trim().slice(0, 60) });
    } else if (/^https?:/.test(href) && a.hostname !== location.hostname) {
      track('outbound_click', { url: href });
    }
  }, true);
  // Expose for main.js form handler
  window.CR_track = track;
})();
