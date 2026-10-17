/* Dogwood DIY - interactive calculators. Each widget is a [data-tool] block
   rendered by build.py; this file wires up whichever ones are on the page. */
(() => {
  const num = (root, name) => {
    const el = root.querySelector(`[name="${name}"]`);
    const v = el ? parseFloat(el.value) : NaN;
    return Number.isFinite(v) ? v : 0;
  };
  const set = (root, key, text) => {
    const el = root.querySelector(`[data-out="${key}"]`);
    if (!el || el.textContent === text) return;
    el.textContent = text;
    el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');
  };
  const fmt = (n, d = 1) => (Math.round(n * 10 ** d) / 10 ** d).toLocaleString('en-US');
  const money = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const syncRanges = (root) => root.querySelectorAll('input[type=range]').forEach((r) => {
    const o = root.querySelector(`output[for="${r.id}"]`); if (o) o.textContent = r.value + (r.dataset.unit || '');
  });

  /* ---------- German schmear ---------- */
  const brickCache = new WeakMap();
  const drawSchmear = (canvas, coverage, seed) => {
    const ctx = canvas.getContext('2d');
    const W = canvas.width = 960, H = canvas.height = 540;
    let s = seed; const rnd = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
    // bricks
    ctx.fillStyle = '#b9ae9d'; ctx.fillRect(0, 0, W, H);
    const bw = 120, bh = 40, gap = 8;
    for (let row = 0, y = 0; y < H; row++, y += bh + gap) {
      for (let x = (row % 2 ? -bw / 2 : 0); x < W; x += bw + gap) {
        const tone = 0.75 + rnd() * 0.35;
        ctx.fillStyle = `rgb(${Math.round(150 * tone)},${Math.round(62 * tone)},${Math.round(44 * tone)})`;
        ctx.fillRect(x, y, bw, bh);
        ctx.fillStyle = 'rgba(0,0,0,.08)'; ctx.fillRect(x, y + bh - 6, bw, 6);
      }
    }
    // mortar joints always pick up some mud
    ctx.fillStyle = `rgba(214,206,192,${0.75 + coverage / 500})`;
    for (let row = 0, y = 0; y < H; row++, y += bh + gap) ctx.fillRect(0, y + bh, W, gap);
    for (let row = 0, y = 0; y < H; row++, y += bh + gap) {
      for (let x = (row % 2 ? -bw / 2 : 0); x < W; x += bw + gap) ctx.fillRect(x - gap, y, gap, bh);
    }
    // smears: each brick is covered with probability ~coverage, partly or fully
    const p = coverage / 100;
    for (let row = 0, y = 0; y < H; row++, y += bh + gap) {
      for (let x = (row % 2 ? -bw / 2 : 0); x < W; x += bw + gap) {
        if (rnd() > p * 1.05) continue;
        const strokes = 3 + Math.floor(rnd() * 4);
        for (let k = 0; k < strokes; k++) {
          const cx = x + bw * (0.15 + rnd() * 0.7), cy = y + bh * (0.15 + rnd() * 0.7);
          const rx = bw * (0.25 + rnd() * 0.4) * (0.7 + p * 0.5), ry = bh * (0.18 + rnd() * 0.3);
          ctx.fillStyle = `rgba(244,239,229,${0.35 + rnd() * 0.35 + p * 0.2})`;
          ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, (rnd() - 0.5) * 0.25, 0, Math.PI * 2); ctx.fill();
        }
      }
    }
    // a few long trowel swipes for texture
    for (let i = 0; i < 6 + p * 10; i++) {
      ctx.fillStyle = `rgba(240,235,224,${0.25 + rnd() * 0.25})`;
      ctx.beginPath();
      ctx.ellipse(rnd() * W, rnd() * H, 60 + rnd() * 120, 8 + rnd() * 14, (rnd() - 0.5) * 0.5, 0, Math.PI * 2);
      ctx.fill();
    }
  };
  const schmear = (root) => {
    const w = num(root, 'width'), h = num(root, 'height'), cov = num(root, 'coverage'), coats = num(root, 'coats') || 1;
    const area = w * h;
    // ~18 sq ft per gallon of pre-mixed mortar at full coverage, one coat
    const gallons = area * (cov / 100) * coats / 18;
    const price = num(root, 'price') || 25;
    set(root, 'area', fmt(area, 0) + ' sq ft');
    set(root, 'gallons', fmt(Math.max(gallons, area ? 0.5 : 0), 1) + ' gal');
    set(root, 'buckets', String(Math.ceil(gallons)));
    set(root, 'cost', money(Math.ceil(gallons) * price + (area ? 22 : 0)));
    set(root, 'time', area ? fmt(Math.max(2, area * coats * 0.09), 0) + ' hrs' : '0 hrs');
    const canvas = root.querySelector('canvas');
    if (canvas) drawSchmear(canvas, cov, 7);
  };

  /* ---------- Paint ---------- */
  const paint = (root) => {
    const L = num(root, 'length'), Wd = num(root, 'width'), H = num(root, 'height');
    const doors = num(root, 'doors'), windows = num(root, 'windows'), coats = num(root, 'coats') || 2;
    const ceiling = root.querySelector('[name="ceiling"]')?.checked;
    let walls = 2 * (L + Wd) * H - doors * 21 - windows * 15;
    walls = Math.max(0, walls);
    const ceil = ceiling ? L * Wd : 0;
    const gal = (walls + ceil) * coats / 350;
    set(root, 'wall', fmt(walls, 0) + ' sq ft');
    set(root, 'gallons', fmt(gal, 1) + ' gal');
    const buy = gal <= 0 ? '0' : gal < 0.75 ? '1 quart+' : Math.ceil(gal) >= 5 ? `${Math.floor(Math.ceil(gal) / 5)}×5 gal + ${Math.ceil(gal) % 5} gal` : `${Math.ceil(gal)} gal`;
    set(root, 'buy', buy);
    set(root, 'primer', fmt((walls + ceil) / 300, 1) + ' gal');
  };

  /* ---------- Mulch / soil ---------- */
  const mulch = (root) => {
    const L = num(root, 'length'), Wd = num(root, 'width'), D = num(root, 'depth');
    const cuft = L * Wd * (D / 12);
    set(root, 'area', fmt(L * Wd, 0) + ' sq ft');
    set(root, 'yards', fmt(cuft / 27, 2) + ' yd³');
    set(root, 'bags2', String(Math.ceil(cuft / 2)));
    set(root, 'bags3', String(Math.ceil(cuft / 3)));
  };

  /* ---------- Caulk + grout ---------- */
  const caulk = (root) => {
    const ft = num(root, 'linear'), bead = num(root, 'bead');
    // 10.1 oz cartridge holds ~18.2 cubic inches
    const perTube = 18.2 / (Math.PI * (bead / 2) ** 2) / 12;
    set(root, 'pertube', fmt(perTube, 0) + ' ft');
    set(root, 'tubes', String(ft ? Math.ceil((ft * 1.15) / perTube) : 0));
    const area = num(root, 'tilearea'), tile = num(root, 'tilesize') || 4;
    // grout lines per sq ft for square tiles = 2 * 12 / tile size (in feet of line)
    const lineFt = area * (2 * 12 / tile);
    const per = num(root, 'perbottle') || 150;
    set(root, 'gline', fmt(lineFt, 0) + ' ft');
    set(root, 'bottles', String(lineFt ? Math.ceil(lineFt / per) : 0));
  };

  /* ---------- Wallpaper remover mix ---------- */
  const wallpaper = (root) => {
    const L = num(root, 'length'), Wd = num(root, 'width'), H = num(root, 'height');
    const layers = num(root, 'layers') || 1;
    const area = 2 * (L + Wd) * H;
    const gal = area / 80 * layers;
    const recipe = root.querySelector('[name="recipe"]')?.value || 'softener';
    set(root, 'area', fmt(area, 0) + ' sq ft');
    set(root, 'gallons', fmt(gal, 1) + ' gal');
    const cupsWater = gal * 16;
    if (recipe === 'softener') {
      set(root, 'mix1', fmt(cupsWater * 0.75, 0) + ' cups hot water');
      set(root, 'mix2', fmt(cupsWater * 0.25, 0) + ' cups fabric softener');
    } else {
      set(root, 'mix1', fmt(cupsWater * 0.5, 0) + ' cups hot water');
      set(root, 'mix2', fmt(cupsWater * 0.5, 0) + ' cups white vinegar');
    }
    set(root, 'time', fmt(Math.max(1, area / 60 * layers), 0) + ' hrs');
  };

  /* ---------- Project budget planner ---------- */
  const KEY = 'dogwood-budget-v1';
  const budget = (root) => {
    const tbody = root.querySelector('tbody');
    const total = () => {
      let t = 0;
      tbody.querySelectorAll('tr').forEach((tr) => {
        const q = parseFloat(tr.querySelector('[data-k=qty]').value) || 0;
        const p = parseFloat(tr.querySelector('[data-k=price]').value) || 0;
        t += q * p;
      });
      const contingency = t * ((num(root, 'buffer') || 0) / 100);
      set(root, 'subtotal', money(t));
      set(root, 'buffer', money(contingency));
      set(root, 'total', money(t + contingency));
      const rows = [...tbody.querySelectorAll('tr')].map((tr) => ({
        item: tr.querySelector('[data-k=item]').value,
        qty: tr.querySelector('[data-k=qty]').value,
        price: tr.querySelector('[data-k=price]').value,
      }));
      try { localStorage.setItem(KEY, JSON.stringify({ rows, buffer: num(root, 'buffer') })); } catch (e) { /* storage unavailable */ }
    };
    const addRow = (r = { item: '', qty: 1, price: '' }) => {
      const tr = document.createElement('tr');
      tr.innerHTML = '<td><input data-k="item" aria-label="Item" placeholder="e.g. Pre-mixed mortar"></td>' +
        '<td><input data-k="qty" aria-label="Quantity" type="number" min="0" step="1"></td>' +
        '<td><input data-k="price" aria-label="Unit price" type="number" min="0" step="0.01" placeholder="$"></td>' +
        '<td><button type="button" class="rm" aria-label="Remove item">×</button></td>';
      tr.querySelector('[data-k=item]').value = r.item;
      tr.querySelector('[data-k=qty]').value = r.qty;
      tr.querySelector('[data-k=price]').value = r.price;
      tbody.appendChild(tr);
    };
    if (!root.dataset.ready) {
      root.dataset.ready = '1';
      let saved = null;
      try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { saved = null; }
      const starter = [
        { item: 'Pre-mixed white mortar (1 gal)', qty: 2, price: 24 },
        { item: 'Grout sponge + putty knife', qty: 1, price: 14 },
        { item: 'Plastic drop cloth', qty: 1, price: 8 },
      ];
      (saved && saved.rows && saved.rows.length ? saved.rows : starter).forEach(addRow);
      if (saved && Number.isFinite(saved.buffer)) root.querySelector('[name=buffer]').value = saved.buffer;
      root.addEventListener('click', (e) => {
        if (e.target.closest('.rm')) { e.target.closest('tr').remove(); total(); }
        if (e.target.closest('[data-add]')) { addRow(); total(); tbody.lastElementChild.querySelector('input').focus(); }
        if (e.target.closest('[data-clear]')) { tbody.innerHTML = ''; addRow(); total(); }
        if (e.target.closest('[data-print]')) window.print();
      });
    }
    total();
  };

  const tools = { schmear, paint, mulch, caulk, wallpaper, budget };
  document.querySelectorAll('[data-tool]').forEach((root) => {
    const fn = tools[root.dataset.tool]; if (!fn) return;
    const run = () => { syncRanges(root); fn(root); };
    root.addEventListener('input', run);
    root.addEventListener('change', run);
    run();
  });
})();
