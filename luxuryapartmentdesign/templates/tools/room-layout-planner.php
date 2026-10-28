<div class="planner" id="planner">
  <div>
    <div class="field-row">
      <label class="field"><span class="field__label">Room width (ft)</span><input type="number" id="pl-w" value="14" min="5" max="40" step="0.5"></label>
      <label class="field"><span class="field__label">Room length (ft)</span><input type="number" id="pl-l" value="12" min="5" max="40" step="0.5"></label>
    </div>
    <p class="field__label" style="margin-top:14px">Add furniture</p>
    <div class="planner__palette" id="pl-palette"></div>
  </div>
  <div>
    <div class="planner__toolbar">
      <button type="button" class="btn btn--small btn--ghost" id="pl-rotate" disabled>Rotate</button>
      <button type="button" class="btn btn--small btn--ghost" id="pl-delete" disabled>Delete</button>
      <button type="button" class="btn btn--small btn--ghost" id="pl-clear">Clear room</button>
      <button type="button" class="btn btn--small btn--gold" id="pl-download">Download PNG</button>
      <p class="planner__hint">Drag to move · arrow keys nudge · R rotates · Delete removes. Grid squares are 1 ft.</p>
    </div>
    <div class="planner__stage" id="pl-stage"></div>
    <ul class="warn-list" id="pl-warnings" aria-live="polite"></ul>
  </div>
</div>
