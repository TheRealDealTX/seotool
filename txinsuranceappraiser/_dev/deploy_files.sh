#!/bin/bash
# Upload specific files to txinsuranceappraiser.com/public_html via the Hostinger File Browser (TUS).
#
# Get credentials from the Hostinger API operation `hosting_files_generate-upload-url`
# (username u401386392, domain txinsuranceappraiser.com). They expire after a few hours.
#
#   export TX_FB_URL='https://…/api/tus/public_html'   # "url"
#   export TX_FB_AUTH='…'                               # "auth_key"
#   export TX_FB_REST='…'                               # "rest_auth_key"
#   _dev/deploy_files.sh content/posts/new-post.json assets/img/blog/new-photo.webp ...
#
# Paths are relative to the txinsuranceappraiser/ folder and are uploaded to the same path on the server.
set -u
: "${TX_FB_URL:?set TX_FB_URL}" "${TX_FB_AUTH:?set TX_FB_AUTH}" "${TX_FB_REST:?set TX_FB_REST}"
cd "$(dirname "$0")/.." || exit 1
ok=0; fail=0
for f in "$@"; do
  case "$f" in _dev/*|README.md) echo "skip $f (not deployed)"; continue;; esac
  [ -f "$f" ] || { echo "MISSING $f"; fail=$((fail+1)); continue; }
  size=$(stat -c%s "$f")
  c=$(curl -sS -o /dev/null -w "%{http_code}" -X POST "$TX_FB_URL/$f?override=true" -H "X-Auth: $TX_FB_AUTH" -H "X-Auth-Rest: $TX_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0")
  p=$(curl -sS -o /dev/null -w "%{http_code}" -X PATCH "$TX_FB_URL/$f?override=true" -H "X-Auth: $TX_FB_AUTH" -H "X-Auth-Rest: $TX_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); echo "ok   $f"; else fail=$((fail+1)); echo "FAIL $c/$p $f"; fi
done
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
