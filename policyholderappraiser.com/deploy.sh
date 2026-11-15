#!/bin/bash
# Upload public/ to the Hostinger website for policyholderappraiser.com through
# the File Browser TUS endpoint. Get fresh credentials (they expire after a few
# hours) from the Hostinger API operation hosting_files_generate-upload-url
# (username u401386392, domain policyholderappraiser.com), then:
#
#   export PHA_FB_URL='https://…/api/tus/public_html'   # "url"
#   export PHA_FB_AUTH='…'                              # "auth_key"
#   export PHA_FB_REST='…'                              # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${PHA_FB_URL:?set PHA_FB_URL}" "${PHA_FB_AUTH:?set PHA_FB_AUTH}" "${PHA_FB_REST:?set PHA_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $PHA_FB_AUTH" -H "X-Auth-Rest: $PHA_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$PHA_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$PHA_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
