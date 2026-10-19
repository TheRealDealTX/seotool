/* Texas Landscape Lights — site interactions */
(() => {
  const d = document, body = d.body;
  const $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k, s) { try { return (s ? sessionStorage : localStorage).getItem(k); } catch (e) { return null; } },
    set(k, v, s) { try { (s ? sessionStorage : localStorage).setItem(k, v); } catch (e) {} },
  };
  const PHONE = '(281) 704-7210', TEL = 'tel:+12817047210';

  /* ---------- header, drawer, to-top ---------- */
  const hdr = $('.hdr'), top = $('.totop');
  const onScroll = () => {
    hdr && hdr.classList.toggle('is-scrolled', scrollY > 20);
    top && top.classList.toggle('is-on', scrollY > innerHeight * 1.3);
    $$('[data-reveal]:not(.is-in)').forEach(el => { if (el.getBoundingClientRect().top < innerHeight) el.classList.add('is-in'); });
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  top && top.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));
  const burger = $('.burger'), drawer = $('#drawer');
  const setNav = open => {
    body.classList.toggle('nav-open', open);
    burger && burger.setAttribute('aria-expanded', open);
    drawer && drawer.setAttribute('aria-hidden', !open);
    body.style.overflow = open ? 'hidden' : '';
    if (open) setTimeout(() => $('.drawer__x') && $('.drawer__x').focus({ preventScroll: true }), 50);
  };
  burger && burger.addEventListener('click', () => setNav(!body.classList.contains('nav-open')));
  $('.scrim') && $('.scrim').addEventListener('click', () => setNav(false));
  drawer && drawer.addEventListener('click', e => { if (e.target.closest('a')) setNav(false); });
  $('.drawer__x') && $('.drawer__x').addEventListener('click', () => { setNav(false); burger && burger.focus(); });
  d.addEventListener('keydown', e => { if (e.key === 'Escape' && body.classList.contains('nav-open')) { setNav(false); burger && burger.focus(); } });
  addEventListener('resize', () => { if (innerWidth > 1100 && body.classList.contains('nav-open')) setNav(false); });

  /* ---------- reveal + counters ---------- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px', threshold: .06 });
    $$('[data-reveal]').forEach(el => io.observe(el));
    const cio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return; cio.unobserve(e.target);
      const el = e.target, end = parseFloat(el.dataset.count), t0 = performance.now();
      const step = now => { const p = Math.min(1, (now - t0) / 1400); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
      reduce ? (el.textContent = end) : requestAnimationFrame(step);
    }), { threshold: .6 });
    $$('[data-count]').forEach(el => cio.observe(el));
  } else $$('[data-reveal]').forEach(el => el.classList.add('is-in'));

  /* ---------- hero light switch ---------- */
  $$('[data-switch]').forEach(btn => {
    const scene = d.getElementById(btn.dataset.switch);
    const set = on => { btn.setAttribute('aria-pressed', on); scene.classList.toggle('is-off', !on); scene.classList.toggle('win-on', on); $('b', btn).textContent = on ? 'Lights on' : 'Lights off'; };
    btn.addEventListener('click', () => set(btn.getAttribute('aria-pressed') !== 'true'));
    set(false); setTimeout(() => set(true), reduce ? 0 : 900);
  });

  /* ---------- tabs ---------- */
  $$('[data-tabs]').forEach(root => {
    const tabs = $$('[role=tab]', root);
    const pick = t => { tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; d.getElementById(x.getAttribute('aria-controls')).hidden = !on; }); };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => pick(t));
      t.addEventListener('keydown', e => {
        const k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (k) { e.preventDefault(); const n = tabs[(i + k + tabs.length) % tabs.length]; n.focus(); pick(n); }
      });
    });
  });

  /* ---------- texas map <-> list ---------- */
  $$('[data-map]').forEach(root => {
    const hi = slug => { $$('[data-city]', root).forEach(el => el.classList.toggle('is-on', el.dataset.city === slug)); };
    $$('[data-city]', root).forEach(el => {
      el.addEventListener('mouseenter', () => hi(el.dataset.city));
      el.addEventListener('focus', () => hi(el.dataset.city));
      el.addEventListener('mouseleave', () => hi(''));
    });
    $$('.dot[data-href]', root).forEach(el => {
      const go = () => location.href = el.dataset.href;
      el.addEventListener('click', go);
      el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
  });

  /* ---------- live weather (Open-Meteo, no key) ---------- */
  const WX = {
    0: ['Clear sky', 'sun'], 1: ['Mostly clear', 'sun'], 2: ['Partly cloudy', 'cloudsun'], 3: ['Overcast', 'cloud'],
    45: ['Fog', 'fog'], 48: ['Freezing fog', 'fog'], 51: ['Light drizzle', 'rain'], 53: ['Drizzle', 'rain'], 55: ['Heavy drizzle', 'rain'],
    56: ['Freezing drizzle', 'snow'], 57: ['Freezing drizzle', 'snow'], 61: ['Light rain', 'rain'], 63: ['Rain', 'rain'], 65: ['Heavy rain', 'rain'],
    66: ['Freezing rain', 'snow'], 67: ['Freezing rain', 'snow'], 71: ['Light snow', 'snow'], 73: ['Snow', 'snow'], 75: ['Heavy snow', 'snow'], 77: ['Snow grains', 'snow'],
    80: ['Rain showers', 'rain'], 81: ['Rain showers', 'rain'], 82: ['Violent showers', 'storm'], 85: ['Snow showers', 'snow'], 86: ['Snow showers', 'snow'],
    95: ['Thunderstorms', 'storm'], 96: ['Storms with hail', 'storm'], 99: ['Severe storms, hail', 'storm'],
  };
  const ICONS = {
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    cloudsun: '<path d="M12 2v2M4.9 4.9l1.4 1.4M20 12h2M19.1 4.9l-1.4 1.4M15.9 13A4 4 0 0 0 8.1 11"/><path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z"/>',
    cloud: '<path d="M17.5 19H9a7 7 0 1 1 6.7-9h1.8a4.5 4.5 0 1 1 0 9Z"/>',
    fog: '<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2M16 17H7M17 21H9"/>',
    rain: '<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2M16 14v6M8 14v6M12 16v6"/>',
    storm: '<path d="M6 16.3A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 .5 9"/><path d="m13 12-3 5h4l-3 5"/>',
    snow: '<path d="M4 14.9A7 7 0 1 1 15.7 8h1.8a4.5 4.5 0 0 1 2.5 8.2M8 15h.01M8 19h.01M12 17h.01M12 21h.01M16 15h.01M16 19h.01"/>',
  };
  const svg = (k, cls = '') => `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONS[k] || ICONS.sun}</svg>`;
  $$('[data-weather]').forEach(root => {
    const sel = $('select', root), cities = JSON.parse(root.dataset.weather);
    const saved = store.get('tll-city');
    if (saved && cities[saved]) sel.value = saved;
    const o = k => $(`[data-w="${k}"]`, root);
    const fmtT = iso => { const [h, m] = iso.slice(11, 16).split(':').map(Number); return `${(h % 12) || 12}:${String(m).padStart(2, '0')} ${h < 12 ? 'am' : 'pm'}`; };
    const tipFor = (dd, cur) => {
      const lo = dd.temperature_2m_min[0], hi = dd.temperature_2m_max[0], rain = dd.precipitation_probability_max[0] ?? 0, wind = dd.wind_speed_10m_max[0], code = dd.weather_code[0];
      if (code >= 95) return [1, 'Storms in the forecast', 'Check that your transformer sits on a GFCI outlet and above standing water. After the storm, walk the yard for knocked-over path lights and exposed wire.'];
      if (lo <= 32) return [1, 'Freeze warning for your lights', 'Low-voltage LED fixtures handle a freeze fine, but cover exposed connections, keep the transformer dry and do not knock ice off lenses. Glass can crack.'];
      if (wind >= 25) return [1, 'Gusty night ahead', 'High winds bend path lights and loosen tree-mounted downlights. Give fixtures a quick check in the morning and re-aim anything that moved.'];
      if (rain >= 60) return [1, 'Wet night ahead', 'Heavy rain is when poor connections fail. If a zone flickers or goes dark after the rain, a corroded splice is the usual suspect.'];
      if (hi >= 100) return [0, 'Triple-digit heat today', 'Heat is hard on cheap fixtures and plastic stakes. Quality brass and aluminum fixtures with integrated LEDs shrug it off. Tonight is still a great night for the patio.'];
      if (rain >= 30) return [0, 'Chance of showers', 'Light rain makes hardscape glisten. Wet stone and pavers reflect landscape lighting beautifully, so it is a good night to look at your layout.'];
      return [0, 'A great night to see your lights', `Clear conditions and a ${Math.round(lo)}°F low. Step outside after sunset: this is the best time to spot dark zones, glare and fixtures that need re-aiming.`];
    };
    const load = async () => {
      const c = cities[sel.value]; store.set('tll-city', sel.value);
      o('city').textContent = c.n;
      root.classList.add('is-loading');
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${c.la}&longitude=${c.lo}&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m,is_day&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunset,sunrise,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=5`;
      try {
        const r = await fetch(url); if (!r.ok) throw 0; const j = await r.json();
        const cur = j.current, dd = j.daily, w = WX[cur.weather_code] || ['—', 'sun'];
        o('temp').textContent = Math.round(cur.temperature_2m) + '°';
        o('cond').textContent = w[0] + ' · ' + Math.round(cur.relative_humidity_2m) + '% humidity';
        o('ico').innerHTML = svg(!cur.is_day && w[1] === 'sun' ? 'moon' : w[1], 'wx__ico');
        o('sunset').textContent = fmtT(dd.sunset[0]);
        o('low').textContent = Math.round(dd.temperature_2m_min[0]) + '°F';
        o('rain').textContent = (dd.precipitation_probability_max[0] ?? 0) + '%';
        o('wind').textContent = Math.round(cur.wind_speed_10m) + ' mph';
        const ss = dd.sunset[0], [sh, sm] = ss.slice(11, 16).split(':').map(Number), on = new Date(2000, 0, 1, sh, sm + 15);
        o('on').textContent = fmtT(`0000-00-00T${String(on.getHours()).padStart(2, '0')}:${String(on.getMinutes()).padStart(2, '0')}`);
        const [warn, tt, tp] = tipFor(dd, cur);
        const tip = o('tip'); tip.classList.toggle('is-warn', !!warn);
        $('b', tip).textContent = tt; $('p', tip).textContent = tp;
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        o('days').innerHTML = dd.time.map((t, i) => {
          const wk = WX[dd.weather_code[i]] || ['', 'sun'], dt = new Date(t + 'T12:00');
          return `<div class="wx__day"><b>${i ? days[dt.getDay()] : 'Today'}</b>${svg(wk[1])}<div><small>${wk[0]} · sunset ${fmtT(dd.sunset[i])}</small><div class="bar" style="width:${Math.max(25, Math.min(100, (dd.temperature_2m_max[i] - 20) / 90 * 100))}%"></div></div><span>${Math.round(dd.temperature_2m_max[i])}° / <small>${Math.round(dd.temperature_2m_min[i])}°</small></span></div>`;
        }).join('');
        o('upd').textContent = 'Updated ' + new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
      } catch (e) {
        o('cond').textContent = 'Live forecast is unavailable right now. Please try again shortly.';
        o('upd').textContent = '';
      }
      root.classList.remove('is-loading');
    };
    sel.addEventListener('change', load);
    const go = () => { load(); };
    if ('IntersectionObserver' in window) { const wio = new IntersectionObserver(es => { if (es[0].isIntersecting) { wio.disconnect(); go(); } }, { rootMargin: '300px' }); wio.observe(root); } else go();
  });

  /* ---------- TOC highlight + copy link ---------- */
  const toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in window) {
    const map = new Map(toc.map(a => [a.getAttribute('href').slice(1), a]));
    const tio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { toc.forEach(a => a.classList.remove('is-on')); map.get(e.target.id)?.classList.add('is-on'); } }), { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((a, id) => { const h = d.getElementById(id); h && tio.observe(h); });
  }
  $$('[data-copy]').forEach(b => b.addEventListener('click', () => {
    navigator.clipboard?.writeText(location.href).then(() => { b.textContent = 'Link copied'; b.classList.add('is-on'); });
  }));

  /* ---------- lead forms ---------- */
  const t0 = Date.now();
  $$('[data-qform]').forEach(f => {
    const ts = $('[name=t]', f); if (ts) ts.value = String(t0);
    f.addEventListener('submit', async e => {
      const st = $('.qform__status', f);
      const miss = $$('[required]', f).find(i => !i.value.trim());
      if (miss) { e.preventDefault(); st.className = 'qform__status err'; st.textContent = 'Please add your name, phone and email so we can reach you.'; miss.focus(); return; }
      const em = $('[name=email]', f);
      if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value.trim())) { e.preventDefault(); st.className = 'qform__status err'; st.textContent = 'Please check your email address.'; em.focus(); return; }
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      const btn = $('button[type=submit]', f), lbl = $('span', btn), was = lbl.textContent;
      btn.disabled = true; lbl.textContent = 'Sending…';
      try {
        const r = await fetch(f.action, { method: 'POST', body: new FormData(f), headers: { Accept: 'application/json' } });
        const j = await r.json().catch(() => ({ ok: false }));
        if (!j.ok) throw new Error(j.error || 'Something went wrong sending your request.');
        f.classList.add('is-sent'); st.className = 'qform__status ok';
        st.innerHTML = `<strong>Thank you!</strong> Your request is in and we will be in touch shortly to talk through your project. Need us sooner? Call <a href="${TEL}">${PHONE}</a>.`;
        store.set('tll-lead', '1');
        window.gtag && gtag('event', 'generate_lead');
      } catch (err) {
        st.className = 'qform__status err'; st.innerHTML = `${err.message} Please call <a href="${TEL}">${PHONE}</a> or email <a href="mailto:info@txlandscapelights.com">info@txlandscapelights.com</a>.`;
        btn.disabled = false; lbl.textContent = was;
      }
    });
  });

  /* ---------- popup: opens 4 seconds after load ---------- */
  const pop = $('#pop');
  if (pop) {
    const skip = /^\/(quote|contact|thank-you)\//.test(location.pathname);
    const until = +store.get('tll-pop-until') || 0;
    let lastFocus = null;
    const close = () => {
      pop.classList.remove('is-open'); pop.setAttribute('aria-hidden', 'true'); body.classList.remove('pop-lock');
      store.set('tll-pop', '1', true);
      if (!$('form', pop).classList.contains('is-sent')) store.set('tll-pop-until', String(Date.now() + 2 * 864e5));
      lastFocus && lastFocus.focus();
    };
    const open = () => {
      if (body.classList.contains('nav-open')) return;
      lastFocus = d.activeElement;
      pop.classList.add('is-open'); pop.setAttribute('aria-hidden', 'false'); body.classList.add('pop-lock');
      setTimeout(() => $('input:not([type=hidden]):not([tabindex="-1"])', pop).focus({ preventScroll: true }), 350);
    };
    $$('[data-pop-close]', pop).forEach(b => b.addEventListener('click', close));
    d.addEventListener('keydown', e => {
      if (!pop.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') {
        const f = $$('a[href],button:not([disabled]),input:not([type=hidden]):not([tabindex="-1"]),select,textarea', pop).filter(x => x.offsetParent);
        if (!f.length) return;
        if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
    $$('[data-pop-open]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); open(); }));
    if (!skip && !store.get('tll-pop', true) && !store.get('tll-lead') && Date.now() > until) setTimeout(open, 4000);
  }
})();
