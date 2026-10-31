<?php
/**
 * SHARED SITE FOOTER. Edit here to change footer links or text everywhere.
 */
defined('RT_APP') || exit;
?>
</main>
<footer class="site-footer">
  <div class="wrap site-footer__grid">
    <div>
      <p class="site-footer__brand">Rodeo Texas</p>
      <p>An independent guide to rodeos held in Texas — from PRCA pro rodeos to youth, high school and ranch rodeos.
        Listings come from official organizer sources and reviewed submissions. Always confirm details with the organizer before you travel.</p>
    </div>
    <nav aria-label="Rodeos">
      <p class="site-footer__h">Rodeos</p>
      <ul>
        <li><a href="/rodeos/">All upcoming rodeos</a></li>
        <li><a href="/rodeos/?when=weekend">This weekend</a></li>
        <li><a href="/rodeos/?when=month">This month</a></li>
        <li><a href="/rodeos/?view=calendar">Calendar</a></li>
        <li><a href="/rodeos/?view=map">Map</a></li>
        <li><a href="/past-events/">Past events</a></li>
      </ul>
    </nav>
    <nav aria-label="About">
      <p class="site-footer__h">Rodeo Texas</p>
      <ul>
        <li><a href="/about/">About &amp; data sources</a></li>
        <li><a href="/blog/">Rodeo guide articles</a></li>
        <li><a href="/submit-event/">Submit an event</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
      </ul>
    </nav>
  </div>
  <div class="wrap site-footer__legal">
    <p>&copy; <?= e(date('Y')) ?> Rodeo Texas. Not affiliated with PRCA, PRORODEO or any rodeo association. Map data &copy; OpenStreetMap contributors.</p>
    <p>As an Amazon Associate, Rodeo Texas earns from qualifying purchases.</p>
  </div>
</footer>
