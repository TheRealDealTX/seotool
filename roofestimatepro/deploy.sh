#!/bin/bash
# Deploy public/ to the Hostinger Agency website for roofestimatepro.com.
#
# Pushes the built files one by one through the website's File Browser TUS
# endpoint (the platform's archive importer only accepts WordPress archives).
# Get the three credentials from the Hostinger API call
# `agency-hosting_generateUploadURLV1` for the website (they expire after a few hours):
#
#   export REP_FB_URL='https://…/api/tus'      # "url" from the response
#   export REP_FB_AUTH='…'                     # "auth_key"
#   export REP_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py --staging && python3 validate.py && ./deploy.sh     # temporary domain
#   python3 build.py && python3 validate.py && ./deploy.sh               # once roofestimatepro.com points here
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
set -u
: "${REP_FB_URL:?set REP_FB_URL}" "${REP_FB_AUTH:?set REP_FB_AUTH}" "${REP_FB_REST:?set REP_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

up() {
  local f=$1 rel=${1#./} size c p
  size=$(stat -c%s "$f")
  c=$(curl -sS --retry 3 --max-time 300 -H "X-Auth: $REP_FB_AUTH" -H "X-Auth-Rest: $REP_FB_REST" -X POST \
        "$REP_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --retry 3 --max-time 300 -H "X-Auth: $REP_FB_AUTH" -H "X-Auth-Rest: $REP_FB_REST" -X PATCH \
        "$REP_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo OK; else echo "FAIL $c/$p $rel"; fi
}
export -f up
export REP_FB_URL REP_FB_AUTH REP_FB_REST

# Eight uploads at a time.
out=$(find . -type f -print0 | sort -z | xargs -0 -P 8 -I{} bash -c 'up "$1"' _ {})
ok=$(grep -c '^OK$' <<<"$out"); fail=$(grep -c '^FAIL' <<<"$out")
grep '^FAIL' <<<"$out"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
