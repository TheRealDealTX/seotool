<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
return [
    'body' => <<<'HTML'
<h2>Does an under desk elliptical count as steps?</h2>
<p>Usually not automatically. Wrist-worn trackers count steps by detecting the arm swing of walking. When you sit and pedal, your arms stay still on the keyboard, so your Fitbit, Apple Watch or Garmin may record few or no steps even after an hour of pedaling.</p>
<p>That's why a step-equivalent is useful. It answers the fairer question: <em>how many steps would take the same effort?</em> This converter compares the energy of pedaling above resting with brisk walking, which is about 100 steps per minute at 3.5 METs.</p>
<h2>How to get credit on your tracker</h2>
<ul>
<li><strong>Log it as a workout:</strong> most apps let you add an elliptical or "other" session, which counts toward active minutes.</li>
<li><strong>Move the tracker:</strong> some people clip the tracker to a shoe or sock while pedaling. Results vary, and it can overcount.</li>
<li><strong>Use a connected machine:</strong> models with Bluetooth, like the [[amazon:cubii-jr2-plus]], can sync strides to an app.</li>
</ul>
<p>Need a tracker that handles workouts well? The [[amazon:fitbit-charge-6]] adds heart-rate based exercise tracking, and the [[amazon:fitbit-inspire-3]] is the budget option. More detail in <a href="/does-under-desk-elliptical-count-as-steps/">does an under desk elliptical count as steps</a>, and see how it compares with walking in <a href="/is-under-desk-elliptical-as-good-as-walking/">is an under desk elliptical as good as walking</a>.</p>
HTML,
    'faq' => [
        ['q' => 'Does an under desk elliptical count as steps on a Fitbit?', 'a' => 'Often not, because wrist trackers count arm swings. Log your session as a workout, or clip the tracker to your shoe, to get credit.'],
        ['q' => 'How many steps is 30 minutes on an under desk elliptical?', 'a' => 'At moderate effort it is roughly 1,500 to 2,000 step-equivalents by energy, though your tracker may count far fewer.'],
        ['q' => 'Is an under desk elliptical as good as walking?', 'a' => 'Minute for minute, brisk walking burns more, but pedaling while you work adds activity you would not otherwise get. See <a href="/is-under-desk-elliptical-as-good-as-walking/">our comparison</a>.'],
    ],
];
