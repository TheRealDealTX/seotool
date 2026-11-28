<div class="calc" data-tool="sci">
  <?= w_head('Scientific Calculator', 'calc', 'Tap the keys or use your keyboard.', false) ?>
  <div class="calc-body">
    <div class="sci-display" aria-live="polite"><div class="sci-expr" data-out="expr"></div><div class="sci-out" data-out="out">0</div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px"><div class="seg" role="group" aria-label="Angle unit"><button type="button" data-ang="deg" aria-pressed="true">DEG</button><button type="button" data-ang="rad" aria-pressed="false">RAD</button></div><button type="button" class="btn btn-ghost btn-sm" data-k="2nd">2nd</button></div>
    <div class="sci-keys">
      <button type="button" class="k-fn" data-k="sin(">sin</button><button type="button" class="k-fn" data-k="cos(">cos</button><button type="button" class="k-fn" data-k="tan(">tan</button><button type="button" class="k-fn" data-k="log(">log</button><button type="button" class="k-fn" data-k="ln(">ln</button>
      <button type="button" class="k-fn" data-k="^2">x²</button><button type="button" class="k-fn" data-k="^">xʸ</button><button type="button" class="k-fn" data-k="sqrt(">√</button><button type="button" class="k-fn" data-k="!">n!</button><button type="button" class="k-fn" data-k="pi">π</button>
      <button type="button" class="k-fn" data-k="(">(</button><button type="button" class="k-fn" data-k=")">)</button><button type="button" class="k-fn" data-k="e">e</button><button type="button" class="k-clear" data-k="C">C</button><button type="button" class="k-clear" data-k="DEL">⌫</button>
      <button type="button" data-k="7">7</button><button type="button" data-k="8">8</button><button type="button" data-k="9">9</button><button type="button" class="k-op" data-k="/">÷</button><button type="button" class="k-op" data-k="%">%</button>
      <button type="button" data-k="4">4</button><button type="button" data-k="5">5</button><button type="button" data-k="6">6</button><button type="button" class="k-op" data-k="*">×</button><button type="button" class="k-op" data-k="NEG">±</button>
      <button type="button" data-k="1">1</button><button type="button" data-k="2">2</button><button type="button" data-k="3">3</button><button type="button" class="k-op" data-k="-">−</button><button type="button" class="k-op" data-k="ANS">Ans</button>
      <button type="button" data-k="0">0</button><button type="button" data-k=".">.</button><button type="button" data-k="E">EXP</button><button type="button" class="k-op" data-k="+">+</button><button type="button" class="k-eq" data-k="=">=</button>
    </div>
    <div class="sci-history" data-out="hist"></div>
  </div>
</div>
