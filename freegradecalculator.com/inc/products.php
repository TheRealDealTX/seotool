<?php
// Curated Amazon picks. Links are Amazon search links carrying the Associates tag,
// so they never break when a listing changes. key => [title, why, icon, badge, query]
function products(): array {
    return [
      'ti-84-plus-ce'   => ['TI-84 Plus CE Graphing Calculator', 'The graphing calculator most US math teachers use — approved for the SAT, ACT and AP exams.', 'calc', 'Best for HS math', 'TI-84 Plus CE graphing calculator'],
      'ti-30xs'         => ['TI-30XS MultiView Scientific Calculator', 'Shows four lines at once and handles fractions naturally. A budget favorite for algebra and chemistry.', 'calc', 'Best value', 'TI-30XS MultiView scientific calculator'],
      'casio-fx-991ex'  => ['Casio fx-991EX ClassWiz', 'High-resolution scientific calculator with spreadsheet mode, matrices and equation solving.', 'calc', 'Most features', 'Casio fx-991EX ClassWiz'],
      'casio-fx-115es'  => ['Casio fx-115ES Plus', 'Natural textbook display and 280 functions — allowed on many engineering exams.', 'calc', 'For engineering', 'Casio fx-115ES Plus scientific calculator'],
      'ti-nspire-cx-ii' => ['TI-Nspire CX II CAS', 'Color graphing calculator with a computer algebra system for calculus and beyond.', 'calc', 'For calculus', 'TI-Nspire CX II CAS'],
      'academic-planner'=> ['2026–2027 Academic Planner', 'Weekly and monthly layouts to track assignments, tests and due dates all year.', 'calendar', 'Stay organized', 'academic planner 2026-2027 weekly monthly'],
      'index-cards'     => ['Ruled Index Cards (Pack)', 'Old-school flashcards still beat rereading for memorizing terms and formulas.', 'layers', 'Study staple', 'ruled index cards 3x5 pack'],
      'highlighters'    => ['Pastel Highlighter Set', 'Soft colors for color-coding notes without bleeding through thin pages.', 'pen', 'Note-taking', 'pastel highlighters set no bleed'],
      'noise-cancelling-headphones' => ['Noise-Cancelling Headphones', 'Block out dorm and library noise for deep-focus study sessions.', 'headphones', 'Focus', 'noise cancelling headphones students'],
      'desk-lamp'       => ['LED Desk Lamp with USB Charging', 'Adjustable brightness and color temperature for late-night studying.', 'lamp', 'Study space', 'LED desk lamp USB charging port dimmable'],
      'sticky-notes'    => ['Sticky Notes Value Pack', 'Mark textbook pages, map out essays, and leave yourself reminders.', 'note', 'Everyday', 'sticky notes value pack'],
      'teacher-gradebook' => ['Teacher Record & Grade Book', 'Spacious grading grid for 40+ students with attendance pages.', 'table', 'For teachers', 'teacher record book grade book'],
      'grading-pens'    => ['Red & Colored Grading Pens', 'Smooth, quick-drying felt-tip pens for marking papers.', 'pen', 'For teachers', 'grading pens felt tip red pack'],
      'visual-timer'    => ['Visual Countdown Timer', 'A physical timer that makes Pomodoro sessions and test practice easy to see.', 'clock', 'Focus', 'visual countdown timer study'],
      'sat-study-guide' => ['Official Digital SAT Study Guide', 'Practice material from the College Board, the people who make the SAT.', 'book', 'Test prep', 'official digital SAT study guide'],
      'act-prep-guide'  => ['Official ACT Prep Guide', 'Real past ACT tests with answer explanations from ACT.', 'book', 'Test prep', 'official ACT prep guide'],
      'straight-a-book' => ['How to Become a Straight-A Student (Cal Newport)', 'Practical study and time-management strategies used by top college students.', 'book', 'Study smarter', 'How to Become a Straight-A Student Cal Newport'],
      'make-it-stick-book' => ['Make It Stick: The Science of Successful Learning', 'Explains retrieval practice and spacing — the study habits research supports.', 'book', 'Study smarter', 'Make It Stick science of successful learning'],
      'laptop-stand'    => ['Adjustable Laptop Stand', 'Raise your screen to eye level for better posture during long study blocks.', 'laptop', 'Study space', 'adjustable laptop stand'],
      'desk-whiteboard' => ['Desktop Whiteboard', 'A small dry-erase board for working practice problems and to-do lists.', 'board', 'Study space', 'desktop whiteboard dry erase small'],
    ];
}
function amazon_url(string $query): string {
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . AMAZON_TAG;
}
