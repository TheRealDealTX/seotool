<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'The price on the bottle tells you little. Enter a few saffron supplements and see what each one really costs per research-matched daily dose, per month and per year.', 'Free Tool');
?>
<div class="wrap layout">
  <div class="prose">
    <section class="tool" id="cost-tool">
      <h2>Compare Saffron Supplement Costs</h2>
      <div class="field" style="max-width:320px"><label for="target">Your daily target dose (mg)</label>
        <select id="target">
          <option value="30">30 mg: mood, PMS</option>
          <option value="28">28 mg: affron® for stress or sleep</option>
          <option value="20">20 mg: eye health</option>
          <option value="176.5">176.5 mg: Satiereal® for appetite</option>
        </select></div>
      <p class="small">Enter each product's current price, capsule count and mg per capsule. Prices on Amazon change daily; check the listing for today's price.</p>
      <div id="rows"></div>
      <p><button type="button" class="btn btn-ghost btn-sm" id="add">+ Add product</button></p>
      <div class="result" id="cost-out" aria-live="polite"></div>
    </section>
    <h2>Why Cost per Effective Dose Matters</h2>
    <p>A 240-capsule bottle of 88.5 mg saffron looks like a bargain, and often is. But if your goal is a 30 mg crocin-standardized dose, comparing it with a 30 mg product means comparing different things. This calculator normalizes everything to the number of capsules you would take to reach your target, rounded to whole capsules, because that is what you'll actually swallow.</p>
    <p>Remember that the cheapest effective product is only a bargain if it's genuine. Weigh price against the extract details in our <a href="/how-to-choose-a-saffron-supplement/">buying checklist</a>.</p>
    <?= aff_note() ?>
    <h3>Check today's prices</h3>
    <ul>
      <?php foreach (['nutricost', 'nootropics-depot', 'vinatura-affron', 'life-extension', 'source-naturals', 'now-foods'] as $cid) { $cp = PRODUCTS[$cid]; ?>
      <li><?= amz($cp['asin'], e($cp['name'])) ?>: <?= e($cp['dose_label']) ?></li>
      <?php } ?>
    </ul>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
<script>
(function(){
  var rows=document.getElementById('rows'), out=document.getElementById('cost-out'), target=document.getElementById('target');
  var seed=[['Product A (30 mg × 60)',29.99,60,30],['Product B (88.5 mg × 240)',19.95,240,88.5],['Product C (15 mg × 30)',5.99,30,15]];
  function add(v){
    v=v||['',0,60,30];
    var d=document.createElement('div');d.className='cost-row';
    d.innerHTML='<div class="field" style="margin:0"><label>Name</label><input type="text" class="n" value="'+v[0].replace(/"/g,'&quot;')+'" placeholder="Brand / product"></div>'+
      '<div class="field" style="margin:0"><label>Price ($)</label><input type="number" class="p" min="0" step="0.01" value="'+v[1]+'"></div>'+
      '<div class="field" style="margin:0"><label>Capsules</label><input type="number" class="c" min="1" value="'+v[2]+'"></div>'+
      '<div class="field" style="margin:0"><label>mg / capsule</label><input type="number" class="m" min="1" step="0.5" value="'+v[3]+'"></div>'+
      '<div class="field" style="margin:0"><label>&nbsp;</label><span class="small"></span></div>'+
      '<button type="button" aria-label="Remove product" title="Remove">×</button>';
    d.querySelector('button').onclick=function(){d.remove();calc();};
    rows.appendChild(d);
  }
  function calc(){
    var t=parseFloat(target.value), res=[];
    rows.querySelectorAll('.cost-row').forEach(function(r,k){
      var n=r.querySelector('.n').value||('Product '+(k+1)), p=+r.querySelector('.p').value, c=+r.querySelector('.c').value, m=+r.querySelector('.m').value;
      if(!(p>0&&c>0&&m>0)) return;
      var caps=Math.max(1,Math.round(t/m)), perDay=p/c*caps, days=Math.floor(c/caps);
      r.querySelector('.small').textContent=caps+'/day';
      res.push({n:n,day:perDay,month:perDay*30,year:perDay*365,days:days,caps:caps,mg:caps*m});
    });
    if(!res.length){out.innerHTML='<p>Add at least one product with a price, count and strength.</p>';return;}
    res.sort(function(a,b){return a.day-b.day;});
    var max=res[res.length-1].month;
    var h='<h3>Cheapest per effective dose: '+esc(res[0].n)+'</h3><div class="table-wrap"><table><thead><tr><th>Product</th><th>Capsules/day</th><th>mg/day</th><th>Per day</th><th>Per month</th><th>Per year</th><th>Bottle lasts</th></tr></thead><tbody>';
    res.forEach(function(x,k){h+='<tr><td>'+(k===0?'🏆 ':'')+esc(x.n)+'<div class="ev-bar" style="margin-top:6px"><i style="width:'+(x.month/max*100)+'%"></i></div></td><td>'+x.caps+'</td><td>'+(+x.mg.toFixed(1))+'</td><td>$'+x.day.toFixed(2)+'</td><td>$'+x.month.toFixed(2)+'</td><td>$'+x.year.toFixed(0)+'</td><td>'+x.days+' days</td></tr>';});
    h+='</tbody></table></div>';
    var off=res.filter(function(x){return x.mg>t*1.5||x.mg<t*0.67;});
    if(off.length) h+='<div class="flag flag-amber">'+off.map(function(x){return esc(x.n);}).join(', ')+': whole-capsule dosing lands well away from your '+t+' mg target, so the comparison is approximate.</div>';
    out.innerHTML=h;
  }
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  seed.forEach(add);
  document.getElementById('add').onclick=function(){add();calc();};
  document.getElementById('cost-tool').addEventListener('input',calc);
  target.addEventListener('change',calc);
  calc();
})();
</script>
