#!/bin/bash
# Upload dist/ to the Hostinger Agency website (UID jlj9tGHeI) through its
# File Browser TUS endpoint. Get fresh credentials (they expire after a few
# hours) from the Hostinger API call `agency-hosting_files_generate-upload-url`:
#
#   export CM_FB_URL='https://…/api/tus'   # "url"
#   export CM_FB_AUTH='…'                  # "auth_key"
#   export CM_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${CM_FB_URL:?set CM_FB_URL}" "${CM_FB_AUTH:?set CM_FB_AUTH}" "${CM_FB_REST:?set CM_FB_REST}"
cd "$(dirname "$0")/dist" || exit 1
fb() { curl -sS --max-time 300 --retry 3 -H "X-Auth: $CM_FB_AUTH" -H "X-Auth-Rest: $CM_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$CM_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$CM_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
