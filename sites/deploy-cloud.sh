#!/bin/bash
# Upload a built site's public/ to a website on the Hostinger Cloud plan
# (order 64270646, account u401386392) through the File Browser TUS API.
#
# Credentials come from the Hostinger API call `hosting_files_generate-upload-url`
# (username u401386392, domain <the site's domain>); they expire after a few hours:
#
#   export FB_URL='https://…'   # "url"
#   export FB_AUTH='…'          # "auth_key"
#   export FB_REST='…'          # "rest_auth_key"
#   ./deploy-cloud.sh <site-dir>          # e.g. ./deploy-cloud.sh pensacolahurricane
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
cd "$(dirname "$0")/${1:?site dir}/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
