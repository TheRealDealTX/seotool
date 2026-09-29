#!/usr/bin/env bash
# Build the Hostinger deployment package.
#
#   tools/build-package.sh OUTDIR [path/to/config.php] [admin-email] [admin-bcrypt-hash]
#
# Produces in OUTDIR:
#   rodeotexas-package.zip   app/ (+ config.php if given) and public_html/, in Hostinger layout:
#                            domains/<domain>/app/          ← outside the web root
#                            domains/<domain>/public_html/  ← web root
#   _install_<token>.php     one-time installer (only when a config is given)
#   install-token.txt        the token (keep private)
set -euo pipefail
OUT=${1:?output dir}
CFG=${2:-}
ADMIN_EMAIL=${3:-}
ADMIN_HASH=${4:-}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$OUT"
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/app" "$STAGE/public_html"
# Application code (no local config, no runtime data)
(cd "$ROOT/app" && tar cf - --exclude='./config.php' --exclude='./storage/*' .) | (cd "$STAGE/app" && tar xf -)
mkdir -p "$STAGE/app/storage/logs" "$STAGE/app/storage/locks" "$STAGE/app/storage/cache" "$STAGE/app/storage/imports"
touch "$STAGE/app/storage/logs/.keep"
(cd "$ROOT/public_html" && tar cf - .) | (cd "$STAGE/public_html" && tar xf -)
if [ -n "$CFG" ]; then cp "$CFG" "$STAGE/app/config.php"; fi

rm -f "$OUT/rodeotexas-package.zip"
(cd "$STAGE" && zip -qr -X "$OUT/rodeotexas-package.zip" app public_html)
echo "Package: $OUT/rodeotexas-package.zip ($(du -h "$OUT/rodeotexas-package.zip" | cut -f1))"

if [ -n "$CFG" ]; then
  TOKEN=$(php -r 'echo bin2hex(random_bytes(24));')
  php -r '
    [$_, $src, $dst, $tok, $email, $hash] = $argv;
    $s = file_get_contents($src);
    $s = str_replace(["__TOKEN__", "__ADMIN_EMAIL__", "__ADMIN_HASH__"], [$tok, $email, $hash], $s);
    file_put_contents($dst, $s);
  ' "$ROOT/deploy/install.php" "$OUT/_install_${TOKEN:0:16}.php" "$TOKEN" "$ADMIN_EMAIL" "$ADMIN_HASH"
  echo "$TOKEN" > "$OUT/install-token.txt"
  echo "Installer: $OUT/_install_${TOKEN:0:16}.php"
fi
