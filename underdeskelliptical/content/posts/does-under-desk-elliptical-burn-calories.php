<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// GSC (6 mo): "under desk elliptical calories burned" 12 impr at 44, "calories burned under desk elliptical",
// "does under desk elliptical burn calories" (37.9), "how many calories does under desk elliptical burn",
// "under desk elliptical calories burned calculator" (16), "do under desk ellipticals burn calories",
// "under desk elliptical calories", "does an (under the) desk elliptical burn calories".
// Table: kcal/hr = MET x 3.5 x kg / 200 x 60, kg = lb / 2.2046, rounded to nearest 5.
return [
    'title' => 'Under Desk Elliptical Calories Burned: Chart + Calculator',
    'description' => 'Under desk elliptical calories burned by body weight and effort: a clear per-hour chart, a free calculator, and how much extra you burn vs just sitting.',
    'h1' => 'Under Desk Elliptical Calories Burned: How Many Per Hour, by Weight',
    'keyword' => 'under desk elliptical calories burned',
    'category' => 'health-benefits',
    'tags' => ['desk-exercise', 'active-sitting', 'fitness-while-working'],
    'published' => '2026-05-18',
    'updated' => '2026-10-22',
    'image' => '/wp-content/uploads/2026/05/Does-Under-Desk-Elliptical-Burn-Calories-1.webp',
    'image_alt' => 'Under desk elliptical calories burned display on a seated pedal machine under a desk',
    'excerpt' => 'How many calories an under desk elliptical burns per hour at your weight and effort, how much of that is extra over sitting, and how to burn more.',
    'summary' => <<<'HTML'
<p>Yes, an under desk elliptical burns calories. Most people burn roughly <strong>115 to 320 calories per hour</strong> depending on body weight and effort, or about 40 to 170 more than sitting still. A 150 lb person pedaling at a moderate pace burns around 200 calories an hour. Adjustable magnetic resistance, as on the [[amazon:cubii-jr2]], lets you push that higher.</p>
HTML,
    'related' => ['can-you-lose-weight-with-under-desk-elliptical', 'what-muscles-does-an-under-desk-elliptical-work', 'under-desk-elliptical-benefits', 'is-an-under-desk-elliptical-good-exercise'],
    'faq' => [
        ['q' => 'How many calories does an under desk elliptical burn?', 'a' => 'Roughly 115 to 320 calories per hour for most adults, depending on body weight and how hard you pedal. A 150 lb person burns about 145 calories an hour at a light pace and about 200 at a moderate pace.'],
        ['q' => 'How many calories does 30 minutes on an under desk elliptical burn?', 'a' => 'Half the hourly figure: about 70 to 100 calories at a light to moderate pace for a 150 lb person, and more if you weigh more or pedal harder. Use the <a href="/tools/under-desk-elliptical-calorie-calculator/">calorie calculator</a> for your numbers.'],
        ['q' => 'Is the calorie count on the elliptical display accurate?', 'a' => 'Treat it as a rough guide. Most built-in displays do not know your weight or measure your effort directly, so they can over- or underestimate. A heart-rate tracker or a MET-based calculator gives a more personal estimate.'],
        ['q' => 'Do motorized under desk ellipticals burn calories?', 'a' => 'Very few in passive mode, because the motor does the work and your effort stays close to sitting. If you pedal along with the motor or use the manual mode, you burn about as much as on a manual machine.'],
        ['q' => 'Does an under desk elliptical burn more calories than a desk bike?', 'a' => 'They are similar at the same effort. Calories depend on how hard you work, not the shape of the pedal path. See <a href="/under-desk-elliptical-vs-bike/">under desk elliptical vs bike</a> for the other differences.'],
    ],
    'body' => <<<'HTML'
<p>Yes, an under desk elliptical burns calories, and the amount is easy to estimate. For most adults, <strong>under desk elliptical calories burned</strong> land between about 115 and 320 per hour, depending on how much you weigh and how hard you pedal. Heavier people and harder effort burn more.</p>
<p>The more useful number is the <em>extra</em> burn compared with sitting still, because you would be burning some calories in your chair anyway. That extra is roughly 40 to 170 calories per hour. Spread across a workday, it adds up to a meaningful amount, though not a dramatic one. Below you will find a chart by body weight, a calculator for your own numbers, and practical ways to burn more without losing focus at work.</p>

<h2>Under Desk Elliptical Calories Burned Per Hour (Chart)</h2>
<p>This chart uses MET values from the Compendium of Physical Activities, the standard reference researchers use to compare activities. A MET (metabolic equivalent) of 1 is your energy use at complete rest. Sitting quietly is about 1.3 METs. Light seated pedaling is about 2.0, moderate is about 2.8 and hard pedaling with resistance is about 3.5.</p>
<div class="table-wrap"><table>
<thead><tr><th>Body weight</th><th>Light (MET 2.0)</th><th>Moderate (MET 2.8)</th><th>Hard (MET 3.5)</th></tr></thead>
<tbody>
<tr><td>120 lb (54 kg)</td><td>115 kcal/hr</td><td>160 kcal/hr</td><td>200 kcal/hr</td></tr>
<tr><td>150 lb (68 kg)</td><td>145 kcal/hr</td><td>200 kcal/hr</td><td>250 kcal/hr</td></tr>
<tr><td>180 lb (82 kg)</td><td>170 kcal/hr</td><td>240 kcal/hr</td><td>300 kcal/hr</td></tr>
<tr><td>210 lb (95 kg)</td><td>200 kcal/hr</td><td>280 kcal/hr</td><td>350 kcal/hr</td></tr>
<tr><td>240 lb (109 kg)</td><td>230 kcal/hr</td><td>320 kcal/hr</td><td>400 kcal/hr</td></tr>
</tbody></table></div>
<p>The formula behind it is: calories per minute = MET × 3.5 × body weight in kg ÷ 200. Multiply by 60 for an hour. Figures are rounded to the nearest 5 calories. Individual results vary with fitness, muscle mass and how steadily you pedal, so think of these as reasonable estimates, not lab measurements.</p>
<div class="callout"><p><strong>What the effort levels feel like:</strong> light means you could sing, and you can type without thinking about your legs. Moderate means you can talk in full sentences but you are breathing a bit faster. Hard means short sentences only, which is fine for a podcast or a muted call but not for writing an email.</p></div>

<h2>Calories Burned vs Sitting: The Number That Matters</h2>
<p>At a desk you already burn about 1.3 METs. So the extra calories from pedaling are the gap between the pedaling MET and 1.3. Here is that gap for a few body weights:</p>
<div class="table-wrap"><table>
<thead><tr><th>Body weight</th><th>Extra per hour, light</th><th>Extra per hour, moderate</th><th>Extra per 2-hour workday, moderate</th></tr></thead>
<tbody>
<tr><td>150 lb</td><td>about 50</td><td>about 105</td><td>about 215</td></tr>
<tr><td>180 lb</td><td>about 60</td><td>about 130</td><td>about 255</td></tr>
<tr><td>210 lb</td><td>about 70</td><td>about 150</td><td>about 300</td></tr>
</tbody></table></div>
<p>That is the honest picture: an under desk elliptical turns idle sitting time into light activity. Two hours at a moderate pace over a workday is roughly a snack's worth of extra calories, every day you do it. It is not a replacement for a run, but it costs you no extra time. If weight loss is your goal, our guide on whether <a href="/can-you-lose-weight-with-under-desk-elliptical/">you can lose weight with an under desk elliptical</a> runs the full math.</p>

<h2>Under Desk Elliptical Calories Burned Calculator</h2>
<p>Enter your weight, how long you pedal and roughly how hard. The calculator uses the same MET approach as the chart and also shows your extra burn over sitting, per session, week and month.</p>
[[tool:calories]]
<p>You can also open the full <a href="/tools/under-desk-elliptical-calorie-calculator/">under desk elliptical calorie calculator</a> on its own page and bookmark it.</p>

<h2>How Many Calories Does an Under Desk Elliptical Burn Per Session?</h2>
<p>Few people pedal for a solid hour. Most use the machine in blocks between meetings or during calls. Here is what common session lengths look like for a 180 lb person, using the chart figures:</p>
<div class="table-wrap"><table>
<thead><tr><th>Session</th><th>Light effort</th><th>Moderate effort</th><th>Per 5-day work week (moderate)</th></tr></thead>
<tbody>
<tr><td>15 minutes</td><td>about 45 kcal</td><td>about 60 kcal</td><td>about 300 kcal</td></tr>
<tr><td>30 minutes</td><td>about 85 kcal</td><td>about 120 kcal</td><td>about 600 kcal</td></tr>
<tr><td>1 hour</td><td>about 170 kcal</td><td>about 240 kcal</td><td>about 1,200 kcal</td></tr>
<tr><td>2 hours (in blocks)</td><td>about 345 kcal</td><td>about 480 kcal</td><td>about 2,400 kcal</td></tr>
</tbody></table></div>
<p>Remember these are total calories, including what you would burn sitting. Only about a third of the light-pace total is extra over sitting, and a little over half of the moderate-pace total, which is why effort matters as much as minutes. A practical target for most office workers is 60 to 120 minutes a day, split into blocks of 15 to 30 minutes. That is long enough to matter and short enough to stay comfortable.</p>

<h2>How It Compares With Walking and Other Desk Options</h2>
<p>Walking at about 3 mph sits around 3.5 METs in the Compendium, the same as the "hard" column in our chart. So an under desk elliptical at a hard effort burns about as much as a steady walk, while light pedaling burns a bit more than half as much. The difference is that you can pedal while you type, and most people cannot walk and write at the same time.</p>
<ul>
<li><strong>Desk bike:</strong> similar burn at the same effort. The circular stroke feels more like cycling and asks a little more of the knees. Our <a href="/under-desk-elliptical-vs-bike/">under desk elliptical vs bike</a> comparison goes deeper.</li>
<li><strong>Walking pad:</strong> burns more per hour because you carry your body weight, but it needs a standing desk and makes precise mouse work harder. A model like the [[amazon:walkingpad-c2|WalkingPad C2]] is the usual pick if you go that route. See <a href="/under-desk-elliptical-vs-walking-pad/">under desk elliptical vs walking pad</a>.</li>
<li><strong>Standing still:</strong> only slightly more than sitting. Standing is good for changing position, but it is not a meaningful calorie burner on its own.</li>
</ul>
<p>The best option is the one you will use for the most minutes. For many desk workers that is the seated elliptical, simply because it does not compete with the work itself.</p>

<h2>What Affects How Many Calories You Burn</h2>
<h3>Body weight</h3>
<p>Moving a heavier body takes more energy, even when seated, because your legs are heavier and your body uses more energy overall. That is why the chart rises steadily with weight.</p>
<h3>Resistance and pace</h3>
<p>This is the factor you control. Going from light to moderate effort raises your burn by about 40 percent. Magnetic resistance is the smoothest way to do it. Machines with a wider resistance range, like the [[amazon:deskcycle-ellipse|DeskCycle Ellipse]], give you more room to work harder as you get fitter.</p>
<h3>Manual vs motorized</h3>
<p>A motorized machine such as the [[amazon:ancheer|ANCHEER]] moves your legs for you. In passive mode, your calorie burn stays close to sitting. These machines are valuable for circulation and limited mobility, but if calories are the goal, pedal along with the motor or choose a manual model. See our <a href="/manual-under-desk-elliptical/">manual under desk elliptical</a> guide.</p>
<h3>Time in the saddle</h3>
<p>Duration matters more than intensity for most desk users, because you can keep a light pace going for hours. Three 30-minute blocks a day add up faster than one hard 15-minute burst you dread.</p>

<h2>Are the Calories on the Display Accurate?</h2>
<p>Most displays estimate under desk elliptical calories burned from strides or revolutions, often without knowing your weight or the resistance setting. They can read high or low. Use them to track consistency (more strides this week than last week) rather than as an exact calorie count.</p>
<p>For a better personal estimate, use the chart above, or wear a tracker with heart-rate monitoring. A heart-rate tracker like the [[amazon:fitbit-charge-6|Fitbit Charge 6]] shows whether you are really reaching a moderate effort. Wrist trackers often miss seated pedaling as steps, though. Our guide on whether an <a href="/does-under-desk-elliptical-count-as-steps/">under desk elliptical counts as steps</a> explains how to log sessions properly.</p>

<h2>How to Burn More Calories on an Under Desk Elliptical</h2>
<ol>
<li><strong>Match effort to the task.</strong> Light resistance while typing, moderate during calls on mute, video or reading.</li>
<li><strong>Add short intervals.</strong> One minute faster, two minutes easy, five rounds. It raises your average effort without wrecking concentration.</li>
<li><strong>Pedal backward sometimes.</strong> It brings in more of the hamstrings and glutes and keeps long sessions from feeling stale. See <a href="/what-muscles-does-an-under-desk-elliptical-work/">what muscles an under desk elliptical works</a>.</li>
<li><strong>Stop the machine sliding.</strong> If you hold back because the machine creeps forward, a [[amazon:cubii-mat|non-slip mat]] fixes it. A rolling chair needs [[amazon:caster-cups|caster cups]].</li>
<li><strong>Use a timer.</strong> Short, scheduled blocks are easier to keep up than "whenever I remember." Our <a href="/tools/desk-pedal-timer/">desk pedal timer</a> handles the reminders.</li>
</ol>

<h2>Best Under Desk Ellipticals for Burning Calories</h2>
<p>For calorie burn, you want a manual machine with enough resistance range to reach moderate or hard effort, and quiet enough that you will actually use it during work. Based on specs and owner reviews:</p>
[[product:cubii-jr2|1]]
[[product:deskcycle-ellipse|2]]
[[product:sunny-sf-e3872|3]]
[[compare:cubii-jr2,deskcycle-ellipse,sunny-sf-e3872,lifepro-flexstride]]
<p>The [[amazon:lifepro-flexstride|Lifepro FlexStride]] is another option with a wide resistance range if you want to work harder. For the full rundown, see the <a href="/what-is-the-best-under-desk-elliptical/">best under desk ellipticals</a>.</p>

<h2>Verdict: Does an Under Desk Elliptical Burn Calories?</h2>
<p>It does. Expect roughly 115 to 320 calories per hour in total, or about 40 to 170 more than sitting, based on your weight and effort. The value comes from volume: an hour or two of easy pedaling during work you would be doing anyway. Pair it with sensible eating and some regular exercise and it becomes a useful part of your daily energy balance.</p>
<p>If you are ready to start, the [[amazon:cubii-jr2]] is the easiest machine to use for hours at a time. Curious what else it can do for you? Read about the wider <a href="/under-desk-elliptical-benefits/">under desk elliptical benefits</a>.</p>
[[button:cubii-jr2|Check the Cubii JR2 on Amazon]]
HTML,
];
