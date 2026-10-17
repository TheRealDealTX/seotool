/* Extracts text lines from a PDF in the browser using pdf.js (loaded on
   demand from cdnjs, only when a PDF is actually dropped). Items are grouped
   into visual lines by their y position and ordered left to right, so a
   two-column estimate header comes out as one line per row. */
(function (root) {
  'use strict';
  var PDFJS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.min.mjs';
  var WORKER_URL = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.min.mjs';
  var libPromise = null;

  function lib() {
    if (!libPromise) {
      libPromise = import(PDFJS_URL).then(function (m) {
        m.GlobalWorkerOptions.workerSrc = WORKER_URL;
        return m;
      });
    }
    return libPromise;
  }

  function linesFromItems(items) {
    var rows = [];
    items.forEach(function (it) {
      if (!it.str || !it.transform) return;
      var x = it.transform[4], y = it.transform[5];
      var row = null;
      for (var i = 0; i < rows.length; i++) { if (Math.abs(rows[i].y - y) <= 2.5) { row = rows[i]; break; } }
      if (!row) { row = { y: y, items: [] }; rows.push(row); }
      row.items.push({ x: x, w: it.width || 0, s: it.str });
    });
    rows.sort(function (a, b) { return b.y - a.y; });
    return rows.map(function (r) {
      r.items.sort(function (a, b) { return a.x - b.x; });
      var out = '', endX = null;
      r.items.forEach(function (it) {
        if (out && endX !== null) out += (it.x - endX > 1.5) ? ' ' : '';
        out += it.s;
        endX = it.x + it.w;
      });
      return out.replace(/\s+/g, ' ').trim();
    }).filter(Boolean);
  }

  /** Resolve to the text of the first `maxPages` pages, one visual line per entry. */
  root.PdfText = {
    lines: function (file, maxPages) {
      maxPages = maxPages || 3;
      return lib().then(function (pdfjs) {
        return file.arrayBuffer().then(function (buf) {
          return pdfjs.getDocument({ data: buf, isEvalSupported: false, disableFontFace: true }).promise;
        }).then(function (doc) {
          var n = Math.min(doc.numPages, maxPages), all = [];
          var chain = Promise.resolve();
          for (var p = 1; p <= n; p++) {
            (function (pageNo) {
              chain = chain.then(function () {
                return doc.getPage(pageNo).then(function (page) { return page.getTextContent(); })
                  .then(function (tc) { all = all.concat(linesFromItems(tc.items)); });
              });
            }(p));
          }
          return chain.then(function () { try { doc.destroy(); } catch (e) {} return all; });
        });
      });
    }
  };
}(window));
