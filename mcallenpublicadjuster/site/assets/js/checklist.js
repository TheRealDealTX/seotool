/* Property Insurance Claim Documentation Checklist — data stays in the browser. */
(function () {
  'use strict';
  var root = document.querySelector('[data-checklist]');
  if (!root) return;

  var common = {
    start: { title: 'Immediately after the loss', items: [
      ['safety', 'Make sure everyone is safe', 'Stay off damaged roofs and away from downed lines, standing water near electricity, and fire-damaged structures until they are cleared.'],
      ['dol', 'Record the date and time of loss', 'Write down when the damage happened or was discovered, and what you observed (hail size, wind, smoke, water source).'],
      ['photos', 'Photograph and video the damage safely', 'Wide shots of each side of the property, then close-ups. Include a reference object for scale and keep the original files with their dates.'],
      ['mitigate', 'Take reasonable steps to prevent further damage', 'Tarp openings, shut off water, board windows. Most policies require reasonable mitigation. Keep the damaged materials or photos of them if they must be removed.'],
      ['notice', 'Report the claim to your insurer promptly', 'Note the date, the person you spoke with, and the claim number. Late notice is a common reason for disputes.']
    ]},
    policy: { title: 'Policy and insurer communication', items: [
      ['policy', 'Locate your full insurance policy', 'Get the declarations page AND the policy forms and endorsements. You can request a certified copy from your insurer or agent.'],
      ['claimno', 'Record the claim number and adjuster contacts', 'Adjuster name, company (staff or independent), phone, email, and any third-party firm involved.'],
      ['log', 'Keep a communication log', 'Date, time, who, what was said, and what was promised. Follow phone calls with a short email confirming key points.'],
      ['letters', 'Organize all insurer correspondence', 'Acknowledgment letters, requests for information, estimates, denial or partial-denial letters, and payment letters in one folder.'],
      ['deadlines', 'Review deadlines', 'Proof-of-loss due dates, repair deadlines for recoverable depreciation, appraisal and suit limitation periods in your policy. Ask in writing if unsure.']
    ]},
    money: { title: 'Estimates, receipts, and expenses', items: [
      ['estimates', 'Collect repair estimates', 'Get detailed, itemized estimates. Compare them line by line with the insurer\'s estimate.'],
      ['carrierest', 'Get a copy of the insurer\'s estimate', 'Ask for the full estimate with line items, depreciation, and the price list date.'],
      ['receipts', 'Keep repair and mitigation receipts', 'Invoices, contracts, and proof of payment for every repair and emergency service.'],
      ['ale', 'Track temporary expenses', 'Hotel, meals above normal, storage, mileage, and other additional living or business expenses, with receipts.'],
      ['payments', 'Track every payment received', 'Check amounts, dates, and what each payment was for. Note any mortgage company endorsement requirements.']
    ]}
  };
  var specific = {
    hail: { label: 'Hail damage', title: 'Hail-specific documentation', items: [
      ['h-softmetal', 'Photograph soft-metal dents', 'Gutters, downspouts, roof vents, AC fins, window wraps, and mailboxes often show hail impacts clearly. Chalk-circle and photograph them.'],
      ['h-roof', 'Document roof impacts (from a safe vantage or by a professional)', 'Bruised or fractured shingles, granule loss, and damaged ridge caps. Test squares are often used by inspectors.'],
      ['h-collateral', 'Record collateral damage', 'Siding, window screens, fences, patio covers, vehicles, and outdoor equipment.'],
      ['h-hailsize', 'Note the hail size you saw', 'Compare with coins or balls, and photograph hailstones with a ruler if you safely can.'],
      ['h-weather', 'Save the storm record for your date of loss', 'Use the Storm Event Lookup for NOAA/NWS reports near your city or ZIP code.']
    ]},
    wind: { label: 'Wind damage', title: 'Wind-specific documentation', items: [
      ['w-shingles', 'Photograph missing, lifted, or creased shingles', 'Include wide shots that show the pattern across roof slopes, plus shingles found in the yard.'],
      ['w-trees', 'Document fallen trees and limbs', 'Photograph where they fell, what they hit, and the stump or break before removal. Keep removal invoices.'],
      ['w-fence', 'Record fences, signs, carports, and outbuildings', 'Show direction of lean and the damaged posts or anchors.'],
      ['w-interior', 'Check for interior water from wind-created openings', 'Ceiling stains, wet insulation, and damaged contents. Photograph before drying or removal.'],
      ['w-weather', 'Save wind reports for the date', 'NWS storm surveys and reports can support the date of loss; they do not prove damage by themselves.']
    ]},
    fire: { label: 'Fire damage', title: 'Fire and smoke documentation', items: [
      ['f-report', 'Get the fire department report', 'Request the incident report number and the report once available.'],
      ['f-rooms', 'Photograph every room, including areas without visible fire', 'Smoke and soot travel through HVAC and wall cavities. Document odor and residue too.'],
      ['f-contents', 'Start a contents inventory', 'Room by room: item, quantity, age, brand/model, and replacement price. Photos and receipts help.'],
      ['f-ale', 'Track additional living expenses (ALE)', 'Hotel, rental, meals, laundry, mileage, pet boarding—keep every receipt.'],
      ['f-water', 'Document water damage from firefighting', 'Wet drywall, flooring, and contents are part of the loss.'],
      ['f-security', 'Secure the property', 'Board-up and fencing invoices; prevent theft and weather damage.']
    ]},
    water: { label: 'Water damage', title: 'Water damage documentation', items: [
      ['wa-source', 'Identify and photograph the source', 'Burst pipe, supply line, water heater, appliance, or roof opening. Keep the failed part if possible.'],
      ['wa-stop', 'Record when the water was stopped', 'Note the shutoff time and who stopped it. Speed matters for coverage and mold.'],
      ['wa-moisture', 'Keep drying and moisture readings', 'Mitigation company moisture maps, equipment logs, and daily readings.'],
      ['wa-tearout', 'Photograph before tear-out', 'Flooring, baseboards, cabinets, and drywall before removal, plus removed materials.'],
      ['wa-flood', 'Separate surface flood water from other water', 'Rising surface water is usually a flood (NFIP) issue, not a homeowners claim. Note how water entered.'],
      ['wa-mold', 'Watch and document any mold growth', 'Many policies limit mold coverage—report it promptly.']
    ]},
    roof: { label: 'Roof damage', title: 'Roof claim documentation', items: [
      ['r-age', 'Gather the roof age and history', 'Installation date, permits, prior repairs, and warranties. Insurers often ask about prior damage.'],
      ['r-material', 'Identify the roof material and layers', 'Composition shingle, tile, metal, or low-slope membrane; number of layers; decking type.'],
      ['r-photos', 'Get slope-by-slope photos', 'From a safe vantage or a qualified inspector: each slope, valleys, flashing, vents, and penetrations.'],
      ['r-interior', 'Document attic and ceiling conditions', 'Water stains, wet insulation, daylight through decking.'],
      ['r-code', 'Ask about code-required items', 'Permits and code requirements for McAllen re-roofing; ask whether your policy includes ordinance or law coverage.'],
      ['r-estimate', 'Compare roof estimates line by line', 'Squares, waste, starter, ridge, drip edge, flashing, vents, steep/high charges, removal, and O&P.']
    ]},
    commercial: { label: 'Commercial property', title: 'Commercial property documentation', items: [
      ['c-schedule', 'Get the full commercial policy and schedules', 'Declarations, building and business personal property limits, coinsurance, deductibles, and business income forms.'],
      ['c-lease', 'Review lease responsibilities', 'Who insures and repairs the roof, HVAC, storefront, and improvements—owner or tenant.'],
      ['c-roof', 'Document roofs and rooftop equipment', 'Membrane or metal panels, flashing, RTUs, skylights, and drains.'],
      ['c-inventory', 'Inventory damaged stock and equipment', 'Quantities, cost records, serial numbers, and photos.'],
      ['c-income', 'Preserve business income records', 'Prior-year financials, monthly sales, payroll, and extra expenses during the shutdown.'],
      ['c-vendors', 'Keep vendor and mitigation records', 'Contracts, invoices, equipment logs, and daily reports.']
    ]}
  };

  var STORE = 'mpa-checklist-v1';
  var state = { cat: null, done: {}, notes: {}, general: '', save: false };
  var panel = root.querySelector('[data-cl-panel]');
  var itemsEl = root.querySelector('[data-cl-items]');
  var bar = root.querySelector('[data-cl-bar]');
  var countEl = root.querySelector('[data-cl-count]');
  var pctEl = root.querySelector('[data-cl-pct]');
  var prog = root.querySelector('[role="progressbar"]');
  var saveBox = root.querySelector('[data-cl-save]');
  var generalEl = root.querySelector('[data-cl-notes]');

  function storage() { try { return window.localStorage; } catch (e) { return null; } }
  function persist() {
    var s = storage(); if (!s) return;
    try { if (state.save) s.setItem(STORE, JSON.stringify(state)); else s.removeItem(STORE); } catch (e) {}
  }
  function restore() {
    var s = storage(); if (!s) return;
    try { var raw = s.getItem(STORE); if (raw) { var st = JSON.parse(raw); if (st && st.save) state = st; } } catch (e) {}
  }
  function groups() {
    if (!state.cat) return [];
    return [common.start, specific[state.cat], common.policy, common.money];
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function render() {
    root.querySelectorAll('[data-cat]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-cat') === state.cat ? 'true' : 'false'); });
    if (!state.cat) { panel.hidden = true; return; }
    panel.hidden = false;
    root.querySelector('[data-cl-title]').textContent = specific[state.cat].label + ' documentation checklist';
    var html = '';
    groups().forEach(function (g, gi) {
      html += '<div class="check-group"><h3>' + esc(g.title) + '</h3>';
      g.items.forEach(function (it) {
        var id = 'ci-' + it[0];
        var done = !!state.done[it[0]];
        var note = state.notes[it[0]] || '';
        html += '<div class="check-item' + (done ? ' is-done' : '') + '"><input type="checkbox" id="' + id + '" data-item="' + it[0] + '"' + (done ? ' checked' : '') + '>' +
          '<label for="' + id + '">' + esc(it[1]) + '</label><p class="ci-help">' + esc(it[2]) + '</p>' +
          '<button type="button" class="ci-note-toggle no-print" data-note-toggle="' + it[0] + '" aria-expanded="' + (note ? 'true' : 'false') + '">' + (note ? 'Hide note' : '+ Add a note') + '</button>' +
          '<textarea aria-label="Note for: ' + esc(it[1]) + '" data-note="' + it[0] + '"' + (note ? '' : ' hidden') + ' maxlength="1000">' + esc(note) + '</textarea></div>';
      });
      html += '</div>';
    });
    itemsEl.innerHTML = html;
    generalEl.value = state.general || '';
    saveBox.checked = !!state.save;
    progress();
  }
  function progress() {
    var ids = []; groups().forEach(function (g) { g.items.forEach(function (it) { ids.push(it[0]); }); });
    var n = ids.filter(function (id) { return state.done[id]; }).length;
    var pct = ids.length ? Math.round(n / ids.length * 100) : 0;
    bar.style.width = pct + '%';
    countEl.textContent = n + ' of ' + ids.length + ' complete';
    pctEl.textContent = pct + '%';
    prog.setAttribute('aria-valuenow', pct);
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-cat]');
    if (b) { state.cat = b.getAttribute('data-cat'); render(); persist(); panel.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    var t = e.target.closest('[data-note-toggle]');
    if (t) {
      var ta = itemsEl.querySelector('[data-note="' + t.getAttribute('data-note-toggle') + '"]');
      ta.hidden = !ta.hidden; t.setAttribute('aria-expanded', ta.hidden ? 'false' : 'true'); t.textContent = ta.hidden ? '+ Add a note' : 'Hide note';
      if (!ta.hidden) ta.focus();
    }
  });
  itemsEl.addEventListener('change', function (e) {
    var id = e.target.getAttribute('data-item'); if (!id) return;
    state.done[id] = e.target.checked;
    e.target.closest('.check-item').classList.toggle('is-done', e.target.checked);
    progress(); persist();
  });
  itemsEl.addEventListener('input', function (e) { var id = e.target.getAttribute('data-note'); if (id) { state.notes[id] = e.target.value; persist(); } });
  generalEl.addEventListener('input', function () { state.general = generalEl.value; persist(); });
  saveBox.addEventListener('change', function () { state.save = saveBox.checked; persist(); });
  root.querySelector('[data-cl-reset]').addEventListener('click', function () {
    if (!window.confirm('Clear all checkmarks and notes for this checklist?')) return;
    state.done = {}; state.notes = {}; state.general = ''; render(); persist();
  });
  root.querySelector('[data-cl-print]').addEventListener('click', function () {
    var d = root.querySelector('[data-print-date]'); if (d) d.textContent = new Date().toLocaleDateString();
    itemsEl.querySelectorAll('textarea').forEach(function (t) { if (t.value) t.hidden = false; });
    window.print();
  });
  root.querySelector('[data-cl-download]').addEventListener('click', function () {
    var lines = ['PROPERTY INSURANCE CLAIM DOCUMENTATION CHECKLIST', specific[state.cat].label, 'Created ' + new Date().toLocaleString() + ' with https://mcallenpublicadjuster.com/claim-documentation-checklist/', ''];
    groups().forEach(function (g) {
      lines.push(g.title.toUpperCase());
      g.items.forEach(function (it) {
        lines.push((state.done[it[0]] ? '[x] ' : '[ ] ') + it[1]);
        lines.push('    ' + it[2]);
        if (state.notes[it[0]]) lines.push('    NOTE: ' + state.notes[it[0]]);
      });
      lines.push('');
    });
    if (state.general) { lines.push('GENERAL NOTES'); lines.push(state.general); lines.push(''); }
    lines.push('This checklist is general guidance, not legal advice. Follow your policy and insurer requirements.');
    lines.push('Free Claim Review: https://mcallenpublicadjuster.com/free-claim-review/ · +1 (832) 503-5866');
    var blob = new Blob([lines.join('\r\n')], { type: 'text/plain;charset=utf-8' });
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'claim-documentation-checklist-' + state.cat + '.txt';
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });
  restore();
  var hash = (location.hash || '').replace('#', '');
  if (specific[hash]) state.cat = hash;
  render();
})();
