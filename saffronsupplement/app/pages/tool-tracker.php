<?php defined('SS_APP') || exit;
echo page_hero($GLOBALS['ss_route'], 'Saffron works gradually, and memory is unreliable. Log your mood, sleep and energy each day for up to 12 weeks and watch the trend on a chart. Everything is saved privately in your own browser.', 'Free Tool');
?>
<div class="wrap layout">
  <div class="prose">
    <section class="tool" id="trk">
      <h2>Today's Check-In</h2>
      <div class="row">
        <div class="field"><label for="tdate">Date</label><input type="date" id="tdate"></div>
        <div class="field"><label for="tdose">Saffron taken today (mg)</label><input type="number" id="tdose" min="0" step="0.5" value="30"></div>
      </div>
      <div class="field"><label for="tmood">Mood: <b id="vmood">5</b>/10</label><input type="range" id="tmood" min="1" max="10" value="5"><div class="scale"><span>Very low</span><span>Great</span></div></div>
      <div class="field"><label for="tsleep">Sleep quality: <b id="vsleep">5</b>/10</label><input type="range" id="tsleep" min="1" max="10" value="5"><div class="scale"><span>Terrible</span><span>Excellent</span></div></div>
      <div class="field"><label for="tenergy">Energy: <b id="venergy">5</b>/10</label><input type="range" id="tenergy" min="1" max="10" value="5"><div class="scale"><span>Drained</span><span>Energized</span></div></div>
      <div class="field"><label for="tnote">Notes (optional)</label><input type="text" id="tnote" maxlength="140" placeholder="e.g. stressful day, slept 6 h, mild nausea"></div>
      <p><button class="btn" type="button" id="tsave">Save Today's Entry</button> <span id="tmsg" class="small" aria-live="polite"></span></p>

      <h2>Your Progress</h2>
      <div id="tsum" class="kv"></div>
      <canvas id="tchart" class="chart" width="800" height="260" role="img" aria-label="Line chart of mood, sleep and energy scores over time"></canvas>
      <p class="small"><span style="color:#5b2a86">■</span> Mood &nbsp; <span style="color:#e8461f">■</span> Sleep &nbsp; <span style="color:#3f7d4e">■</span> Energy &nbsp;·&nbsp; lines show 7-day averages</p>
      <div class="table-wrap"><table class="log-table"><thead><tr><th>Date</th><th>Dose</th><th>Mood</th><th>Sleep</th><th>Energy</th><th>Notes</th><th></th></tr></thead><tbody id="tlog"></tbody></table></div>
      <p><button class="btn btn-ghost btn-sm" type="button" id="tcsv">Download CSV</button> <button class="btn btn-ghost btn-sm" type="button" id="tdemo">Load demo data</button> <button class="btn btn-ghost btn-sm" type="button" id="tclear">Clear all</button></p>
    </section>

    <h2>How to Use the Tracker</h2>
    <ol class="steps">
      <li><strong>Log a baseline.</strong> Ideally record 5–7 days <em>before</em> starting saffron so you have something to compare against.</li>
      <li><strong>Check in at the same time daily</strong>, for example each evening, rating the whole day.</li>
      <li><strong>Keep your dose steady.</strong> Changing dose or timing makes trends harder to read.</li>
      <li><strong>Review at weeks 4, 8 and 12.</strong> Compare the 7-day averages with your baseline. A rise of 1–2 points is meaningful.</li>
    </ol>
    <p>Your data is stored only in this browser (localStorage). It isn't sent to Saffron Supplement or anyone else, and clearing your browser data erases it, so download the CSV now and then as a backup.</p>
    <?= med_note() ?>
  </div>
  <?php require __DIR__ . '/_sidebar.php'; ?>
