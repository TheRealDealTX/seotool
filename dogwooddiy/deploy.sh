#!/bin/bash
# Deploy ./public to the Hostinger Agency website for dogwooddiy.com (UID cMBtJbc7B).
#
# Pushes the built files one by one through the website's File Browser TUS
# endpoint. Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export DW_FB_URL='https://…/api/tus'      # "url"
#   export DW_FB_AUTH='…'                     # "auth_key"
#   export DW_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_cache_clear-website`, or hPanel).
set -u
: "${DW_FB_URL:?set DW_FB_URL}" "${DW_FB_AUTH:?set DW_FB_AUTH}" "${DW_FB_REST:?set DW_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $DW_FB_AUTH" -H "X-Auth-Rest: $DW_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$DW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$DW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
