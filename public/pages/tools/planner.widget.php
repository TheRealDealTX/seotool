<?php defined('SCC') || exit;
$zones = [
    // value, label, hint, type, priority
    ['front', 'Front door', 'Faces, packages, visitors', 'out', 3],
    ['drive', 'Driveway / parking', 'Vehicles, plates', 'out', 3],
    ['back', 'Back door', 'Most common forced entry point', 'out', 3],
    ['yard', 'Backyard / garden', 'Wide view of the lot', 'out', 2],
    ['sideL', 'Side passage (left)', 'Gates, bins, side windows', 'out', 2],
    ['sideR', 'Side passage (right)', 'Gates, bins, side windows', 'out', 2],
    ['garage', 'Garage door', 'Tools, bikes, vehicles', 'out', 2],
    ['gate', 'Gate / entrance', 'Long driveways, farm gates', 'out', 1],
    ['shed', 'Shed / outbuilding', 'Equipment, fuel, tools', 'out', 1],
    ['patio', 'Pool / patio / deck', 'Safety + furniture', 'out', 1],
    ['fence', 'Perimeter / fence line', 'Large lots and acreage', 'out', 1],
    ['hall', 'Entry hallway (indoor)', 'Catches anyone who gets in', 'in', 2],
    ['living', 'Living area (indoor)', 'Pets, kids, valuables', 'in', 1],
    ['stairs', 'Stairs / landing (indoor)', 'Route to bedrooms', 'in', 1],
];
$defaults = ['front', 'drive', 'back', 'yard'];
?>
<div class="tool" data-tool="planner">
  <div class="tool-head"><?= icon('map', 22) ?><strong>CCTV Camera Planner</strong><span>How many cameras do you need?</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="field"><label for="pl-prop">Property type</label>
        <select id="pl-prop" name="prop">
          <option value="apt">Apartment / condo</option>
          <option value="town">Townhouse</option>
          <option value="house" selected>Detached house</option>
          <option value="large">Large house (3,000+ sq ft)</option>
          <option value="acre">Acreage / farm / ranch</option>
          <option value="biz">Small business / shop</option>
        </select>
      </div>
      <div class="field"><span class="lbl">Coverage level</span><div class="seg">
        <label><input type="radio" name="lvl" value="1"><span>Essential</span></label>
        <label><input type="radio" name="lvl" value="2" checked><span>Balanced</span></label>
        <label><input type="radio" name="lvl" value="3"><span>Complete</span></label>
      </div><small>Essential = entry points only. Balanced adds blind spots. Complete covers every checked zone, with extra cameras on big lots.</small></div>
      <div class="field"><span class="lbl">Zones you want covered</span>
        <div class="chk-grid">
<?php foreach ($zones as [$v, $l, $h, $t, $p]): ?>
          <label class="chk"><input type="checkbox" data-zone value="<?= $v ?>" data-label="<?= e($l) ?>" data-type="<?= $t ?>" data-p="<?= $p ?>"<?= in_array($v, $defaults, true) ? ' checked' : '' ?>><span><?= e($l) ?><em><?= e($h) ?></em></span></label>
<?php endforeach; ?>
        </div>
      </div>
      <div class="row2">
        <div class="field"><label for="pl-pow">Outdoor power outlets</label><select id="pl-pow" name="pow"><option value="many">Near most spots</option><option value="few" selected>A few</option><option value="none">None / hard to wire</option></select></div>
        <div class="field"><label for="pl-net">Wi‑Fi outdoors</label><select id="pl-net" name="net"><option value="good" selected>Strong everywhere</option><option value="part">Weak at the edges</option><option value="none">None at far spots</option></select></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero"><div class="big" data-o="total">—</div><p data-o="sum"></p></div>
      <div class="results">
        <div class="res"><b data-o="out">—</b><span>Outdoor cameras</span></div>
        <div class="res"><b data-o="in">—</b><span>Indoor cameras</span></div>
        <div class="res"><b data-o="solar">—</b><span>Good candidates for solar</span></div>
        <div class="res"><b data-o="cost">—</b><span>Typical hardware budget</span></div>
      </div>
      <h4>Your camera plan</h4>
      <div data-copy><ul class="plan-list" data-o="plan"></ul><div data-o="tips"></div></div>
      <div class="btn-row"><button type="button" class="btn btn-sun btn-sm" data-act="copy">Copy my plan</button><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><button type="button" class="btn btn-line btn-sm" data-act="print">Print plan</button></div>
      <p class="tool-note">Budget ranges are typical US retail for consumer cameras in late 2026 and exclude professional installation and monitoring.</p>
    </div>
  </form>
</div>