</div>
<script>
(function(){
  var KEY='ss_tracker_v1', mem=[];
  function load(){try{return JSON.parse(localStorage.getItem(KEY))||[];}catch(e){return mem;}}
  function save(d){mem=d;try{localStorage.setItem(KEY,JSON.stringify(d));}catch(e){}}
  var $=function(id){return document.getElementById(id);};
  var today=new Date(); $('tdate').value=today.toISOString().slice(0,10);
  ['mood','sleep','energy'].forEach(function(k){var r=$('t'+k);r.addEventListener('input',function(){$('v'+k).textContent=r.value;});});
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function avg(a){return a.length?a.reduce(function(x,y){return x+y;},0)/a.length:0;}
  function render(){
    var d=load().sort(function(a,b){return a.date<b.date?-1:1;});
    var tb=$('tlog');tb.innerHTML='';
    d.slice().reverse().forEach(function(x){var tr=document.createElement('tr');tr.innerHTML='<td>'+esc(x.date)+'</td><td>'+esc(x.dose)+' mg</td><td>'+x.mood+'</td><td>'+x.sleep+'</td><td>'+x.energy+'</td><td>'+esc(x.note||'')+'</td><td><button class="btn btn-sm btn-ghost" data-d="'+esc(x.date)+'">Delete</button></td>';tb.appendChild(tr);});
    if(!d.length) tb.innerHTML='<tr><td colspan="7">No entries yet. Save your first check-in above, or load demo data to see how it works.</td></tr>';
    var first=d.slice(0,7), last=d.slice(-7);
    var f=function(k,a){return avg(a.map(function(x){return x[k];}));};
    $('tsum').innerHTML=d.length?['mood','sleep','energy'].map(function(k){var ch=f(k,last)-f(k,first);return '<div><span>'+k+' (last 7 days)</span><b>'+f(k,last).toFixed(1)+' <small style="font-size:.8rem;color:'+(ch>=0?'#3f7d4e':'#c2380f')+'">'+(ch>=0?'▲':'▼')+Math.abs(ch).toFixed(1)+' vs first week</small></b></div>';}).join('')+'<div><span>Days logged</span><b>'+d.length+' / 84</b></div>':'';
    draw(d);
  }
  function draw(d){
    var c=$('tchart'),x=c.getContext('2d'),W=c.width=c.clientWidth*(window.devicePixelRatio||1),H=c.height=260*(window.devicePixelRatio||1),s=(window.devicePixelRatio||1);
    x.clearRect(0,0,W,H);x.font=(12*s)+'px Inter,sans-serif';x.fillStyle='#6c6375';
    var L=34*s,R=10*s,T=12*s,B=26*s,w=W-L-R,h=H-T-B;
    for(var g=0;g<=10;g+=2){var y=T+h-(g/10)*h;x.strokeStyle='#efe8f4';x.beginPath();x.moveTo(L,y);x.lineTo(W-R,y);x.stroke();x.fillText(g,8*s,y+4*s);}
    if(d.length<2){x.fillText('Log at least 2 days to see your chart.',L+10*s,T+h/2);return;}
    [['mood','#5b2a86'],['sleep','#e8461f'],['energy','#3f7d4e']].forEach(function(m){
      x.strokeStyle=m[1];x.lineWidth=2.5*s;x.beginPath();
      d.forEach(function(p,i){var win=d.slice(Math.max(0,i-6),i+1),v=avg(win.map(function(q){return q[m[0]];}));var px=L+(i/(d.length-1))*w,py=T+h-(v/10)*h;i?x.lineTo(px,py):x.moveTo(px,py);});
      x.stroke();
    });
    x.fillStyle='#6c6375';x.fillText(d[0].date,L,H-6*s);var e=d[d.length-1].date;x.fillText(e,W-R-x.measureText(e).width,H-6*s);
  }
  $('tsave').onclick=function(){
    var e={date:$('tdate').value,dose:+$('tdose').value||0,mood:+$('tmood').value,sleep:+$('tsleep').value,energy:+$('tenergy').value,note:$('tnote').value.slice(0,140)};
    if(!e.date){$('tmsg').textContent='Pick a date.';return;}
    var d=load().filter(function(x){return x.date!==e.date;});d.push(e);save(d);$('tmsg').textContent='Saved ✓';$('tnote').value='';render();
  };
  $('tlog').onclick=function(ev){var b=ev.target.closest('button[data-d]');if(!b)return;save(load().filter(function(x){return x.date!==b.dataset.d;}));render();};
  $('tclear').onclick=function(){if(confirm('Delete all tracker entries from this browser?')){save([]);render();}};
  $('tdemo').onclick=function(){var d=[],base=new Date();base.setDate(base.getDate()-41);for(var i=0;i<42;i++){var dt=new Date(base);dt.setDate(base.getDate()+i);var t=i/41,r=function(){return Math.round((Math.random()-.5)*2);};d.push({date:dt.toISOString().slice(0,10),dose:i<7?0:30,mood:Math.min(10,Math.max(1,Math.round(4+t*2.5)+r())),sleep:Math.min(10,Math.max(1,Math.round(4.5+t*2)+r())),energy:Math.min(10,Math.max(1,Math.round(5+t*1.5)+r())),note:i===7?'Started saffron 30 mg':(i===0?'Baseline (demo)':'')});}save(d);render();};
  $('tcsv').onclick=function(){var d=load();var csv='date,dose_mg,mood,sleep,energy,notes\n'+d.map(function(x){return [x.date,x.dose,x.mood,x.sleep,x.energy,'"'+String(x.note||'').replace(/"/g,'""')+'"'].join(',');}).join('\n');var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='saffron-tracker.csv';a.click();};
  window.addEventListener('resize',function(){draw(load().sort(function(a,b){return a.date<b.date?-1:1;}));});
  render();
})();
</script>
