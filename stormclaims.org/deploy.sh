#!/bin/bash
# Deploy stormclaims.org to its Hostinger website (Web hosting, user u401386392).
#
# Credentials come from the Hostinger API call `hosting_files_generate-upload-url`
# for domain stormclaims.org (they expire after a few hours):
#
#   export SC_FB_URL='https://…/api/tus/public_html'   # "url"
#   export SC_FB_AUTH='…'                              # "auth_key"
#   export SC_FB_REST='…'                              # "rest_auth_key"
#   ./deploy.sh
set -u
: "${SC_FB_URL:?set SC_FB_URL}" "${SC_FB_AUTH:?set SC_FB_AUTH}" "${SC_FB_REST:?set SC_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $SC_FB_AUTH" -H "X-Auth-Rest: $SC_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$SC_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$SC_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name 'deploy.sh' ! -name 'README.md' -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
