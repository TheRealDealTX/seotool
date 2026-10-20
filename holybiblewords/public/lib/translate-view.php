<?php
// /translate/ — shown inside the commentary popup (same-origin iframe). The parent
// page hands over the commentary HTML; Google's free Website Translator element
// translates it in place to Cebuano. Nothing is stored or sent to our server.
header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: public, max-age=86400');
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Translation</title>
<style>
  :root { color-scheme: light dark; --bg: #fff; --text: #1c2622; --muted: #5d6b65; --accent: #1b6aa3; --line: #d8e1dc; }
  @media (prefers-color-scheme: dark) { :root { --bg: #161d22; --text: #e3e9e6; --muted: #98a6a0; --accent: #6db4e8; --line: #2a353c; } }
  :root.dark { --bg: #161d22; --text: #e3e9e6; --muted: #98a6a0; --accent: #6db4e8; --line: #2a353c; }
  :root.light { --bg: #fff; --text: #1c2622; --muted: #5d6b65; --accent: #1b6aa3; --line: #d8e1dc; }
  html, body { margin: 0; background: var(--bg); color: var(--text); }
  body { padding: 4px 16px 24px; font: 1.02rem/1.7 "Iowan Old Style", "Palatino Linotype", Georgia, serif; top: 0 !important; position: static !important; }
  h1 { font: 700 1rem system-ui, sans-serif; margin: 6px 0 2px; }
  h4 { font: 700 .95rem system-ui, sans-serif; color: var(--accent); margin: 14px 0 4px; }
  p { margin: 10px 0; }
  a { color: var(--accent); }
  strong { font-family: system-ui, sans-serif; font-size: .92em; }
  .status { font: .85rem system-ui, sans-serif; color: var(--muted); margin: 0 0 8px; }
  .gt { font: .75rem system-ui, sans-serif; color: var(--muted); border-top: 1px solid var(--line); margin-top: 18px; padding-top: 8px; }
  /* keep Google's top banner and hover popups out of the way */
  .goog-te-banner-frame, iframe.skiptranslate, #goog-gt-tt, .goog-te-balloon-frame, .VIpgJd-ZVi9od-ORHb-OEVmcd { display: none !important; }
  .goog-text-highlight, #content font { background: none !important; box-shadow: none !important; }
</style>
<script>
  // translate straight to Cebuano on load (the element reads this cookie)
  document.cookie = 'googtrans=/en/ceb; path=/translate/; SameSite=Lax';
  try { var t = parent.document.documentElement.dataset.theme; if (t === 'dark' || t === 'light') document.documentElement.className = t; } catch (e) {}
</script>
</head>
<body>
<p class="status notranslate" id="status">Ginahubad sa Cebuano… (Translating to Cebuano…)</p>
<h1 id="title" class="notranslate"></h1>
<div id="content"></div>
<div class="gt notranslate">Machine translation by Google Translate. It may contain mistakes. <span id="gt"></span></div>
<script>
  var data = null;
  try { data = parent.hbwTranslatePayload || null; } catch (e) {}
  if (data) {
    document.getElementById('title').textContent = data.title || '';
    document.getElementById('content').innerHTML = data.html || '';
    // links open in the main window, in the reader's version
    document.querySelectorAll('#content a[href^="/"]').forEach(function (a) { a.target = '_top'; });
  } else {
    document.getElementById('status').textContent = 'Nothing to translate.';
  }
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({ pageLanguage: 'en', includedLanguages: 'ceb', autoDisplay: false }, 'gt');
    var tries = 0, t = setInterval(function () {
      // done when Google has rewritten the text
      if (document.documentElement.classList.contains('translated-ltr') || ++tries > 40) {
        clearInterval(t);
        document.getElementById('status').textContent = tries > 40 ? 'Couldn’t translate right now. Check your connection and try again.' : 'Hinubad sa Cebuano (Translated to Cebuano)';
      }
    }, 250);
  }
</script>
<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>
