<?php
/* Minimal SMTP client (implicit TLS / AUTH LOGIN) — no Composer needed.
 * Credentials come from a config file OUTSIDE the web root (see README), never from the repo. */
defined('CPA') or exit;

function mail_config(): ?array {
  foreach ([SITE_ROOT . '/../.private/cpacalculator-mail.php', SITE_ROOT . '/app/config.local.php'] as $f) {
    if (is_file($f)) { $c = include $f; if (is_array($c)) return $c; }
  }
  return null;
}

function smtp_send(string $to, string $subject, string $body, string $replyTo = '', ?string &$err = null): bool {
  $c = mail_config();
  if (!$c) { $err = 'mail not configured'; return false; }
  $host = $c['host'] ?? 'smtp.hostinger.com'; $port = (int) ($c['port'] ?? 465);
  $fp = @stream_socket_client("ssl://$host:$port", $no, $str, 20, STREAM_CLIENT_CONNECT, stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]));
  if (!$fp) { $err = "connect: $str"; return false; }
  stream_set_timeout($fp, 20);
  $read = function () use ($fp) { $d = ''; while (($l = fgets($fp, 515)) !== false) { $d .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $d; };
  $cmd = function (string $s, string $expect) use ($fp, $read, &$err) { if ($s !== '') fwrite($fp, $s . "\r\n"); $r = $read(); if (strpos($r, $expect) !== 0) { $err = trim($r); return false; } return true; };
  $from = $c['user'];
  $hdr = [
    'Date: ' . date('r'), 'From: "CPA Calculator" <' . $from . '>', 'To: <' . $to . '>',
    'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=', 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit', 'Message-ID: <' . bin2hex(random_bytes(12)) . '@cpacalculator.com>',
  ];
  if ($replyTo && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) $hdr[] = 'Reply-To: <' . $replyTo . '>';
  $data = implode("\r\n", $hdr) . "\r\n\r\n" . preg_replace('/^\./m', '..', str_replace(["\r\n", "\r"], "\n", $body));
  $data = str_replace("\n", "\r\n", $data);
  $ok = $cmd('', '220') && $cmd('EHLO cpacalculator.com', '250') && $cmd('AUTH LOGIN', '334') && $cmd(base64_encode($from), '334')
     && $cmd(base64_encode($c['pass']), '235') && $cmd('MAIL FROM:<' . $from . '>', '250') && $cmd('RCPT TO:<' . $to . '>', '25')
     && $cmd('DATA', '354') && $cmd($data . "\r\n.", '250');
  @fwrite($fp, "QUIT\r\n"); fclose($fp);
  return $ok;
}
