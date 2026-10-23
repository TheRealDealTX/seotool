<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Five quick questions. We\'ll match you with the saffron extract, dose and product that best fits your goal, preferences and budget.', 'Free Tool');
?>
<div class="wrap layout">
  <div class="prose">
    <section class="tool" id="quiz">
      <div class="progress" aria-hidden="true"><i id="qbar"></i></div>
      <div class="quiz-step on" data-q="goal">
        <h2>1. What's your main reason for trying saffron?</h2>
        <div class="opts">
          <button class="opt" data-v="mood">Low mood or emotional balance<small>Feeling flat, down or unmotivated</small></button>
          <button class="opt" data-v="stress">Stress and everyday anxiety<small>Tense, wired, can't switch off</small></button>
          <button class="opt" data-v="sleep">Better sleep<small>Unrefreshing or restless nights</small></button>
          <button class="opt" data-v="eyes">Eye health<small>Supporting macular health with age</small></button>
          <button class="opt" data-v="appetite">Snacking and cravings<small>Grazing between meals</small></button>
          <button class="opt" data-v="pms">PMS symptoms<small>Monthly mood swings and irritability</small></button>
        </div>
      </div>
      <div class="quiz-step" data-q="evidence">
        <h2>2. How important is clinical research behind the exact extract?</h2>
        <div class="opts">
          <button class="opt" data-v="high">Very important<small>I want a branded extract with its own trials</small></button>
          <button class="opt" data-v="mid">Somewhat<small>Disclosed standardization is enough</small></button>
          <button class="opt" data-v="low">Not very<small>I mainly want good value</small></button>
        </div>
      </div>
      <div class="quiz-step" data-q="form">
        <h2>3. Any preference on format?</h2>
        <div class="opts">
          <button class="opt" data-v="any">Capsules are fine</button>
          <button class="opt" data-v="soft">Easy to swallow (softgel)</button>
          <button class="opt" data-v="vegan">Must be vegan</button>
          <button class="opt" data-v="blend">I'd like a combo formula (e.g. with magnesium)</button>
        </div>
      </div>
      <div class="quiz-step" data-q="budget">
        <h2>4. What's your budget?</h2>
        <div class="opts">
          <button class="opt" data-v="low">As low as possible</button>
          <button class="opt" data-v="mid">Mid-range is fine</button>
          <button class="opt" data-v="high">I'll pay for premium quality</button>
        </div>
      </div>
      <div class="quiz-step" data-q="meds">
        <h2>5. Do you take antidepressants, blood thinners or blood-pressure medication, or are you pregnant?</h2>
        <div class="opts">
          <button class="opt" data-v="no">No</button>
          <button class="opt" data-v="yes">Yes</button>
          <button class="opt" data-v="unsure">Not sure</button>
        </div>
      </div>
      <div class="quiz-step" data-q="result"><div id="qres" aria-live="polite"></div>
        <p style="margin-top:18px"><button class="btn btn-ghost" id="qreset" type="button">Retake the quiz</button></p>
      </div>
    </section>
    <h2>How We Match You</h2>
    <p>Each product in our <a href="/best-saffron-supplements/">best saffron supplements</a> review is tagged with the goals its dose and extract suit, whether it uses a branded or standardized extract, its format, and our editorial score. The quiz weights those against your answers. It always prioritizes products whose dose matches the research for your goal.</p>
    <?= aff_note() ?>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
