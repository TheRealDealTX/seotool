<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Tick anything that applies to you. The checker flags what to discuss with your doctor or pharmacist before you start a saffron supplement. It runs entirely in your browser and nothing is sent or stored.', 'Free Tool');
?>
<div class="wrap layout">
  <div class="prose">
    <section class="tool" id="safe-tool">
      <h2>Saffron Safety Checker</h2>
      <div class="field"><fieldset><legend>Life stage &amp; conditions</legend><div class="chips">
        <label class="chip"><input type="checkbox" value="preg"><span>Pregnant / trying to conceive</span></label>
        <label class="chip"><input type="checkbox" value="bf"><span>Breastfeeding</span></label>
        <label class="chip"><input type="checkbox" value="bipolar"><span>Bipolar disorder</span></label>
        <label class="chip"><input type="checkbox" value="lowbp"><span>Low blood pressure</span></label>
        <label class="chip"><input type="checkbox" value="bleed"><span>Bleeding disorder</span></label>
        <label class="chip"><input type="checkbox" value="surgery"><span>Surgery in next 2 weeks</span></label>
        <label class="chip"><input type="checkbox" value="under18"><span>Under 18</span></label>
        <label class="chip"><input type="checkbox" value="allergy"><span>Pollen allergies (olive, ryegrass, saltwort)</span></label>
        <label class="chip"><input type="checkbox" value="severe"><span>Severe depression / suicidal thoughts</span></label>
      </div></fieldset></div>
      <div class="field"><fieldset><legend>Medications &amp; supplements</legend><div class="chips">
        <label class="chip"><input type="checkbox" value="ssri"><span>Antidepressant (SSRI/SNRI/MAOI/TCA)</span></label>
        <label class="chip"><input type="checkbox" value="thinner"><span>Blood thinner / aspirin</span></label>
        <label class="chip"><input type="checkbox" value="bp"><span>Blood-pressure medication</span></label>
        <label class="chip"><input type="checkbox" value="diabetes"><span>Diabetes medication</span></label>
        <label class="chip"><input type="checkbox" value="sedative"><span>Sedative / sleeping pill</span></label>
        <label class="chip"><input type="checkbox" value="sero"><span>5-HTP, St John's wort or SAMe</span></label>
        <label class="chip"><input type="checkbox" value="lithium"><span>Lithium or mood stabilizer</span></label>
      </div></fieldset></div>
      <div class="field" style="max-width:320px"><label for="sdose">Planned daily dose</label>
        <select id="sdose"><option value="30">Up to 30 mg (or 176 mg Satiereal®)</option><option value="100">31–100 mg</option><option value="200">More than 100 mg</option></select></div>
      <div class="result" id="safe-out" aria-live="polite"></div>
    </section>
    <p class="note note-med"><strong>This is not a diagnosis.</strong> The checker summarizes cautions from published research and standard herbal references. Only a healthcare professional who knows your history can tell you whether saffron is right for you. See the <a href="/saffron-side-effects/">full side-effects guide</a>.</p>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
<script>
(function(){
  var M={
    preg:['red','Pregnancy','High doses of saffron may stimulate uterine contractions. Avoid saffron supplements unless your obstetrician approves. Culinary amounts are generally considered fine.'],
    bf:['amber','Breastfeeding','There is too little safety data on saffron supplements while breastfeeding. Stick to food amounts unless your doctor advises otherwise.'],
    bipolar:['red','Bipolar disorder','Saffron\'s antidepressant-like activity could, in theory, trigger mania or hypomania. Only use it under your psychiatrist\'s guidance.'],
    lowbp:['amber','Low blood pressure','Saffron may lower blood pressure slightly. Monitor for dizziness.'],
    bleed:['red','Bleeding disorder','High doses of saffron may affect platelets. Discuss with your hematologist first.'],
    surgery:['amber','Upcoming surgery','Stop saffron supplements at least 2 weeks before surgery because of possible bleeding and blood-pressure effects.'],
    under18:['amber','Under 18','Only one supervised trial has included teenagers. Use only under a doctor\'s guidance.'],
    allergy:['amber','Pollen allergies','People allergic to Olea (olive), Lolium (ryegrass) or Salsola pollen may be more likely to react to saffron. Watch for itching, swelling or breathing problems.'],
    severe:['red','Severe depression','Please speak to a doctor or call/text 988 (US) now. Saffron has only been studied for mild-to-moderate symptoms and is not a substitute for care.'],
    ssri:['red','Antidepressants','Possible additive serotonin effects. Some trials combined saffron with SSRIs under supervision, so only do this with your prescriber\'s approval. Know the signs of serotonin syndrome: agitation, fast heartbeat, fever, tremor.'],
    thinner:['red','Blood thinners','Saffron may increase bleeding risk, especially at higher doses. Ask your doctor; you may need closer monitoring.'],
    bp:['amber','Blood-pressure medication','Saffron may add to the blood-pressure-lowering effect. Check your readings when you start.'],
    diabetes:['amber','Diabetes medication','Saffron may slightly lower blood sugar. Monitor your glucose more closely for the first few weeks.'],
    sedative:['amber','Sedatives','Possible additive drowsiness. Avoid driving until you know how you react.'],
    sero:['red','Other serotonergic supplements','Stacking saffron with 5-HTP, St John\'s wort or SAMe may increase serotonin effects. Avoid combining without medical advice.'],
    lithium:['amber','Mood stabilizers','There are no clear interaction data, but because of saffron\'s mood effects, your psychiatrist should be involved.']
  };
  var tool=document.getElementById('safe-tool'), out=document.getElementById('safe-out'), dose=document.getElementById('sdose');
  function run(){
    var sel=[].slice.call(tool.querySelectorAll('input:checked')).map(function(x){return x.value;});
    var red=sel.filter(function(k){return M[k][0]==='red';}), amber=sel.filter(function(k){return M[k][0]==='amber';});
    var d=+dose.value, h;
    if(d===200) red.push('_dose'); else if(d===100) amber.push('_dose');
    M._dose=d===200?['red','Dose above 100 mg/day','Doses above 100 mg/day go beyond the range used safely in trials. Minor blood changes were seen at 400 mg/day. Most goals need only 20–30 mg.']:['amber','Dose 31–100 mg/day','This is above the 20–30 mg used in most trials. Higher doses have not been shown to work better.'];
    if(red.length) h='<h3>🔴 Talk to your doctor before taking saffron</h3><p>We found '+red.length+' important caution'+(red.length>1?'s':'')+'.</p>';
    else if(amber.length) h='<h3>🟡 Probably fine, but check with a professional</h3><p>A few things are worth mentioning to your pharmacist.</p>';
    else h='<h3>🟢 No common cautions flagged</h3><p>Based on your answers, saffron at research doses (20–30 mg/day) is generally well tolerated. Start with food and watch for mild nausea or headache.</p><p><a class="btn" href="/tools/saffron-dosage-calculator/">Calculate your dose</a> &nbsp; <a href="/best-saffron-supplements/">See top-rated products</a></p>';
    red.concat(amber).forEach(function(k){var m=M[k];h+='<div class="flag flag-'+m[0]+'"><strong>'+m[1]+':</strong> '+m[2]+'</div>';});
    if(red.length||amber.length) h+='<p class="small">Tip: screenshot or print this page and take it to your appointment.</p><p><button class="btn btn-ghost btn-sm" type="button" onclick="window.print()">Print results</button></p>';
    out.innerHTML=h;
  }
  tool.addEventListener('change',run); run();
})();
</script>
