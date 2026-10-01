<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/**
 * Photo registry. Every photo is an openly licensed image from Wikimedia
 * Commons, cropped to 3:2 and resized to 480/960/1600px WebP. These are
 * illustrative stock photos, NOT Friendswood Roofers projects; captions and
 * the /image-credits/ page say so. Replace with the company's own photos
 * when available (keep the same file names and sizes, or add new keys).
 */
return [
    'hero-roofing-crew' => [
        'alt' => 'Roofing crew replacing asphalt shingles on a single-story brick home',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'FEMA - 44364 - Roof repair workers in Oklahoma',
        'author' => 'Win Henderson / FEMA',
        'license' => 'Public domain', 'license_url' => '',
        'source' => 'https://commons.wikimedia.org/wiki/File:FEMA_-_44364_-_Roof_repair_workers_in_Oklahoma.jpg',
    ],
    'shingle-damage' => [
        'alt' => 'Close-up of asphalt shingles with torn and missing tabs',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Asphalt shingles damage',
        'author' => 'Samuel Bolton',
        'license' => 'CC BY-SA 4.0', 'license_url' => 'https://creativecommons.org/licenses/by-sa/4.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Asphalt_shingles_damage.jpg',
    ],
    'shingle-bundles-on-roof' => [
        'alt' => 'Bundles of new shingles staged on a roof ridge above a gutter',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Shingles atop roof',
        'author' => 'Joe Mabel',
        'license' => 'CC BY 4.0', 'license_url' => 'https://creativecommons.org/licenses/by/4.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Shingles_atop_roof.jpg',
    ],
    'worn-shingles-eaves' => [
        'alt' => 'Aged asphalt shingles with curling edges and granule loss near the eaves',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Faster wear of asphalt shingles along eaves',
        'author' => 'Dale Mahalko',
        'license' => 'CC BY-SA 3.0', 'license_url' => 'https://creativecommons.org/licenses/by-sa/3.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Faster_wear_of_asphalt_shingles_along_eaves.JPG',
    ],
    'wind-damaged-roof' => [
        'alt' => 'House roof with patches of shingles blown off by high wind',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'WindDamageRoof',
        'author' => 'Infrogmation',
        'license' => 'CC BY-SA 2.5', 'license_url' => 'https://creativecommons.org/licenses/by-sa/2.5/',
        'source' => 'https://commons.wikimedia.org/wiki/File:WindDamageRoof.jpg',
    ],
    'asphalt-shingles-closeup' => [
        'alt' => 'Rows of gray architectural asphalt shingles on a residential roof',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Shingle Roof 1 2017-04-21',
        'author' => 'FASTILY',
        'license' => 'CC BY-SA 4.0', 'license_url' => 'https://creativecommons.org/licenses/by-sa/4.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Shingle_Roof_1_2017-04-21.jpg',
    ],
    'standing-seam-metal-roof' => [
        'alt' => 'Aerial view of a single-story home with a gray standing seam metal roof',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Standing seam metal roof low pitch roof-2',
        'author' => 'Wikideas1',
        'license' => 'CC0 1.0', 'license_url' => 'https://creativecommons.org/publicdomain/zero/1.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Standing_seam_metal_roof_low_pitch_roof-2.jpg',
    ],
    'metal-roof-aerial' => [
        'alt' => 'Overhead view of a low-pitch standing seam metal roof on a ranch-style house',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Standing seam metal roof low pitch roof-3',
        'author' => 'Wikideas1',
        'license' => 'CC0 1.0', 'license_url' => 'https://creativecommons.org/publicdomain/zero/1.0/',
        'source' => 'https://commons.wikimedia.org/wiki/File:Standing_seam_metal_roof_low_pitch_roof-3.jpg',
    ],
    'roof-cleaning-maintenance' => [
        'alt' => 'Roof professional using a low-pressure sprayer to clean a shingle roof',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'UglyShinglesMichigan3',
        'author' => 'Uglyshingles (Wikimedia Commons user)',
        'license' => 'Public domain', 'license_url' => '',
        'source' => 'https://commons.wikimedia.org/wiki/File:UglyShinglesMichigan3.JPG',
    ],
    'roofing-crew-trucks' => [
        'alt' => 'Work trucks parked beside a building while a crew works on its roof',
        'w' => 1600, 'h' => 1067, 'widths' => [480, 960, 1600],
        'title' => 'Getting a new roof (5954796326)',
        'author' => 'USDA Forest Service, Northern Region',
        'license' => 'Public domain', 'license_url' => '',
        'source' => 'https://commons.wikimedia.org/wiki/File:Getting_a_new_roof_(5954796326).jpg',
    ],
];
