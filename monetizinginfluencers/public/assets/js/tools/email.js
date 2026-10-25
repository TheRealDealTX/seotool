/* Influencer Email Generator */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('em-form')) return;
  var mode = 'brand', seed = 0, k = 0;

  function v(id, fallback) { var x = ($(id).value || '').trim(); return x || fallback; }
  function pick(arr) { k++; return arr[(seed * (k + 2) + k) % arr.length]; }
  function pickN(arr, n) { var out = [], i; for (i = 0; i < n; i++) out.push(arr[(seed + i) % arr.length]); return out; }
  function clean(s) { return s.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim(); }

  function brand() {
    var d = {
      brand: v('b-brand', 'our brand'), sender: v('b-sender', 'the team'), product: v('b-product', 'our product'),
      name: v('b-name', 'there'), handle: v('b-handle', ''), recent: v('b-recent', 'your latest post'),
      platform: v('b-platform', 'Instagram'), comp: $('b-comp').value, tone: $('em-tone').value
    };
    var offer = {
      paid: ['This would be a paid collaboration, and we would love to hear your rates for ' + aan(d.platform) + ' post.',
             'We have budget set aside for this and would pay your standard rate for ' + d.platform + ' content.',
             'It is a paid partnership: send over your rate card and we will build the brief around what works for you.'],
      gifted: ['To be upfront, this would start as a gifted collaboration: we would send you ' + d.product + ' to try, with no obligation to post.',
               'We would love to send you ' + d.product + ' as a gift. No strings attached, and if you love it we would talk about a paid partnership next.',
               'This is a gifted opportunity to begin with: free product, zero pressure, and a conversation about paid work if it is a fit.'],
      affiliate: ['We would set you up with a personal discount code and a commission on every sale it drives, plus free product to try.',
                  'This would be an affiliate partnership: you earn a commission on every sale through your link, and your audience gets an exclusive discount.',
                  'We offer our creator partners a generous commission on every sale and a code for their followers.']
    }[d.comp];
    var openers = {
      friendly: ['Hi ' + d.name + ',\n\nI just watched ' + d.recent + ' and had to reach out. The way you explain things feels genuinely helpful, not salesy, and that is rare.',
                 'Hey ' + d.name + '!\n\nLong-time lurker here. ' + cap(d.recent) + ' is the reason I am writing: it is exactly the kind of content our customers love.',
                 'Hi ' + d.name + ',\n\nI am ' + d.sender + ' from ' + d.brand + '. Your ' + d.recent.replace(/^your /, '') + ' stopped my scroll, and I have been sending it to my whole team.'],
      professional: ['Hi ' + d.name + ',\n\nMy name is ' + d.sender + ' and I lead creator partnerships at ' + d.brand + '. I came across ' + d.recent + ' and was impressed by how engaged your community is.',
                     'Dear ' + d.name + ',\n\nI am reaching out from ' + d.brand + '. We have been following your work, particularly ' + d.recent + ', and believe there is a strong fit with our audience.',
                     'Hello ' + d.name + ',\n\nI am ' + d.sender + ' at ' + d.brand + '. ' + cap(d.recent) + ' is a great example of why your audience trusts your recommendations.'],
      bold: ['Hi ' + d.name + ',\n\n' + cap(d.recent) + ' = instant fan. Quick one:',
             d.name + ',\n\nLoved ' + d.recent + '. Straight to the point:',
             'Hey ' + d.name + ',\n\n' + d.sender + ' from ' + d.brand + ' here. Big fan of ' + d.recent + '.']
    }[d.tone];
    var why = ['We are launching ' + d.product + ' and your audience is exactly who we built it for.',
               'We think ' + d.product + ' would fit naturally into the content you already make' + (d.handle ? ' on ' + d.handle : '') + '.',
               'Your followers keep asking the questions ' + d.product + ' was designed to answer.'];
    var ask = {
      friendly: ['Would you be open to chatting? Happy to send more details whenever suits you.', 'If that sounds fun, just reply and I will send over the details.', 'Any interest? I would love to hear what kind of collaborations you enjoy most.'],
      professional: ['Would you be open to a short call this week, or should I send a brief by email?', 'Could you share your rates and availability for the coming month?', 'If this is of interest, I would be glad to send a full brief and timeline.'],
      bold: ['Interested? Reply "yes" and I will send the brief.', 'Worth a quick chat?', 'In? Send me your rates and I will make it happen.']
    }[d.tone];
    var signoff = d.tone === 'professional' ? 'Kind regards,' : d.tone === 'bold' ? 'Cheers,' : 'Thanks so much,';
    var body = pick(openers) + '\n\n' + pick(why) + ' ' + pick(offer) + '\n\n' + pick(ask) + '\n\n' + signoff + '\n' + d.sender + '\n' + d.brand;
    var subjects = pickN([
      d.brand + ' x ' + d.name + ': ' + (d.comp === 'paid' ? 'paid collab idea' : d.comp === 'gifted' ? 'can we send you something?' : 'partnership + commission'),
      'Loved ' + d.recent.replace(/^your /, 'your ') + ' (collab idea inside)',
      (d.comp === 'paid' ? 'Paid ' : '') + d.platform + ' partnership with ' + d.brand,
      'Quick question about working together, ' + d.name,
      d.name + ', would you try ' + d.product + '?'
    ], 3);
    var dm = 'Hi ' + d.name + '! ' + d.sender + ' from ' + d.brand + ' here. Loved ' + d.recent + '. ' +
      ({ paid: 'We would love to pay you to feature ' + d.product + '.', gifted: 'Could we send you ' + d.product + ' to try? No strings attached.', affiliate: 'We would love to offer you a commission partnership on ' + d.product + '.' }[d.comp]) +
      ' What is the best email for details?';
    return { subjects: subjects, body: clean(body), dm: dm.replace(/…\./g, '…') };
  }

  function creator() {
    var d = {
      name: v('c-name', 'me'), handle: v('c-handle', ''), niche: v('c-niche', 'my niche'), platform: v('c-platform', 'Instagram'),
      followers: v('c-followers', ''), er: v('c-er', ''), brand: v('c-brand', 'your brand'), contact: v('c-contact', ''),
      idea: v('c-idea', 'a short content series featuring your product'), proof: v('c-proof', ''), tone: $('em-tone').value
    };
    var hi = d.contact ? (d.tone === 'professional' ? 'Hi ' + d.contact + ',' : 'Hey ' + d.contact + ',') : (d.tone === 'professional' ? 'Hello ' + d.brand + ' team,' : 'Hi ' + d.brand + ' team,');
    var stats = (d.followers ? d.followers + ' followers' : '') + (d.followers && d.er ? ' and a ' : '') + (d.er ? d.er + ' engagement rate' : '');
    var intro = {
      friendly: ['I am ' + d.name + (d.handle ? ' (' + d.handle + ')' : '') + ', a ' + d.niche + ' creator on ' + d.platform + ', and I have been a genuine ' + d.brand + ' fan for a while.',
                 'I am ' + d.name + ', I make ' + d.niche + ' content on ' + d.platform + (d.handle ? ' as ' + d.handle : '') + ', and ' + d.brand + ' keeps coming up in my comments.'],
      professional: ['My name is ' + d.name + (d.handle ? ' (' + d.handle + ')' : '') + '. I create ' + d.niche + ' content on ' + d.platform + (stats ? ' for an audience of ' + stats : '') + '.',
                     'I am ' + d.name + ', a ' + d.niche + ' creator on ' + d.platform + '. I am reaching out with a partnership idea for ' + d.brand + '.'],
      bold: [d.name + ' here (' + (d.handle || d.platform) + '), ' + d.niche + ' creator.', 'Quick pitch from a ' + d.niche + ' creator who already uses ' + d.brand + '.']
    }[d.tone];
    var pitch = ['I would love to create ' + d.idea + '.', 'Here is the idea: ' + d.idea + '.', 'I have an idea I think your team will like: ' + d.idea + '.'];
    var proof = (stats && d.tone !== 'professional' ? 'My ' + d.platform + ' has ' + stats + '. ' : '') + (d.proof ? cap(d.proof) + ', which lines up closely with ' + d.brand + '\'s customers.' : '');
    var close = {
      friendly: ['I have attached my media kit. Would you be up for a quick chat about it?', 'Happy to share rates and past results, or tweak the idea to fit your goals. What do you think?'],
      professional: ['My media kit and rates are attached. Would you be available for a 15-minute call next week?', 'I would be glad to send a detailed proposal with deliverables, timeline and pricing.'],
      bold: ['Media kit attached. Want the rates?', 'Want to make it happen? I can start next week.']
    }[d.tone];
    var signoff = d.tone === 'professional' ? 'Best regards,' : d.tone === 'bold' ? 'Talk soon,' : 'Thanks for reading!';
    var body = hi + '\n\n' + pick(intro) + '\n\n' + pick(pitch) + ' ' + proof + '\n\n' + pick(close) + '\n\n' + signoff + '\n' + d.name + (d.handle ? '\n' + d.handle : '');
    var subjects = pickN([
      'Content idea for ' + d.brand + ': ' + shorten(d.idea, 42),
      d.niche.charAt(0).toUpperCase() + d.niche.slice(1) + ' creator x ' + d.brand + ' partnership',
      (d.followers ? d.followers + ' engaged ' + d.niche + ' fans' : 'An engaged ' + d.niche + ' audience') + ' for ' + d.brand,
      'Collab pitch from ' + (d.handle || d.name),
      'Would ' + d.brand + ' be up for this?'
    ], 3);
    var dm = 'Hi! I am ' + d.name + (d.handle ? ' (' + d.handle + ')' : '') + ', a ' + d.niche + ' creator and big fan of ' + d.brand + '. I have an idea for ' + shorten(d.idea, 70) + '. Who is the best person to send a quick pitch to?';
    return { subjects: subjects, body: clean(body), dm: dm.replace(/…\./g, '…') };
  }

  function aan(w) { return (/^[aeiou]/i.test(w) ? 'an ' : 'a ') + w; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function shorten(s, n) { return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : s; }

  function render(animate) {
    k = 0;
    var out = mode === 'brand' ? brand() : creator();
    var ul = $('em-subjects');
    ul.innerHTML = '';
    out.subjects.forEach(function (s) {
      var li = document.createElement('li'), span = document.createElement('span'), b = document.createElement('button');
      span.textContent = s; b.type = 'button'; b.className = 'btn btn-ghost btn-sm'; b.textContent = 'Copy';
      b.setAttribute('aria-label', 'Copy subject line: ' + s);
      b.addEventListener('click', function () { if (window.MI) MI.copy(s, b); });
      li.appendChild(span); li.appendChild(b); ul.appendChild(li);
    });
    $('em-body').textContent = out.body;
    $('em-dm').textContent = out.dm;
    if (animate) ['em-subjects', 'em-body', 'em-dm'].forEach(function (id) { var el = $(id); el.classList.remove('typing'); void el.offsetWidth; el.classList.add('typing'); });
  }

  document.querySelectorAll('[data-mode]').forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.mode;
      document.querySelectorAll('[data-mode]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      $('em-brand').hidden = mode !== 'brand';
      $('em-creator').hidden = mode === 'brand';
      render(true);
    });
  });
  $('em-go').addEventListener('click', function () { render(true); if (window.MI) MI.confetti(70); });
  $('em-again').addEventListener('click', function () { seed++; render(true); });
  $('em-form').addEventListener('input', function () { render(false); });
  $('em-form').addEventListener('change', function () { render(false); });
  render(false);
})();
