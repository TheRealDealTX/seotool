#!/bin/bash
# Deploy saffronsupplement.com to its Hostinger Agency website (UID JfEovlw7l).
#
# Uploads each site file through the website's File Browser TUS endpoint.
# Get the three credentials from the Hostinger API operation
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export SS_FB_URL='https://…/api/tus'   # "url"
#   export SS_FB_AUTH='…'                  # "auth_key"
#   export SS_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh
set -u
: "${SS_FB_URL:?set SS_FB_URL}" "${SS_FB_AUTH:?set SS_FB_AUTH}" "${SS_FB_REST:?set SS_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $SS_FB_AUTH" -H "X-Auth-Rest: $SS_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$SS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$SS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -path './app/private/*' ! -name '*.py' ! -name 'deploy.sh' ! -name 'README.md' ! -path '*/__pycache__/*' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
