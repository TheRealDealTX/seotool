/* Homepage: luxury look score */
(function () {
  'use strict';
  var form = document.querySelector('[data-luxury-score]');
  if (!form) return;
  var tips = {
    rug: ['Size up your rug', 'An undersized rug is the most common giveaway. Use our <a href="/tools/rug-size-calculator/">rug size calculator</a> so the front legs of every seat rest on it.'],
    curtains: ['Hang curtains high and wide', 'Mount the rod 4–6 in. below the ceiling and 8–12 in. past the frame. The <a href="/tools/curtain-size-calculator/">curtain size calculator</a> gives exact numbers.'],
    light: ['Layer your lighting', 'Add a floor lamp and a table lamp so you can switch the ceiling light off at night. Plan it with the <a href="/tools/room-lighting-calculator/">room lighting calculator</a>.'],
    warm: ['Switch to warm bulbs', 'Swap cool-white bulbs for 2700K warm white. It is the cheapest upgrade in this list and changes the whole mood.'],
    art: ['Rehang your art', 'Center art 57–60 in. from the floor and 8–10 in. above furniture. Our <a href="/tools/art-hanging-calculator/">art hanging calculator</a> gives you the nail height.'],
    palette: ['Edit your palette', 'Pick 3–4 colors and use the 60-30-10 rule. Try the <a href="/tools/room-color-palette-generator/">room color palette generator</a>.'],
    texture: ['Add natural texture', 'Bring in linen, wool, wood or stone. See our <a href="/quiet-luxury-interior-design/">quiet luxury interior design</a> guide.'],
    clutter: ['Clear the surfaces', 'Closed storage and clear surfaces read as calm and expensive. Start with the <a href="/declutter-checklist/">declutter checklist</a>.'],
    hardware: ['Upgrade the hardware', 'Heavier knobs, pulls and switch plates are a renter-friendly upgrade you can take with you. More ideas in <a href="/renter-friendly-upgrades/">renter-friendly upgrades</a>.'],
    plants: ['Bring in something living', 'One large plant or a vase of branches adds height and life. See <a href="/how-to-arrange-garden-pots/">how to arrange potted plants</a>.']
  };
  var order = ['rug', 'light', 'curtains', 'warm', 'clutter', 'art', 'palette', 'texture', 'hardware', 'plants'];
  var num = form.querySelector('[data-score-num]'), dial = form.querySelector('.score__dial');
  var label = form.querySelector('[data-score-label]'), tip = form.querySelector('[data-score-tip]');
  function update() {
    var on = Array.prototype.map.call(form.querySelectorAll('input:checked'), function (i) { return i.value; });
    var score = on.length * 10;
    num.textContent = score;
    dial.style.setProperty('--p', score);
    dial.style.background = 'radial-gradient(closest-side, var(--cream) 78%, transparent 79%), conic-gradient(var(--gold) ' + score + '%, var(--stone) 0)';
    var next = order.filter(function (k) { return on.indexOf(k) === -1; })[0];
    label.textContent = score === 100 ? 'Designer level. Beautifully done.' : score >= 70 ? 'Very polished, almost there' : score >= 40 ? 'Good bones, a few easy wins left' : on.length ? 'Plenty of upside, start here' : 'Tick the boxes to see your score';
    tip.innerHTML = next && on.length ? '<strong>Your next move: ' + tips[next][0] + '.</strong> ' + tips[next][1] : (score === 100 ? 'Explore our <a href="/luxury-apartment-interior-design/">luxury apartment interior design guide</a> for finishing touches.' : '');
  }
  form.addEventListener('change', update);
  update();
})();
