/* Shop VIP Gifts — interactive tools. Each tool initialises only if its root element is on the page. */
(function () {
  "use strict";
  var IMG = "/assets/img/";
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  /* =====================================================================
     1. Gift Finder quiz
     ===================================================================== */
  var GIFTS = [
    { n: "Engraved crystal decanter set", img: "wine", p: "$120–$250", t: [3], w: ["partner", "parent", "boss", "client"], o: ["milestone", "anniversary", "holiday", "thankyou"], v: ["foodie", "homebody", "professional"], g: "/gifts-for-him/", why: "Heavy crystal and a custom engraving turn an everyday bar piece into an heirloom." },
    { n: "Single-origin chocolate tasting box", img: "chocolates", p: "$45–$90", t: [1, 2], w: ["partner", "parent", "friend", "client", "boss", "host"], o: ["birthday", "holiday", "thankyou", "justbecause"], v: ["foodie"], g: "/luxury-gift-boxes/", why: "Small-batch bars with tasting notes feel like a private chocolatier visit." },
    { n: "Classic pearl strand necklace", img: "pearls", p: "$250–$900", t: [4], w: ["partner", "parent"], o: ["anniversary", "birthday", "milestone"], v: ["style"], g: "/gifts-for-her/", why: "Pearls never date, and a velvet presentation box does half the work." },
    { n: "Minimalist leather-strap watch", img: "watch", p: "$150–$400", t: [3], w: ["partner", "parent", "friend"], o: ["birthday", "milestone", "anniversary"], v: ["style", "professional"], g: "/gifts-for-him/", why: "A clean dial worn daily is a reminder of you every time they check the time." },
    { n: "Monogrammed leather wallet", img: "wallet", p: "$60–$150", t: [2], w: ["partner", "parent", "friend", "boss"], o: ["birthday", "holiday", "justbecause"], v: ["style", "professional"], g: "/personalized-gifts/", why: "Full-grain leather plus their initials — useful, personal and built to patina." },
    { n: "Premium noise-cancelling headphones", img: "headphones", p: "$200–$450", t: [3], w: ["partner", "friend", "parent"], o: ["birthday", "holiday"], v: ["techie", "traveler"], g: "/gifts-for-him/", why: "Silence on demand is a genuine luxury for commuters and frequent flyers." },
    { n: "Flagship smartwatch", img: "smartwatch", p: "$250–$800", t: [4], w: ["partner", "parent"], o: ["birthday", "holiday", "milestone"], v: ["techie", "wellness"], g: "/gifts-for-him/", why: "Health tracking, payments and messages on the wrist — the tech gift they'll use hourly." },
    { n: "Couples spa day", img: "spa", p: "$250–$600", t: [4], w: ["partner", "parent"], o: ["anniversary", "birthday", "justbecause"], v: ["wellness"], g: "/experience-gifts/", why: "Time to slow down together is the rarest gift of all." },
    { n: "Chef's tasting-menu dinner", img: "dinner", p: "$200–$500", t: [3, 4], w: ["partner", "parent", "friend", "client"], o: ["anniversary", "milestone", "thankyou"], v: ["foodie"], g: "/experience-gifts/", why: "A reserved table at the restaurant they keep talking about says you were listening." },
    { n: "Weekend coastal getaway", img: "beach", p: "$600–$2,000", t: [5], w: ["partner", "parent"], o: ["anniversary", "milestone"], v: ["traveler", "wellness"], g: "/experience-gifts/", why: "Two nights somewhere beautiful beats any object for a milestone." },
    { n: "Travel upgrade voucher", img: "travel", p: "$500+", t: [5], w: ["partner", "boss", "client"], o: ["milestone", "thankyou"], v: ["traveler", "professional"], g: "/experience-gifts/", why: "Lounge access or a seat upgrade is pure VIP treatment for road warriors." },
    { n: "Vintage champagne & crystal flutes", img: "wine-toast", p: "$100–$300", t: [3], w: ["client", "boss", "host", "friend"], o: ["holiday", "milestone", "thankyou"], v: ["foodie", "professional"], g: "/corporate-gifts/", why: "Celebratory, shareable and appropriate for almost any professional relationship." },
    { n: "Executive gift box", img: "gift-pattern", p: "$75–$200", t: [2, 3], w: ["client", "boss"], o: ["holiday", "thankyou"], v: ["professional", "foodie"], g: "/corporate-gifts/", why: "Curated, beautifully packed and easy to send to a whole client list." },
    { n: "Fresh flower subscription (3 months)", img: "bouquet", p: "$150–$350", t: [3], w: ["parent", "partner", "host"], o: ["birthday", "justbecause", "thankyou"], v: ["homebody", "style"], g: "/gifts-for-her/", why: "A new arrangement every month keeps the gesture alive long after the day." },
    { n: "Fountain pen & leather journal set", img: "note-pen", p: "$80–$250", t: [2, 3], w: ["boss", "client", "friend", "parent"], o: ["milestone", "thankyou", "birthday"], v: ["professional"], g: "/personalized-gifts/", why: "A tool for big ideas — engrave the barrel to make it unmistakably theirs." },
    { n: "Fine-jewelry drop earrings", img: "earrings", p: "$150–$600", t: [3, 4], w: ["partner", "parent", "friend"], o: ["birthday", "anniversary", "holiday"], v: ["style"], g: "/gifts-for-her/", why: "Statement sparkle that works from the office to a black-tie evening." },
    { n: "Gold chain bracelet", img: "bracelet", p: "$100–$400", t: [3], w: ["partner", "friend", "parent"], o: ["birthday", "anniversary", "justbecause"], v: ["style"], g: "/gifts-for-her/", why: "Stackable, everyday gold that gets worn — not saved for best." },
    { n: "Leather crossbody bag", img: "leather-bag", p: "$150–$500", t: [3, 4], w: ["partner", "parent", "friend"], o: ["birthday", "holiday"], v: ["style", "traveler"], g: "/gifts-for-her/", why: "Hands-free, polished and ready for travel days and city weekends." },
    { n: "Specialty coffee subscription", img: "coffee", p: "$40–$120", t: [1, 2], w: ["friend", "parent", "client", "host", "boss"], o: ["thankyou", "holiday", "justbecause"], v: ["foodie", "homebody"], g: "/luxury-gift-boxes/", why: "Fresh-roasted beans each month make every morning feel a little upgraded." },
    { n: "Artisan skincare ritual set", img: "beauty", p: "$60–$200", t: [2, 3], w: ["partner", "parent", "friend"], o: ["birthday", "holiday", "justbecause"], v: ["wellness", "style"], g: "/gifts-for-her/", why: "A curated ritual is a nudge to take ten minutes for themselves." },
    { n: "Cashmere throw for the sofa", img: "home", p: "$150–$400", t: [3], w: ["parent", "host", "partner"], o: ["holiday", "thankyou"], v: ["homebody", "wellness"], g: "/luxury-gift-boxes/", why: "Cloud-soft and used every evening — luxury you can curl up in." },
    { n: "Made-to-measure suit fitting", img: "suit", p: "$600+", t: [5], w: ["partner"], o: ["milestone", "birthday"], v: ["style", "professional"], g: "/gifts-for-him/", why: "Nothing feels more VIP than clothing cut for your exact shape." },
    { n: "Statement leather handbag", img: "handbag", p: "$500+", t: [5], w: ["partner", "parent"], o: ["milestone", "anniversary", "birthday"], v: ["style"], g: "/gifts-for-her/", why: "An investment piece they'd hesitate to buy for themselves." },
    { n: "Patisserie celebration cake", img: "cake", p: "$60–$150", t: [2], w: ["friend", "parent", "partner", "boss"], o: ["birthday", "milestone"], v: ["foodie"], g: "/luxury-gift-boxes/", why: "A custom showpiece cake turns any gathering into an occasion." },
    { n: "Gourmet holiday hamper", img: "holiday", p: "$100–$250", t: [3], w: ["client", "host", "boss", "parent"], o: ["holiday", "thankyou"], v: ["foodie", "professional"], g: "/corporate-gifts/", why: "Shareable treats a whole office or family can enjoy." },
    { n: "Wine club membership", img: "wine", p: "$150–$500", t: [3, 4], w: ["friend", "client", "parent", "boss"], o: ["holiday", "birthday", "thankyou"], v: ["foodie"], g: "/experience-gifts/", why: "Hand-picked bottles arriving all year long — the gift that keeps showing up." },
    { n: "Curated 'open-one-a-day' gift box", img: "gift-ribbon", p: "$100–$300", t: [3], w: ["friend", "partner"], o: ["holiday", "birthday"], v: ["homebody", "foodie"], g: "/luxury-gift-boxes/", why: "Multiple little reveals stretch the excitement over days." },
    { n: "Professional family photo session", img: "family", p: "$250–$600", t: [4], w: ["parent"], o: ["holiday", "milestone", "justbecause"], v: ["homebody"], g: "/experience-gifts/", why: "Portraits they'll frame and keep for decades." },
    { n: "Private celebration night", img: "balloons", p: "$300–$1,000+", t: [4, 5], w: ["friend", "partner"], o: ["birthday", "milestone"], v: ["foodie", "style"], g: "/experience-gifts/", why: "Book the room, the menu and the guest list — they just show up." },
    { n: "Hostess candle & truffle set", img: "gift-pink", p: "$30–$60", t: [1], w: ["host", "friend"], o: ["thankyou", "holiday", "justbecause"], v: ["homebody", "foodie"], g: "/luxury-gift-boxes/", why: "An elegant thank-you that arrives wrapped and ready to hand over." },
    { n: "Client thank-you box", img: "gift-hands", p: "$50–$100", t: [1, 2], w: ["client", "boss"], o: ["thankyou", "holiday"], v: ["professional", "foodie"], g: "/corporate-gifts/", why: "Thoughtful, branded-lightly and easy to scale across accounts." },
    { n: "Framed custom map or art print", img: "flower-heart", p: "$80–$300", t: [2, 3], w: ["partner", "parent", "friend", "host"], o: ["anniversary", "holiday", "milestone"], v: ["homebody"], g: "/personalized-gifts/", why: "Mark the place you met, married or moved — personal art for their wall." }
  ];
  var QUIZ_LABEL = {
    partner: "Partner", parent: "Parent", friend: "Friend", client: "Client", boss: "Boss", host: "Host",
    birthday: "Birthday", anniversary: "Anniversary", holiday: "Holiday", thankyou: "Thank you", milestone: "Milestone", justbecause: "Just because"
  };

  var finder = $("[data-gift-finder]");
  if (finder) {
    var steps = $$(".q-step", finder), bar = $(".progress span", finder), back = $("[data-back]", finder), next = $("[data-next]", finder);
    var answers = { who: null, occ: null, budget: null, vibe: [] }, idx = 0;
    var keys = ["who", "occ", "budget", "vibe"];

    $$(".chip", finder).forEach(function (chip) {
      chip.addEventListener("click", function () {
        var step = chip.closest(".q-step"), key = step.getAttribute("data-key"), multi = step.hasAttribute("data-multi");
        if (multi) {
          var on = chip.getAttribute("aria-pressed") !== "true";
          var picked = $$('.chip[aria-pressed="true"]', step).length;
          if (on && picked >= 3) return;
          chip.setAttribute("aria-pressed", on ? "true" : "false");
          answers[key] = $$('.chip[aria-pressed="true"]', step).map(function (c) { return c.getAttribute("data-val"); });
        } else {
          $$(".chip", step).forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
          chip.setAttribute("aria-pressed", "true");
          answers[key] = chip.getAttribute("data-val");
          setTimeout(function () { if (idx < steps.length - 2) go(idx + 1); }, 260);
        }
        sync();
      });
    });
    function valid(i) { var k = keys[i]; if (!k) return true; return k === "vibe" ? answers.vibe.length > 0 : !!answers[k]; }
    function sync() {
      bar.style.width = ((idx) / (steps.length - 1) * 100) + "%";
      back.style.visibility = idx === 0 || idx === steps.length - 1 ? "hidden" : "visible";
      next.style.display = idx === steps.length - 1 ? "none" : "";
      next.textContent = idx === steps.length - 2 ? "Reveal my gifts ✦" : "Next →";
      next.disabled = !valid(idx);
    }
    function go(i) {
      steps[idx].classList.remove("active"); idx = i; steps[idx].classList.add("active");
      if (idx === steps.length - 1) render();
      sync();
      var top = finder.getBoundingClientRect().top + window.scrollY - 100;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
    }
    next.addEventListener("click", function () { if (valid(idx)) go(idx + 1); });
    back.addEventListener("click", function () { if (idx > 0) go(idx - 1); });
    $("[data-restart]", finder).addEventListener("click", function () {
      answers = { who: null, occ: null, budget: null, vibe: [] };
      $$(".chip", finder).forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
      go(0);
    });

    function render() {
      var tier = parseInt(answers.budget, 10);
      var scored = GIFTS.map(function (g) {
        var s = 0;
        if (g.w.indexOf(answers.who) > -1) s += 4; else s -= 2;
        if (g.o.indexOf(answers.occ) > -1) s += 2;
        answers.vibe.forEach(function (v) { if (g.v.indexOf(v) > -1) s += 3; });
        var dist = Math.min.apply(null, g.t.map(function (t) { return Math.abs(t - tier); }));
        s += dist === 0 ? 4 : dist === 1 ? 1 : -4;
        return { g: g, s: s };
      }).sort(function (a, b) { return b.s - a.s; }).slice(0, 6);
      var max = 4 + 2 + answers.vibe.length * 3 + 4;
      $("[data-summary]", finder).textContent = "For your " + QUIZ_LABEL[answers.who].toLowerCase() + " · " + QUIZ_LABEL[answers.occ].toLowerCase() + " · " + $('[data-key="budget"] .chip[aria-pressed="true"]', finder).textContent.trim();
      $("[data-results]", finder).innerHTML = scored.map(function (x, i) {
        var pct = Math.max(52, Math.min(99, Math.round(x.s / max * 100)));
        return '<article class="result" style="animation-delay:' + (i * 80) + 'ms"><img src="' + IMG + x.g.img + '.webp" alt="' + esc(x.g.n) + '" loading="lazy" width="400" height="300"><div>' +
          '<span class="match">' + pct + '% match</span><h3>' + esc(x.g.n) + '</h3><p>' + esc(x.g.why) + '</p>' +
          '<div class="meta"><span>' + esc(x.g.p) + '</span><a href="' + x.g.g + '">See the guide →</a></div></div></article>';
      }).join("");
    }
    sync();
  }

  /* =====================================================================
     2. Gift Budget Planner
     ===================================================================== */
  var planner = $("[data-budget]");
  if (planner) {
    var WEIGHT = { Partner: 4, Child: 3, Parent: 3, Sibling: 2, Friend: 1.5, Client: 2, Colleague: 1, Host: 1, Other: 1 };
    var REL = Object.keys(WEIGHT);
    var rowsEl = $(".rows", planner), totalEl = $("#bp-total", planner), KEY = "svg-budget-v1";
    var saved = store(KEY) || { total: 1000, rows: [
      { n: "Alex", r: "Partner", a: 300 }, { n: "Mom", r: "Parent", a: 150 }, { n: "Dad", r: "Parent", a: 150 },
      { n: "Sam", r: "Sibling", a: 80 }, { n: "Top client", r: "Client", a: 120 }
    ] };
    totalEl.value = saved.total;

    function addRow(d) {
      d = d || { n: "", r: "Friend", a: 0 };
      var row = document.createElement("div");
      row.className = "brow";
      row.innerHTML = '<input type="text" aria-label="Name" placeholder="Name" value="' + esc(d.n) + '">' +
        '<select aria-label="Relationship">' + REL.map(function (r) { return "<option" + (r === d.r ? " selected" : "") + ">" + r + "</option>"; }).join("") + "</select>" +
        '<input class="amt" type="number" min="0" step="5" inputmode="decimal" aria-label="Amount in dollars" value="' + (d.a || "") + '" placeholder="$">' +
        '<button type="button" class="icon-btn" aria-label="Remove">×</button>';
      row.querySelector("button").addEventListener("click", function () { row.remove(); calc(); });
      row.addEventListener("input", calc);
      rowsEl.appendChild(row);
    }
    function data() {
      return $$(".brow", rowsEl).map(function (r) {
        var f = r.querySelectorAll("input,select");
        return { n: f[0].value, r: f[1].value, a: parseFloat(f[2].value) || 0 };
      });
    }
    function money(n) { return "$" + Math.round(n).toLocaleString(); }
    function calc() {
      var rows = data(), total = parseFloat(totalEl.value) || 0;
      var spent = rows.reduce(function (s, r) { return s + r.a; }, 0), left = total - spent;
      $("[data-spent]", planner).textContent = money(spent);
      $("[data-left]", planner).textContent = (left < 0 ? "−" : "") + money(Math.abs(left));
      $("[data-left-label]", planner).textContent = left < 0 ? "over budget" : "left to spend";
      $("[data-people]", planner).textContent = rows.length;
      $("[data-avg]", planner).textContent = rows.length ? money(spent / rows.length) : "$0";
      var m = $(".meter span", planner), pct = total ? Math.min(100, spent / total * 100) : 0;
      m.style.width = pct + "%"; m.classList.toggle("over", spent > total);
      $("[data-pct]", planner).textContent = total ? Math.round(spent / total * 100) + "% of budget used" : "Set a total budget";
      var groups = {};
      rows.forEach(function (r) { groups[r.r] = (groups[r.r] || 0) + r.a; });
      var maxG = Math.max.apply(null, [1].concat(Object.keys(groups).map(function (k) { return groups[k]; })));
      $(".bars", planner).innerHTML = Object.keys(groups).sort(function (a, b) { return groups[b] - groups[a]; }).map(function (k) {
        return '<div class="bar-row"><div class="split-row"><span>' + k + '</span><b>' + money(groups[k]) + '</b></div><div class="bar"><span style="width:' + (groups[k] / maxG * 100) + '%"></span></div></div>';
      }).join("");
      store(KEY, { total: total, rows: rows });
    }
    saved.rows.forEach(addRow);
    totalEl.addEventListener("input", calc);
    $("[data-add]", planner).addEventListener("click", function () { addRow(); calc(); var i = rowsEl.lastChild.querySelector("input"); i.focus(); });
    $("[data-auto]", planner).addEventListener("click", function () {
      var total = parseFloat(totalEl.value) || 0, rowsN = $$(".brow", rowsEl);
      var w = rowsN.map(function (r) { return WEIGHT[r.querySelector("select").value] || 1; });
      var sum = w.reduce(function (a, b) { return a + b; }, 0) || 1;
      rowsN.forEach(function (r, i) { r.querySelector(".amt").value = Math.floor(total * w[i] / sum / 5) * 5; });
      calc();
    });
    $("[data-clear]", planner).addEventListener("click", function () { rowsEl.innerHTML = ""; addRow(); calc(); });
    $("[data-copy]", planner).addEventListener("click", function (e) {
      var rows = data(), txt = "My gift budget (" + money(parseFloat(totalEl.value) || 0) + ")\n" + rows.map(function (r) { return "• " + (r.n || "—") + " (" + r.r + "): " + money(r.a); }).join("\n");
      copy(txt, e.currentTarget);
    });
    calc();
  }

  function copy(text, btn) {
    var done = function () { var t = btn.textContent; btn.textContent = "Copied ✓"; setTimeout(function () { btn.textContent = t; }, 1600); };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
    else fallback();
    function fallback() {
      var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (e) {}
      ta.remove();
    }
  }

  /* =====================================================================
     3. Gift Message Generator
     ===================================================================== */
  var MSG = {
    birthday: {
      heartfelt: ["Happy birthday, {name}. You make every room warmer just by walking into it — I hope this year gives back even a fraction of what you give everyone else.",
        "{name}, another year of you is something worth celebrating properly. Thank you for being exactly who you are. Happy birthday.",
        "To {name} on your birthday: may this year be full of easy mornings, big laughs and every good thing you've been waiting for."],
      witty: ["Happy birthday, {name}! I was going to get you something you needed — then I remembered you already have me.",
        "{name}, you're not getting older, you're becoming a limited edition. Happy birthday!",
        "Cake: check. Gift: check. Pretending you don't look a day older: easy, actually. Happy birthday, {name}!"],
      formal: ["Wishing you a very happy birthday, {name}, and a year ahead filled with health, success and celebration.",
        "Warmest birthday wishes, {name}. May the coming year bring you every success.",
        "Happy birthday, {name}. It's a pleasure to celebrate you today — with best wishes for the year ahead."]
    },
    anniversary: {
      heartfelt: ["{name}, every year with you is my favorite year so far. Here's to all the ones still ahead of us.",
        "Happy anniversary, {name}. Thank you for choosing me — and for choosing me again every single day.",
        "To {name}: you're still the best decision I've ever made. Happy anniversary, my love."],
      witty: ["Happy anniversary, {name}! Still the only person I'd share the last slice of pizza with.",
        "{name}, another year of you putting up with me deserves a gift. Here it is. Happy anniversary!",
        "Happy anniversary to my favorite roommate, travel buddy and snack thief, {name}."],
      formal: ["Congratulations on your anniversary, {name}. Wishing you many more years of happiness together.",
        "Warmest wishes on your anniversary, {name}. May your partnership continue to flourish.",
        "Celebrating you both today, {name}, with heartfelt congratulations on another wonderful year."]
    },
    holiday: {
      heartfelt: ["{name}, the best part of this season is the people in it — and you're right at the top of my list. Happy holidays.",
        "Wishing you a holiday full of warmth, rest and the people you love, {name}. Thank you for being a gift all year long.",
        "Merry everything, {name}. I hope this brings a little extra sparkle to your season."],
      witty: ["{name}, I checked the list twice and you were definitely on the nice side. Mostly. Happy holidays!",
        "Happy holidays, {name}! Please enjoy this gift responsibly — or don't, it's the holidays.",
        "Season's greetings, {name}! Consider this my official bribe for a seat at your holiday table."],
      formal: ["Wishing you and your family a joyful holiday season and a prosperous New Year, {name}.",
        "With warm wishes for a peaceful holiday season and every success in the year ahead, {name}.",
        "Season's greetings, {name}. Thank you for a wonderful year — we look forward to the next."]
    },
    thankyou: {
      heartfelt: ["{name}, thank you doesn't quite cover it, but it's a start. I'm so grateful for everything you did.",
        "Your kindness meant more than you know, {name}. This is a small thank-you for a very big gesture.",
        "Thank you, {name}, for showing up when it mattered most. I won't forget it."],
      witty: ["{name}, you went above and beyond — this gift is my way of saying please never stop.",
        "Thank you, {name}! Consider this a down payment on all the favors I still owe you.",
        "{name}, you're officially in my 'people who are absolutely awesome' file. Thank you!"],
      formal: ["Please accept this with our sincere thanks, {name}. Your support is greatly appreciated.",
        "Thank you, {name}, for your generosity and thoughtfulness. It has not gone unnoticed.",
        "With grateful thanks, {name}, for your time, expertise and care."]
    },
    congrats: {
      heartfelt: ["{name}, I've watched how hard you worked for this, and I couldn't be prouder. Congratulations — you earned every bit of it.",
        "Congratulations, {name}! This is just the beginning of something wonderful.",
        "So proud of you, {name}. Take a moment to enjoy this — you deserve it."],
      witty: ["Congratulations, {name}! Please remember us little people when you're famous.",
        "{name}, you did the thing! Now go celebrate like the overachiever you are.",
        "Big news calls for a big gift. Congratulations, {name} — the bar is officially raised."],
      formal: ["Congratulations on this well-deserved achievement, {name}. Wishing you continued success.",
        "Heartiest congratulations, {name}. Your dedication is an inspiration.",
        "Congratulations, {name}, on reaching this milestone. We look forward to celebrating many more."]
    },
    client: {
      heartfelt: ["{name}, working with you this year has been a genuine pleasure. Thank you for your trust and partnership.",
        "Partners like you, {name}, make the work worth doing. Thank you for a wonderful year together.",
        "{name}, we don't take your loyalty for granted. Here's a small token of our real appreciation."],
      witty: ["{name}, you're the kind of client we'd clone if the science were there. Thank you for everything!",
        "Thank you, {name}! Our team voted, and you won 'Favorite Client' — again.",
        "{name}, this gift has no invoice attached. Promise. Thank you for a brilliant year!"],
      formal: ["Thank you for your continued partnership, {name}. We value your business and look forward to the year ahead.",
        "With sincere appreciation for your trust and collaboration, {name}.",
        "On behalf of our entire team, thank you, {name}, for the privilege of working with you."]
    },
    wedding: {
      heartfelt: ["{name}, watching you two find each other has been a joy. Wishing you a lifetime of love and laughter.",
        "Congratulations, {name}! May your marriage be filled with all the right ingredients: love, patience and plenty of adventure.",
        "To {name} on your wedding day — may today be the first page of your best story yet."],
      witty: ["Congratulations, {name}! Remember: you're a team now, which means you can split the blame.",
        "{name}, here's to love, laughter and finally having someone to open jars for you.",
        "Cheers to the happy couple, {name}! May your Wi-Fi be strong and your arguments short."],
      formal: ["Warmest congratulations on your marriage, {name}. Wishing you both a lifetime of happiness.",
        "With best wishes to you both on your wedding day, {name}, and for the many happy years ahead.",
        "Congratulations, {name}. May your life together be blessed with love and joy."]
    }
  };
  var SIGN = { heartfelt: ["With love,", "All my love,", "Always,"], witty: ["Cheers,", "Your favorite,", "High fives,"], formal: ["Kind regards,", "With best wishes,", "Warm regards,"] };

  var gen = $("[data-msg]");
  if (gen) {
    var out = $(".msg-out", gen), state = { occ: "birthday", tone: "heartfelt", i: 0 };
    $$(".chip", gen).forEach(function (c) {
      c.addEventListener("click", function () {
        var grp = c.closest("[data-group]"), key = grp.getAttribute("data-group");
        $$(".chip", grp).forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        c.setAttribute("aria-pressed", "true"); state[key] = c.getAttribute("data-val"); state.i = 0; write();
      });
    });
    $$("input", gen).forEach(function (i) { i.addEventListener("input", write); });
    function write() {
      var list = MSG[state.occ][state.tone], name = $("#mg-name").value.trim() || "friend", from = $("#mg-from").value.trim();
      var line = list[state.i % list.length].replace(/\{name\}/g, name);
      var sign = SIGN[state.tone][state.i % 3];
      out.innerHTML = esc(line) + (from ? '<span class="sig">' + esc(sign) + "<br>" + esc(from) + "</span>" : '<span class="sig">' + esc(sign) + "</span>");
      out.dataset.text = line + "\n\n" + sign + (from ? "\n" + from : "");
    }
    $("[data-shuffle]", gen).addEventListener("click", function () { state.i++; write(); out.animate && out.animate([{ opacity: 0, transform: "translateY(8px)" }, { opacity: 1, transform: "none" }], { duration: 350 }); });
    $("[data-copy-msg]", gen).addEventListener("click", function (e) { copy(out.dataset.text, e.currentTarget); });
    write();
  }

  /* =====================================================================
     4. Anniversary Gifts by Year
     ===================================================================== */
  var ANNIV = {
    1: ["Paper", "Clocks", "Gold", "Carnation", "A framed print of your first-date location, concert tickets in a keepsake folder, or a bound book of love letters."],
    2: ["Cotton", "China", "Garnet", "Lily of the valley", "Egyptian-cotton robes or bedding, a fine bone-china breakfast set, or a garnet pendant."],
    3: ["Leather", "Crystal & glass", "Pearl", "Sunflower", "A monogrammed leather weekender, a crystal decanter, or pearl studs."],
    4: ["Linen & fruit", "Appliances", "Blue topaz", "Hydrangea", "A linen picnic set with a vineyard visit, a statement espresso machine, or blue topaz jewelry."],
    5: ["Wood", "Silverware", "Sapphire", "Daisy", "A custom wooden keepsake box, an engraved silver serving set, or sapphire cufflinks or earrings."],
    6: ["Iron & sugar", "Wood", "Amethyst", "Calla lily", "A cast-iron cookware set with a cooking class, a dessert tasting, or an amethyst piece."],
    7: ["Wool & copper", "Desk sets", "Onyx", "Freesia", "A cashmere-wool throw, a copper bar set, or an executive desk set."],
    8: ["Bronze", "Linens & lace", "Tourmaline", "Lilac", "A bronze sculpture, luxury bed linens, or tourmaline jewelry."],
    9: ["Pottery", "Leather", "Lapis lazuli", "Bird of paradise", "A pottery class for two, a handmade ceramic set, or a leather watch strap upgrade."],
    10: ["Tin & aluminum", "Diamond jewelry", "Diamond", "Daffodil", "Diamond earrings or an eternity band, or a tin-type portrait session."],
    11: ["Steel", "Fashion jewelry", "Turquoise", "Tulip", "A stainless-steel chef's knife set, a stylish watch, or turquoise jewelry."],
    12: ["Silk & linen", "Pearls", "Jade", "Peony", "Silk pajamas, a pearl strand, or a jade keepsake."],
    13: ["Lace", "Textiles & furs", "Citrine", "Chrysanthemum", "Delicate lace lingerie, a luxe faux-fur throw, or citrine jewelry."],
    14: ["Ivory", "Gold jewelry", "Opal", "Dendrobium orchid", "A gold bracelet, opal earrings, or an orchid with an ivory-toned keepsake."],
    15: ["Crystal", "Watches", "Ruby", "Rose", "A matching pair of watches, a crystal vase with fifteen roses, or ruby jewelry."],
    20: ["China", "Platinum", "Emerald", "Aster", "Platinum jewelry, a heritage china collection, or a trip to the Emerald Isle."],
    25: ["Silver", "Silver", "Silver", "Iris", "Engraved sterling silver, a silver-anniversary vow renewal, or a 25-memories album."],
    30: ["Pearl", "Diamond", "Pearl", "Lily", "A pearl strand, diamond upgrade, or a pearl-diving island vacation."],
    35: ["Coral", "Jade", "Emerald", "Orchid", "A tropical reef trip, coral or jade jewelry, or an emerald piece."],
    40: ["Ruby", "Ruby", "Ruby", "Gladiolus", "Ruby jewelry, a 40-year family celebration dinner, or vintage ruby port."],
    45: ["Sapphire", "Sapphire", "Sapphire", "Blue iris", "Sapphire jewelry or a blue-water cruise for two."],
    50: ["Gold", "Gold", "Gold", "Yellow rose & violet", "Gold jewelry, a golden-anniversary family party, or a professionally restored wedding album."],
    55: ["Emerald", "Emerald", "Emerald", "Calla lily", "Emerald jewelry or a family trip to somewhere green and storied."],
    60: ["Diamond", "Diamond", "Diamond", "Diamond-white rose", "A diamond keepsake, a 60-year family portrait, or a heritage video documentary of your story."]
  };
  var annivRoot = $("[data-anniv]");
  if (annivRoot) {
    var grid = $(".years", annivRoot), card = $("[data-anniv-card]", annivRoot), years = Object.keys(ANNIV).map(Number);
    years.forEach(function (y) {
      var b = document.createElement("button");
      b.type = "button"; b.textContent = y; b.setAttribute("aria-label", "Year " + y);
      if (y % 5 === 0 || y === 1) b.classList.add("milestone");
      b.addEventListener("click", function () { show(y); });
      grid.appendChild(b);
    });
    function nearest(n) { var best = years[0]; years.forEach(function (y) { if (y <= n) best = y; }); return best; }
    function ord(n) { var s = ["th", "st", "nd", "rd"], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }
    function show(y, note) {
      var d = ANNIV[y];
      $$("button", grid).forEach(function (b) { b.classList.toggle("active", +b.textContent === y); });
      card.innerHTML = '<div class="anniv-card"><div class="ac-side"><span class="yr">' + y + '</span><b style="font-family:var(--serif);font-size:1.4rem">' + ord(y) + ' anniversary</b>' +
        (note ? '<p style="color:rgba(255,255,255,.7);margin:10px 0 0;font-size:.92rem">' + esc(note) + "</p>" : "") + '</div><div class="ac-body">' +
        '<div class="anniv-facts"><div><small>Traditional</small><b>' + d[0] + '</b></div><div><small>Modern</small><b>' + d[1] + '</b></div>' +
        '<div><small>Gemstone</small><b>' + d[2] + '</b></div><div><small>Flower</small><b>' + d[3] + '</b></div></div>' +
        '<h3>VIP gift ideas</h3><p style="margin:0;color:var(--muted)">' + d[4] + "</p></div></div>";
    }
    $("[data-anniv-form]", annivRoot).addEventListener("submit", function (e) {
      e.preventDefault();
      var v = $("#an-date").value, n = parseInt($("#an-year").value, 10);
      if (v) {
        var wed = new Date(v + "T00:00:00"), now = new Date();
        var count = now.getFullYear() - wed.getFullYear();
        var thisYear = new Date(now.getFullYear(), wed.getMonth(), wed.getDate());
        if (thisYear < now) count += 1;
        var next = new Date(wed.getFullYear() + count, wed.getMonth(), wed.getDate());
        var days = Math.ceil((next - now) / 864e5);
        if (count < 1) count = 1;
        var y = ANNIV[count] ? count : nearest(count);
        show(y, "Your " + ord(count) + " anniversary is in " + days + " day" + (days === 1 ? "" : "s") + (y !== count ? " — showing the closest listed year." : "."));
      } else if (n > 0) {
        var yy = ANNIV[n] ? n : nearest(n);
        show(yy, yy !== n ? "Year " + n + " isn't a named anniversary — showing year " + yy + "." : "");
      }
    });
    show(1);
  }
})();
