#!/bin/bash
# Deploy the static build to the Hostinger Agency website (UID IBqTPWf6a,
# temporary domain darkblue-quail-416052.hostingersite.com).
#
# Pushes the built files one by one through the website's File Browser TUS
# endpoint. Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export OH_FB_URL='https://…/api/tus'      # "url" from the response
#   export OH_FB_AUTH='…'                     # "auth_key"
#   export OH_FB_REST='…'                     # "rest_auth_key"
#   STAGING=1 python3 build.py && ./deploy.sh     # while on the temporary domain
#   python3 build.py && ./deploy.sh               # once ollieharperstudio.com is attached
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
set -u
: "${OH_FB_URL:?set OH_FB_URL}" "${OH_FB_AUTH:?set OH_FB_AUTH}" "${OH_FB_REST:?set OH_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $OH_FB_AUTH" -H "X-Auth-Rest: $OH_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$OH_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$OH_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path '*/__pycache__' -o -name '*.py' -o -name 'README.md' -o -name 'deploy.sh' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
