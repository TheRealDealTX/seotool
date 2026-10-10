#!/bin/bash
# Deploy public/ to the Hostinger Agency website for asmith.photography
# (UID xpKP4rrWT, temporary domain purple-baboon-917875.hostingersite.com).
#
# Pushes each built file through the website's File Browser TUS endpoint.
# Get credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (website_uid xpKP4rrWT); they expire:
#
#   export AS_FB_URL='https://…/api/tus'   # "url"
#   export AS_FB_AUTH='…'                  # "auth_key"
#   export AS_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh [files…]
#
# With no arguments every file in public/ is uploaded. Clear the site cache afterwards.
set -u
: "${AS_FB_URL:?set AS_FB_URL}" "${AS_FB_AUTH:?set AS_FB_AUTH}" "${AS_FB_REST:?set AS_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $AS_FB_AUTH" -H "X-Auth-Rest: $AS_FB_REST" "$@"; }
up() {
  local rel=${1#./} size; size=$(stat -c%s "$1")
  local c p
  c=$(fb -X POST "$AS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$AS_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$1" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo ok; else echo "FAIL $c/$p $rel" >&2; echo fail; fi
}
export -f up fb; export AS_FB_URL AS_FB_AUTH AS_FB_REST
if [ $# -gt 0 ]; then printf '%s\n' "$@"; else find . -type f | sort; fi \
  | xargs -P 6 -I{} bash -c 'up "{}"' | sort | uniq -c
