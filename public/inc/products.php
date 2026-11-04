<?php
/**
 * Amazon affiliate product catalog (tracking ID AMAZON_TAG = solarcctvcamera-20, set in bootstrap.php).
 *
 * Each product links either to a verified product page (asin) or to an Amazon
 * search for the exact product name (q). Search links earn the same commission
 * and never break when a listing is replaced, so they are used whenever an ASIN
 * could not be confirmed. Specs here are conservative and come from manufacturer
 * pages; always phrase them as "check the listing".
 *
 * In article bodies: <!--products:id1,id2,id3--> renders a gear grid and turns on
 * the affiliate disclosure for that page.
 */
defined('SCC') || (http_response_code(404) && exit);

function products(): array
{
    return [
        // ---- Cameras ----
        'argus4pro' => ['Reolink Argus 4 Pro + Solar Panel 2', 'camera', ['q' => 'Reolink Argus 4 Pro Solar Panel 2'],
            ['4K', '180° dual-lens view', 'Color night vision', 'Dual-band Wi‑Fi 6', '6 W panel kit'],
            'A wide 180° stitched view from one camera, with a detachable 6 W panel. Good for covering a whole yard or driveway from a corner.'],
        'eufy-s220' => ['eufy SoloCam S220', 'camera', ['asin' => 'B0BZ55JZ4S'],
            ['2K', 'Built-in solar panel', '2.4 GHz Wi‑Fi', 'Local storage', 'No monthly fee'],
            'Budget one-piece camera with the panel built in. Best in open, sunny spots where a small panel can keep up.'],
        'eufy-s340' => ['eufy SoloCam S340', 'camera', ['asin' => 'B0CCYP6KFM'],
            ['3K wide + telephoto', 'Pan & tilt', 'Built-in solar panel', 'Local storage', 'No subscription required'],
            'Dual-lens pan-tilt camera with an integrated panel. One camera can watch a wide area and zoom in on detail.'],
        'ring-solar' => ['Ring Spotlight Cam Plus Solar', 'camera', ['q' => 'Ring Spotlight Cam Plus Solar'],
            ['1080p HDR', 'Spotlight + siren', 'Color night vision', 'Solar panel included', 'Ring Protect for recordings'],
            'Fits homes already on Ring. Note that saving and reviewing recordings needs a Ring Protect subscription.'],
        'go-pt-ultra' => ['Reolink Go PT Ultra + Solar Panel 2', 'camera', ['q' => 'Reolink Go PT Ultra 4G LTE solar'],
            ['4K', '4G LTE (nano SIM)', 'Pan & tilt', '6 W panel', 'microSD'],
            'Cellular pan-tilt camera for farms, gates and job sites with no Wi‑Fi. Needs a data plan on a supported carrier.'],
        'arlo-go2' => ['Arlo Go 2', 'camera', ['asin' => 'B0BLZVB2NQ'],
            ['1080p', 'LTE or Wi‑Fi', 'Spotlight', 'microSD backup', 'Solar panel sold separately'],
            'Switches between LTE and Wi‑Fi, so it suits sites where Wi‑Fi comes and goes. Pair with an Arlo solar panel.'],
        'cell-trail' => ['Cellular trail camera with solar panel', 'camera', ['q' => 'cellular trail camera solar panel'],
            ['4G LTE', 'Long standby', 'Photo + video', 'Weatherproof', 'App alerts'],
            'For hunting land, vacant lots and remote fence lines where you want photo alerts rather than live security video.'],
        'streetlight-cam' => ['Solar street light with camera', 'camera', ['q' => 'solar street light with security camera'],
            ['Light + camera in one', 'Wi‑Fi or 4G versions', 'Pole mount', 'Built-in battery'],
            'All-in-one light and camera for driveways and yards. Sanity-check lumen and watt claims against panel size before buying.'],
        // ---- Power ----
        'panel-reolink' => ['Reolink Solar Panel 2 (6 W)', 'power', ['q' => 'Reolink Solar Panel 2 6W'],
            ['6 W', 'Adjustable bracket', 'Weatherproof', 'For compatible Reolink cameras'],
            'Upgrade or replacement panel for Reolink battery cameras. Check the connector matches your model.'],
        'panel-usbc' => ['5 V USB-C solar panel for battery cameras', 'power', ['q' => 'USB-C solar panel for security camera 5V'],
            ['5 V USB-C', '3–6 W typical', 'Long cable', 'Adjustable mount'],
            'Generic panels work with many cameras that charge over USB-C. Match the connector and voltage to your camera first.'],
        'ext-cable' => ['Solar panel extension cable for cameras', 'power', ['q' => 'solar panel extension cable security camera'],
            ['3–10 m lengths', 'Weatherproof', 'Brand-specific connectors'],
            'Lets the panel sit in the sun while the camera stays in the shade. Buy the version made for your camera’s connector.'],
        'panel-100w' => ['100 W 12 V solar panel', 'power', ['q' => '100W 12V monocrystalline solar panel'],
            ['100 W', '12 V nominal', 'Monocrystalline', 'Pre-drilled frame'],
            'For DIY systems that power several cameras, a PoE switch or a router from one shared battery.'],
        'mppt' => ['MPPT solar charge controller (20–30 A)', 'power', ['q' => 'MPPT solar charge controller 30A LiFePO4'],
            ['12/24 V', 'LiFePO4 support', 'Load output', 'Low-voltage cutoff'],
            'The brain of a shared 12 V solar system. MPPT controllers harvest more in cold and cloudy weather than PWM ones.'],
        'lifepo4' => ['12 V 100 Ah LiFePO4 battery', 'power', ['q' => '12V 100Ah LiFePO4 battery'],
            ['12.8 V', '~1.28 kWh', 'Built-in BMS', 'Thousands of cycles'],
            'Stores several days of power for multi-camera or 24/7 systems. Choose one with low-temperature charge protection in cold climates.'],
        'power-station' => ['Portable power station (300–500 Wh)', 'power', ['q' => 'portable power station 500Wh solar generator'],
            ['300–500 Wh', 'AC + USB-C outputs', 'Solar input', 'Portable'],
            'Runs plug-in cameras, a hotspot or a router for a weekend at a campsite or cabin, and recharges from a folding panel.'],
        // ---- Storage & network ----
        'sd-sandisk' => ['SanDisk High Endurance microSD (128 GB)', 'storage', ['q' => 'SanDisk High Endurance microSDXC 128GB'],
            ['Built for continuous recording', 'U3 / V30', 'Up to 128–256 GB', '2-year warranty'],
            'Surveillance-grade card that tolerates constant rewriting. Check your camera’s maximum supported card size.'],
        'sd-samsung' => ['Samsung PRO Endurance microSD', 'storage', ['q' => 'Samsung PRO Endurance microSD 128GB'],
            ['Endurance-rated', 'U3 / V30', '64–256 GB'],
            'A second endurance-rated option for cameras and dash cams. Format it in the camera, not on a computer.'],
        'outdoor-ap' => ['Outdoor Wi‑Fi access point / mesh extender', 'network', ['q' => 'outdoor wifi access point weatherproof mesh'],
            ['Weatherproof', '2.4 GHz + 5 GHz', 'PoE powered'],
            'Pushes strong Wi‑Fi out to the yard so cameras transmit faster and use less battery.'],
        'wifi-bridge' => ['Point-to-point Wi‑Fi bridge kit', 'network', ['q' => 'point to point wireless bridge outdoor'],
            ['Line-of-sight link', 'Hundreds of meters+', 'Pre-paired pair'],
            'Carries your home internet to a barn, gate or shed with no cable. Needs clear line of sight between the two dishes.'],
        // ---- Mounting & extras ----
        'gutter-mount' => ['Gutter mount for security cameras', 'mount', ['q' => 'gutter mount security camera'],
            ['No drilling', 'Clamps to gutter edge', 'Adjustable arm'],
            'Renter-friendly way to get a camera high on the house without screws in the siding.'],
        'pole-mount' => ['Pole mount bracket with stainless straps', 'mount', ['q' => 'security camera pole mount bracket stainless steel band'],
            ['Fits posts and poles', 'Stainless hose-clamp straps', 'No drilling into the pole'],
            'Mounts a camera or panel on a fence post, light pole or gate post.'],
        'siding-hook' => ['Vinyl siding hooks / clips', 'mount', ['q' => 'vinyl siding hooks no hole heavy duty'],
            ['No holes', 'Slip under siding', 'Light loads only'],
            'For light cameras on vinyl siding. Check the weight rating against your camera and panel.'],
        'antitheft' => ['Anti-theft security mount', 'mount', ['q' => 'anti theft security camera mount lock'],
            ['Lockable bracket', 'Security screws', 'Tether options'],
            'Makes a battery camera much harder to twist off and walk away with: worth it at gates and job sites.'],
        'driveway-alarm' => ['Wireless driveway alarm sensor', 'extra', ['q' => 'wireless driveway alarm motion sensor long range'],
            ['Long-range wireless', 'Weatherproof PIR sensor', 'Indoor chime receiver'],
            'An instant chime when a vehicle passes, independent of Wi‑Fi. Pairs well with a camera at the gate.'],
        'solar-flood' => ['Solar motion flood light', 'extra', ['q' => 'solar motion sensor flood light outdoor'],
            ['Motion activated', 'Separate solar panel', 'No wiring'],
            'Lights the scene so night footage switches to color and intruders know they are seen.'],
        'warning-sign' => ['Video surveillance warning signs', 'extra', ['q' => 'video surveillance warning sign reflective aluminum'],
            ['Reflective aluminum', 'Weatherproof', 'Pre-drilled'],
            'Cheap deterrent that also helps meet notice rules on rental and commercial property.'],
    ];
}

