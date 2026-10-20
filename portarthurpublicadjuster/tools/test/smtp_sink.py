#!/usr/bin/env python3
"""Minimal local SMTP sink for form tests: accepts every message and writes it to
/tmp/papa-mail/<n>.eml. Usage: python3 tools/test/smtp_sink.py [port]  (default 2525)."""
import os, socketserver, sys

OUT = '/tmp/papa-mail'
os.makedirs(OUT, exist_ok=True)


class H(socketserver.StreamRequestHandler):
    def w(self, s):
        self.wfile.write((s + '\r\n').encode())

    def handle(self):
        self.w('220 localhost sink')
        rcpt, data = [], None
        while True:
            line = self.rfile.readline()
            if not line:
                return
            cmd = line.decode('utf-8', 'replace').strip()
            up = cmd.upper()
            if up.startswith(('EHLO', 'HELO')):
                self.w('250-localhost'); self.w('250 AUTH PLAIN')
            elif up.startswith('AUTH'):
                if len(cmd.split()) < 3:      # "AUTH PLAIN" then credentials on the next line
                    self.w('334 '); self.rfile.readline()
                self.w('235 ok')
            elif up.startswith('MAIL FROM'):
                rcpt = []; self.w('250 ok')
            elif up.startswith('RCPT TO'):
                rcpt.append(cmd[8:].strip()); self.w('250 ok')
            elif up == 'DATA':
                self.w('354 go'); buf = []
                while True:
                    l = self.rfile.readline()
                    if l in (b'.\r\n', b'.\n', b''):
                        break
                    buf.append(l)
                n = len(os.listdir(OUT)) + 1
                with open(os.path.join(OUT, f'{n}.eml'), 'wb') as f:
                    f.write(('X-Sink-Rcpt: ' + ', '.join(rcpt) + '\r\n').encode() + b''.join(buf))
                self.w('250 queued')
            elif up == 'QUIT':
                self.w('221 bye'); return
            else:
                self.w('250 ok')


socketserver.ThreadingTCPServer.allow_reuse_address = True
socketserver.ThreadingTCPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 2525), H).serve_forever()
