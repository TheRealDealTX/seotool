<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Timer schedules';
$P['lead'] = 'Look up sunset and civil dusk for Texas cities on any date, with month-by-month timer settings for your landscape lighting.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_dusk(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>When Should Landscape Lights Turn On?</h2>
<p>Lights look best when they come on just after sunset, while there is still deep blue in the sky — designers call this the <em>blue hour</em>. Switching on 10–20 minutes after sunset lets the lighting build as the sky darkens instead of looking washed out by daylight.</p>
<p>Texas sunsets swing a lot through the year. In Austin, sunset moves from around 5:30 pm in early December to nearly 8:40 pm in late June, and daylight saving time shifts everything by an hour in March and November. A simple clock timer that is never adjusted ends up switching on in daylight half the year and in darkness the other half.</p>
<h2>Timer Options</h2>
<ul>
<li><strong>Photocell:</strong> turns lights on at dusk automatically. Mount it where your own fixtures and porch lights won't fool it.</li>
<li><strong>Astronomical timer:</strong> calculates sunset for your location every day — no adjustments, no photocell drift. This is what we install on most systems.</li>
<li><strong>Smart controller:</strong> sunset-based schedules plus app control, dimming and scenes. See <a href="/services/smart-lighting-systems/">smart lighting systems</a>.</li>
</ul>
<p>Pair your schedule with an off time that suits your street — 11 pm or midnight for most neighborhoods, or dusk-to-dawn on a low-output path zone for safety. The <a href="/tools/energy-savings-calculator/">energy calculator</a> shows how little LED lights cost to run either way.</p>

  </div>
</section>
<?php faqs([
    ['What time do landscape lights usually turn on?', 'About 10–20 minutes after sunset. Use the tool above to find the exact time for your city and date.'],
    ['Should landscape lights stay on all night?', 'Most homeowners turn decorative zones off at 11 pm or midnight and leave a low path or security zone on until dawn.'],
    ['Do I need to adjust my timer for daylight saving time?', 'Basic clock timers need adjusting; astronomical timers and smart controllers adjust automatically.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/dusk-timer/'); ?>
  </div>
</section>
<?php cta_band();
