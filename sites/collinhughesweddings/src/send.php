<?php
// Contact form handler: emails inquiries to the studio inbox.
$to = 'info@collinhughesweddings.com';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /contact/', true, 303); exit; }
if (!empty($_POST['website'])) { header('Location: /contact/?sent=1#main', true, 303); exit; } // honeypot

$clean = function ($k, $max = 300) {
    $v = trim((string)($_POST[$k] ?? ''));
    return mb_substr(str_replace(["\r", "\n"], ' ', $v), 0, $max);
};
$name  = $clean('name');
$email = filter_var($clean('email'), FILTER_VALIDATE_EMAIL);
$date  = $clean('date');
$venue = $clean('venue');
$msg   = mb_substr(trim((string)($_POST['message'] ?? '')), 0, 5000);

if ($name === '' || !$email || $msg === '') { header('Location: /contact/?sent=0#main', true, 303); exit; }

$body = "New wedding inquiry from the website\n\n"
      . "Names: $name\nEmail: $email\nWedding date: $date\nVenue: $venue\n\n$msg\n";
$headers = "From: Collin Hughes Weddings <$to>\r\n"
         . "Reply-To: $email\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";
$ok = mail($to, "Wedding inquiry: $name", $body, $headers);
header('Location: /contact/?sent=' . ($ok ? '1' : '0') . '#main', true, 303);
