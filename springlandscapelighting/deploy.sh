#!/bin/bash
# Push public_html/ to the Hostinger Agency website (UID o4crWzsNE, plain php-fpm) through its
# File Browser TUS endpoint. Get the credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export SL_FB_URL='https://…/api/tus'   # "url"
#   export SL_FB_AUTH='…'                  # "auth_key"
#   export SL_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh
#
# Then clear the cache (`agency-hosting_cache_clear-website`).
# Never uploads app/data/ (server-side leads + form secret live there).
set -u
: "${SL_FB_URL:?set SL_FB_URL}" "${SL_FB_AUTH:?set SL_FB_AUTH}" "${SL_FB_REST:?set SL_FB_REST}"
cd "$(dirname "$0")/public_html" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $SL_FB_AUTH" -H "X-Auth-Rest: $SL_FB_REST" -H "Tus-Resumable: 1.0.0" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$SL_FB_URL/public_html/$rel?override=true" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$SL_FB_URL/public_html/$rel?override=true" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -path './app/data/leads.php' ! -path './app/data/secret.php' ! -path './index.php' | sort; echo ./index.php)  # front controller last
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
