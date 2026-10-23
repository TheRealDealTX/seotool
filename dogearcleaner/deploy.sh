#!/bin/bash
# Deploy the built site (./site) to the Hostinger Agency website for dogearcleaner.com.
#
# Pushes every file in ./site through the website's File Browser TUS endpoint
# (the archive importer only accepts WordPress archives). Get the three
# credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# for the website UID (they expire after a few hours):
#
#   export DEC_FB_URL='https://…/api/tus'   # "url"
#   export DEC_FB_AUTH='…'                  # "auth_key"
#   export DEC_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (hPanel, or the API's clear-cache operation).
set -u
: "${DEC_FB_URL:?set DEC_FB_URL}" "${DEC_FB_AUTH:?set DEC_FB_AUTH}" "${DEC_FB_REST:?set DEC_FB_REST}"
cd "$(dirname "$0")/site" || exit 1

fb() { curl -sS --max-time 300 --retry 3 -H "X-Auth: $DEC_FB_AUTH" -H "X-Auth-Rest: $DEC_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$DEC_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$DEC_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"

# Pages are served by <dir>/index.php + <dir>/.page.html; remove any index.html
# left over from earlier deploys so it can't shadow the short-cache PHP stub.
REST="${DEC_FB_URL%/tus}/resources/public_html"
while IFS= read -r d; do
  d=${d#./}; d=${d%/index.php}
  code=$(fb -X DELETE "$REST/$d/index.html" -o /dev/null -w "%{http_code}")
  [ "$code" = 204 ] && echo "removed stale $d/index.html"
done < <(find . -name index.php -mindepth 2 | sort)
[ "$fail" -eq 0 ]
