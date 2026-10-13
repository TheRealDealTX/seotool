<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'additional-living-expense-calculator',
    'title' => 'Additional Living Expense (ALE) Calculator: Loss of Use Claims',
    'desc' => 'Estimate your additional living expense (Coverage D, loss of use) claim after a fire, flood or storm makes your Houston home unlivable. Free ALE calculator.',
    'h1' => 'Additional Living Expense (ALE) Calculator',
    'lede' => 'When a covered loss makes your home unlivable, Coverage D pays the <em>extra</em> cost of living somewhere else. Estimate what your loss-of-use claim should be.',
    'form' => '
<form data-tool="ale" data-out="out-ale" class="tool-grid">
  <label>Temporary housing per month ($)<input name="housing" inputmode="decimal" value="3200"><span class="hint">Hotel, short-term rental or apartment</span></label>
  <label>Food &amp; meals per month ($)<input name="meals" inputmode="decimal" value="1400"></label>
  <label>Extra mileage / commuting per month ($)<input name="mileage" inputmode="decimal" value="250"></label>
  <label>Utilities, laundry, storage per month ($)<input name="utilities" inputmode="decimal" value="300"></label>
  <label>Other extra costs per month ($)<input name="other" inputmode="decimal" value="150"><span class="hint">Pet boarding, moving, furniture rental</span></label>
  <label>Normal monthly housing cost ($)<input name="normal_housing" inputmode="decimal" value="0"><span class="hint">Mortgage keeps going? Enter 0. Renters: your rent if you no longer pay it</span></label>
  <label>Normal monthly grocery spend ($)<input name="normal_food" inputmode="decimal" value="800"></label>
  <label>Months displaced<input name="months" inputmode="decimal" value="6"></label>
  <label>Coverage D limit ($)<input name="limit" inputmode="decimal" value="70000"><span class="hint">Often 20%&ndash;30% of Coverage A</span></label>
</form>
<div class="tool-result" id="out-ale" aria-live="polite"></div>',
    'prose' => '
<h2>What additional living expense covers</h2>
<p>Additional living expense (ALE), also called loss of use or Coverage D, reimburses the increase in your cost of living while your home is being repaired. It is not a flat per-diem; it is the difference between what you normally spend and what you are spending now. After Harvey, Uri and Beryl, many Houston families found ALE cut off before their homes were livable because repairs took longer than the insurer assumed.</p>
<ul class="checklist">
  <li>Hotel or rental housing comparable to your home</li>
  <li>Restaurant meals beyond your normal grocery bill</li>
  <li>Extra mileage to work and school</li>
  <li>Laundry, storage, pet boarding and furniture rental</li>
  <li>Evacuation costs when a civil authority orders you out</li>
</ul>
<p>Keep every receipt and a simple monthly log. Use our <a href="/tools/contents-inventory/">contents inventory builder</a> for the belongings side of the claim.</p>',
    'faqs' => [
        ['How long does ALE last?', 'For the shortest reasonable time needed to repair or replace the home, or until you settle elsewhere, subject to the Coverage D limit. Some policies also have a time limit, such as 12 or 24 months.'],
        ['Does ALE cover my mortgage?', 'No. You keep paying the mortgage. ALE covers the additional costs on top of your normal expenses.'],
    ],
]);
