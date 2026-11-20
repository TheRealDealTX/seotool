<?php defined('WCA') || exit; partial('partials/tool_head', ['tool' => $tool]); ?>
<div class="wrap tool narrow" data-tool="quiz">
  <div class="card quiz">
    <div class="progress"><i data-q-progress></i></div>
    <div data-q-stage></div>
    <div class="quiz-nav"><button type="button" class="btn btn-ghost" data-q-back hidden>← Back</button></div>
  </div>
  <div data-q-results hidden>
    <h2>Your top matches</h2>
    <div class="card-grid" data-q-cards></div>
    <p><button type="button" class="btn btn-ghost" data-q-restart>Retake the quiz</button> <a class="btn" href="/apartments/">See all apartments</a></p>
  </div>
</div>
<?php partial('partials/tool_foot', compact('tools', 'slug', 'all')); ?>
