<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Pick your goal and enter the milligrams per capsule on your bottle. The calculator returns a research-matched daily dose, how many capsules to take, when to take them and how long to wait for results.', 'Free Tool');
?>
<div class="wrap layout">
  <div class="prose">
    <section class="tool" id="dose-tool">
      <h2>Calculate Your Saffron Dose</h2>
      <div class="field"><fieldset><legend>1. What is your main goal?</legend>
        <div class="chips" id="goal">
          <label class="chip"><input type="radio" name="goal" value="mood" checked><span>Mood</span></label>
          <label class="chip"><input type="radio" name="goal" value="stress"><span>Stress / anxiety</span></label>
          <label class="chip"><input type="radio" name="goal" value="sleep"><span>Sleep</span></label>
          <label class="chip"><input type="radio" name="goal" value="eyes"><span>Eye health</span></label>
          <label class="chip"><input type="radio" name="goal" value="pms"><span>PMS</span></label>
          <label class="chip"><input type="radio" name="goal" value="appetite"><span>Appetite</span></label>
          <label class="chip"><input type="radio" name="goal" value="libido"><span>Sexual function</span></label>
        </div></fieldset></div>
      <div class="row">
        <div class="field"><label for="ext">2. Extract type on the label</label>
          <select id="ext">
            <option value="std">Standardized extract (crocin/safranal %)</option>
            <option value="affron">affron®</option>
            <option value="satiereal">Satiereal®</option>
            <option value="generic">Generic / not stated</option>
          </select></div>
        <div class="field"><label for="mg">3. mg of saffron per capsule</label>
          <input type="number" id="mg" min="1" max="1000" step="0.5" value="30" inputmode="decimal"></div>
        <div class="field"><label for="sens">4. Sensitive to supplements?</label>
          <select id="sens"><option value="0">No</option><option value="1">Yes, start low</option></select></div>
      </div>
      <div class="result" id="dose-out" aria-live="polite"></div>
    </section>

    <h2>How the Calculator Works</h2>
    <p>Each goal maps to the daily dose and schedule used in published human trials, for example 30 mg/day split twice daily for mood (Hausenblas 2013) or 20 mg/day for macular health (Falsini 2010). The calculator divides that target by your capsule strength and rounds to the nearest practical count. If rounding pushes you more than 50% above the studied dose, it suggests a lower-strength product instead.</p>
    <p>If you choose "start low," it halves the dose for the first week, a common way to check tolerance. For the reasoning behind each number, see our <a href="/saffron-dosage/">saffron dosage guide</a>.</p>
    <p class="note">The output is general information, not a prescription. Check with your doctor, especially if you take medication. Our <a href="/tools/saffron-safety-checker/">safety checker</a> can flag interactions to discuss.</p>
    <?= aff_note() ?>
    <?= product_inline('nootropics-depot', '30 mg per capsule: one a day covers mood, stress and sleep targets.') ?>
    <?= product_inline('source-naturals', '15 mg tablets: ideal for the twice-daily protocols.') ?>
    <?= faq_block([
      ['How do I calculate my saffron dose?', '<p>Find the dose used in trials for your goal (e.g. 30 mg/day for mood), then divide by the mg per capsule on your product. The calculator does this for you and adds timing.</p>'],
      ['What if my capsule is 88.5 mg?', '<p>For Satiereal® appetite protocols, take one 88.5 mg capsule twice daily. For mood with a generic 88.5 mg extract, one capsule a day is more than the 30 mg used in trials, but strength varies. Consider a 28–30 mg standardized product instead.</p>'],
    ]) ?>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
