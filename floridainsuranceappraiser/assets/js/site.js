/* Florida Insurance Appraiser — nav, home gap estimator, lead form */
(function(){
  var burger=document.querySelector('.burger'),nav=document.getElementById('nav');
  if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('show');burger.setAttribute('aria-expanded',o)})}
  document.querySelectorAll('.nav li>button').forEach(function(b){
    b.addEventListener('click',function(e){e.stopPropagation();var li=b.parentNode,o=!li.classList.contains('open');
      document.querySelectorAll('.nav li.open').forEach(function(x){if(x!==li){x.classList.remove('open');x.querySelector('button').setAttribute('aria-expanded','false')}});
      li.classList.toggle('open',o);b.setAttribute('aria-expanded',o)});
  });
  document.addEventListener('click',function(){document.querySelectorAll('.nav li.open').forEach(function(x){x.classList.remove('open')})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('.nav li.open').forEach(function(x){x.classList.remove('open')})});

  window.fiaMoney=function(n){return '$'+Math.round(n).toLocaleString('en-US')};
  window.fiaNum=function(el){var v=parseFloat(String(el.value).replace(/[^0-9.\-]/g,''));return isNaN(v)?0:v};

  /* homepage quick gap estimator */
  var q=document.getElementById('quickgap');
  if(q){
    var run=function(){
      var ins=fiaNum(q.ins),con=fiaNum(q.con),gap=Math.max(con-ins,0),pct=con>0?gap/con*100:0;
      q.querySelector('.big').textContent=fiaMoney(gap);
      q.querySelector('.meter i').style.width=Math.min(pct,100)+'%';
      var t=q.querySelector('.verdict-text');
      if(!con){t.textContent='Enter both numbers to see the spread.';}
      else if(gap<=0){t.textContent='No gap — the carrier’s number meets or beats your estimate.';}
      else if(gap<5000){t.textContent=pct.toFixed(0)+'% spread. Small gaps are often fixed with a documented supplement before appraisal.';}
      else{t.textContent=pct.toFixed(0)+'% of your estimate is in dispute. A gap this size is worth a line-by-line appraisal review.';}
    };
    q.addEventListener('input',run);run();
  }

  /* lead form → /api/contact.php */
  document.querySelectorAll('form[data-lead-form]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();var msg=f.querySelector('.form-msg'),btn=f.querySelector('button[type=submit]');
      if(!f.checkValidity()){f.reportValidity();return}
      btn.disabled=true;msg.className='form-msg';msg.textContent='Sending…';
      fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
        .then(function(r){return r.json().catch(function(){return {ok:false}})})
        .then(function(d){
          if(d.ok){f.reset();msg.className='form-msg ok';msg.textContent='Thank you — your claim details were sent. We’ll reply within one business day.';}
          else{msg.className='form-msg err';msg.textContent=(d.error||'Something went wrong.')+' Please call '+f.dataset.phone+'.';}
        })
        .catch(function(){msg.className='form-msg err';msg.textContent='Could not send right now. Please call '+f.dataset.phone+'.'})
        .finally(function(){btn.disabled=false});
    });
  });
})();
