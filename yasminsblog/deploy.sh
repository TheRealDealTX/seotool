#!/bin/bash
# Deploy ./public to a Hostinger Agency website (plain php-fpm, not WordPress).
#
# Uploads each built file through the website's File Browser TUS endpoint.
# Get the credentials from the Hostinger API call
# `agency-hosting_generateUploadURLV1` for the yasminsblog website (they expire
# after a few hours):
#
#   export YB_FB_URL='https://…/api/tus'   # "url"
#   export YB_FB_AUTH='…'                  # "auth_key"
#   export YB_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
set -u
: "${YB_FB_URL:?set YB_FB_URL}" "${YB_FB_AUTH:?set YB_FB_AUTH}" "${YB_FB_REST:?set YB_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $YB_FB_AUTH" -H "X-Auth-Rest: $YB_FB_REST" "$@"; }
enc() { python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$1"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=$(enc "${f#./}")
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$YB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$YB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p ${f#./}"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
