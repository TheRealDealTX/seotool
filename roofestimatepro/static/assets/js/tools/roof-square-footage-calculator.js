/* Roof Square Footage Calculator */
(function () {
  "use strict";
  var N = REP.num, PF = REP.pitchFactor;
  var WASTE = { gable: 10, hip: 15, complex: 18 };
  var SHAPE = { rect: "Rectangle", tri: "Triangle", trap: "Trapezoid" };
  var TEAL = "#1fa59e", PEACH = "#FCBE8E", INK = "#cfdddb", MUTED = "#8ba29f";

  function sf(n) { return N(Math.round(n), 0) + " sq ft"; }
  function txt(x, y, s, o) {
    o = o || {};
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" fill="' + (o.fill || INK) + '" font-size="' + (o.size || 12) +
      '" font-family="Inter,system-ui,sans-serif" text-anchor="' + (o.anchor || "middle") + '"' + (o.weight ? ' font-weight="' + o.weight + '"' : "") + ">" + REP.esc(s) + "</text>";
  }

  // Footprint mode: plan view with overhang + cross-section drawn to pitch.
  function figFootprint(L, W, pL, pW, rise) {
    var w = 600, h = 250, box = 250, sc = box / Math.max(pL, pW), ox = 10, oy = 34;
    var ow = pL * sc, oh = pW * sc, fx = ox + (pL - L) / 2 * sc, fy = oy + (pW - W) / 2 * sc;
    var s = '<svg viewBox="0 0 ' + w + " " + h + '" xmlns="http://www.w3.org/2000/svg" role="img">';
    s += txt(ox, 20, "PLAN VIEW", { anchor: "start", size: 17, fill: MUTED, weight: 700 });
    s += '<rect x="' + ox + '" y="' + oy + '" width="' + ow.toFixed(1) + '" height="' + oh.toFixed(1) + '" fill="rgba(31,165,158,.18)" stroke="' + TEAL + '" stroke-width="2" rx="2"/>';
    s += '<rect x="' + fx.toFixed(1) + '" y="' + fy.toFixed(1) + '" width="' + (L * sc).toFixed(1) + '" height="' + (W * sc).toFixed(1) + '" fill="none" stroke="' + PEACH + '" stroke-dasharray="5 4" stroke-width="1.5"/>';
    s += txt(ox + ow / 2, oy + oh + 20, N(pL, 1) + " × " + N(pW, 1) + " ft incl. overhang", { size: 17 });
    s += txt(ox + ow / 2, oy + oh / 2 + 4, "walls " + N(L, 1) + " × " + N(W, 1) + " ft", { size: 17, fill: PEACH });
    // cross-section
    var cx = 320, cw = 260, run = cw / 2, ang = Math.atan(rise / 12), ht = Math.min(150, run * Math.tan(ang)), base = 205;
    var runDraw = rise > 0 && run * Math.tan(ang) > 150 ? 150 / Math.tan(ang) : run;
    s += txt(cx, 20, "SECTION AT " + rise + "/12", { anchor: "start", size: 17, fill: MUTED, weight: 700 });
    var mid = cx + cw / 2;
    s += '<polygon points="' + (mid - runDraw).toFixed(1) + "," + base + " " + mid + "," + (base - ht).toFixed(1) + " " + (mid + runDraw).toFixed(1) + "," + base +
      '" fill="rgba(31,165,158,.18)" stroke="' + TEAL + '" stroke-width="2.5" stroke-linejoin="round"/>';
    s += '<line x1="' + (mid - runDraw) + '" y1="' + (base + 6) + '" x2="' + (mid + runDraw) + '" y2="' + (base + 6) + '" stroke="' + MUTED + '" stroke-width="1"/>';
    s += txt(mid, base + 28, "pitch factor " + PF(rise).toFixed(3), { size: 18, fill: PEACH, weight: 600 });
    return s + "</svg>";
  }

  // Plane mode: each plane drawn at true (sloped) size, same scale.
  function figPlanes(list) {
    var w = 600, h = 230, gap = 14, pad = 10;
    var totalW = list.reduce(function (a, p) { return a + Math.max(p.wa, p.wb); }, 0) + gap * (list.length - 1);
    var maxH = Math.max.apply(null, list.map(function (p) { return p.hs; }));
    var sc = Math.min((w - 2 * pad - gap * (list.length - 1)) / Math.max(1e-6, totalW - gap * (list.length - 1)), 150 / Math.max(1e-6, maxH));
    var s = '<svg viewBox="0 0 ' + w + " " + h + '" xmlns="http://www.w3.org/2000/svg" role="img">';
    s += txt(pad, 20, "PLANES AT TRUE SLOPED SIZE (ONE OF EACH)", { anchor: "start", size: 17, fill: MUTED, weight: 700 });
    var x = pad, base = 196, cols = [TEAL, PEACH, "#9fd9d5", "#f29d5c", "#6b8f8b", "#c58b5c"];
    list.forEach(function (p, i) {
      var bw = Math.max(p.wa, p.wb) * sc, hh = p.hs * sc, c = cols[i % cols.length], pts;
      if (p.shape === "rect") pts = [[x, base], [x + bw, base], [x + bw, base - hh], [x, base - hh]];
      else if (p.shape === "tri") pts = [[x, base], [x + bw, base], [x + bw / 2, base - hh]];
      else { var top = p.wb * sc, bot = p.wa * sc, off = (bw - top) / 2, offb = (bw - bot) / 2; pts = [[x + offb, base], [x + offb + bot, base], [x + off + top, base - hh], [x + off, base - hh]]; }
      s += '<polygon points="' + pts.map(function (q) { return q[0].toFixed(1) + "," + q[1].toFixed(1); }).join(" ") +
        '" fill="' + c + '" fill-opacity=".22" stroke="' + c + '" stroke-width="2" stroke-linejoin="round"/>';
      if (bw > 60) s += txt(x + bw / 2, base + 22, (p.qty > 1 ? p.qty + "× " : "") + N(Math.round(p.one), 0) + " sf", { size: 17 });
      x += bw + gap;
    });
    return s + "</svg>";
  }

  REP.tool({
    id: "roof-square-footage-calculator",
    name: "Roof Square Footage Calculator",
    rowDefaults: {
      planes: [
        { name: "Front & back (trapezoids)", shape: "trap", a: 50, b: 20, h: 15, pitch: 6, qty: 2 },
        { name: "Hip ends (triangles)", shape: "tri", a: 30, b: 0, h: 15, pitch: 6, qty: 2 }
      ]
    },
    compute: function (v) {
      var warnings = [], notes = [], rows = [], figure = "", roofSf = 0, planSf = 0, pitchText, kpiExtra;
      var wastePct = v.style === "custom" ? Math.max(0, v.waste_custom) : WASTE[v.style];
      if (v.style === "custom" && (v.waste_custom < 0 || v.waste_custom > 40)) warnings.push("Waste factors outside 0–40% are unusual. Check the custom waste value.");

      if (v.mode === "footprint") {
        var rise = v.pitch, pf = PF(rise), e = Math.max(0, v.eave) / 12, r = Math.max(0, v.rake) / 12, L, W;
        if (v.fp_input === "area") {
          if (!(v.fp_area > 0)) return { warnings: ["Enter the footprint area in square feet."] };
          L = W = Math.sqrt(v.fp_area);
        } else {
          if (!(v.length > 0 && v.width > 0)) return { warnings: ["Enter the footprint length and width in feet."] };
          L = v.length; W = v.width;
        }
        var pL = L + 2 * r, pW = W + 2 * e;
        var foot = L * W;
        planSf = pL * pW; roofSf = planSf * pf;
        rows.push(["Footprint (walls)", v.fp_input === "area" ? "entered" : N(L, 1) + " × " + N(W, 1) + " ft", sf(foot)]);
        rows.push(["Overhang (" + v.eave + " in eave, " + v.rake + " in rake)", N(pL, 1) + " × " + N(pW, 1) + " ft", "+" + sf(planSf - foot)]);
        rows.push(["Plan area under the roof", "", sf(planSf)]);
        rows.push(["× pitch factor " + rise + "/12", pf.toFixed(3), "+" + sf(roofSf - planSf)]);
        pitchText = rise + "/12";
        kpiExtra = { label: "Pitch factor (" + rise + "/12)", text: pf.toFixed(3) };
        figure = figFootprint(L, W, pL, pW, rise);
        if (v.eave > 36 || v.rake > 36) notes.push("Overhangs over 36 in. are unusual. Check that you entered inches, not feet.");
        if (rise < 2) notes.push("Below 2/12 the roof needs a low-slope membrane, not shingles. Use the flat & commercial roof calculator for materials.");
        if (rise >= 13) notes.push("Very steep roofs (13/12 and up) are often mansards or decorative planes; check whether all of the roof really has this pitch.");
      } else {
        var planes = (v.rows.planes || []), list = [], bad = 0, steepSf = 0, pitches = {};
        planes.forEach(function (p, i) {
          var qty = Math.max(1, Math.round(p.qty || 1)), a = p.a, b = p.b, hh = p.h, base;
          var name = (p.name || "Plane " + (i + 1)).trim() || "Plane " + (i + 1);
          if (!(a > 0 && hh > 0) || (p.shape === "trap" && !(b > 0))) { bad++; return; }
          base = p.shape === "rect" ? a * hh : p.shape === "tri" ? a * hh / 2 : (a + b) / 2 * hh;
          var f = PF(p.pitch), one = v.dims === "plan" ? base * f : base, plan1 = v.dims === "plan" ? base : base / f;
          var tot = one * qty;
          roofSf += tot; planSf += plan1 * qty;
          if (p.pitch >= 7) steepSf += tot;
          pitches[p.pitch] = (pitches[p.pitch] || 0) + tot;
          var hs = v.dims === "plan" ? hh * f : hh;
          list.push({ shape: p.shape, wa: a, wb: p.shape === "trap" ? b : p.shape === "rect" ? a : 0, hs: hs, qty: qty, one: one });
          rows.push([name, SHAPE[p.shape] + (qty > 1 ? " ×" + qty : ""), p.pitch + "/12", sf(tot)]);
        });
        if (bad) warnings.push(bad + " plane" + (bad > 1 ? "s are" : " is") + " missing a length or height (trapezoids also need the ridge length) and " + (bad > 1 ? "were" : "was") + " left out.");
        if (roofSf <= 0) return { warnings: warnings.concat(["Enter at least one plane with a base length and an eave-to-ridge height."]) };
        if (list.length) figure = figPlanes(list);
        var keys = Object.keys(pitches).sort(function (x, y) { return pitches[y] - pitches[x]; });
        pitchText = keys.length === 1 ? keys[0] + "/12" : "mixed (mostly " + keys[0] + "/12)";
        kpiExtra = { label: "Steep area (7/12 and up)", text: steepSf > 0 ? sf(steepSf) : "None" };
        if (v.dims === "sloped") notes.push("Sloped measurements: no pitch factor applied. If these numbers came from a plan or satellite image, switch to plan view.");
        else notes.push("Plan measurements: each plane was multiplied by its own pitch factor.");
        if (keys.some(function (k) { return +k < 2; })) notes.push("Planes under 2/12 need a low-slope membrane, not shingles. Price them with the flat & commercial roof calculator.");
      }

      var sq = roofSf / 100;
      var bps = Math.max(1, Math.round(v.bundles_per_sq || 3));
      var sqWaste = sq * (1 + wastePct / 100);
      var bundles = Math.ceil(sqWaste * bps - 1e-9);
      var sqOrder = bundles / bps;
      var head = v.mode === "footprint" ? ["Step", "Detail", "Area"] : ["Plane", "Shape", "Pitch", "Area"];
      var foot = v.mode === "footprint" ? ["Roof area", "", sf(roofSf)] : ["Total roof area", "", "", sf(roofSf)];
      if (v.mode === "planes" && rows.length > 6) notes.push(rows.length + " planes entered.");

      notes.push("Order quantity covers the field shingles only. Starter strip, hip and ridge cap are extra; the shingle calculator counts them.");

      return {
        headline: { label: "Total roof area (sq ft)", value: Math.round(roofSf), format: "int",
          sub: N(sq, 2) + " squares · " + N(sqOrder, 2) + " squares to order" },
        figure: figure,
        kpis: [
          { label: "Roof squares (measured)", text: N(sq, 2) },
          { label: "Waste factor", text: N(wastePct, wastePct % 1 ? 1 : 0) + "%" },
          { label: "Squares to order", text: N(sqOrder, 2) },
          { label: "Bundles (" + bps + " per square)", text: N(bundles, 0) },
          { label: "Plan (horizontal) area", text: sf(planSf) },
          kpiExtra
        ],
        warnings: warnings,
        table: { title: v.mode === "footprint" ? "How the area was built" : "Per-plane areas", head: head, rows: rows, foot: foot },
        notes: notes,
        summary: [
          "Method: " + (v.mode === "footprint" ? "house footprint" : "plane by plane (" + (v.dims === "plan" ? "plan-view dimensions" : "sloped dimensions") + ")"),
          "Pitch: " + pitchText,
          "Plan area: " + Math.round(planSf) + " sq ft; roof area: " + Math.round(roofSf) + " sq ft (" + sq.toFixed(2) + " squares)",
          "Waste: " + wastePct + "% (" + v.style + "); order " + sqOrder.toFixed(2) + " squares = " + bundles + " bundles"
        ].concat(v.mode === "planes" ? rows.map(function (r) { return "  " + r[0] + ": " + r[1] + ", " + r[2] + ", " + r[3]; }) : [])
      };
    }
  });
})();
