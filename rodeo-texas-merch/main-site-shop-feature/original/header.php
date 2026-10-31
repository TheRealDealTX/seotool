<?php
/**
 * SHARED SITE HEADER: logo and main navigation. Edit the $__nav array to change
 * menu items everywhere.
 */
defined('RT_APP') || exit;

$__nav = [
    ['/rodeos/', 'Find rodeos'],
    ['/rodeos/?when=weekend', 'This weekend'],
    ['/past-events/', 'Past events'],
    ['/blog/', 'Rodeo guide'],
    ['/submit-event/', 'Submit an event'],
];
$__here = request_path();
?>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="Rodeo Texas home">
      <svg class="brand__mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">
        <circle cx="32" cy="32" r="29" fill="#7a3b1b"/>
        <circle cx="32" cy="32" r="25" fill="none" stroke="#e9c77b" stroke-width="2" stroke-dasharray="4 3"/>
        <path d="M32 13l5.3 11 12.1 1.7-8.8 8.5 2.1 12L32 40.5 21.3 46.2l2.1-12-8.8-8.5 12.1-1.7z" fill="#f4e6c8"/>
      </svg>
      <span class="brand__text"><span class="brand__name">Rodeo Texas</span><span class="brand__tag">The Lone Star rodeo schedule</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">
      <span class="nav-toggle__bar"></span><span class="visually-hidden">Menu</span>
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
        <?php foreach ($__nav as [$__href, $__label]):
            $__active = strtok($__href, '?') === $__here && !str_contains($__href, '?'); ?>
          <li><a href="<?= e($__href) ?>"<?= $__active ? ' aria-current="page"' : '' ?>><?= e($__label) ?></a></li>
        <?php endforeach; ?>
        <li><a class="nav-favs" href="/favorites/">Favorites <span class="fav-count" data-fav-count hidden>0</span></a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main" tabindex="-1">
