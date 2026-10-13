<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/service-areas/';
$crumbs = [['Home', '/'], ['Service Areas', $path]];
$areas = [
    ['Sugar Land', '77478, 77479, 77498', 'Our home base. We cover every Sugar Land neighborhood—First Colony, Telfair, Riverstone, New Territory, Sugar Creek, Avalon, Commonwealth, Imperial, Lake Pointe, Sugar Lakes, Settlers Park and more—from the Town Square district to the homes along the Brazos.'],
    ['Missouri City', 'Fort Bend County', 'East of Sugar Land along Highway 6 and the Fort Bend Parkway, including Sienna, Lake Olympia and Quail Valley—neighborhoods that see the same hail, hurricane and freeze claims.'],
    ['Stafford', 'Fort Bend County', 'Stafford’s mix of homes, retail and light industrial property along US-59/I-69 means plenty of commercial and business interruption claims alongside residential losses.'],
    ['Richmond', 'Fort Bend County seat', 'Home of the Brazos River gauge Fort Bend watches during every big rain. River and flash flooding, wind and hail claims are common here.'],
    ['Rosenberg', 'Fort Bend County', 'Older housing stock and newer master-planned communities along US-59 and the Brazos face wind, hail and flood risks—and the coverage disputes that come with them.'],
    ['Fulshear & Cross Creek Ranch', 'Fort Bend County', 'Fast-growing northwest Fort Bend, where newer roofs still get hail and wind damage and builders’ materials raise matching questions.'],
    ['Greatwood & Pecan Grove', 'Unincorporated Fort Bend', 'Established communities near the Brazos with levee protection, mature trees and the tree-impact and roof claims that follow every big wind event.'],
    ['Katy, Pearland & greater Houston', 'Harris / Brazoria / Fort Bend', 'We also represent homeowners and businesses across the Houston metro. Call to confirm availability for your address.'],
];
page_start([
    'title' => 'Service Areas | Public Adjuster Serving Sugar Land & Fort Bend County',
    'description' => 'Sugar Land Public Adjuster serves Sugar Land, Missouri City, Stafford, Richmond, Rosenberg, Fulshear, Greatwood and greater Houston. Free claim reviews.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
]);
page_hero('Service Areas', 'A Sugar Land public adjuster serving every Sugar Land neighborhood and the surrounding Fort Bend County communities.', $crumbs, 'Where we work');
?>
<div class="container content-layout">
  <div>
    <div class="grid-2">
<?php foreach ($areas as [$name, $sub, $blurb]): ?>
      <div class="card"><h2 class="h3"><?= e($name) ?></h2><p class="small muted"><?= e($sub) ?></p><p><?= e($blurb) ?></p></div>
<?php endforeach; ?>
    </div>
    <div class="prose mt-2">
      <h2>Sugar Land neighborhoods we serve</h2>
      <ul class="chips">
        <li>First Colony</li><li>Telfair</li><li>Riverstone</li><li>New Territory</li><li>Sugar Creek</li><li>Avalon</li><li>Commonwealth</li><li>Imperial</li><li>Lake Pointe</li><li>Sugar Lakes</li><li>Settlers Park</li><li>Covington Woods</li><li>Venetian Estates</li><li>Riverpark</li><li>Brazos Landing</li><li>Sugar Mill</li><li>Oyster Creek area</li>
      </ul>
      <h2 class="mt-2">Why a local public adjuster in Sugar Land matters</h2>
      <p>Local experience counts in a claim. We know Houston-area repair pricing, how insurers have handled claims after Ike, Harvey, Uri and Beryl, and which issues—matching, wind vs. water, slab leaks on expansive clay soils, tree impact—come up again and again in Fort Bend County. That lets us anticipate the insurer’s position and document the claim to answer it.</p>
      <p>Not sure whether we cover your address? Call or text <?= tel_link() ?>. Check current conditions on the <a href="/sugar-land-weather/">live storm tracker</a> or explore <a href="/services/">our claim services</a>.</p>
    </div>
  </div>
  <?php sidebar_cta(); ?>
</div>
<?php page_end(); ?>
