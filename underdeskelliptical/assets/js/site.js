/* underdeskelliptical.com: mobile nav, archive filters and the interactive tools.
   Each tool is a <div class="tool" data-tool="..."> rendered by inc/tools.php. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fmt = function (n) { return Math.round(n).toLocaleString('en-US'); };
  var SIT = 1.3, WALK = 3.5;

  // ---- nav ----
  var toggle = $('.nav-toggle'), nav = $('#site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---- blog filter chips ----
  $$('[data-filter-grid]').forEach(function (bar) {
    var grid = $(bar.getAttribute('data-filter-grid'));
    bar.addEventListener('click', function (ev) {
      var b = ev.target.closest('.chip'); if (!b) return;
      $$('.chip', bar).forEach(function (c) { c.classList.toggle('on', c === b); });
      var f = b.getAttribute('data-f');
      $$('.card', grid).forEach(function (c) { c.hidden = f !== 'all' && c.getAttribute('data-cat') !== f; });
    });
  });

  function kcalPerMin(met, kg) { return met * 3.5 * kg / 200; }
  function val(form, name) {
    var el = form.elements[name];
    if (!el) return null;
    if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return null; }
    return el.value;
  }

  var tools = {
    calories: function (root) {
      var form = $('form', root);
      function run() {
        var w = parseFloat(val(form, 'weight')) || 170;
        var kg = val(form, 'unit') === 'kg' ? w : w / 2.2046;
        var min = +val(form, 'minutes'), met = +val(form, 'met'), days = +val(form, 'days');
        form.elements.minOut.value = min; form.elements.daysOut.value = days;
        var session = kcalPerMin(met, kg) * min;
        var extra = kcalPerMin(met - SIT, kg) * min;
        $('[data-out=session]', root).textContent = fmt(session);
        $('[data-out=extra]', root).textContent = fmt(extra);
        $('[data-out=week]', root).textContent = fmt(extra * days);
        $('[data-out=lbs]', root).textContent = (extra * days * 4.33 / 3500).toFixed(1);
        var vals = { sit: kcalPerMin(SIT, kg) * min, ude: session, walk: kcalPerMin(WALK, kg) * min };
        var max = vals.walk;
        Object.keys(vals).forEach(function (k) {
          $('[data-bar=' + k + ']', root).style.width = (vals[k] / max * 100) + '%';
          $('[data-barv=' + k + ']', root).textContent = fmt(vals[k]) + ' cal';
        });
      }
      form.addEventListener('input', run); form.addEventListener('change', run); run();
    },

    steps: function (root) {
      var form = $('form', root), ring = $('[data-ring]', root), C = 2 * Math.PI * 52;
      function run() {
        var min = +val(form, 'minutes'), met = +val(form, 'met'), goal = +val(form, 'goal');
        form.elements.minOut.value = min;
        // Effort-matched: brisk walking (3.5 MET) ~ 100 steps/min, scaled on energy above sitting.
        var steps = min * 100 * (met - SIT) / (WALK - SIT);
        var pct = Math.min(1, steps / goal);
        $('[data-out=steps]', root).textContent = fmt(steps);
        ring.style.strokeDasharray = C; ring.style.strokeDashoffset = C * (1 - pct);
        $('[data-out=summary]', root).innerHTML = '<strong>' + Math.round(steps / goal * 100) + '%</strong> of your ' + fmt(goal) +
          '-step goal. That is about the same energy as walking for <strong>' + fmt(steps / 100) + ' minutes</strong> at a brisk pace.';
      }
      form.addEventListener('input', run); form.addEventListener('change', run); run();
    },

    clearance: function (root) {
      var form = $('form', root);
      function run() {
        var desk = parseFloat(val(form, 'desk')), knee = parseFloat(val(form, 'knee')), pedal = parseFloat(val(form, 'pedal'));
        if (!desk || !knee) return;
        var need = knee + pedal, gap = desk - need;
        var v = $('[data-out=verdict]', root), adv = $('[data-out=advice]', root);
        var pos = Math.max(2, Math.min(98, 50 + gap * 8));
        $('[data-meter]', root).style.left = pos + '%';
        v.className = 'verdict ' + (gap >= 1.5 ? 'ok' : gap >= 0 ? 'tight' : 'no');
        if (gap >= 1.5) {
          v.textContent = 'Fits: about ' + gap.toFixed(1) + '" of spare clearance';
          adv.innerHTML = 'Your knees should clear the desk at the top of each stride. Any <a href="/what-is-the-best-under-desk-elliptical/">top-rated under desk elliptical</a> of this type will work.';
        } else if (gap >= 0) {
          v.textContent = 'Tight: only ' + gap.toFixed(1) + '" to spare';
          adv.innerHTML = 'It will work, but you may brush the desk. Sit slightly further back, lower your chair an inch, or choose a <a href="/compact-under-desk-elliptical/">low-profile compact model</a> such as the DeskCycle Ellipse.';
        } else {
          v.textContent = 'Won\'t fit: knees ' + Math.abs(gap).toFixed(1) + '" too high';
          adv.innerHTML = 'Try a lower-profile machine, lower your chair, or raise the desk. A <a href="/compact-under-desk-elliptical/">compact under desk elliptical</a> or a standing setup with a <a href="/under-desk-elliptical-vs-walking-pad/">walking pad</a> may suit you better.';
        }
      }
      form.addEventListener('input', run); form.addEventListener('change', run); run();
    },

    timer: function (root) {
      var form = $('form', root), btn = $('[data-act=start]', root), reset = $('[data-act=reset]', root);
      var key = 'ude-timer-' + new Date().toISOString().slice(0, 10);
      var total = 0; try { total = +localStorage.getItem(key) || 0; } catch (e) {}
      var phase = 'pedal', round = 1, left = 0, tick = null, ctx = null;
      function cfg() { return { work: Math.max(1, +val(form, 'work')) * 60, rest: Math.max(0, +val(form, 'rest')) * 60, rounds: Math.max(1, +val(form, 'rounds')) }; }
      function chime() {
        try {
          ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
          [0, .18].forEach(function (d, i) {
            var o = ctx.createOscillator(), g = ctx.createGain();
            o.frequency.value = i ? 880 : 660; o.connect(g); g.connect(ctx.destination);
            g.gain.setValueAtTime(.0001, ctx.currentTime + d); g.gain.exponentialRampToValueAtTime(.2, ctx.currentTime + d + .02);
            g.gain.exponentialRampToValueAtTime(.0001, ctx.currentTime + d + .5); o.start(ctx.currentTime + d); o.stop(ctx.currentTime + d + .55);
          });
        } catch (e) {}
      }
      function draw() {
        var c = cfg();
        $('[data-out=clock]', root).textContent = Math.floor(left / 60) + ':' + ('0' + (left % 60)).slice(-2);
        $('[data-out=round]', root).textContent = round; $('[data-out=rounds]', root).textContent = c.rounds;
        $('[data-out=total]', root).textContent = Math.floor(total / 60);
        var p = $('[data-out=phase]', root);
        p.textContent = tick ? (phase === 'pedal' ? 'Pedal' : 'Rest') : (left ? 'Paused' : 'Ready');
        p.classList.toggle('pedal', phase === 'pedal' && !!tick);
        document.title = tick ? (phase === 'pedal' ? '▶ Pedal ' : '⏸ Rest ') + $('[data-out=clock]', root).textContent : document.title.replace(/^[▶⏸] \S+ \S+ /, '');
      }
      function init() { phase = 'pedal'; round = 1; left = cfg().work; draw(); }
      function step() {
        left--;
        if (phase === 'pedal') { total++; try { localStorage.setItem(key, total); } catch (e) {} }
        if (left <= 0) {
          var c = cfg(); chime();
          if (phase === 'pedal' && c.rest && round < c.rounds) { phase = 'rest'; left = c.rest; }
          else if (round < c.rounds) { round++; phase = 'pedal'; left = c.work; }
          else { clearInterval(tick); tick = null; btn.textContent = 'Start'; $('[data-out=phase]', root).textContent = 'Done. Nice work!'; left = 0; return draw(); }
        }
        draw();
      }
      btn.addEventListener('click', function () {
        if (tick) { clearInterval(tick); tick = null; btn.textContent = 'Resume'; }
        else { if (!left) init(); tick = setInterval(step, 1000); btn.textContent = 'Pause'; chime(); }
        draw();
      });
      reset.addEventListener('click', function () { clearInterval(tick); tick = null; btn.textContent = 'Start'; init(); });
      form.addEventListener('input', function () { if (!tick) init(); });
      init();
    },

    quiz: function (root) {
      var form = $('form', root), out = $('.quiz-results', root);
      var data = JSON.parse($('.quiz-data', root).textContent);
      var budgetRank = { 'sunny-sf-e3872': 0, 'fryline': 0, 'putnen': 0, 'jisuo': 0, 'mysuntown': 0, 'lvpiman': 0, 'fntkech': 0, 'geoneo': 0, 'flex-fitness': 0, 'fousae': 0, 'viamotion': 0, 'yosuda': 0, 'damkee': 1, 'cubii-move': 1, 'cubii-go': 1, 'cubii-jr1': 1, 'stamina-inmotion-e1000': 1, 'sperax-walking-pad': 1, 'ancheer': 1, 'yosuda-electric': 1, 'cubii-jr2': 2, 'deskcycle-ellipse': 2, 'lifepro-flexstride': 2, 'deskcycle-2': 1, 'merach': 2, 'cubii-jr2-plus': 2, 'cubii-pro': 2, 'lifepro-autoglide': 2, 'legxercise': 2, 'walkingpad-c2': 2, 'urevo-2in1': 2, 'fitdesk-fdx2': 2, 'niceday': 2 };
      var known = { 'cubii-jr2': 3, 'deskcycle-ellipse': 3, 'sunny-sf-e3872': 2, 'ancheer': 2, 'lifepro-flexstride': 2, 'stamina-inmotion-e1000': 2, 'walkingpad-c2': 2, 'legxercise': 2, 'cubii-move': 1, 'cubii-jr2-plus': 1, 'lifepro-autoglide': 1, 'deskcycle-2': 1, 'yosuda-electric': 1, 'merach': 1 };
      $('[data-act=quiz]', root).addEventListener('click', function () {
        var a = { use: val(form, 'use'), goal: val(form, 'goal'), noise: val(form, 'noise'), budget: val(form, 'budget'), who: val(form, 'who') };
        var want = { low: 0, mid: 1, high: 2 }[a.budget];
        var scored = Object.keys(data).map(function (k) {
          var p = data[k], s = known[k] || 0, t = p.t;
          if (a.use === 'seated') { if (p.st && t !== 'strider') s -= 20; if (t === 'strider') s -= 4; if (t === 'hybrid') s -= 20; }
          if (a.use === 'standing') { if (!p.st) s -= 20; else s += 4; }
          if (a.use === 'both') { if (t === 'strider') s += 8; else if (p.st) s -= 2; }
          if (a.goal === 'burn') { if (t === 'manual' || t === 'strider' || t === 'walking-pad' || t === 'desk-bike') s += 3; if (t === 'motorized') s -= 3; }
          if (a.goal === 'circ') { if (t === 'motorized') s += 6; }
          if (a.goal === 'move') { if (t === 'manual') s += 2; }
          if (a.noise === 'high') { if (/Whisper|Very quiet/.test(p.q || '')) s += 3; else if (p.q === 'Quiet') s += 1; else s -= 3; }
          if (a.who === 'senior') { s += p.s ? 2 : -10; if (t === 'motorized') s += 2; if (t === 'walking-pad') s -= 6; }
          var b = budgetRank[k] === undefined ? 1 : budgetRank[k];
          s -= Math.abs(b - want) * 2.5;
          if (t === 'desk-bike' && a.goal !== 'burn') s -= 3;
          return { k: k, s: s, p: p };
        }).sort(function (x, y) { return y.s - x.s; }).slice(0, 3);
        var top = scored[0].s;
        out.innerHTML = '<h4>Your top matches</h4>' + scored.map(function (r, i) {
          var pct = Math.max(62, Math.min(98, Math.round(96 - (top - r.s) * 4)));
          return '<div class="qr">' + (r.p.i ? '<img src="' + r.p.i + '" alt="' + r.p.n + '" loading="lazy">' : '<div></div>') +
            '<div><span class="match">' + (i === 0 ? 'Best match · ' : '') + pct + '% match</span><h4>' + r.p.n + '</h4><p>' + r.p.b + '</p>' +
            '<a class="btn btn-amz btn-sm" href="' + r.p.u + '" target="_blank" rel="sponsored nofollow noopener">Check Price on Amazon</a> ' +
            (r.p.r ? '<a class="btn btn-ghost btn-sm" href="' + r.p.r + '">Read guide</a>' : '') + '</div></div>';
        }).join('');
        out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    },

    finder: function (root) {
      var rows = $$('tbody tr', root), count = $('[data-out=count]', root);
      function apply(f) {
        var n = 0;
        rows.forEach(function (r) {
          var d = r.dataset, show = f === 'all' || d.type === f ||
            (f === 'quiet' && d.quiet === '1') || (f === 'seniors' && d.seniors === '1') || (f === 'standing' && d.standing === '1');
          r.hidden = !show; if (show) n++;
        });
        count.textContent = 'Showing ' + n + ' of ' + rows.length + ' models.';
      }
      $('.chips', root).addEventListener('click', function (ev) {
        var b = ev.target.closest('.chip'); if (!b) return;
        $$('.chip', root).forEach(function (c) { c.classList.toggle('on', c === b); });
        apply(b.getAttribute('data-f'));
      });
      apply('all');
    }
  };

  $$('.tool[data-tool]').forEach(function (el) {
    var fn = tools[el.getAttribute('data-tool')];
    if (fn) { try { fn(el); } catch (e) { if (window.console) console.error(e); } }
  });
})();
