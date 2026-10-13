/* Claim documentation checklist: progress saved in localStorage */
(function () {
  'use strict';
  var root = document.querySelector('[data-cl]');
  if (!root) return;
  var KEY = 'txpa-checklist-v1';

  var BASICS = ['Basics for every claim', [
    'Claim number, date reported, and the insurer adjuster\'s name and email',
    'Full policy: declarations page plus every endorsement (ask the insurer or agent for a certified copy)',
    'Date of loss written down, with how you know it (storm alert, leak discovered, fire report)',
    'Claim diary started: every call, who you spoke with, what was said',
    'All emergency repair, tarp and mitigation invoices saved',
    'Additional living expense receipts (hotel, meals above normal, mileage) if you cannot stay home',
    'Copies of everything the insurer sends: letters, estimates, engineer reports, photos',
  ]];
  var LISTS = {
    roof: [BASICS,
      ['Storm-date evidence', [
        'Storm date confirmed with NOAA reports (use the storm report lookup tool)',
        'Photos of hail on the ground, with a coin or ruler for scale, if you have them',
        'Neighbors with claims or roof replacements from the same storm noted',
        'Older photos of the roof (listing photos, drone, Google Street View) showing its condition before the storm',
      ]],
      ['Roof and exterior', [
        'Wide shot of each roof slope and elevation (front, back, both sides)',
        'Close-ups of hail hits on shingles, with chalk circles and a scale reference',
        'Soft metals: gutters, downspouts, vents, flashing, AC fins, mailbox (they hold dents and support the storm date)',
        'Ridge cap, starter course and drip edge condition',
        'Siding, window screens, wraps, fences, painted surfaces, outdoor furniture',
        'Any interior water stains from roof leaks, photographed and dated',
        'Roof age and material documented (permit, invoice or inspection report)',
      ]],
    ],
    water: [BASICS,
      ['Source and cause', [
        'Photo or video of the source (burst pipe, supply line, appliance, roof opening) before it is repaired',
        'Failed part kept: pipe section, supply line, valve or water heater fitting',
        'Plumber\'s invoice stating the cause and that the failure was sudden',
        'Date the water was first noticed, and how',
      ]],
      ['Damage and mitigation', [
        'Room-by-room video showing the waterline on walls, cabinets and flooring',
        'Moisture readings or the mitigation company\'s drying logs and moisture maps',
        'Photos of materials before removal: flooring, padding, baseboards, cabinets, drywall',
        'Samples of flooring and carpet kept for matching',
        'Mitigation contract, drying equipment list and daily logs',
        'Mold observed: photographed and reported to the insurer in writing',
        'Damaged contents listed (use the contents inventory builder)',
      ]],
    ],
    fire: [BASICS,
      ['Official records', [
        'Fire department incident report requested',
        'Photos taken before the board-up and before debris removal',
        'Utility shut-off and restoration dates noted',
      ]],
      ['Structure', [
        'Room-by-room photos and video, including unburned rooms with smoke residue',
        'Smoke and soot in attic, HVAC returns, ductwork and inside cabinets photographed',
        'Odor documented (in writing, room by room) even where there is no visible soot',
        'Code-upgrade items noted (electrical, smoke detectors, insulation) for ordinance or law coverage',
      ]],
      ['Contents', [
        'Room-by-room contents inventory with age and replacement cost',
        'Photos of items before disposal; serial numbers on electronics and appliances',
        'Cleaning vs. replacement decisions put in writing with the contents company',
        'Older photos and videos of rooms (phones, social media) to show what was there',
      ]],
    ],
    storm: [BASICS,
      ['Which policy covers what', [
        'Homeowners policy, windstorm policy (TWIA, if coastal) and flood policy all located',
        'Separate claims filed with each carrier that may owe (wind and flood are usually separate)',
        'TWIA one-year filing deadline noted on your calendar, if applicable',
        'Named-storm or percentage deductible amounts confirmed',
      ]],
      ['Wind vs. water evidence', [
        'High-water marks photographed with a tape measure, inside and outside',
        'Roof, window and wall openings photographed. Rain through a wind-created opening is a different claim from rising water',
        'Fallen trees on structures photographed before removal',
        'Timeline of when wind damage and flooding occurred, if known',
      ]],
      ['After the storm', [
        'Tarping and board-up invoices with photos of the work',
        'Spoiled food and outage-related losses listed (check your policy for limits)',
        'Mold growth photographed and reported promptly',
        'Contents inventory started for anything damaged',
      ]],
    ],
  };

  var loss = 'roof';
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {} }
  function id(s) { return loss + ':' + s.slice(0, 60); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function render() {
    var html = '';
    LISTS[loss].forEach(function (sec) {
      var done = sec[1].filter(function (t) { return saved[id(t)]; }).length;
      html += '<div class="cl-section"><h3>' + esc(sec[0]) + ' <span>' + done + ' / ' + sec[1].length + '</span></h3>';
      sec[1].forEach(function (t) {
        var on = !!saved[id(t)];
        html += '<label class="tcheck' + (on ? ' is-done' : '') + '"><input type="checkbox" data-id="' + esc(id(t)) + '"' + (on ? ' checked' : '') + '><span>' + esc(t) + '</span></label>';
      });
      html += '</div>';
    });
    root.querySelector('[data-out="sections"]').innerHTML = html;
    progress();
  }
  function progress() {
    var all = root.querySelectorAll('[data-id]'), on = root.querySelectorAll('[data-id]:checked');
    var pct = all.length ? Math.round(on.length / all.length * 100) : 0;
    root.querySelector('[data-ring]').style.setProperty('--v', pct);
    root.querySelector('[data-out="pct"]').textContent = pct + '%';
  }

  root.addEventListener('change', function (e) {
    var cb = e.target.closest('[data-id]'); if (!cb) return;
    if (cb.checked) saved[cb.getAttribute('data-id')] = 1; else delete saved[cb.getAttribute('data-id')];
    save(); render();
  });
  root.querySelector('[data-seg="loss"]').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    this.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-on', x === b); });
    loss = b.getAttribute('data-v'); render();
  });
  root.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]'); if (!a) return;
    if (a.getAttribute('data-act') === 'print') window.print();
    if (a.getAttribute('data-act') === 'reset' && window.confirm('Clear all checks for this list?')) {
      Object.keys(saved).forEach(function (k) { if (k.indexOf(loss + ':') === 0) delete saved[k]; });
      save(); render();
    }
  });
  render();
})();
