#!/bin/bash
# Upload public/ to holybiblewords.com's public_html through the Hostinger
# File Browser TUS endpoint. Get the credentials from the Hostinger API call
# `hosting_files_generate-upload-url` (username u401386392, domain
# holybiblewords.com); they expire after a few hours:
#
#   export HB_FB_URL='https://…/api/tus/public_html'   # "url" as returned
#   export HB_FB_AUTH='…' HB_FB_REST='…'                # "auth_key", "rest_auth_key"
#   ./deploy.sh
#
# Then clear the cache (API `hosting_cache_clear-website`, or hPanel), which also
# purges the Hostinger CDN.
set -u
: "${HB_FB_URL:?set HB_FB_URL}" "${HB_FB_AUTH:?set HB_FB_AUTH}" "${HB_FB_REST:?set HB_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $HB_FB_AUTH" -H "X-Auth-Rest: $HB_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$HB_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$HB_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
