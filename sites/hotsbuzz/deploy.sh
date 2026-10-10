#!/bin/bash
# Deploy ./public to the hotsbuzz Hostinger Agency website (plain php-fpm
# website, currently on its temporary domain). Same mechanism as the repo-root
# deploy.sh: files go one by one through the website's File Browser TUS API.
# Get the three credentials from the Hostinger API call
# `agency-hosting_generateUploadURLV1` for the hotsbuzz website (they expire
# after a few hours):
#
#   export HB_FB_URL='https://…/api/tus'      # "url" from the response
#   export HB_FB_AUTH='…'                     # "auth_key"
#   export HB_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
set -u
: "${HB_FB_URL:?set HB_FB_URL}" "${HB_FB_AUTH:?set HB_FB_AUTH}" "${HB_FB_REST:?set HB_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $HB_FB_AUTH" -H "X-Auth-Rest: $HB_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$HB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$HB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
