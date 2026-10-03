#!/bin/sh
# Build the upload-ready ZIP for Hostinger's public_html.
# Usage: sh tools/package.sh   -> dist/mcallenpublicadjuster-public_html.zip
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/dist"
STAGE=$(mktemp -d)
mkdir -p "$OUT"
cp -a "$ROOT/site/." "$STAGE/"
# Never ship local secrets, logs, caches, or test files.
rm -f "$STAGE/includes/config.local.php" "$STAGE/data/.secret"
find "$STAGE/data/cache" "$STAGE/data/logs" "$STAGE/data/ratelimit" -type f ! -name .htaccess -delete
find "$STAGE" -name '*.tmp' -delete -o -name '*.lock' -delete
rm -f "$OUT/mcallenpublicadjuster-public_html.zip"
(cd "$STAGE" && zip -qr -X "$OUT/mcallenpublicadjuster-public_html.zip" . -x '.DS_Store')
rm -rf "$STAGE"
ls -la "$OUT/mcallenpublicadjuster-public_html.zip"
unzip -l "$OUT/mcallenpublicadjuster-public_html.zip" | tail -1
