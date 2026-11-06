/* Florida Insurance Appraiser — free claim tools */
(function(){
  var M=window.fiaMoney,N=window.fiaNum,$=function(id){return document.getElementById(id)};
  function out(root,key,val){var el=root.querySelector('[data-o="'+key+'"]');if(el)el.textContent=val}
  function bind(form,fn){form.addEventListener('input',fn);form.addEventListener('change',fn);fn()}
  var page=document.querySelector('main');

  /* 1. Appraisal worth-it */
  var w=document.querySelector('[data-tool="worth"]');
  if(w)bind(w,function(){
    var ins=N($('w_ins')),con=N($('w_con')),gap=Math.max(con-ins,0),fee=N($('w_fee')),pct=$('w_feetype').value==='pct';
    var ump=N($('w_ump'))/2*parseFloat($('w_umpchance').value);
    var costAt=function(rec){return (pct?rec*fee/100:fee)+ump};
    out(page,'gap',M(gap));out(page,'cost',M(costAt(gap*0.5)));
    var be;
    if(pct){be=fee>=100?Infinity:ump/(gap*(1-fee/100))}else{be=gap?(fee+ump)/gap:Infinity}
    out(page,'be',isFinite(be)&&gap?Math.min(be*100,999).toFixed(0)+'%':'—');
    var rows='';[0.25,0.5,0.75].forEach(function(s){var rec=gap*s,net=rec-costAt(rec);
      rows+='<tr><td>'+(s*100)+'% of the gap</td><td>'+M(rec)+'</td><td style="color:'+(net<0?'#bf4526':'#12595a')+';font-weight:800">'+(net<0?'−':'')+M(Math.abs(net))+'</td></tr>'});
    $('worth-rows').innerHTML=rows;
    var v=$('worth-verdict');
    if(!gap)v.textContent='There’s no disputed amount yet — enter an estimate higher than the insurer’s.';
    else if(be<0.2)v.textContent='Strong case on the numbers: appraisal pays for itself if the award recovers about '+(be*100).toFixed(0)+'% of the gap. Make sure your estimate is fully documented.';
    else if(be<0.5)v.textContent='Borderline: the award needs to recover about '+(be*100).toFixed(0)+'% of the gap to break even. Get your estimate reviewed line by line before invoking appraisal.';
    else v.textContent='Appraisal costs are large relative to the gap. Consider a documented supplement, re-inspection request or DFS mediation first.';
  });

  /* 2. Hurricane deductible */
  var h=document.querySelector('[data-tool="hurdeduct"]');
  if(h)bind(h,function(){
    var cova=N($('h_cova')),p=$('h_pct').value,aop=N($('h_aop')),loss=N($('h_loss')),used=N($('h_used'));
    $('h_flat').closest('.field').style.display=p==='flat'?'':'none';
    var ded=p==='flat'?N($('h_flat')):cova*parseFloat(p);
    var applied=used>0?Math.max(ded-used,aop):ded;
    var pay=Math.max(loss-applied,0);
    out(page,'ded',M(ded));out(page,'applied',M(applied));out(page,'pay',M(pay));
    var v=$('hur-verdict');
    if(!loss)v.textContent='Enter an estimated damage amount.';
    else if(pay===0)v.textContent='Your estimated damage is at or below the deductible, so no payment would be due on these numbers. If the insurer’s estimate missed items, a full re-estimate could change that.';
    else v.textContent='The deductible absorbs '+(Math.min(applied/loss,1)*100).toFixed(0)+'% of this loss. Every $1,000 added to the documented amount of loss adds $1,000 to the payment.';
  });

  /* 3. ACV */
  var a=document.querySelector('[data-tool="acv"]');
  if(a){
    $('a_item').addEventListener('change',function(){if(this.value!=='custom')$('a_life').value=this.value});
    bind(a,function(){
      var life=Math.max(N($('a_life')),1),rcv=N($('a_rcv')),age=N($('a_age')),cond=parseFloat($('a_cond').value),cap=parseFloat($('a_cap').value);
      var rate=Math.min(Math.max(age/life+cond*(age/life),0),cap);
      var dep=rcv*rate;
      out(page,'rate',(rate*100).toFixed(1)+'%');out(page,'dep',M(dep));out(page,'acv',M(rcv-dep));
      $('acv-verdict').textContent=rcv?'On a replacement cost policy, the '+M(dep)+' holdback is usually recoverable after repairs are completed and documented. If the insurer’s depreciation is much higher than this, ask which life expectancy and age they used.':'';
    });
  }

  /* 4. Deadlines */
  var d=document.querySelector('[data-tool="deadline"]');
  if(d)bind(d,function(){
    var lv=$('d_loss').value,nv=$('d_notice').value,ul=$('dl-out');
    if(!lv){ul.innerHTML='<li><span>Enter your date of loss to build the timeline.</span></li>';return}
    var loss=new Date(lv+'T12:00:00'),notice=nv?new Date(nv+'T12:00:00'):null,today=new Date();today.setHours(12,0,0,0);
    var add=function(dt,days,months){var x=new Date(dt);if(months)x.setMonth(x.getMonth()+months);if(days)x.setDate(x.getDate()+days);return x};
    var fmt=function(x){return x.toLocaleDateString('en-US',{month:'long',day:'numeric',year:'numeric'})};
    var rows=[['Notice deadline — new or reopened claim (1 year after loss)',add(loss,0,12)],['Notice deadline — supplemental claim (18 months after loss)',add(loss,0,18)]];
    if(notice){rows.push(['Insurer acknowledgment of claim (about 7 days after notice)',add(notice,7)]);rows.push(['Insurer pay-or-deny decision (generally 60 days after notice)',add(notice,60)])}
    ul.innerHTML=rows.map(function(r){var days=Math.round((r[1]-today)/864e5),past=days<0;
      return '<li class="'+(past?'past':'')+'"><span>'+r[0]+'</span><b>'+fmt(r[1])+' · '+(past?Math.abs(days)+' days ago':days+' days left')+'</b></li>'}).join('');
  });

  /* 5. Roof */
  var r=document.querySelector('[data-tool="roof"]');
  if(r)bind(r,function(){
    var oh=N($('r_oh'))/12*2,L=N($('r_len'))+oh,W=N($('r_wid'))+oh,p=parseFloat($('r_pitch').value),waste=parseFloat($('r_style').value);
    var f=Math.sqrt(1+Math.pow(p/12,2)),area=L*W*f,sq=area/100*(1+waste),ins=N($('r_ins'));
    out(page,'area',Math.round(area).toLocaleString()+' sq ft');out(page,'sq',sq.toFixed(1));out(page,'bund',Math.ceil(sq*3));
    var v=$('roof-verdict'),base='Pitch factor '+f.toFixed(3)+'. About '+Math.ceil(area/100/10)+' rolls of 10-square synthetic underlayment. ';
    if(ins>0){var diff=sq-ins;v.textContent=base+(Math.abs(diff)/sq<0.05?'The insurer’s '+ins+' squares are within 5% of this estimate.':'The insurer’s estimate is '+Math.abs(diff).toFixed(1)+' squares '+(diff>0?'lower':'higher')+' than this estimate ('+(Math.abs(diff)/sq*100).toFixed(0)+'%). Worth verifying with an aerial report or field measurement.')}
    else v.textContent=base+'Enter the insurer’s squares to compare.';
  });

  /* 6. Inventory */
  var inv=document.querySelector('[data-tool="inventory"]');
  if(inv){
    var CATS=[['Electronics',6],['Furniture',12],['Appliances',12],['Clothing',5],['Bedding & linens',6],['Kitchenware',10],['Tools & equipment',10],['Rugs & flooring',10],['Decor & art',20],['Toys & sports',6],['Other',10]];
    var KEY='fia-inventory-v1',body=$('inv-body'),rows=[];
    try{rows=JSON.parse(localStorage.getItem(KEY))||[]}catch(e){rows=[]}
    if(!rows.length)rows=[{item:'',room:'',qty:1,age:0,cat:'Electronics',cost:''}];
    var esc=function(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
    function render(){
      body.innerHTML=rows.map(function(x,i){return '<tr data-i="'+i+'"><td><input data-k="item" value="'+esc(x.item)+'" placeholder="e.g. 55&quot; TV" aria-label="Item"></td><td><input data-k="room" value="'+esc(x.room)+'" placeholder="Living room" aria-label="Room"></td><td><input data-k="qty" type="number" min="1" value="'+esc(x.qty)+'" aria-label="Quantity"></td><td><input data-k="age" type="number" min="0" step="0.5" value="'+esc(x.age)+'" aria-label="Age"></td><td><select data-k="cat" aria-label="Category">'+CATS.map(function(c){return '<option'+(c[0]===x.cat?' selected':'')+'>'+c[0]+'</option>'}).join('')+'</select></td><td><input data-k="cost" inputmode="decimal" value="'+esc(x.cost)+'" placeholder="0" aria-label="Unit replacement cost"></td><td><button type="button" class="x" aria-label="Remove row">×</button></td></tr>'}).join('');
      totals();
    }
    function life(cat){for(var i=0;i<CATS.length;i++)if(CATS[i][0]===cat)return CATS[i][1];return 10}
    function totals(){
      var rcv=0,acv=0,n=0;
      rows.forEach(function(x){var c=parseFloat(x.cost)||0,q=parseFloat(x.qty)||0,t=c*q;if(t>0)n+=q;rcv+=t;acv+=t*Math.max(1-(parseFloat(x.age)||0)/life(x.cat),0.2)});
      out(inv,'count',n);out(inv,'rcv',M(rcv));out(inv,'acv',M(acv));
      try{localStorage.setItem(KEY,JSON.stringify(rows))}catch(e){}
    }
    body.addEventListener('input',function(e){var t=e.target,tr=t.closest('tr');if(!tr||!t.dataset.k)return;rows[+tr.dataset.i][t.dataset.k]=t.value;totals()});
    body.addEventListener('click',function(e){if(e.target.classList.contains('x')){rows.splice(+e.target.closest('tr').dataset.i,1);if(!rows.length)rows.push({item:'',room:'',qty:1,age:0,cat:'Electronics',cost:''});render()}});
    $('inv-add').onclick=function(){rows.push({item:'',room:rows.length?rows[rows.length-1].room:'',qty:1,age:0,cat:'Electronics',cost:''});render();var ins=body.querySelectorAll('tr:last-child input');if(ins[0])ins[0].focus()};
    $('inv-clear').onclick=function(){if(confirm('Clear every item from this list?')){rows=[{item:'',room:'',qty:1,age:0,cat:'Electronics',cost:''}];render()}};
    $('inv-print').onclick=function(){window.print()};
    $('inv-csv').onclick=function(){
      var q=function(s){return '"'+String(s==null?'':s).replace(/"/g,'""')+'"'};
      var lines=[['Item','Room','Qty','Age (yrs)','Category','Unit cost','Total RCV','Est. ACV'].map(q).join(',')];
      rows.forEach(function(x){var c=parseFloat(x.cost)||0,n=parseFloat(x.qty)||0,t=c*n;lines.push([x.item,x.room,n,x.age,x.cat,c.toFixed(2),t.toFixed(2),(t*Math.max(1-(parseFloat(x.age)||0)/life(x.cat),0.2)).toFixed(2)].map(q).join(','))});
      var blob=new Blob([lines.join('\n')],{type:'text/csv'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='contents-inventory.csv';document.body.appendChild(a);a.click();a.remove();
    };
    render();
  }

  /* 7. Quiz */
  var qz=document.querySelector('[data-tool="quiz"]');
  if(qz){
    var Q=[
      ['I have a complete, certified copy of my policy, including endorsements.',10,'Request a certified copy of your policy in writing from your insurer.'],
      ['I have the insurer’s full, line-item estimate (not just the payment letter).',10,'Ask the adjuster for the complete estimate with line items and depreciation shown.'],
      ['I have my own detailed, line-item repair estimate.',12,'Get a detailed contractor or independent estimate — ideally in Xactimate or Symbility format.'],
      ['I have dated photos or video of the damage from before repairs or cleanup.',10,'Gather every photo and video, including phone timestamps and mitigation company photos.'],
      ['I know my date of loss and have reported the claim in writing.',8,'Confirm your claim number and the date of loss the insurer has on file.'],
      ['I know my deductible amount (and hurricane deductible, if any).',6,'Check your declarations page for the hurricane and all-other-perils deductibles.'],
      ['I have read the appraisal provision in my policy.',8,'Find the “Appraisal” condition in your policy and note its deadlines and fee terms.'],
      ['The dispute is about how much, not whether the damage is covered.',10,'If the insurer denied coverage, appraisal may not resolve it — consider legal advice on coverage.'],
      ['I have receipts or invoices for emergency repairs and mitigation.',6,'Collect invoices for tarping, water extraction, drying and any temporary repairs.'],
      ['I have kept records of extra living expenses (if displaced).',4,'Save hotel, rental and meal receipts that exceed your normal costs.'],
      ['I have a contents inventory for damaged personal property.',6,'Start a room-by-room list with the contents inventory builder.'],
      ['I have a log of calls, emails and letters with the insurer.',10,'Start a simple log: date, who you spoke to and what was said or promised.']
    ];
    var list=$('quiz-list');
    list.innerHTML=Q.map(function(x,i){return '<li><label><input type="checkbox" data-i="'+i+'"> <span>'+x[0]+'</span></label></li>'}).join('');
    var run=function(){
      var s=0,todo=[];list.querySelectorAll('input').forEach(function(c){var x=Q[+c.dataset.i];if(c.checked)s+=x[1];else todo.push(x[2])});
      out(qz,'score',s+' / 100');qz.querySelector('.meter i').style.width=s+'%';
      out(qz,'label',s>=75?'Ready to discuss appraisal — your file is in good shape.':s>=40?'Getting there — close the gaps below first.':'Early stage — focus on documentation before invoking appraisal.');
      $('quiz-todo').innerHTML=todo.length?'<h3 style="margin-top:22px">Your next steps</h3><ul class="ticks">'+todo.map(function(t){return '<li>'+t+'</li>'}).join('')+'</ul>':'';
    };
    list.addEventListener('change',run);run();
  }
})();