<script>
(function(){
  var G={
    mood:{t:30,split:2,when:'Morning and evening with food',wait:'4–8 weeks',page:'/saffron-for-depression-and-mood/',label:'low mood'},
    stress:{t:28,split:1,when:'With breakfast, or split morning/evening',wait:'4–8 weeks',page:'/saffron-benefits/#anxiety',label:'stress'},
    sleep:{t:28,split:2,when:'Morning + about 1 hour before bed (or all in the evening)',wait:'2–4 weeks',page:'/saffron-for-sleep/',label:'sleep'},
    eyes:{t:20,split:1,when:'Once daily with a meal',wait:'About 3 months',page:'/saffron-for-eye-health/',label:'eye health'},
    pms:{t:30,split:2,when:'Morning and evening, every day of the cycle',wait:'2 menstrual cycles',page:'/saffron-for-pms/',label:'PMS'},
    appetite:{t:176.5,split:2,when:'Before lunch and before dinner',wait:'4–8 weeks',page:'/saffron-for-weight-loss/',label:'appetite'},
    libido:{t:30,split:2,when:'Morning and evening',wait:'About 4 weeks',page:'/saffron-benefits/#libido',label:'sexual function'}
  };
  var out=document.getElementById('dose-out'), mg=document.getElementById('mg'), ext=document.getElementById('ext'), sens=document.getElementById('sens');
  function goal(){return document.querySelector('input[name=goal]:checked').value;}
  function fmt(n){return (Math.round(n*10)/10).toString();}
  function calc(){
    var g=G[goal()], m=parseFloat(mg.value), e=ext.value, warn=[];
    if(!m||m<=0){out.innerHTML='<p>Enter the milligrams per capsule from your label.</p>';return;}
    var target=g.t;
    if(goal()==='appetite'&&e!=='satiereal') warn.push('The appetite research used Satiereal® specifically. Results with other extracts are unknown.');
    if(goal()!=='appetite'&&e==='satiereal'){warn.push('Satiereal® was studied at 176.5 mg/day for appetite. For other goals there is no Satiereal®-specific dose, so we use the generic 30 mg target as a cautious guide.');}
    if(e==='affron'&&(goal()==='mood'||goal()==='pms'||goal()==='libido')) target=28;
    if(e==='generic') warn.push('Your product doesn\'t state its standardization, so its real strength is unknown. A standardized or branded extract makes dosing far more reliable.');
    var caps=Math.max(1,Math.round(target/m)), actual=caps*m, ratio=actual/target;
    if(ratio>1.5) warn.push('Your capsule is strong for this goal: one capsule gives '+fmt(actual)+' mg vs the studied '+fmt(target)+' mg. Consider a lower-strength product.');
    if(ratio<0.67) warn.push('Even at '+caps+' capsules you\'d only reach '+fmt(actual)+' mg.');
    if(actual>100) warn.push('This exceeds 100 mg/day. Only go above that range with medical advice.');
    var perDose = g.split===2&&caps>=2 ? Math.round(caps/2*10)/10 : caps;
    var sched = g.split===2&&caps>=2 ? perDose+' capsule'+(perDose>1?'s':'')+' twice a day' : caps+' capsule'+(caps>1?'s':'')+' once a day';
    var h='<h3>Your saffron plan for '+g.label+'</h3><div class="big">'+fmt(target)+' mg/day</div><div class="kv">'+
      '<div><span>Capsules</span><b>'+sched+'</b></div><div><span>You\'ll get</span><b>'+fmt(actual)+' mg/day</b></div>'+
      '<div><span>When</span><b style="font-size:1rem">'+g.when+'</b></div><div><span>Judge results after</span><b>'+g.wait+'</b></div></div>';
    if(sens.value==='1') h+='<p><strong>Week 1:</strong> take about half ('+fmt(actual/2)+' mg/day, e.g. one capsule a day or every other day), then step up to the full plan if you feel fine.</p>';
    warn.forEach(function(w){h+='<div class="flag flag-amber">'+w+'</div>';});
    h+='<p style="margin:12px 0 0"><a href="'+g.page+'">Read the research on saffron for '+g.label+' &rarr;</a></p>';
    out.innerHTML=h;
  }
  document.getElementById('dose-tool').addEventListener('input',calc);
  document.getElementById('dose-tool').addEventListener('change',calc);
  ext.addEventListener('change',function(){ if(ext.value==='satiereal'&&parseFloat(mg.value)<60) mg.value=88.5; if(ext.value==='affron'&&parseFloat(mg.value)>40) mg.value=28; calc(); });
  calc();
})();
</script>
