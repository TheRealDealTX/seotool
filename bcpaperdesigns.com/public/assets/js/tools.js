/* BC Paper Designs — party tools */
(function () {
  "use strict";
  var BC = window.BC || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function seg(wrap, cb) {
    var btns = $$("button", wrap);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        cb(b.getAttribute("data-v"));
      });
    });
    var on = btns.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })[0];
    return on ? on.getAttribute("data-v") : null;
  }
  function printWith(html) {
    var area = $("#print-area");
    if (!area) { area = document.createElement("div"); area.id = "print-area"; document.body.appendChild(area); }
    area.innerHTML = html;
    document.body.classList.add("printing");
    var done = function () { document.body.classList.remove("printing"); window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    setTimeout(function () { window.print(); setTimeout(done, 1500); }, 150);
  }

  /* ================= Banner maker ================= */
  var bm = $("[data-tool=banner]");
  if (bm) (function () {
    var text = $("#bm-text"), stage = $("#bm-stage"), colorsWrap = $("#bm-colors"), ink = $("#bm-ink"), count = $("#bm-count");
    var state = { shape: "pennant", font: "serif" };
    var qs = new URLSearchParams(location.search);
    if (qs.get("text")) text.value = qs.get("text").slice(0, 60);
    if (qs.get("colors")) {
      var cs = qs.get("colors").split(",").filter(function (c) { return /^#?[0-9a-fA-F]{6}$/.test(c); }).slice(0, 4);
      $$("input[type=color]", colorsWrap).forEach(function (inp, i) { if (cs[i]) inp.value = cs[i].charAt(0) === "#" ? cs[i] : "#" + cs[i]; });
    }
    function colors() { return $$("input[type=color]", colorsWrap).map(function (i) { return i.value; }); }
    function opts() { return { colors: colors(), shape: state.shape, font: state.font, ink: ink.value, perRow: 12, dots: state.shape !== "circle" }; }
    function draw() {
      stage.innerHTML = BC.bunting(text.value, opts());
      var letters = text.value.replace(/\s/g, "").length;
      count.textContent = letters + " letter" + (letters === 1 ? "" : "s") + " = " + letters + " sheet" + (letters === 1 ? "" : "s") + " of 8.5 x 11 cardstock";
    }
    state.shape = seg($("#bm-shape"), function (v) { state.shape = v; draw(); }) || "pennant";
    state.font = seg($("#bm-font"), function (v) { state.font = v; draw(); }) || "serif";
    text.addEventListener("input", draw);
    ink.addEventListener("input", draw);
    colorsWrap.addEventListener("input", draw);
    $$(".preset", bm).forEach(function (p) {
      p.addEventListener("click", function () {
        var cs = p.getAttribute("data-colors").split(",");
        $$("input[type=color]", colorsWrap).forEach(function (inp, i) { inp.value = cs[i % cs.length]; });
        if (p.getAttribute("data-ink")) ink.value = p.getAttribute("data-ink");
        draw();
      });
    });
    $("#bm-print").addEventListener("click", function () {
      var o = opts(), chars = (o.font === "script" ? text.value : text.value.toUpperCase()).replace(/\s+/g, "").split("");
      if (!chars.length) return BC.toast("Type a message first");
      printWith(chars.map(function (c, i) { return '<div class="pp">' + BC.bigFlag(c, i, o) + "</div>"; }).join(""));
    });
    $("#bm-party").addEventListener("click", function (e) { if (BC.confetti) BC.confetti(e.clientX, e.clientY, 150); });
    draw();
  })();

  /* ================= Food calculator ================= */
  var fc = $("[data-tool=food]");
  if (fc) (function () {
    var f = { adults: $("#fc-adults"), kids: $("#fc-kids"), hours: $("#fc-hours"), meal: $("#fc-meal") };
    var out = $("#fc-out"), hoursOut = $("#fc-hours-out");
    var type = seg($("#fc-type"), function (v) { type = v; calc(); }) || "birthday";
    function n(el) { return Math.max(0, parseFloat(el.value) || 0); }
    function ceil(x, step) { step = step || 1; return Math.ceil(x / step) * step; }
    function calc() {
      var a = n(f.adults), k = n(f.kids), h = Math.max(1, n(f.hours)), meal = f.meal.value;
      hoursOut.textContent = h + (h === 1 ? " hour" : " hours");
      var eq = a + k * 0.65, guests = a + k;
      // finger food pieces: 6/person first hour (less if a meal is served), +3 per extra hour
      var perFirst = meal === "meal" ? 4 : meal === "dessert" ? 2 : 6;
      var bites = ceil(eq * (perFirst + (h - 1) * 3), 12);
      var cupcakes = ceil(guests * (type === "shower" ? 1.1 : 1.25), 12);
      var cake = Math.ceil(guests * 1.1);
      var cakeSize = cake <= 12 ? "one 6-inch round (2 layers)" : cake <= 24 ? "one 8-inch round (2 layers)" : cake <= 38 ? "one 10-inch round (2 layers)" : cake <= 50 ? "a half sheet cake" : "a full sheet cake";
      var drinks = Math.ceil(a * (2 + (h - 1)) + k * (1.5 + (h - 1) * 0.75));
      var ice = Math.ceil(guests * 1 + (h > 2 ? guests * 0.5 : 0));
      var plates = ceil(guests * (meal === "meal" ? 2 : 1.5), 10);
      var napkins = ceil(guests * 3, 10), cups = ceil(guests * 2, 10), favors = k > 0 ? Math.ceil(k * 1.1) : Math.ceil(a * 1.05);
      var fruit = Math.max(1, Math.ceil(eq * 0.25 * 10) / 10);
      var items = [
        [bites, "finger-food pieces", "Sandwich quarters, skewers, crackers and dips combined"],
        [cupcakes, "cupcakes", "Rounded up to full dozens (or " + cake + " cake servings: " + cakeSize + ")"],
        [drinks, "drinks", "Juice boxes, lemonade, water and coffee combined"],
        [ice + " lb", "of ice", "About 1 lb per guest, more if it runs past 2 hours"],
        [fruit + " lb", "of fruit", "Cut fruit or a fruit tray, a crowd favorite"],
        [plates, "plates", "Mix dessert and dinner plates"],
        [cups, "cups", "Guests lose track of their cup; plan two each"],
        [napkins, "napkins", "Three per guest, plus extras for cake time"],
        [favors, "favor bags", "One per child plus about 10% spare"]
      ];
      out.innerHTML = items.map(function (it) { return '<div class="res"><b>' + it[0] + "</b><span>" + it[1] + "</span><small>" + it[2] + "</small></div>"; }).join("");
      var key = "bc-food"; if (BC.store) BC.store(key, { a: a, k: k, h: h, meal: meal, type: type });
    }
    var saved = BC.store && BC.store("bc-food");
    if (saved) { f.adults.value = saved.a; f.kids.value = saved.k; f.hours.value = saved.h; f.meal.value = saved.meal; }
    Object.keys(f).forEach(function (k) { f[k].addEventListener("input", calc); f[k].addEventListener("change", calc); });
    $("#fc-print").addEventListener("click", function () {
      printWith('<div class="pp-list"><h1>Party shopping list</h1><p>' + n(f.adults) + " adults, " + n(f.kids) + " kids, " + n(f.hours) + " hours</p><ul>" +
        $$(".res", out).map(function (r) { return "<li><strong>" + r.querySelector("b").textContent + "</strong> " + r.querySelector("span").textContent + " - " + r.querySelector("small").textContent + "</li>"; }).join("") + "</ul></div>");
    });
    calc();
  })();

  /* ================= Planning timeline ================= */
  var tl = $("[data-tool=timeline]");
  if (tl) (function () {
    var dateIn = $("#tl-date"), nameIn = $("#tl-name"), list = $("#tl-list"), cd = $("#tl-countdown");
    var PLAN = {
      shower: [
        [56, "8 weeks before", ["Set the budget and guest count with the parents-to-be", "Pick a date, time and venue", "Choose a theme and color palette", "Start the guest list with mailing and email addresses"]],
        [42, "6 weeks before", ["Order or design invitations", "Ask the parents to finish their registry", "Book any rentals: tables, chairs, linens", "Plan the menu and decide on catering or potluck"]],
        [35, "5 weeks before", ["Send invitations (4-6 weeks ahead is standard)", "Add the registry link and RSVP date to the invite"]],
        [21, "3 weeks before", ["Choose 2-3 games and print the cards", "Order the cake or plan the dessert table", "Order or print the banner, cake topper and cupcake toppers"]],
        [14, "2 weeks before", ["Buy favors and prizes", "Make the decor: centerpieces, door sign, favor tags", "Plan the room layout and photo backdrop"]],
        [7, "1 week before", ["Follow up on missing RSVPs", "Confirm the cake, rentals and any helpers", "Buy non-perishable food, drinks and paper goods", "Assemble favors and attach tags"]],
        [2, "2 days before", ["Grocery shop for fresh food", "Prep make-ahead dishes", "Charge the camera or phone and make a playlist"]],
        [1, "The day before", ["Set up tables, banner and backdrop", "Lay out serving dishes with sticky-note labels", "Prepare a gift-opening station with a pen and list"]],
        [0, "Party day", ["Pick up the cake and ice", "Set out food 30 minutes before guests arrive", "Assign someone to record gifts for thank-you notes", "Enjoy it, and take photos of the decor before guests arrive"]],
        [-7, "Within 2 weeks after", ["Help the parents send thank-you cards", "Share photos with guests"]]
      ],
      birthday: [
        [42, "6 weeks before", ["Set the budget and guest count", "Choose the date, time and venue", "Let the birthday child pick the theme", "Book entertainment or activities"]],
        [28, "4 weeks before", ["Send invitations (3-4 weeks ahead)", "Order the cake", "Book rentals: bounce house, tables, chairs"]],
        [21, "3 weeks before", ["Plan the menu and the activity schedule", "Order or print the banner, cake topper and cupcake toppers"]],
        [14, "2 weeks before", ["Buy favors and craft supplies", "Make decorations: centerpieces, door sign, favor tags", "Plan games and gather prizes"]],
        [7, "1 week before", ["Follow up on RSVPs and allergies", "Buy paper goods, drinks and non-perishables", "Assemble favor bags", "Confirm cake pickup time"]],
        [2, "2 days before", ["Grocery shop for fresh food", "Prep make-ahead snacks", "Make a playlist"]],
        [1, "The day before", ["Hang the banner and set up the dessert table", "Blow up balloons (latex lasts about 12-24 hours)", "Lay out serving dishes and labels"]],
        [0, "Party day", ["Pick up the cake and ice", "Set out food 30 minutes before guests arrive", "Photograph the decor before guests arrive", "Hand out favors at the door"]],
        [-3, "A few days after", ["Send thank-you cards", "Share photos with families"]]
      ]
    };
    var type = seg($("#tl-type"), function (v) { type = v; render(); }) || "shower";
    var saved = (BC.store && BC.store("bc-timeline")) || {};
    if (saved.date) dateIn.value = saved.date; else { var d = new Date(); d.setDate(d.getDate() + 49); dateIn.value = d.toISOString().slice(0, 10); }
    if (saved.name) nameIn.value = saved.name;
    if (saved.type) { type = saved.type; $$("#tl-type button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === type ? "true" : "false"); }); }
    var done = saved.done || {};
    function fmt(d) { return d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" }); }
    function render() {
      var party = dateIn.value ? new Date(dateIn.value + "T12:00:00") : null;
      if (!party || isNaN(party)) { list.innerHTML = "<p>Pick a party date to build your timeline.</p>"; return; }
      var today = new Date(); today.setHours(12, 0, 0, 0);
      var days = Math.round((party - today) / 864e5);
      cd.innerHTML = days >= 0 ? "<div><b>" + days + "</b><span>days to go</span></div><div><b>" + Math.floor(days / 7) + "</b><span>weeks</span></div><div><b>" + fmt(party).split(",")[0] + "</b><span>party day</span></div>"
        : "<div><b>" + (-days) + "</b><span>days since</span></div>";
      var colors = ["#ff6f61", "#ffcf5a", "#5cc9b5", "#ab97ff", "#8fd3ff"];
      list.innerHTML = PLAN[type].map(function (g, gi) {
        var when = new Date(party); when.setDate(when.getDate() - g[0]);
        var past = when < today && g[0] > 0;
        return '<li class="tl-group' + (past ? " past" : "") + '" style="--c:' + colors[gi % colors.length] + '"><span class="when">' + fmt(when) + (past ? " · passed" : "") + "</span><h3>" + g[1] + '</h3><ul class="checks" style="grid-template-columns:1fr">' +
          g[2].map(function (t, ti) { var id = type + "-" + gi + "-" + ti; return '<li><label><input type="checkbox" data-id="' + id + '"' + (done[id] ? " checked" : "") + "><span>" + esc(t) + "</span></label></li>"; }).join("") + "</ul></li>";
      }).join("");
      save();
    }
    function save() { if (BC.store) BC.store("bc-timeline", { date: dateIn.value, name: nameIn.value, type: type, done: done }); }
    list.addEventListener("change", function (e) { var id = e.target.getAttribute("data-id"); if (id) { done[id] = e.target.checked; save(); } });
    dateIn.addEventListener("change", render); nameIn.addEventListener("input", save);
    $("#tl-print").addEventListener("click", function () { window.print(); });
    $("#tl-ics").addEventListener("click", function () {
      if (!dateIn.value) return;
      var d = dateIn.value.replace(/-/g, ""), nx = new Date(dateIn.value + "T12:00:00"); nx.setDate(nx.getDate() + 1);
      var end = nx.toISOString().slice(0, 10).replace(/-/g, ""), title = nameIn.value || (type === "shower" ? "Baby shower" : "Birthday party");
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//BC Paper Designs//Party Timeline//EN", "BEGIN:VEVENT", "UID:" + Date.now() + "@bcpaperdesigns.com",
        "DTSTAMP:" + new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z", "DTSTART;VALUE=DATE:" + d, "DTEND;VALUE=DATE:" + end, "SUMMARY:" + title.replace(/[,;]/g, " "),
        "DESCRIPTION:Planned with bcpaperdesigns.com/tools/party-planning-timeline/", "END:VEVENT", "END:VCALENDAR"].join("\r\n");
      var a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar" })); a.download = "party.ics"; document.body.appendChild(a); a.click(); a.remove();
    });
    render();
  })();

  /* ================= Theme finder quiz ================= */
  var qz = $("[data-tool=quiz]");
  if (qz) (function () {
    var data = JSON.parse($("#theme-data").textContent);
    var qs = $$(".quiz-q", qz), bar = $(".progress i", qz), result = $("#quiz-result"), answers = {}, step = 0;
    function go(i) {
      step = i; qs.forEach(function (q, j) { q.classList.toggle("active", j === i); });
      bar.style.width = (i / qs.length * 100) + "%"; result.hidden = true;
    }
    qs.forEach(function (q, i) {
      $$(".quiz-opts button", q).forEach(function (b) {
        b.addEventListener("click", function () {
          answers[q.getAttribute("data-q")] = b.getAttribute("data-v");
          if (i < qs.length - 1) go(i + 1); else finish();
        });
      });
      var back = $(".quiz-back", q); if (back) back.addEventListener("click", function () { go(Math.max(0, i - 1)); });
    });
    function finish() {
      qs.forEach(function (q) { q.classList.remove("active"); }); bar.style.width = "100%";
      var scored = data.map(function (t) {
        var s = 0, tags = t.tags;
        if (answers.occasion === "shower" && (t.occasion === "baby-shower" || t.occasion === "both")) s += 5;
        if (answers.occasion === "birthday" && (t.occasion === "birthday" || t.occasion === "both")) s += 5;
        ["vibe", "color", "world"].forEach(function (k) { if (answers[k] && tags.indexOf(answers[k]) > -1) s += 3; });
        if (answers.occasion === "shower" && answers.who && tags.indexOf(answers.who) > -1) s += 2;
        if (answers.occasion === "birthday" && answers.who && tags.indexOf(answers.who) > -1) s += 2;
        return { t: t, s: s + Math.random() * 0.5 };
      }).sort(function (a, b) { return b.s - a.s; }).slice(0, 3);
      result.innerHTML = '<h2 style="margin-top:0">Your top party themes</h2><p class="lead">Based on your answers, start with these. Each guide has a palette, decor list and a printable checklist.</p><div class="grid-cards">' +
        scored.map(function (x) {
          var t = x.t;
          return '<a class="tcard" href="' + t.url + '"><div class="tcard-img"><img src="' + t.img + '" alt="" loading="lazy" width="480" height="360"></div><div class="tcard-body"><h3>' + esc(t.name) + "</h3><p>" + esc(t.tagline) + '</p><div class="dots">' +
            t.palette.map(function (c) { return '<i style="background:' + c + '"></i>'; }).join("") + "</div></div></a>";
        }).join("") + '</div><p style="margin-top:22px"><button class="btn btn--ghost" type="button" id="quiz-again">Take the quiz again</button></p>';
      result.hidden = false;
      $("#quiz-again").addEventListener("click", function () { answers = {}; go(0); });
      var r = result.getBoundingClientRect(); if (BC.confetti) BC.confetti(r.left + r.width / 2, Math.max(80, r.top), 140);
      result.scrollIntoView({ behavior: BC.reduce ? "auto" : "smooth", block: "start" });
    }
    go(0);
  })();

  /* ================= Bingo generator ================= */
  var bg = $("[data-tool=bingo]");
  if (bg) (function () {
    var LISTS = {
      gifts: ["Onesies", "Diapers", "Wipes", "Bottles", "Pacifier", "Swaddle", "Baby monitor", "Car seat", "Stroller", "Bibs", "Board books", "Burp cloths", "Socks", "Baby lotion", "Thermometer", "Hooded towel", "Crib sheets", "Teether", "Rattle", "Diaper bag", "Bath tub", "Nail clippers", "Sleep sack", "Play mat", "Baby carrier", "Sun hat", "Night light", "Bouncer", "High chair", "Breast pump", "Diaper cream", "Washcloths", "Mittens", "Blanket", "Stuffed animal", "Baby shampoo", "Sippy cup", "Changing pad", "Bottle brush", "Gift card"],
      books: ["Goodnight story", "Board book", "Fairy tale", "Bath book", "Alphabet book", "Counting book", "Nursery rhymes", "Bedtime classic", "Touch-and-feel", "Lift-the-flap", "Picture book", "Animal book", "Colors book", "Poetry", "Lullabies", "Pop-up book", "First words", "Dr. or rhyming book", "Book with a bear", "Book with a bunny", "Book about love", "Book about a moon", "Shapes book", "Farm book", "Ocean book", "Opposites book", "Signed message", "Parent favorite", "Grandparent favorite", "Bilingual book", "Cloth book", "Book about bugs", "Book about trucks", "Book about the sea", "Seasons book", "Music book"],
      birthday: ["Balloon", "Cupcake", "Candles", "Party hat", "Present", "Confetti", "Banner", "Piñata", "Ice cream", "Cake", "Sprinkles", "Streamers", "Juice box", "Goody bag", "Sticker", "Whistle", "Crown", "Bubbles", "Card", "Bow", "Song", "Games", "Friends", "Pizza", "Popcorn", "Lemonade", "Ribbon", "Photo booth", "Party favor", "Dance", "Clown nose", "Wish", "Thank you", "Cookie", "Fruit cup", "Tiara"]
    };
    var title = $("#bg-title"), num = $("#bg-num"), list = $("#bg-list"), custom = $("#bg-custom"), color = $("#bg-color"), prev = $("#bg-preview");
    var cards = [];
    function words() {
      if (list.value === "custom") return custom.value.split(/\n|,/).map(function (s) { return s.trim(); }).filter(Boolean);
      return LISTS[list.value];
    }
    function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
    function card(c) {
      var cells = c.slice(0, 12).concat(["FREE"]).concat(c.slice(12, 24));
      return '<div class="bingo" style="--bc:' + color.value + '"><h4>' + esc(title.value || "Baby Shower Bingo") + '</h4><div class="letters"><b>B</b><b>I</b><b>N</b><b>G</b><b>O</b></div><div class="cells">' +
        cells.map(function (w, i) { return i === 12 ? '<span class="free">FREE</span>' : "<span>" + esc(w) + "</span>"; }).join("") + "</div></div>";
    }
    function gen() {
      var w = words(), n = Math.min(40, Math.max(1, parseInt(num.value, 10) || 1));
      $("#bg-custom-wrap").hidden = list.value !== "custom";
      if (w.length < 24) { prev.innerHTML = "<p>Add at least 24 words (you have " + w.length + ").</p>"; cards = []; return; }
      var seen = {}; cards = [];
      for (var i = 0, tries = 0; i < n && tries < 500; tries++) { var c = shuffle(w).slice(0, 24), k = c.join("|"); if (!seen[k]) { seen[k] = 1; cards.push(c); i++; } }
      prev.innerHTML = cards.slice(0, 6).map(card).join("") + (cards.length > 6 ? '<p style="align-self:center">+ ' + (cards.length - 6) + " more unique cards will print.</p>" : "");
    }
    [title, num, list, custom, color].forEach(function (el) { el.addEventListener("input", gen); el.addEventListener("change", gen); });
    $("#bg-new").addEventListener("click", gen);
    $("#bg-print").addEventListener("click", function () {
      if (!cards.length) return;
      var html = "";
      for (var i = 0; i < cards.length; i += 2) html += '<div class="pp-bingo">' + card(cards[i]) + (cards[i + 1] ? card(cards[i + 1]) : "") + "</div>";
      printWith(html);
    });
    gen();
  })();
})();
