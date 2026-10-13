/* Contents inventory builder: autosaves to localStorage, exports CSV */
(function () {
  'use strict';
  var root = document.querySelector('[data-inv]');
  if (!root) return;
  var KEY = 'txpa-inventory-v1';
  var LIFE = { Electronics: 5, Clothing: 4, Furniture: 12, Appliances: 12, Tools: 15, Decor: 15, Other: 10 };
  var rows = [];
  try { rows = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { rows = []; }
  if (!rows.length) rows = [{ room: 'Living room', item: '', notes: '', cat: 'Furniture', qty: 1, age: '', cost: '' }];
  var tbody = root.querySelector('[data-rows]');
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  function save() { try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch (e) {} }
  function acvOf(r) {
    var cost = (parseFloat(r.cost) || 0) * (parseFloat(r.qty) || 0);
    var dep = Math.min(0.8, (parseFloat(r.age) || 0) / (LIFE[r.cat] || 10));
    return { rcv: cost, acv: cost * (1 - dep) };
  }
  function render() {
    tbody.innerHTML = rows.map(function (r, i) {
      return '<tr data-i="' + i + '">' +
        '<td><input data-k="room" value="' + esc(r.room) + '" aria-label="Room"></td>' +
        '<td><input data-k="item" value="' + esc(r.item) + '" placeholder="e.g. Sofa" aria-label="Item"></td>' +
        '<td><input data-k="notes" value="' + esc(r.notes) + '" placeholder="Brand, model, link" aria-label="Notes"></td>' +
        '<td><select data-k="cat" aria-label="Category">' + Object.keys(LIFE).map(function (c) { return '<option' + (c === r.cat ? ' selected' : '') + '>' + c + '</option>'; }).join('') + '</select></td>' +
        '<td><input data-k="qty" type="number" min="1" value="' + esc(r.qty) + '" style="width:64px" aria-label="Quantity"></td>' +
        '<td><input data-k="age" type="number" min="0" step="0.5" value="' + esc(r.age) + '" style="width:72px" aria-label="Age"></td>' +
        '<td><input data-k="cost" type="number" min="0" step="1" value="' + esc(r.cost) + '" placeholder="$" aria-label="Replacement cost"></td>' +
        '<td><button type="button" class="icon-btn" data-del aria-label="Remove row">×</button></td></tr>';
    }).join('');
    totals();
  }
  function totals() {
    var rcv = 0, acv = 0, count = 0, rooms = {};
    rows.forEach(function (r) {
      if (!r.item && !r.cost) return;
      var v = acvOf(r); rcv += v.rcv; acv += v.acv; count += parseFloat(r.qty) || 0; if (r.room) rooms[r.room.trim().toLowerCase()] = 1;
    });
    root.querySelector('[data-out="count"]').textContent = count;
    root.querySelector('[data-out="rcv"]').textContent = money(rcv);
    root.querySelector('[data-out="acv"]').textContent = money(acv);
    root.querySelector('[data-out="rooms"]').textContent = Object.keys(rooms).length;
  }
  function addRow(room) {
    var last = rows[rows.length - 1];
    rows.push({ room: room || (last ? last.room : ''), item: '', notes: '', cat: last ? last.cat : 'Other', qty: 1, age: '', cost: '' });
    save(); render();
    var inputs = tbody.querySelectorAll('tr:last-child input[data-k="item"]');
    if (inputs[0]) inputs[0].focus();
  }

  tbody.addEventListener('input', function (e) {
    var tr = e.target.closest('tr'), k = e.target.getAttribute('data-k');
    if (!tr || !k) return;
    rows[+tr.getAttribute('data-i')][k] = e.target.value;
    save(); totals();
  });
  tbody.addEventListener('click', function (e) {
    if (!e.target.closest('[data-del]')) return;
    rows.splice(+e.target.closest('tr').getAttribute('data-i'), 1);
    if (!rows.length) rows.push({ room: '', item: '', notes: '', cat: 'Other', qty: 1, age: '', cost: '' });
    save(); render();
  });
  tbody.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.closest('tr:last-child')) { e.preventDefault(); addRow(); }
  });
  root.querySelector('[data-rooms]').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (b) addRow(b.textContent);
  });
  root.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]'); if (!a) return;
    var act = a.getAttribute('data-act');
    if (act === 'add') addRow();
    if (act === 'print') window.print();
    if (act === 'clear' && window.confirm('Delete the whole inventory from this browser? Export a CSV first if you need it.')) {
      rows = []; addRow('');
    }
    if (act === 'csv') {
      var q = function (s) { s = String(s == null ? '' : s); if (/^[=+\-@]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
      var lines = [['Room', 'Item', 'Brand / model / notes', 'Category', 'Quantity', 'Age (years)', 'Replacement cost each', 'Replacement cost total', 'Estimated ACV'].map(q).join(',')];
      rows.forEach(function (r) {
        if (!r.item && !r.cost) return;
        var v = acvOf(r);
        lines.push([r.room, r.item, r.notes, r.cat, r.qty, r.age, r.cost, v.rcv.toFixed(2), v.acv.toFixed(2)].map(q).join(','));
      });
      var blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
      var link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = 'contents-inventory.csv';
      document.body.appendChild(link); link.click(); link.remove();
    }
  });
  render();
})();
