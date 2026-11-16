#!/bin/bash
# Deploy ./public to the Hostinger Agency website (UID 85ugmexVF).
#
# Pushes each built file through the website's File Browser TUS endpoint. Get the
# three credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid 85ugmexVF; they expire after a few hours):
#
#   export RF_FB_URL='https://…/api/tus'   # "url"
#   export RF_FB_AUTH='…'                  # "auth_key"
#   export RF_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh [changed-files-only]
#
# Then clear the site cache (`agency-hosting_cache_clear-website`).
set -u
: "${RF_FB_URL:?set RF_FB_URL}" "${RF_FB_AUTH:?set RF_FB_AUTH}" "${RF_FB_REST:?set RF_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $RF_FB_AUTH" -H "X-Auth-Rest: $RF_FB_REST" "$@"; }
up() {
  local f=$1 rel=${1#./} size; size=$(stat -c%s "$f")
  local c p
  c=$(fb -X POST "$RF_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$RF_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "ok $rel"; else echo "FAIL $c/$p $rel"; fi
}
export -f up fb; export RF_FB_URL RF_FB_AUTH RF_FB_REST
find . -type f | sort | xargs -P 6 -I{} bash -c 'up "{}"' > ../deploy.log
echo "uploaded=$(grep -c '^ok' ../deploy.log) failed=$(grep -c '^FAIL' ../deploy.log)"
grep '^FAIL' ../deploy.log
[ "$(grep -c '^FAIL' ../deploy.log)" -eq 0 ]
