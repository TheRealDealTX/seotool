<div class="narrow-lg">
  <h1>Roommate tools</h1>
  <p class="muted">Everything you need to go from "maybe" to moved in.</p>
  <div class="grid grid-2 tools-grid">
    <a class="card tool" href="/match"><span class="tool-ic">💘</span><h3>Roommate Match</h3><p class="muted">Swipe through your best matches. Like each other and you're instantly connected.</p></a>
    <a class="card tool" href="/quiz"><span class="tool-ic">🧩</span><h3>Roommate Quiz</h3><p class="muted"><?= current_user()['quiz_type'] ? 'Your type: ' . e(QUIZ_TYPES[current_user()['quiz_type']]['name']) . '. Retake anytime.' : 'Discover your roommate type in 60 seconds and get better matches.' ?></p></a>
    <a class="card tool" href="/tools/rent-split"><span class="tool-ic">🧮</span><h3>Rent Split Calculator</h3><p class="muted">Split rent fairly by room size, private bathrooms and parking — then send it to your roommate.</p></a>
    <a class="card tool" href="/agreements"><span class="tool-ic">📝</span><h3>Roommate Agreement</h3><p class="muted">Agree on rent, bills, chores, quiet hours and guests — edit together and sign online.<?= $agreements ? " ($agreements active)" : '' ?></p></a>
    <a class="card tool" href="/properties?mine=1"><span class="tool-ic">💬</span><h3>Property Lounges</h3><p class="muted">Group chats for each apartment community. Meet everyone interested in the same place.</p></a>
    <a class="card tool" href="/safety"><span class="tool-ic">🛡️</span><h3>Safety checklist</h3><p class="muted">How to vet a roommate and avoid rental scams.</p></a>
  </div>
</div>
