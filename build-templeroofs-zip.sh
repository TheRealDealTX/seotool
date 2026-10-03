#!/bin/sh
# Package templeroofs/ as a Hostinger-ready ZIP (site files at the ZIP root).
# Runtime data (cache, logs, rate-limit records, generated secret, saved leads)
# is excluded; empty storage folders and their protections are kept.
set -e
cd "$(dirname "$0")/templeroofs"
OUT="../releases/templeroofs-hostinger-ready.zip"
mkdir -p ../releases
rm -f "$OUT"
zip -r -9 -X -q "$OUT" . \
  -x 'storage/cache/*.json' 'storage/cache/*.lock' 'storage/cache/*.tmp' \
     'storage/ratelimit/*.json' 'storage/logs/*.log' 'storage/secret.php' \
     'storage/undelivered-leads/*' 'storage/undelivered-leads/' \
     '*.DS_Store'
echo "Built $OUT"
unzip -l "$OUT" | tail -1
