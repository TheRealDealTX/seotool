#!/bin/bash
# Upload public/ to the Hostinger Agency website through its File Browser TUS endpoint.
# Get fresh credentials (they expire after a few hours) from the Hostinger API call
# `agency-hosting_files_generate-upload-url` with website_uid 8ppHiZSjN, then:
#
#   export LS_FB_URL='https://…/api/tus' LS_FB_AUTH='…' LS_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${LS_FB_URL:?set LS_FB_URL}" "${LS_FB_AUTH:?set LS_FB_AUTH}" "${LS_FB_REST:?set LS_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
export LS_FB_URL LS_FB_AUTH LS_FB_REST

up() {
  local rel=${1#./} size c p
  size=$(stat -c%s "$1")
  c=$(curl -sS --max-time 300 -H "X-Auth: $LS_FB_AUTH" -H "X-Auth-Rest: $LS_FB_REST" -X POST \
        "$LS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --max-time 300 -H "X-Auth: $LS_FB_AUTH" -H "X-Auth-Rest: $LS_FB_REST" -X PATCH \
        "$LS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$1" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo OK; else echo "FAIL $c/$p $rel"; fi
}
export -f up
out=$(find . -type f | sort | xargs -P 8 -I{} bash -c 'up "$@"' _ {})
echo "$out" | grep FAIL
echo "uploaded=$(echo "$out" | grep -c '^OK') failed=$(echo "$out" | grep -c FAIL)"
! echo "$out" | grep -q FAIL
