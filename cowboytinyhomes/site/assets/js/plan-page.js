// Plan pages: preview tabs (with the 3D viewer loaded on first open) and the cost estimate.

// ---- Tabs ------------------------------------------------------------------------------
document.querySelectorAll('[data-tabs]').forEach(root => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const select = (tab, focus) => {
    tabs.forEach(t => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
    if (tab.hasAttribute('data-3d-tab')) {
      const el = document.getElementById(tab.getAttribute('aria-controls')).querySelector('.viewer');
      import('./plan-3d.js').then(m => m.mount(el)).catch(() => {});
    }
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', e => {
      const k = { ArrowRight: 1, ArrowLeft: -1, Home: -i, End: tabs.length - 1 - i }[e.key];
      if (k === undefined) return;
      e.preventDefault();
      select(tabs[(i + k + tabs.length) % tabs.length], true);
    });
  });
  if (location.hash === '#3d') select(tabs.find(t => t.hasAttribute('data-3d-tab')));
});

// ---- Cost estimate ----------------------------------------------------------------------
// Mirrors generator/thb_qty.py estimate(): contractor = (materials + labor) * 1.18 + permits,
// plus 10% contingency; owner-builder = materials + 55% of electrical/plumbing/HVAC labor +
// permits + 12% contingency on materials.
const tool = document.querySelector('.cost-tool');
if (tool) {
  const data = JSON.parse(tool.dataset.cost);
  const FINISH = new Set(['Windows & doors', 'Exterior finish', 'Flooring & trim', 'Cabinets & counters', 'Appliances', 'Drywall & paint', 'Plumbing']);
  const TRADES = new Set(['Electrical', 'Plumbing', 'HVAC & ventilation']);
  const region = tool.querySelector('#c-region');
  const finish = tool.querySelector('#c-finish');
  const fmt = n => '$' + Math.round(n).toLocaleString('en-US');
  let build = 'gc';
  function update() {
    const r = +region.value, f = +finish.value;
    let mat = 0, lab = 0, help = 0;
    const rows = data.cats.map(c => {
      const m = c.materials * r * (FINISH.has(c.name) ? f : 1);
      const l = c.labor * r;
      mat += m; lab += l;
      if (TRADES.has(c.name)) help += l * 0.55;
      return { name: c.name, m, l: build === 'gc' ? l : (TRADES.has(c.name) ? l * 0.55 : 0) };
    });
    const permits = data.permits * r;
    const total = build === 'gc' ? ((mat + lab) * 1.18 + permits) * 1.10 : mat + help + permits + mat * 0.12;
    tool.querySelector('[data-out="total"]').textContent = fmt(total);
    tool.querySelector('[data-out="psf"]').textContent = fmt(total / data.sqft) + ' per sq ft';
    const max = Math.max(...rows.map(x => x.m + x.l));
    rows.forEach(x => {
      const row = tool.querySelector(`[data-cat="${CSS.escape(x.name)}"]`);
      if (!row) return;
      row.querySelector('.bar-m').style.width = (x.m / max * 100) + '%';
      row.querySelector('.bar-l').style.width = (x.l / max * 100) + '%';
      row.querySelector('.bar-val').textContent = fmt(x.m + x.l);
    });
  }
  region.addEventListener('change', update);
  finish.addEventListener('change', update);
  tool.querySelectorAll('[data-build]').forEach(b => b.addEventListener('click', () => {
    build = b.dataset.build;
    tool.querySelectorAll('[data-build]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    update();
  }));
  update();
}
