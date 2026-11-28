<div class="calc" data-tool="words">
  <?= w_head('Word Counter', 'text', 'Paste or type your essay — counts update live.', false) ?>
  <div class="calc-body">
    <textarea class="input" name="text" rows="9" placeholder="Start typing or paste your essay here…" aria-label="Your text" style="min-height:220px"></textarea>
    <div class="grid-2" style="margin-top:12px;align-items:end"><?= w_field('goal', 'Word goal (optional)', '500', 'words', 'numeric') ?><div><button type="button" class="btn btn-ghost" data-clear style="width:100%"><?= icon('trash') ?> Clear text</button></div></div>
    <div class="bar-track" style="margin-top:4px" data-goalbar hidden><div class="bar-fill" data-out="goalfill"></div></div>
    <div class="stats"><div class="stat"><span>Words</span><b data-out="w">0</b></div><div class="stat"><span>Characters</span><b data-out="c">0</b></div><div class="stat"><span>No spaces</span><b data-out="cn">0</b></div><div class="stat"><span>Sentences</span><b data-out="s">0</b></div><div class="stat"><span>Paragraphs</span><b data-out="p">0</b></div><div class="stat"><span>Reading time</span><b data-out="rt">0 min</b></div><div class="stat"><span>Speaking time</span><b data-out="st">0 min</b></div></div>
    <p class="lbl" style="margin:16px 0 4px">Most used words</p><div data-out="top" class="note">—</div>
  </div>
</div>
