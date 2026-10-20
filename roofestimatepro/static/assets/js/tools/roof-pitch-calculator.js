/* Roof Pitch Calculator */
(function () {
  "use strict";
  var N = REP.num, TEAL = "#1fa59e", PEACH = "#FCBE8E", INK = "#cfdddb", MUTED = "#8ba29f";
  var DEG = 180 / Math.PI, drawn = false;

  function ftin(ft) {
    if (!isFinite(ft) || ft <= 0) return "—";
    var eighths = Math.round(ft * 96), f = Math.floor(eighths / 96), rem = eighths - f * 96;
    var inch = Math.floor(rem / 8), e = rem % 8, frac = "";
    if (e) { var d = 8; while (e % 2 === 0) { e /= 2; d /= 2; } frac = "-" + e + "/" + d; }
    return f + "′ " + inch + frac + "″";
  }
  function t(x, y, s, o) {
    o = o || {};
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" fill="' + (o.fill || INK) + '" font-size="' + (o.size || 21) +
      '" font-family="Inter,system-ui,sans-serif" text-anchor="' + (o.anchor || "middle") + '" font-weight="' + (o.weight || 600) + '">' + REP.esc(s) + "</text>";
  }

  function figure(x, ang) {
    var W = 600, H = 270, maxW = 430, maxH = 190, base = 225, x0 = 70;
    var w = maxW, h = maxW * x / 12;
    if (h > maxH) { h = maxH; w = maxH * 12 / x; }
    var x1 = x0 + w, ytop = base - h, anim = !drawn;
    var len = Math.sqrt(w * w + h * h);
    var s = '<svg viewBox="0 0 ' + W + " " + H + '" xmlns="http://www.w3.org/2000/svg" role="img">';
    if (anim) s += "<style>.rp-hyp{stroke-dasharray:" + len.toFixed(0) + ";stroke-dashoffset:" + len.toFixed(0) + ";animation:rpd .8s ease-out forwards}.rp-fill{opacity:0;animation:rpf .6s .3s ease-out forwards}" +
      "@keyframes rpd{to{stroke-dashoffset:0}}@keyframes rpf{to{opacity:1}}@media(prefers-reduced-motion:reduce){.rp-hyp,.rp-fill{animation:none;stroke-dashoffset:0;opacity:1}}</style>";
    s += '<polygon class="rp-fill" points="' + x0 + "," + base + " " + x1.toFixed(1) + "," + base + " " + x1.toFixed(1) + "," + ytop.toFixed(1) + '" fill="rgba(31,165,158,.16)"/>';
    s += '<line x1="' + x0 + '" y1="' + base + '" x2="' + x1.toFixed(1) + '" y2="' + base + '" stroke="' + MUTED + '" stroke-width="2"/>';
    s += '<line x1="' + x1.toFixed(1) + '" y1="' + base + '" x2="' + x1.toFixed(1) + '" y2="' + ytop.toFixed(1) + '" stroke="' + PEACH + '" stroke-width="2.5"/>';
    s += '<line class="rp-hyp" x1="' + x0 + '" y1="' + base + '" x2="' + x1.toFixed(1) + '" y2="' + ytop.toFixed(1) + '" stroke="' + TEAL + '" stroke-width="5" stroke-linecap="round"/>';
    // right-angle mark
    if (h > 16) s += '<path d="M' + (x1 - 12).toFixed(1) + " " + base + " v-12 h12" + '" fill="none" stroke="' + MUTED + '" stroke-width="1.5"/>';
    // angle arc
    var r = Math.min(70, w * 0.45);
    if (x > 0) s += '<path d="M' + (x0 + r) + " " + base + " A" + r + " " + r + " 0 0 0 " + (x0 + r * Math.cos(ang)).toFixed(1) + " " + (base - r * Math.sin(ang)).toFixed(1) + '" fill="none" stroke="' + PEACH + '" stroke-width="2"/>';
    var la = ang / 2;
    if (x > 0) s += t(x0 + (r + 34) * Math.cos(la), base - (r + 34) * Math.sin(la) + 6, N(ang * DEG, 1) + "°", { fill: PEACH, size: 22 });
    s += t(x0 + w / 2, base + 30, "run 12", { fill: MUTED });
    if (x > 0) s += t(x1 + 12, base - h / 2 + 6, "rise " + N(x, 2), { anchor: "start", fill: PEACH });
    var mx = x0 + w / 2, my = base - h / 2;
    if (x > 0) s += t(mx - 10, my - 12, "rafter " + N(Math.sqrt(144 + x * x), 2), { fill: TEAL, anchor: "end" });
    drawn = true;
    return s + "</svg>";
  }

  function klass(x) {
    if (x < 2) return ["Low slope", "Membrane roofing (TPO, PVC, EPDM, mod-bit, built-up or coatings). Shingles and tile are not allowed below 2/12."];
    if (x < 4) return ["Low slope for shingles", "Shingles are allowed with two layers of underlayment; tile needs 2.5/12 or more. Walkable."];
    if (x < 6.5) return ["Conventional, walkable", "All steep-slope products with standard underlayment. No steep labor charge."];
    if (x < 9.5) return ["Steep", "Roof jacks and fall protection needed; insurance estimates add a 7/12–9/12 steep charge."];
    if (x <= 12.5) return ["Very steep", "Slow, harnessed work; estimates add the 10/12–12/12 steep charge."];
    return ["Extreme / mansard", "Over 12/12: highest steep charge, and shingles need the manufacturer's steep-slope nailing."];
  }

  function mats(x) {
    function ok(c) { return c ? "OK" : "Not suitable"; }
    return [
      ["Asphalt shingles", x < 2 ? "Not suitable" : x < 4 ? "OK, double underlayment" : "OK"],
      ["Clay / concrete tile", x < 2.5 ? "Not suitable" : x < 4 ? "OK, double underlayment" : "OK"],
      ["Wood shakes / shingles", ok(x >= 3)],
      ["Standing seam metal", x < 0.25 ? "Below 1/4:12" : x < 3 ? "Check panel rating" : "OK"],
      ["Exposed-fastener metal", x < 0.5 ? "Not suitable" : x < 3 ? "Only with lap sealant" : "OK"],
      ["Membranes (TPO, EPDM, mod-bit)", x < 0.25 ? "Needs tapered insulation" : x <= 3 ? "OK" : "Unusual at this pitch"]
    ];
  }

  REP.tool({
    id: "roof-pitch-calculator",
    name: "Roof Pitch Calculator",
    compute: function (v) {
      var x, src, warnings = [], notes = [];
      if (v.method === "rise") {
        if (!(v.run > 0)) return { warnings: ["Enter a run greater than zero."] };
        if (v.rise < 0) return { warnings: ["Rise cannot be negative."] };
        x = v.rise / v.run * 12;
        src = "rise " + v.rise + " over run " + v.run + " " + (v.units === "ft" ? "ft" : "in");
      } else if (v.method === "angle") {
        if (!(v.angle >= 0 && v.angle < 90)) return { warnings: ["Enter an angle from 0° up to (but not including) 90°."] };
        x = 12 * Math.tan(v.angle / DEG);
        src = "angle " + v.angle + "°";
      } else if (v.method === "level") {
        if (!(v.level_len > 0)) return { warnings: ["Enter the length of the level in inches."] };
        if (v.level_rise < 0) return { warnings: ["The gap under the level cannot be negative."] };
        x = v.level_rise / v.level_len * 12;
        src = v.level_rise + " in gap under a " + v.level_len + " in level";
      } else {
        if (!(v.raf_run > 0 && v.raf_len > 0)) return { warnings: ["Enter both the rafter length and its horizontal run."] };
        if (v.raf_len <= v.raf_run) return { warnings: ["The rafter must be longer than its horizontal run (equal means a flat roof)."] };
        x = Math.sqrt(v.raf_len * v.raf_len - v.raf_run * v.raf_run) / v.raf_run * 12;
        src = v.raf_len + " ft rafter over a " + v.raf_run + " ft run";
      }
      if (!isFinite(x)) return { warnings: ["Check the inputs."] };
      if (x > 36) warnings.push("That is steeper than 36/12 (about 72°), which is closer to a wall than a roof. Check the inputs.");

      var ang = Math.atan(x / 12), pf = REP.pitchFactor(x), hv = REP.hipFactor(x);
      var whole = Math.round(x), half = Math.round(x * 2) / 2;
      var cls = klass(x);
      var exact = Math.abs(x - whole) < 0.005;
      var kpis = [
        { label: "Exact pitch", text: N(x, 2) + "/12" },
        { label: "Angle", text: N(ang * DEG, 2) + "°" },
        { label: "Percent grade", text: N(x / 12 * 100, 1) + "%" },
        { label: "Pitch multiplier", text: pf.toFixed(3) },
        { label: "Hip / valley factor", text: hv.toFixed(3) },
        { label: "Steepness", text: cls[0] }
      ];
      var rows = [
        ["Pitch (nearest whole)", whole + "/12"],
        ["Pitch (nearest ½)", (half % 1 ? Math.floor(half) + "½" : half) + "/12"],
        ["Rise per foot of run", N(x, 2) + " in"],
        ["Ratio", "1 : " + (x > 0 ? N(12 / x, 2) : "∞")]
      ];
      var run = Math.max(0, v.calc_run), oh = Math.max(0, v.calc_oh) / 12, rafterLine = "";
      if (run > 0) {
        var common = (run + oh) * pf, hip = run * hv;
        rows.push(["Common rafter, " + N(run, 2) + " ft run" + (oh ? " + " + v.calc_oh + " in overhang" : ""), ftin(common) + " (" + N(common, 2) + " ft)"]);
        rows.push(["Total rise over " + N(run, 2) + " ft", ftin(run * x / 12)]);
        if (x > 0) rows.push(["Hip / valley rafter (no overhang)", ftin(hip) + " (" + N(hip, 2) + " ft)"]);
        kpis.push({ label: "Common rafter length", text: ftin(common) });
        rafterLine = "Common rafter for " + run + " ft run" + (oh ? " + " + v.calc_oh + " in overhang" : "") + ": " + ftin(common) + " (" + common.toFixed(2) + " ft); hip/valley " + hip.toFixed(2) + " ft";
        notes.push("Rafter length is the line length along the top edge; deduct half the ridge board thickness before cutting.");
      }
      mats(x).forEach(function (m) { rows.push([m[0], m[1]]); });
      notes.unshift(cls[1]);
      if (x >= 2 && x < 4) notes.push("Two layers of underlayment (or a self-adhered underlayment) are required for shingles from 2/12 up to 4/12.");
      if (Math.abs(x - half) > 0.1) notes.push("Not a whole or half pitch. Real roofs are framed to whole or half pitches; re-measure if you expected a standard pitch.");

      return {
        headline: { label: "Roof pitch", text: (exact ? whole : N(x, 2)) + "/12",
          sub: N(ang * DEG, 1) + "° · " + N(x / 12 * 100, 0) + "% grade · multiplier " + pf.toFixed(3) },
        figure: figure(x, ang),
        kpis: kpis,
        warnings: warnings,
        table: { title: "Conversions & materials at this pitch", head: ["Item", "Value"], rows: rows },
        notes: notes,
        summary: [
          "Measured from: " + src,
          "Pitch: " + N(x, 2) + "/12 (nearest whole " + whole + "/12), angle " + N(ang * DEG, 2) + "°, grade " + N(x / 12 * 100, 1) + "%",
          "Pitch multiplier " + pf.toFixed(3) + "; hip/valley factor " + hv.toFixed(3),
          "Steepness: " + cls[0]
        ].concat(rafterLine ? [rafterLine] : [])
      };
    }
  });
})();