function amazon_link(array $p): string
{
    $src = $p[2];
    if (!empty($src['asin'])) return 'https://www.amazon.com/dp/' . rawurlencode($src['asin']) . '/?tag=' . AMAZON_TAG;
    return 'https://www.amazon.com/s?k=' . rawurlencode($src['q']) . '&tag=' . AMAZON_TAG;
}

function products_grid(array $ids): string
{
    $all = products();
    $label = ['camera' => 'Camera', 'power' => 'Solar & power', 'storage' => 'Storage', 'network' => 'Network', 'mount' => 'Mounting', 'extra' => 'Add-on'];
    $h = '<div class="gear reveal"><p class="gear-title">' . icon('star', 16) . ' Recommended gear</p><div class="gear-grid">';
    foreach ($ids as $id) {
        $id = trim($id);
        if (!isset($all[$id])) continue;
        [$name, $cat, , $chips, $blurb] = $all[$id];
        $h .= '<div class="gear-item"><span class="tag">' . e($label[$cat] ?? $cat) . '</span><h4>' . e($name) . '</h4>'
            . '<ul class="spec-chips">' . implode('', array_map(fn($c) => '<li>' . e($c) . '</li>', $chips)) . '</ul>'
            . '<p>' . e($blurb) . '</p>'
            . '<a class="btn btn-sun btn-sm" href="' . e(amazon_link($all[$id])) . '" rel="sponsored nofollow noopener" target="_blank">View on Amazon</a></div>';
    }
    return $h . '</div><p class="gear-note">Affiliate links. Prices, bundles and specs change, so confirm compatibility on the listing.</p></div>';
}
