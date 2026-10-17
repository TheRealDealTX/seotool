#!/bin/bash
# Deploy ./public to the Hostinger Agency website for bcpaperdesigns.com (UID DVA2OMwns).
#
# Uploads each built file through the website's File Browser TUS endpoint. Get the
# three credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid DVA2OMwns; they expire after a few hours):
#
#   export BC_FB_URL='https://…/api/tus'   # "url"
#   export BC_FB_AUTH='…'                  # "auth_key"
#   export BC_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (hPanel, or the Agency cache-clear API call).
set -u
: "${BC_FB_URL:?set BC_FB_URL}" "${BC_FB_AUTH:?set BC_FB_AUTH}" "${BC_FB_REST:?set BC_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $BC_FB_AUTH" -H "X-Auth-Rest: $BC_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$BC_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$BC_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
