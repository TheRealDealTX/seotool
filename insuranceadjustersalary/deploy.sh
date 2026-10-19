#!/bin/bash
# Deploy insuranceadjustersalary to its Hostinger Agency website (UID SU5z7VSkt) through the
# File Browser TUS endpoint. Get credentials from `agency-hosting_files_generate-upload-url`
# (they expire after a few hours):
#
#   export IAS_FB_URL='https://…/api/tus'   # "url"
#   export IAS_FB_AUTH='…'                  # "auth_key"
#   export IAS_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh
set -u
: "${IAS_FB_URL:?set IAS_FB_URL}" "${IAS_FB_AUTH:?set IAS_FB_AUTH}" "${IAS_FB_REST:?set IAS_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $IAS_FB_AUTH" -H "X-Auth-Rest: $IAS_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$IAS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$IAS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name 'deploy.sh' ! -name 'README.md' ! -name 'POST_SPEC.md' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
