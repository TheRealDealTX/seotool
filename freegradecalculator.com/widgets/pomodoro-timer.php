<div class="calc" data-tool="pomo">
  <?= w_head('Pomodoro Study Timer', 'clock', 'Focus. Break. Repeat.', false) ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="focus">Focus</button><button type="button" role="tab" aria-selected="false" data-mode="short">Short break</button><button type="button" role="tab" aria-selected="false" data-mode="long">Long break</button></div>
    <input class="input" name="task" placeholder="What are you working on?" aria-label="Current task" style="text-align:center">
    <div class="ring timer-ring" data-ring="t"><svg viewBox="0 0 120 120" aria-hidden="true"><circle class="ring-bg" cx="60" cy="60" r="52"/><circle class="ring-fg" cx="60" cy="60" r="52" stroke-dasharray="326.73" stroke-dashoffset="0"/></svg><div class="ring-val"><span><span data-out="time">25:00</span><small data-out="phase">Focus</small></span></div></div>
    <div class="calc-actions" style="justify-content:center"><button type="button" class="btn btn-primary" data-start style="flex:0 1 220px"><?= icon('zap') ?> <span>Start</span></button><button type="button" class="btn btn-ghost" data-reset-timer><?= icon('reset') ?> Reset</button></div>
    <p class="note" style="text-align:center">Completed focus sessions today: <b data-out="done">0</b></p>
    <details><summary style="font-weight:700;cursor:pointer">Timer settings</summary><div class="grid-4" style="margin-top:12px"><?= w_field('fm', 'Focus (min)', '25', '', 'numeric', '25') ?><?= w_field('sm', 'Short break', '5', '', 'numeric', '5') ?><?= w_field('lm', 'Long break', '15', '', 'numeric', '15') ?><?= w_field('every', 'Long break every', '4', '', 'numeric', '4') ?></div></details>
  </div>
</div>
