"""Interactive tool pages. Each tool's widget markup is wired up by assets/js/tools.js
through its data-tool attribute; the copy below the widget is the page's indexable content."""

TOOLS = [
    {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "short": "Check your body mass index and healthy weight range.",
        "seo_title": "BMI Calculator: Check Your Body Mass Index",
        "description": "Free BMI calculator with metric and imperial units. See your body mass index, category and the healthy weight range for your height in seconds.",
        "keyword": "bmi calculator",
        "image": "core-crunches",
        "icon": "gauge",
        "widget": """
<form class="tool-form" data-tool="bmi" novalidate>
  <div class="seg" role="radiogroup" aria-label="Units">
    <label><input type="radio" name="units" value="imperial" checked><span>US (ft / lb)</span></label>
    <label><input type="radio" name="units" value="metric"><span>Metric (cm / kg)</span></label>
  </div>
  <div class="field-row" data-units="imperial">
    <label class="field"><span>Height (ft)</span><input type="number" name="ft" min="3" max="8" value="5" inputmode="numeric"></label>
    <label class="field"><span>Height (in)</span><input type="number" name="in" min="0" max="11" value="7" inputmode="numeric"></label>
    <label class="field"><span>Weight (lb)</span><input type="number" name="lb" min="50" max="700" value="160" inputmode="decimal"></label>
  </div>
  <div class="field-row" data-units="metric" hidden>
    <label class="field"><span>Height (cm)</span><input type="number" name="cm" min="100" max="250" value="170" inputmode="decimal"></label>
    <label class="field"><span>Weight (kg)</span><input type="number" name="kg" min="25" max="320" value="72" inputmode="decimal"></label>
  </div>
</form>
<div class="tool-result" data-out="bmi" aria-live="polite">
  <div class="gauge">
    <div class="gauge-track"><span class="g-under"></span><span class="g-normal"></span><span class="g-over"></span><span class="g-obese"></span></div>
    <div class="gauge-needle" data-bmi-needle></div>
    <div class="gauge-labels"><span>15</span><span>18.5</span><span>25</span><span>30</span><span>40</span></div>
  </div>
  <div class="result-grid">
    <div class="stat"><span class="stat-label">Your BMI</span><b class="stat-big" data-bmi-value>&ndash;</b></div>
    <div class="stat"><span class="stat-label">Category</span><b data-bmi-cat>&ndash;</b></div>
    <div class="stat"><span class="stat-label">Healthy weight for your height</span><b data-bmi-range>&ndash;</b></div>
  </div>
</div>
""",
        "body": """
<h2>How this BMI calculator works</h2>
<p>Body mass index (BMI) is your weight in kilograms divided by your height in meters squared. In US units the formula is weight in pounds &times; 703 &divide; height in inches squared. The calculator updates as you type and shows where you land on the standard adult ranges used by the CDC and the World Health Organization.</p>
<div class="table-wrap"><table><thead><tr><th>BMI</th><th>Category</th></tr></thead><tbody>
<tr><td>Below 18.5</td><td>Underweight</td></tr><tr><td>18.5 &ndash; 24.9</td><td>Healthy weight</td></tr>
<tr><td>25 &ndash; 29.9</td><td>Overweight</td></tr><tr><td>30 and above</td><td>Obesity</td></tr></tbody></table></div>
<h2>What BMI can and can't tell you</h2>
<p>BMI is a quick screening number, not a diagnosis. It doesn't know how much of your weight is muscle, so strong, athletic people often score as &ldquo;overweight&rdquo; while carrying little body fat. It also says nothing about where fat is stored, which matters for health. Pair it with your waist measurement, how you feel, your energy and your bloodwork, and talk to your doctor before making big changes.</p>
<p>BMI ranges for children and teens are age and sex specific percentiles, so this calculator is for adults 20 and older.</p>
<h2>Next steps</h2>
<p>If you want to change your weight, the most useful next number is your daily calorie target. Try the <a href="/tools/calorie-calculator/">calorie calculator</a>, then read our guide on <a href="/how-to-calculate-a-calorie-deficit/">how to calculate a calorie deficit</a> and these <a href="/essential-ways-to-lose-weight-naturally/">29 ways to lose weight naturally</a>.</p>
""",
        "faq": [
            {"q": "What is a healthy BMI?", "a": "For adults, a BMI from 18.5 to 24.9 is classed as a healthy weight range."},
            {"q": "Is BMI accurate for athletes?", "a": "Not very. BMI can't tell muscle from fat, so muscular people often score higher than their body fat would suggest."},
            {"q": "Can I use this BMI calculator for kids?", "a": "No. Children and teens use age- and sex-specific BMI percentiles, so ask a pediatrician or use a child BMI chart."},
        ],
    },
    {
        "slug": "calorie-calculator",
        "name": "Calorie Calculator",
        "short": "Estimate your TDEE and daily calories to lose, maintain or gain.",
        "seo_title": "Calorie Calculator: Daily Calories & TDEE",
        "description": "Estimate your BMR, TDEE and daily calories to lose, maintain or gain weight with this free calorie calculator, plus a simple protein, carb and fat split.",
        "keyword": "calorie calculator",
        "image": "balanced-plate",
        "icon": "flame",
        "widget": """
<form class="tool-form" data-tool="calories" novalidate>
  <div class="seg" role="radiogroup" aria-label="Units">
    <label><input type="radio" name="units" value="imperial" checked><span>US</span></label>
    <label><input type="radio" name="units" value="metric"><span>Metric</span></label>
  </div>
  <div class="seg" role="radiogroup" aria-label="Sex">
    <label><input type="radio" name="sex" value="f" checked><span>Female</span></label>
    <label><input type="radio" name="sex" value="m"><span>Male</span></label>
  </div>
  <div class="field-row">
    <label class="field"><span>Age</span><input type="number" name="age" min="15" max="90" value="32" inputmode="numeric"></label>
  </div>
  <div class="field-row" data-units="imperial">
    <label class="field"><span>Height (ft)</span><input type="number" name="ft" min="3" max="8" value="5" inputmode="numeric"></label>
    <label class="field"><span>Height (in)</span><input type="number" name="in" min="0" max="11" value="6" inputmode="numeric"></label>
    <label class="field"><span>Weight (lb)</span><input type="number" name="lb" min="70" max="700" value="165" inputmode="decimal"></label>
  </div>
  <div class="field-row" data-units="metric" hidden>
    <label class="field"><span>Height (cm)</span><input type="number" name="cm" min="120" max="250" value="168" inputmode="decimal"></label>
    <label class="field"><span>Weight (kg)</span><input type="number" name="kg" min="30" max="320" value="75" inputmode="decimal"></label>
  </div>
  <label class="field"><span>Activity level</span>
    <select name="activity">
      <option value="1.2">Mostly sitting (little exercise)</option>
      <option value="1.375" selected>Light (exercise 1&ndash;3 days/week)</option>
      <option value="1.55">Moderate (exercise 3&ndash;5 days/week)</option>
      <option value="1.725">Very active (6&ndash;7 days/week)</option>
      <option value="1.9">Athlete / physical job + training</option>
    </select>
  </label>
</form>
<div class="tool-result" aria-live="polite">
  <div class="result-grid">
    <div class="stat"><span class="stat-label">BMR (at rest)</span><b data-cal="bmr">&ndash;</b></div>
    <div class="stat"><span class="stat-label">Maintenance (TDEE)</span><b class="stat-big" data-cal="tdee">&ndash;</b></div>
  </div>
  <div class="goal-cards">
    <div class="goal goal-lose"><span>Lose ~0.5&ndash;1 lb/week</span><b data-cal="lose">&ndash;</b><small>calories / day</small></div>
    <div class="goal goal-keep"><span>Maintain</span><b data-cal="keep">&ndash;</b><small>calories / day</small></div>
    <div class="goal goal-gain"><span>Lean gain</span><b data-cal="gain">&ndash;</b><small>calories / day</small></div>
  </div>
  <p class="macro-title">Sample macro split at your fat-loss target</p>
  <div class="macro-bar"><span class="m-p" data-macro="p"></span><span class="m-c" data-macro="c"></span><span class="m-f" data-macro="f"></span></div>
  <ul class="macro-legend"><li><i class="m-p"></i>Protein <b data-macro-g="p">&ndash;</b></li><li><i class="m-c"></i>Carbs <b data-macro-g="c">&ndash;</b></li><li><i class="m-f"></i>Fat <b data-macro-g="f">&ndash;</b></li></ul>
</div>
""",
        "body": """
<h2>How the calorie calculator works</h2>
<p>We estimate your basal metabolic rate (BMR) with the Mifflin-St Jeor equation, the formula most dietitians use today, then multiply it by an activity factor to get your total daily energy expenditure (TDEE), the calories you burn on an average day.</p>
<ol class="steps">
<li><strong>BMR.</strong> Men: 10 &times; weight (kg) + 6.25 &times; height (cm) &minus; 5 &times; age + 5. Women: the same, minus 161 instead of plus 5.</li>
<li><strong>TDEE.</strong> BMR &times; activity factor (1.2 to 1.9).</li>
<li><strong>Goal.</strong> Fat loss uses a moderate deficit of about 20% (never below a sensible floor), lean gain adds about 10%.</li>
</ol>
<h2>Using your numbers</h2>
<p>Treat the result as a starting point. Track your weight for two to three weeks: if the trend isn't moving the way you want, adjust by 100 to 200 calories. Keep protein high while losing weight so more of what you lose is fat, not muscle. Our <a href="/tools/protein-calculator/">protein calculator</a> gives you a daily target.</p>
<p>Want the full walk-through with a worked example? Read <a href="/how-to-calculate-a-calorie-deficit/">how to calculate a calorie deficit</a>, then fill your plate with these <a href="/healthy-breakfast-foods-for-weight-loss/">healthy breakfast foods for weight loss</a>.</p>
<div class="callout callout-warn"><strong>Heads up:</strong> If you are pregnant, breastfeeding, under 18, or managing a medical condition, get calorie targets from your doctor or a registered dietitian.</div>
""",
        "faq": [
            {"q": "What is TDEE?", "a": "Total daily energy expenditure: the calories you burn in a day from your resting metabolism, digestion, daily movement and exercise."},
            {"q": "How big should a calorie deficit be?", "a": "For most people a deficit of roughly 300 to 500 calories a day, or about 20% below maintenance, is sustainable and protects muscle."},
            {"q": "Why isn't my weight changing at the calculated calories?", "a": "Calculators are estimates. Water shifts hide fat loss for a week or two, so watch the multi-week trend and adjust by 100 to 200 calories if needed."},
        ],
    },
    {
        "slug": "protein-calculator",
        "name": "Protein Calculator",
        "short": "Find your daily protein target and how much to eat per meal.",
        "seo_title": "Protein Calculator: How Much Protein Per Day?",
        "description": "Work out how much protein you need per day for your goal, from general health to building muscle, and see it split per meal with easy food examples.",
        "keyword": "protein calculator",
        "image": "salmon-protein-bowl",
        "icon": "egg",
        "widget": """
<form class="tool-form" data-tool="protein" novalidate>
  <div class="field-row">
    <label class="field"><span>Body weight</span><input type="number" name="w" min="30" max="700" value="165" inputmode="decimal"></label>
    <div class="seg seg-inline" role="radiogroup" aria-label="Weight unit">
      <label><input type="radio" name="unit" value="lb" checked><span>lb</span></label>
      <label><input type="radio" name="unit" value="kg"><span>kg</span></label>
    </div>
  </div>
  <label class="field"><span>Your goal</span>
    <select name="goal">
      <option value="0.8,1.0">General health (mostly inactive)</option>
      <option value="1.1,1.4">Active lifestyle / endurance training</option>
      <option value="1.6,2.2" selected>Build muscle (lifting 3+ days/week)</option>
      <option value="1.6,2.4">Lose fat and keep muscle</option>
      <option value="1.0,1.2">Healthy aging (65+)</option>
    </select>
  </label>
  <label class="field"><span>Meals per day: <b data-out-meals>4</b></span><input type="range" name="meals" min="2" max="6" value="4"></label>
</form>
<div class="tool-result" aria-live="polite">
  <div class="result-grid">
    <div class="stat"><span class="stat-label">Daily protein</span><b class="stat-big" data-pro="day">&ndash;</b></div>
    <div class="stat"><span class="stat-label">Per meal</span><b data-pro="meal">&ndash;</b></div>
  </div>
  <p class="macro-title">One meal's worth looks like&hellip;</p>
  <ul class="food-chips" data-pro="foods"></ul>
</div>
""",
        "body": """
<h2>How much protein do you need?</h2>
<p>The baseline recommended dietary allowance is 0.8 grams of protein per kilogram of body weight, which is enough to prevent deficiency in inactive adults. Research on people who lift weights points to roughly 1.6 to 2.2 g/kg to support muscle growth, and the higher end helps hold on to muscle while you are in a calorie deficit.</p>
<div class="table-wrap"><table><thead><tr><th>Goal</th><th>g per kg</th><th>g per lb</th></tr></thead><tbody>
<tr><td>General health</td><td>0.8 &ndash; 1.0</td><td>0.36 &ndash; 0.45</td></tr>
<tr><td>Active / endurance</td><td>1.1 &ndash; 1.4</td><td>0.5 &ndash; 0.64</td></tr>
<tr><td>Build muscle</td><td>1.6 &ndash; 2.2</td><td>0.73 &ndash; 1.0</td></tr>
<tr><td>Fat loss, keep muscle</td><td>1.6 &ndash; 2.4</td><td>0.73 &ndash; 1.1</td></tr></tbody></table></div>
<h2>Spread it across the day</h2>
<p>Most people find it easier, and muscles seem to respond well, when protein is split into three to five meals of roughly 20 to 40 grams rather than one huge dinner. Read the full guide: <a href="/how-much-protein-do-you-need-to-build-muscle/">how much protein you need to build muscle</a>. Eating plant-based? See our <a href="/vegan-diet-for-weight-loss-weight-loss-tips/">vegan diet for weight loss tips</a>.</p>
<div class="callout callout-warn"><strong>Heads up:</strong> If you have kidney disease or have been told to limit protein, follow your doctor's guidance instead of these ranges.</div>
""",
        "faq": [
            {"q": "Is 1 gram of protein per pound too much?", "a": "For healthy adults who train hard it is at the high end of the useful range but generally considered safe. Most people building muscle do well between 0.7 and 1 g per pound."},
            {"q": "Should I use my current weight or goal weight?", "a": "If you carry a lot of extra weight, base the calculation on your goal weight or a healthy weight for your height to avoid an unrealistically high number."},
            {"q": "Can I get enough protein without supplements?", "a": "Yes. Powders are just convenient. Eggs, dairy, fish, poultry, tofu, tempeh, beans and lentils can cover your target."},
        ],
    },
    {
        "slug": "water-intake-calculator",
        "name": "Water Intake Calculator",
        "short": "See how much water to drink daily and track your glasses.",
        "seo_title": "Water Intake Calculator: How Much to Drink",
        "description": "Estimate how much water you should drink each day based on your weight, workouts and climate, then tap to track your glasses with this free water calculator.",
        "keyword": "water intake calculator",
        "image": "water-bottle",
        "icon": "drop",
        "widget": """
<form class="tool-form" data-tool="water" novalidate>
  <div class="field-row">
    <label class="field"><span>Body weight</span><input type="number" name="w" min="30" max="700" value="160" inputmode="decimal"></label>
    <div class="seg seg-inline" role="radiogroup" aria-label="Weight unit">
      <label><input type="radio" name="unit" value="lb" checked><span>lb</span></label>
      <label><input type="radio" name="unit" value="kg"><span>kg</span></label>
    </div>
  </div>
  <label class="field"><span>Exercise today: <b data-out-ex>30</b> min</span><input type="range" name="ex" min="0" max="180" step="15" value="30"></label>
  <label class="check"><input type="checkbox" name="hot"><span>Hot or humid weather</span></label>
</form>
<div class="tool-result water-result" aria-live="polite">
  <div class="water-glass"><div class="water-fill" data-water-fill></div><span class="water-pct" data-water-pct>0%</span></div>
  <div>
    <div class="result-grid">
      <div class="stat"><span class="stat-label">Daily goal</span><b class="stat-big" data-water="oz">&ndash;</b></div>
      <div class="stat"><span class="stat-label">That's about</span><b data-water="cups">&ndash;</b></div>
    </div>
    <p class="macro-title">Tap a glass each time you drink 8 oz (saved on this device)</p>
    <div class="glasses" data-water-glasses></div>
    <button type="button" class="btn btn-ghost btn-sm" data-water-reset>Reset today</button>
  </div>
</div>
""",
        "body": """
<h2>How we estimate your water needs</h2>
<p>A common starting point is about half an ounce of water per pound of body weight (roughly 33 ml per kg), plus around 12 ounces for every 30 minutes of exercise, and a little more in hot or humid weather. It's a practical daily drinking goal, not a medical prescription.</p>
<p>For context, the U.S. National Academies put adequate total fluid intake at about 15.5 cups a day for men and 11.5 cups for women, and that includes the water in food and other drinks.</p>
<h2>Signs you're drinking enough</h2>
<ul class="checklist"><li>Your urine is pale yellow most of the day.</li><li>You rarely feel very thirsty.</li><li>You don't get headaches or fatigue late in the afternoon.</li></ul>
<p>Learn more in <a href="/how-much-water-should-you-drink-a-day/">how much water you should drink a day</a>, and see how hydration fits into these <a href="/10-best-glow-up-tips-that-actually-work/">glow-up tips</a>.</p>
<div class="callout callout-warn"><strong>Heads up:</strong> People with heart or kidney conditions may need to limit fluids. Follow your doctor's advice.</div>
""",
        "faq": [
            {"q": "Do coffee and tea count toward water intake?", "a": "Yes. Moderate amounts of coffee and tea still hydrate you overall, though plain water is the best everyday choice."},
            {"q": "Can you drink too much water?", "a": "Yes. Drinking very large amounts quickly, especially during long endurance events, can dangerously lower blood sodium. Sip steadily instead of chugging."},
            {"q": "Is the 8 glasses a day rule right?", "a": "It's a reasonable reminder but not a scientific rule. Your needs depend on body size, activity, climate and what you eat."},
        ],
    },
    {
        "slug": "running-pace-calculator",
        "name": "Running Pace Calculator",
        "short": "Turn a finish time into pace per mile and km, with splits.",
        "seo_title": "Running Pace Calculator: Pace, Time & Splits",
        "description": "Free running pace calculator. Enter a distance and time to get your pace per mile and per kilometer, speed and full race splits for 5K, 10K, half and marathon.",
        "keyword": "running pace calculator",
        "image": "runners-at-sunrise",
        "icon": "timer",
        "widget": """
<form class="tool-form" data-tool="pace" novalidate>
  <div class="chips" role="radiogroup" aria-label="Distance">
    <label><input type="radio" name="preset" value="5" checked><span>5K</span></label>
    <label><input type="radio" name="preset" value="10"><span>10K</span></label>
    <label><input type="radio" name="preset" value="21.0975"><span>Half</span></label>
    <label><input type="radio" name="preset" value="42.195"><span>Marathon</span></label>
    <label><input type="radio" name="preset" value="custom"><span>Custom</span></label>
  </div>
  <div class="field-row">
    <label class="field"><span>Distance</span><input type="number" name="dist" min="0.1" step="0.01" value="5" inputmode="decimal"></label>
    <div class="seg seg-inline" role="radiogroup" aria-label="Distance unit">
      <label><input type="radio" name="dunit" value="km" checked><span>km</span></label>
      <label><input type="radio" name="dunit" value="mi"><span>mi</span></label>
    </div>
  </div>
  <div class="field-row">
    <label class="field"><span>Hours</span><input type="number" name="h" min="0" max="24" value="0" inputmode="numeric"></label>
    <label class="field"><span>Minutes</span><input type="number" name="m" min="0" max="59" value="30" inputmode="numeric"></label>
    <label class="field"><span>Seconds</span><input type="number" name="s" min="0" max="59" value="0" inputmode="numeric"></label>
  </div>
</form>
<div class="tool-result" aria-live="polite">
  <div class="result-grid">
    <div class="stat"><span class="stat-label">Pace / mile</span><b class="stat-big" data-pace="mi">&ndash;</b></div>
    <div class="stat"><span class="stat-label">Pace / km</span><b data-pace="km">&ndash;</b></div>
    <div class="stat"><span class="stat-label">Speed</span><b data-pace="speed">&ndash;</b></div>
  </div>
  <p class="macro-title">Predicted finish at this pace</p>
  <div class="table-wrap"><table class="splits"><thead><tr><th>Race</th><th>Finish time</th></tr></thead><tbody data-pace="races"></tbody></table></div>
</div>
""",
        "body": """
<h2>How to use the pace calculator</h2>
<p>Pick a race distance (or enter a custom one), type your finish time, and the calculator shows your average pace per mile and per kilometer plus your speed. The table underneath shows what that same pace would mean over other common race distances, which is handy for setting realistic goals.</p>
<h2>Pace tips for new runners</h2>
<p>Most of your weekly runs should feel conversational: you can speak in full sentences. That &ldquo;easy&rdquo; pace is often one to two minutes per mile slower than your 5K race pace, and that's exactly where endurance is built. Our <a href="/the-beginners-guide-to-starting-a-running-routine/">beginner's guide to starting a running routine</a> includes an 8-week run/walk plan.</p>
<p>Flat feet or sore arches after runs? Start with <a href="/how-to-choose-running-shoes-for-flat-feet/">how to choose running shoes for flat feet</a> or take the <a href="/tools/shoe-finder-quiz/">shoe finder quiz</a>.</p>
""",
        "faq": [
            {"q": "What is a good 5K pace for a beginner?", "a": "Anything you can finish comfortably. Many new runners finish a 5K between 30 and 40 minutes, roughly 10 to 13 minutes per mile."},
            {"q": "How do I convert pace per km to pace per mile?", "a": "Multiply your per-kilometer pace by 1.609. For example, 6:00 per km is about 9:39 per mile."},
            {"q": "Are race predictions accurate?", "a": "The table assumes you hold the same pace, which gets harder over longer distances. Expect to run slightly slower per mile as the distance grows."},
        ],
    },
    {
        "slug": "shoe-finder-quiz",
        "name": "Shoe Finder Quiz",
        "short": "Five quick questions to find the right shoe type for your feet.",
        "seo_title": "Shoe Finder Quiz: Best Shoe Type for Flat Feet",
        "description": "Take our free shoe finder quiz to see which shoe type suits your arches, sport and comfort needs, from stability running shoes to supportive tennis shoes for flat feet.",
        "keyword": "shoe finder quiz",
        "image": "neon-trainer",
        "icon": "shoe",
        "widget": """
<div class="quiz" data-tool="quiz">
  <div class="quiz-progress"><span data-quiz-bar></span></div>
  <div class="quiz-step is-active" data-q="arch">
    <p class="quiz-q">Do the wet test: step on paper with a wet foot. What does the print look like?</p>
    <div class="quiz-opts">
      <button type="button" data-v="flat">Almost the whole foot shows (flat / low arch)</button>
      <button type="button" data-v="medium">About half the arch shows (medium arch)</button>
      <button type="button" data-v="high">Just heel and ball, thin band between (high arch)</button>
      <button type="button" data-v="unsure">Not sure</button>
    </div>
  </div>
  <div class="quiz-step" data-q="sport">
    <p class="quiz-q">What will you mostly use the shoes for?</p>
    <div class="quiz-opts">
      <button type="button" data-v="tennis">Tennis, pickleball or court sports</button>
      <button type="button" data-v="running">Running</button>
      <button type="button" data-v="walking">Walking and all-day wear</button>
      <button type="button" data-v="gym">Gym and training classes</button>
    </div>
  </div>
  <div class="quiz-step" data-q="pain">
    <p class="quiz-q">Any discomfort after activity?</p>
    <div class="quiz-opts">
      <button type="button" data-v="arch">Arch or heel pain</button>
      <button type="button" data-v="knee">Knees, shins or ankles roll in</button>
      <button type="button" data-v="none">No real pain</button>
    </div>
  </div>
  <div class="quiz-step" data-q="orthotic">
    <p class="quiz-q">Do you wear custom orthotics or insoles?</p>
    <div class="quiz-opts">
      <button type="button" data-v="yes">Yes</button>
      <button type="button" data-v="no">No</button>
    </div>
  </div>
  <div class="quiz-step" data-q="feel">
    <p class="quiz-q">What do you want underfoot?</p>
    <div class="quiz-opts">
      <button type="button" data-v="plush">Soft and cushioned</button>
      <button type="button" data-v="firm">Firm and stable</button>
      <button type="button" data-v="light">Light and fast</button>
    </div>
  </div>
  <div class="quiz-result" data-quiz-result hidden>
    <span class="pill">Your match</span>
    <h3 data-quiz-title></h3>
    <p data-quiz-text></p>
    <ul class="checklist" data-quiz-list></ul>
    <div class="quiz-actions"><a class="btn" data-quiz-link href="/best-tennis-shoes-for-flat-feet/">Read the guide</a><button type="button" class="btn btn-ghost" data-quiz-restart>Start over</button></div>
  </div>
</div>
""",
        "body": """
<h2>Why shoe type matters more than brand</h2>
<p>Flat or low arches often let the foot roll inward (overpronate) more than usual. Shoes with a firmer medial post, a wide stable base and a structured heel counter help control that motion, while neutral shoes leave room for custom orthotics. The quiz matches your arch, sport and comfort preferences to the shoe category that usually works best.</p>
<h2>Read the full guides</h2>
<ul class="checklist">
<li><a href="/best-tennis-shoes-for-flat-feet/">Best tennis shoes for flat feet</a>: court shoes with real lateral support.</li>
<li><a href="/how-to-choose-running-shoes-for-flat-feet/">How to choose running shoes for flat feet</a>: stability vs motion control vs neutral.</li>
<li><a href="/flat-feet-exercises/">Flat feet exercises</a> and <a href="/plantar-fasciitis-stretches/">plantar fasciitis stretches</a> to build stronger, happier feet.</li>
</ul>
<div class="callout callout-note"><strong>Good to know:</strong> Persistent foot, knee or heel pain is worth a visit to a podiatrist or physical therapist. A quiz can't replace a gait assessment.</div>
""",
        "faq": [
            {"q": "How do I know if I have flat feet?", "a": "Wet your foot and step on paper or cardboard. If almost the entire sole shows with little curve on the inside, you likely have low arches or flat feet."},
            {"q": "Should people with flat feet wear stability shoes?", "a": "Many do well in stability shoes, especially if their ankles roll inward. If you wear custom orthotics, a neutral shoe with a removable insole often fits them better."},
            {"q": "Can I play tennis in running shoes?", "a": "It's not recommended. Running shoes are built for forward motion and lack the lateral support and durable outsole tennis needs for quick side-to-side moves."},
        ],
    },
    {
        "slug": "interval-timer",
        "name": "Interval Timer",
        "short": "A free HIIT and Tabata timer with sound cues.",
        "seo_title": "Interval Timer: Free HIIT & Tabata Timer",
        "description": "Free online interval timer for HIIT, Tabata and circuit workouts. Set work, rest and rounds, get audio beeps, and follow a big progress ring from any phone.",
        "keyword": "interval timer",
        "image": "battle-ropes-hiit",
        "icon": "timer",
        "widget": """
<div class="timer" data-tool="timer">
  <div class="chips" role="radiogroup" aria-label="Presets">
    <label><input type="radio" name="preset" value="20,10,8" checked><span>Tabata 20/10 &times; 8</span></label>
    <label><input type="radio" name="preset" value="40,20,10"><span>HIIT 40/20 &times; 10</span></label>
    <label><input type="radio" name="preset" value="45,15,12"><span>Circuit 45/15 &times; 12</span></label>
    <label><input type="radio" name="preset" value="30,30,10"><span>Beginner 30/30 &times; 10</span></label>
  </div>
  <div class="field-row">
    <label class="field"><span>Work (sec)</span><input type="number" name="work" min="5" max="600" value="20" inputmode="numeric"></label>
    <label class="field"><span>Rest (sec)</span><input type="number" name="rest" min="0" max="600" value="10" inputmode="numeric"></label>
    <label class="field"><span>Rounds</span><input type="number" name="rounds" min="1" max="50" value="8" inputmode="numeric"></label>
  </div>
  <div class="timer-face" data-phase="ready">
    <svg viewBox="0 0 200 200" aria-hidden="true"><circle class="ring-bg" cx="100" cy="100" r="88"/><circle class="ring" cx="100" cy="100" r="88" data-timer-ring/></svg>
    <div class="timer-read">
      <span class="timer-phase" data-timer-phase>Ready</span>
      <b class="timer-time" data-timer-time>00:20</b>
      <span class="timer-round" data-timer-round>Round 0 / 8</span>
    </div>
  </div>
  <div class="timer-controls">
    <button type="button" class="btn" data-timer-start>Start</button>
    <button type="button" class="btn btn-ghost" data-timer-reset>Reset</button>
    <label class="check"><input type="checkbox" data-timer-sound checked><span>Sound</span></label>
  </div>
  <p class="timer-total">Total workout time: <b data-timer-total>4:00</b></p>
</div>
""",
        "body": """
<h2>How to use the interval timer</h2>
<p>Choose a preset or set your own work time, rest time and number of rounds, then press Start. The ring turns lime during work and blue during rest, and you'll hear a short beep at each change plus a countdown in the last three seconds. Keep your phone screen on during the workout.</p>
<h2>Workouts to pair it with</h2>
<ul class="checklist">
<li><a href="/full-body-home-workout-no-equipment/">30-minute full-body home workout</a> &mdash; use 40 seconds on, 20 off.</li>
<li><a href="/10-basic-calisthenics-exercises-for-beginners/">10 basic calisthenics exercises</a> &mdash; beginners start at 30/30.</li>
<li><a href="/hiit-vs-steady-state-cardio-for-fat-loss/">HIIT vs steady-state cardio</a> &mdash; when intervals make sense.</li>
</ul>
<div class="callout callout-tip"><strong>Tip:</strong> Classic Tabata (20 seconds hard, 10 seconds rest, eight rounds) only works at a genuinely high effort. If you're new to exercise, start with 30/30 and build up.</div>
""",
        "faq": [
            {"q": "What is a Tabata workout?", "a": "Eight rounds of 20 seconds of very hard work followed by 10 seconds of rest, four minutes in total."},
            {"q": "How long should a HIIT workout be?", "a": "For most people 10 to 25 minutes of intervals, plus a warm-up and cooldown, is plenty. Two or three sessions a week is a good limit."},
            {"q": "Does the timer work on my phone?", "a": "Yes. It runs in your mobile browser. Tap Start once so the browser allows sound, and keep the screen awake."},
        ],
    },
]
