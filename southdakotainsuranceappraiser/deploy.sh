#!/bin/bash
# Push ./public to the Hostinger Agency website's public_html via the File Browser TUS API.
# Get fresh credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid 2FJj5lTsf; they expire after a few hours):
#   export SDIA_FB_URL='https://…/tus'  SDIA_FB_AUTH='…'  SDIA_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the site cache (`agency-hosting_cache_clear-website`).
# deploy.sh only adds and overwrites. To remove a page that was deleted or renamed:
#   curl -X DELETE -H "X-Auth: $SDIA_FB_AUTH" -H "X-Auth-Rest: $SDIA_FB_REST" "${SDIA_FB_URL%/tus}/resources/public_html/<path>"
set -u
: "${SDIA_FB_URL:?set SDIA_FB_URL}" "${SDIA_FB_AUTH:?set SDIA_FB_AUTH}" "${SDIA_FB_REST:?set SDIA_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $SDIA_FB_AUTH" -H "X-Auth-Rest: $SDIA_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$SDIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$SDIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