<script>
(function(){
  var P=<?= products_json() ?>;
  var price={'nutricost':1,'source-naturals':1,'now-foods':1,'zazzee':2,'nootropics-depot':2,'vinatura-affron':2,'pink-stork':2,'sports-research':3,'life-extension':3,'affron-magnesium':2,'thorne':3,'brainmd':3};
  var branded={'vinatura-affron':1,'life-extension':1,'affron-magnesium':1};
  var soft={'sports-research':1}, blend={'affron-magnesium':1,'brainmd':1};
  var doseFor={mood:'30 mg/day (15 mg twice daily) or 28 mg affron®',stress:'28 mg/day',sleep:'28 mg/day (14 mg twice, or evening)',eyes:'20 mg/day',appetite:'176.5 mg/day Satiereal® (88 mg before 2 meals)',pms:'30 mg/day (15 mg twice daily)'};
  var steps=[].slice.call(document.querySelectorAll('.quiz-step')), A={}, i=0, bar=document.getElementById('qbar');
  function show(n){steps.forEach(function(s,k){s.classList.toggle('on',k===n);});bar.style.width=Math.min(100,(n+1)*100/6)+'%';var first=i===n;i=n;var b=steps[n].querySelector('button');if(b&&!first)b.focus({preventScroll:true});}
  steps.forEach(function(s){s.addEventListener('click',function(ev){var b=ev.target.closest('.opt');if(!b)return;A[s.dataset.q]=b.dataset.v;if(s.dataset.q==='meds'){result();show(5);}else show(i+1);});});
  document.getElementById('qreset').addEventListener('click',function(){A={};show(0);});
  function score(p){
    var s=p.score*2;
    if(p.goals.indexOf(A.goal)>-1) s+=12; else s-=15;
    if(A.goal==='appetite'&&p.id==='life-extension') s+=10;
    if((A.goal==='stress'||A.goal==='sleep')&&p.id.indexOf('affron')>-1) s+=6;
    if(A.goal==='eyes'&&p.std) s+=3;
    if(A.evidence==='high') s+=branded[p.id]?8:(p.std?2:-4);
    if(A.evidence==='mid') s+=p.std?4:-2;
    if(A.evidence==='low') s+=(4-price[p.id])*2;
    if(A.form==='soft') s+=soft[p.id]?10:0;
    if(A.form==='vegan') s+=p.vegan?4:-20;
    if(A.form==='blend') s+=blend[p.id]?10:0; else if(blend[p.id]) s-=3;
    if(A.budget==='low') s+=(3-price[p.id])*4;
    if(A.budget==='high') s+=price[p.id]*2;
    return s;
  }
  function result(){
    var r=P.map(function(p){return {p:p,s:score(p)};}).sort(function(a,b){return b.s-a.s;});
    var top=r[0].p, alt=r.slice(1,3).map(function(x){return x.p;});
    var h='<p class="kicker">Your match</p><h2 style="margin-top:0">'+top.name+'</h2><p><span class="badge">'+top.badge+'</span> Editorial score <b>'+top.score.toFixed(1)+'/10</b></p>'+
      '<div class="kv"><div><span>Your research dose</span><b style="font-size:1.05rem">'+doseFor[A.goal]+'</b></div><div><span>Why this one</span><b style="font-size:1rem">'+(top.goals.indexOf(A.goal)>-1?'Dose and extract suit your goal':'Best overall fit for your answers')+'</b></div></div>'+
      '<p><a class="btn btn-amz" href="'+top.url+'" rel="sponsored nofollow noopener" target="_blank">Check Price on Amazon &rarr;</a> &nbsp; <a href="/best-saffron-supplements/#'+top.id+'">Read our review</a></p>';
    if(A.meds!=='no') h+='<div class="flag flag-red"><strong>Talk to your doctor first.</strong> Saffron may interact with antidepressants, blood thinners and blood-pressure drugs, and high doses aren\'t advised in pregnancy. <a href="/tools/saffron-safety-checker/">Run the safety checker</a>.</div>';
    h+='<h3>Also worth considering</h3><ul>';
    alt.forEach(function(p){h+='<li><a href="'+p.url+'" rel="sponsored nofollow noopener" target="_blank">'+p.name+'</a> <span class="small">('+p.badge+')</span></li>';});
    h+='</ul><p class="small">Next: work out exact capsule timing with the <a href="/tools/saffron-dosage-calculator/">dosage calculator</a>.</p>';
    document.getElementById('qres').innerHTML=h;
  }
  show(0);
})();
</script>
