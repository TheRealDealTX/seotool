#!/bin/bash
# Push ./public to the Hostinger Agency website's public_html via the File Browser TUS API.
# Get fresh credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid nFY9v8sgn; they expire after a few hours):
#   export NYIA_FB_URL='https://…/tus'  NYIA_FB_AUTH='…'  NYIA_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the site cache (`agency-hosting_cache_clear-website`).
# This script only adds and overwrites. To remove a page or file that no longer exists in the build:
#   curl -X DELETE -H "X-Auth: $NYIA_FB_AUTH" -H "X-Auth-Rest: $NYIA_FB_REST" "${NYIA_FB_URL%/tus}/resources/public_html/<path>"
set -u
: "${NYIA_FB_URL:?set NYIA_FB_URL}" "${NYIA_FB_AUTH:?set NYIA_FB_AUTH}" "${NYIA_FB_REST:?set NYIA_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
# Never ship a dir/index.html page: the host would serve it without running the canonical-host guard.
if find . -name index.html | grep -q .; then echo "refusing: index.html page found in public/"; exit 1; fi
fb() { curl -sS --max-time 300 -H "X-Auth: $NYIA_FB_AUTH" -H "X-Auth-Rest: $NYIA_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(fb -X POST "$NYIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$NYIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && break
    sleep $((try * 2))
  done
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
