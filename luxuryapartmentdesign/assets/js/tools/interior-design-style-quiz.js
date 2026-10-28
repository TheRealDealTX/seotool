(function () {
  'use strict';
  var root = document.getElementById('quiz');
  if (!root) return;
  var stage = root.querySelector('.quiz__stage'), bar = root.querySelector('.quiz__progress span');

  // Style keys: QL quiet luxury, JP japandi, MM modern minimalist, WC warm contemporary,
  // AD art deco glam, OM organic modern, CP classic parisian, MC mid-century modern
  var STYLES = {
    QL: { name: 'Quiet Luxury', colors: ['#efe9df', '#cbbfae', '#8a7d6b', '#3b352e'], desc: 'Tonal, tailored and understated. You want rooms that feel expensive without announcing it: cashmere-soft neutrals, boucle and wool, travertine and walnut, and furniture with clean, generous lines.', tips: ['Build a tonal palette of oatmeal, mushroom, taupe and espresso.', 'Invest in one beautifully made sofa and keep accessories minimal.', 'Swap cool bulbs for warm 2700K light on dimmers.'], read: ['/quiet-luxury-interior-design/', 'Quiet luxury interior design guide'] },
    JP: { name: 'Japandi', colors: ['#f2ede4', '#d8c8ad', '#8c7a63', '#2f2c28'], desc: 'Calm, natural and purposeful. Japanese restraint meets Scandinavian warmth: low furniture, light oak and dark wood, paper and linen, handmade ceramics and lots of breathing room.', tips: ['Choose low-profile furniture in light oak or ash with one darker wood accent.', 'Use a flatweave or textured wool rug in a natural tone.', 'Display a few handmade objects rather than many.'], read: ['/japandi-rug-the-perfect-blend-of-minimalism-and-warmth/', 'Japandi rug guide'] },
    MM: { name: 'Modern Minimalist', colors: ['#ffffff', '#e5e5e3', '#9a9a96', '#1d1d1b'], desc: 'Crisp, edited and architectural. You love clean planes, a limited palette and storage that hides everything. Every object has to earn its place.', tips: ['Keep surfaces clear with closed, handleless storage.', 'Stick to two or three colors and one material accent.', 'Let one large artwork or sculptural light be the focal point.'], read: ['/types-of-minimalism/', 'The types of minimalism'] },
    WC: { name: 'Warm Contemporary', colors: ['#f4ede3', '#d9b99b', '#a5673f', '#3d3129'], desc: 'Relaxed, current and inviting. You like comfortable modern shapes in warm colors: caramel leather, rust and terracotta, cream upholstery and plenty of layered textiles.', tips: ['Layer throws and cushions in rust, camel and cream.', 'Mix a modern sofa with a vintage wood side table.', 'Use warm table lamps instead of overhead light at night.'], read: ['/apartment-living-room-ideas/', 'Apartment living room ideas'] },
    AD: { name: 'Art Deco Glam', colors: ['#f3ece0', '#c9a24a', '#1f4a45', '#141414'], desc: 'Bold, glamorous and geometric. Velvet, brass, lacquer and marble, with fluted details, curves and jewel tones. You want a little drama.', tips: ['Add one velvet piece in emerald, sapphire or deep teal.', 'Bring in brass through lighting, mirrors and hardware.', 'Use geometric patterns on a rug or cushions.'], read: ['/how-to-make-your-apartment-look-expensive/', 'How to make your apartment look expensive'] },
    OM: { name: 'Organic Modern', colors: ['#f5f1ea', '#d6cbb8', '#7f8a6e', '#4a3f35'], desc: 'Soft, natural and grounded. Rounded shapes, plaster textures, jute and linen, stone and lots of greenery. Modern, but never cold.', tips: ['Choose curved furniture and round mirrors.', 'Add large plants and branches in stoneware vessels.', 'Use limewash or warm white walls for texture.'], read: ['/luxury-apartment-interior-design/', 'Luxury apartment interior design'] },
    CP: { name: 'Classic Parisian', colors: ['#faf7f1', '#e4d9c8', '#b6a48a', '#2d2a26'], desc: 'Elegant, romantic and collected. Herringbone floors, molding, gilded mirrors and antique finds mixed with modern pieces. Effortless, never fussy.', tips: ['Lean an oversized gilt or brass mirror against a wall.', 'Mix one antique piece with clean modern furniture.', 'Add peel-and-stick or applied molding panels (with landlord approval).'], read: ['/trim-around-front-door/', 'Door trim and molding ideas'] },
    MC: { name: 'Mid-Century Modern', colors: ['#f4efe6', '#d8a24a', '#7a4b2a', '#2f3a3a'], desc: 'Optimistic, functional and graphic. Tapered legs, teak and walnut, sculptural lighting and pops of mustard, olive and teal.', tips: ['Look for a walnut or teak credenza as your anchor piece.', 'Add a sculptural floor lamp or globe pendant.', 'Use mustard or teal as a 10% accent color.'], read: ['/apartment-decorating-ideas/', 'Apartment decorating ideas'] }
  };

  var Q = [
    { q: 'Which color palette feels most like home?', o: [
      ['Soft neutrals: oatmeal, taupe, mushroom', { QL: 3, JP: 1, OM: 1 }, ['#efe9df', '#cbbfae', '#8a7d6b']],
      ['Crisp white, grey and black', { MM: 3, MC: 0 }, ['#ffffff', '#9a9a96', '#1d1d1b']],
      ['Warm caramel, rust and cream', { WC: 3, MC: 1 }, ['#f4ede3', '#d9b99b', '#a5673f']],
      ['Jewel tones with gold', { AD: 3, CP: 1 }, ['#1f4a45', '#c9a24a', '#141414']],
      ['Sage, sand and natural wood', { OM: 3, JP: 2 }, ['#f5f1ea', '#7f8a6e', '#4a3f35']],
      ['Mustard, teal and walnut', { MC: 3 }, ['#d8a24a', '#2f3a3a', '#7a4b2a']]] },
    { q: 'Pick the sofa you would sit on first.', o: [
      ['A deep, tailored sofa in boucle or wool', { QL: 3, OM: 1 }],
      ['A low, simple sofa in natural linen on a wood base', { JP: 3, OM: 1 }],
      ['A sleek, armless sofa with clean lines', { MM: 3 }],
      ['A curved velvet sofa', { AD: 3, OM: 1 }],
      ['A slouchy leather sofa in cognac', { WC: 3, MC: 1 }],
      ['A sofa with tapered wooden legs and button tufting', { MC: 3, CP: 1 }]] },
    { q: 'Which material do you want to run your hand over?', o: [
      ['Travertine and cashmere', { QL: 3, CP: 1 }],
      ['Light oak and handmade paper', { JP: 3 }],
      ['Polished concrete and matte lacquer', { MM: 3 }],
      ['Brass, marble and velvet', { AD: 3, CP: 1 }],
      ['Plaster, jute and stoneware', { OM: 3, JP: 1 }],
      ['Teak, leather and wool', { MC: 2, WC: 2 }]] },
    { q: 'How should a room feel when you walk in?', o: [
      ['Calm and quietly expensive', { QL: 3, JP: 1 }],
      ['Serene and uncluttered, like a retreat', { JP: 2, MM: 2 }],
      ['Cozy and welcoming', { WC: 3, OM: 1 }],
      ['Glamorous and a little dramatic', { AD: 3 }],
      ['Romantic and collected over time', { CP: 3 }],
      ['Cheerful, graphic and fun', { MC: 3 }]] },
    { q: 'Your ideal Saturday at home involves…', o: [
      ['A good book, a candle and a perfectly made bed', { QL: 2, CP: 1, JP: 1 }],
      ['Tea, a tidy space and a long bath', { JP: 3, MM: 1 }],
      ['Friends over for a long, relaxed dinner', { WC: 3, MC: 1 }],
      ['Cocktails and getting dressed up', { AD: 3 }],
      ['Repotting plants and opening the windows', { OM: 3 }],
      ['Browsing vintage shops and flea markets', { CP: 2, MC: 2 }]] },
    { q: 'What would you hang over the sofa?', o: [
      ['One large, quiet abstract in neutral tones', { QL: 3, MM: 1 }],
      ['Ink brushwork or a single ceramic piece on a ledge', { JP: 3 }],
      ['Nothing; the wall is part of the design', { MM: 3 }],
      ['A gilt mirror or a bold, glamorous print', { AD: 2, CP: 2 }],
      ['A textile hanging or botanical prints', { OM: 2, WC: 1 }],
      ['A graphic mid-century poster', { MC: 3 }]] },
    { q: 'Pick a light fixture.', o: [
      ['A plaster or alabaster sconce', { QL: 2, OM: 1, CP: 1 }],
      ['A paper lantern pendant', { JP: 3, OM: 1 }],
      ['Slim recessed or linear lights', { MM: 3 }],
      ['A fluted brass chandelier', { AD: 3, CP: 1 }],
      ['A woven rattan pendant', { OM: 2, WC: 2 }],
      ['A sputnik or arc floor lamp', { MC: 3 }]] },
    { q: 'If you had $1,000 to spend, you would buy…', o: [
      ['One investment piece, beautifully made', { QL: 3, MM: 1 }],
      ['A few handcrafted objects and a natural rug', { JP: 2, OM: 2 }],
      ['Hidden storage to keep everything out of sight', { MM: 3, JP: 1 }],
      ['A statement velvet chair and brass lamp', { AD: 3 }],
      ['An antique mirror and a vintage side table', { CP: 3, MC: 1 }],
      ['Layers of throws, cushions and warm lamps', { WC: 3 }]] }
  ];

  var answers = [], step = 0;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function show() {
    bar.style.width = (step / Q.length * 100) + '%';
    if (step >= Q.length) return result();
    var q = Q[step];
    stage.innerHTML = '<p class="quiz__step">Question ' + (step + 1) + ' of ' + Q.length + '</p><h2 class="quiz__q">' + esc(q.q) + '</h2>' +
      '<div class="quiz__opts">' + q.o.map(function (o, i) {
        var dots = o[2] ? '<span class="dots">' + o[2].map(function (c) { return '<i style="background:' + c + '"></i>'; }).join('') + '</span>' : '';
        return '<button type="button" class="quiz__opt" data-i="' + i + '">' + dots + '<span>' + esc(o[0]) + '</span></button>';
      }).join('') + '</div>' +
      '<div class="quiz__nav">' + (step ? '<button type="button" class="link-btn" data-back>&larr; Back</button>' : '<span></span>') + '<span class="quiz__step">Pick the one that feels most like you</span></div>';
    stage.querySelectorAll('.quiz__opt').forEach(function (b) {
      b.addEventListener('click', function () { answers[step] = +b.getAttribute('data-i'); step++; show(); });
    });
    var back = stage.querySelector('[data-back]');
    if (back) back.addEventListener('click', function () { step--; show(); });
    var first = stage.querySelector('.quiz__opt');
    if (first && answers.length) first.focus();
  }

  function result() {
    var score = {};
    Object.keys(STYLES).forEach(function (k) { score[k] = 0; });
    answers.forEach(function (a, i) { var w = Q[i].o[a][1]; for (var k in w) score[k] += w[k]; });
    var ranked = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
    var max = 24, top = STYLES[ranked[0]], second = STYLES[ranked[1]];
    var total = ranked.reduce(function (s, k) { return s + score[k]; }, 0) || 1;
    try { localStorage.setItem('lad-style', ranked[0]); } catch (e) {}
    stage.innerHTML = '<div class="quiz__result"><p class="result__label">Your interior design style</p><h2>' + top.name + '</h2>' +
      '<div class="palette-strip">' + top.colors.map(function (c) { return '<span style="background:' + c + '" title="' + c + '"></span>'; }).join('') + '</div>' +
      '<p>' + top.desc + '</p><p><strong>With a touch of ' + second.name + '.</strong> ' + second.desc.split('.')[0] + '.</p>' +
      '<h3>Get the look in your apartment</h3><ul>' + top.tips.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>' +
      '<div class="quiz__bars">' + ranked.slice(0, 5).map(function (k) {
        var pct = Math.round(score[k] / total * 100);
        return '<div class="quiz__bar"><span>' + STYLES[k].name + '</span><div><span style="width:' + Math.min(100, score[k] / max * 100 * 2.2) + '%"></span></div><span>' + pct + '%</span></div>';
      }).join('') + '</div>' +
      '<div class="tool-actions"><a class="btn btn--gold" href="' + top.read[0] + '">Read: ' + top.read[1] + '</a>' +
      '<a class="btn btn--ghost" href="/tools/room-color-palette-generator/">Build your palette</a>' +
      '<button type="button" class="btn btn--ghost" data-restart>Retake quiz</button></div></div>';
    stage.querySelector('[data-restart]').addEventListener('click', function () { answers = []; step = 0; show(); });
    if (window.gtag) window.gtag('event', 'style_quiz_complete', { style: top.name });
  }
  show();
})();
