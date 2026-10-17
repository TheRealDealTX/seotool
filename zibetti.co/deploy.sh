#!/bin/bash
# Deploy ./site to the Hostinger Agency website for zibetti.co (UID SnbVxef3f).
#
# Pushes each file through the website's File Browser TUS endpoint. Get the three
# credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (they expire after a few hours):
#
#   export ZB_FB_URL='https://…/api/tus'   # "url"
#   export ZB_FB_AUTH='…'                  # "auth_key"
#   export ZB_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${ZB_FB_URL:?set ZB_FB_URL}" "${ZB_FB_AUTH:?set ZB_FB_AUTH}" "${ZB_FB_REST:?set ZB_FB_REST}"
cd "$(dirname "$0")/site" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $ZB_FB_AUTH" -H "X-Auth-Rest: $ZB_FB_REST" "$@"; }

upload() {
  local rel=$1 size c p
  size=$(stat -c%s "$rel")
  c=$(fb -X POST "$ZB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$ZB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "ok $rel"; else echo "FAIL $c/$p $rel"; fi
}
export -f upload fb
export ZB_FB_URL ZB_FB_AUTH ZB_FB_REST

find . -type f | sed 's#^\./##' | sort | xargs -P 6 -I{} bash -c 'upload "$@"' _ {} > /tmp/zb-deploy.log
ok=$(grep -c '^ok ' /tmp/zb-deploy.log); fail=$(grep -c '^FAIL' /tmp/zb-deploy.log)
grep '^FAIL' /tmp/zb-deploy.log
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
