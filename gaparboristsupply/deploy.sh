#!/bin/bash
# Deploy site/ to the Hostinger Agency website for gaparboristsupply.com
# (UID wvWrkASNv, temporary domain greenyellow-woodcock-344499.hostingersite.com).
#
# Pushes each built file through the website's File Browser TUS endpoint. Get the
# three credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (they expire after a few hours):
#
#   export GAP_FB_URL='https://…/api/tus'   # "url" from the response
#   export GAP_FB_AUTH='…'                  # "auth_key"
#   export GAP_FB_REST='…'                  # "rest_auth_key"
#   php scripts/compile.php && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
set -u
: "${GAP_FB_URL:?set GAP_FB_URL}" "${GAP_FB_AUTH:?set GAP_FB_AUTH}" "${GAP_FB_REST:?set GAP_FB_REST}"
cd "$(dirname "$0")/site" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $GAP_FB_AUTH" -H "X-Auth-Rest: $GAP_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$GAP_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$GAP_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f \( -path './data/products/*' -o -path './data/categories/*' \
          -o -name 'brands.json' -o -name 'guides.json' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
