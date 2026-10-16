#!/bin/bash
# Deploy public/ to the Hostinger Agency website for relationadvisor.com
# (website UID 28XI7AXR5, temporary domain cyan-hummingbird-576843.hostingersite.com).
#
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid 28XI7AXR5); they expire after a few hours:
#
#   export RA_FB_URL='https://…/api/tus'   # "url"
#   export RA_FB_AUTH='…'                  # "auth_key"
#   export RA_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Files are uploaded one by one (8 in parallel) into public_html/.
set -u
: "${RA_FB_URL:?set RA_FB_URL}" "${RA_FB_AUTH:?set RA_FB_AUTH}" "${RA_FB_REST:?set RA_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
export RA_FB_URL RA_FB_AUTH RA_FB_REST

upload() {
  local rel=${1#./} size c p i
  size=$(stat -c%s "$1")
  for i in 1 2 3; do
    c=$(curl -sS --max-time 120 -X POST "$RA_FB_URL/public_html/$rel?override=true" -H "X-Auth: $RA_FB_AUTH" -H "X-Auth-Rest: $RA_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -X PATCH "$RA_FB_URL/public_html/$rel?override=true" -H "X-Auth: $RA_FB_AUTH" -H "X-Auth-Rest: $RA_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$1" -o /dev/null -w "%{http_code}")
    if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "OK $rel"; return 0; fi
    sleep $((i * 2))
  done
  echo "FAIL $c/$p $rel"
}
export -f upload

find . -type f | sort | xargs -P 8 -I{} bash -c 'upload "{}"' > ../.deploy.log
ok=$(grep -c '^OK' ../.deploy.log); fail=$(grep -c '^FAIL' ../.deploy.log)
grep '^FAIL' ../.deploy.log
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
