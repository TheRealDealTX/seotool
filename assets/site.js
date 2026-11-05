(function(){
  var R = window.SBA_RATES; if(!R) return;
  function cap(amount, type){
    var list = type==="fixed" ? R.fixed_caps : R.variable_caps;
    for (var i=0;i<list.length;i++){ if(amount<=list[i].max) return {i:i, spread:list[i].spread, rate:R.prime+list[i].spread}; }
    var l=list[list.length-1]; return {i:list.length-1, spread:l.spread, rate:R.prime+l.spread};
  }
  function money(n){ return "$"+Math.round(n).toLocaleString("en-US"); }
  function pct(n){ return n.toFixed(2)+"%"; }
  function payment(P, rate, years){
    var r=rate/100/12, n=years*12; if(!r) return P/n;
    return P*r/(1-Math.pow(1+r,-n));
  }
  // amount slider uses a log-ish scale so small loans are reachable
  var steps=[10000,25000,40000,50000,75000,100000,150000,200000,250000,300000,350000,500000,750000,1000000,1500000,2000000,3000000,4000000,5000000];

  var ladder=document.getElementById("ladder");
  if(ladder){
    var type="variable", slider=ladder.querySelector("input[type=range]"), out=ladder.querySelector("output");
    var fig=ladder.querySelector(".cap-figure"), capt=ladder.querySelector(".cap-caption"), rungs=ladder.querySelector(".rungs");
    function drawRungs(){
      var list = type==="fixed"?R.fixed_caps:R.variable_caps, maxRate=R.prime+8;
      rungs.innerHTML = list.map(function(c){
        var total=R.prime+c.spread;
        return '<li class="rung"><span>'+c.band+'</span><span class="bar" aria-hidden="true"><i class="base" style="width:'+(R.prime/maxRate*100)+'%"></i><i class="spread" style="width:'+(c.spread/maxRate*100)+'%"></i></span><b class="num">'+pct(total)+'</b></li>';
      }).join("");
    }
    function update(){
      var amt=steps[+slider.value]; out.textContent=money(amt);
      var c=cap(amt,type);
      fig.textContent=pct(c.rate);
      capt.textContent="Highest "+type+" rate a lender can charge on a "+money(amt)+" SBA 7(a) loan: prime "+pct(R.prime)+" plus "+c.spread.toFixed(1)+" points.";
      [].forEach.call(rungs.children,function(li,i){ li.classList.toggle("on", i===c.i); });
    }
    ladder.querySelectorAll(".toggle button").forEach(function(b){
      b.addEventListener("click",function(){
        type=b.dataset.type;
        ladder.querySelectorAll(".toggle button").forEach(function(x){x.setAttribute("aria-pressed", x===b?"true":"false");});
        drawRungs(); update();
      });
    });
    slider.max=steps.length-1; slider.value=steps.indexOf(500000);
    slider.addEventListener("input",update); drawRungs(); update();
  }

  var calc=document.getElementById("calc");
  if(calc){
    var f=function(id){return calc.querySelector("#"+id);};
    function run(){
      var amt=Math.max(0,+f("c-amt").value||0), yrs=Math.max(1,+f("c-yrs").value||10), typ=f("c-type").value;
      var c=cap(amt,typ), rateIn=f("c-rate");
      if(!rateIn.dataset.touched){ rateIn.value=c.rate.toFixed(2); }
      var rate=+rateIn.value||c.rate, pm=payment(amt,rate,yrs);
      f("o-cap").textContent=pct(c.rate);
      f("o-pay").textContent=money(pm);
      f("o-int").textContent=money(pm*yrs*12-amt);
      f("o-note").textContent = rate>c.rate+1e-9 ? "That rate is above the SBA maximum for this loan size. A lender can't charge it on a 7(a) loan." : "";
    }
    calc.addEventListener("input",function(e){ if(e.target.id==="c-rate") e.target.dataset.touched="1"; if(e.target.id==="c-amt"||e.target.id==="c-type"){ delete f("c-rate").dataset.touched; } run(); });
    run();
  }

  var q=document.getElementById("lender-q");
  if(q){
    var items=document.querySelectorAll("[data-name]"), count=document.getElementById("lender-count");
    q.addEventListener("input",function(){
      var v=q.value.trim().toLowerCase(), n=0;
      items.forEach(function(li){ var hit=!v||li.dataset.name.indexOf(v)>-1; li.hidden=!hit; if(hit)n++; });
      document.querySelectorAll("[data-state-group]").forEach(function(g){ g.hidden = !g.querySelector("[data-name]:not([hidden])"); });
      count.textContent = n===1 ? "1 lender" : n+" lenders";
    });
  }
})();
/* track lender-match CTA clicks */
document.addEventListener("click",function(ev){var a=ev.target.closest&&ev.target.closest("a.btn-match");if(a&&window.gtag){try{gtag("event","lender_match_cta",{cta:a.getAttribute("data-cta")||"aside",page:location.pathname});}catch(e){}}});
