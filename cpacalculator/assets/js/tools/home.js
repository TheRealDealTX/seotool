(function () {
  var form = document.getElementById('home-calc');
  if (!form) return;
  var C = window.CPA;
  C.bind(form, function (f) {
    var s = C.str(f, 'status');
    var r = C.estimate({ status: s, wages: C.val(f, 'income'), seIncome: C.val(f, 'side') });
    var tax = r.incomeTax + r.se.total + r.niit;
    var take = Math.max(0, r.gross - tax - r.fica.total);
    C.big(form, 'tax', tax);
    C.set(form, 'eff', C.pct(r.gross ? tax / r.gross : 0));
    C.set(form, 'marg', Math.round(r.marginal * 100) + '%');
    C.set(form, 'take', C.money(take));
  });
})();
