#!/bin/bash
# Push ./public to the Hostinger Agency website's public_html via the File Browser TUS API.
# Get fresh credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid BijEtYhpF; they expire after a few hours):
#   export WIA_FB_URL='https://…/tus'  WIA_FB_AUTH='…'  WIA_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the site cache (`agency-hosting_cache_clear-website`).
#
# This script only adds and overwrites. To remove a page or file that no longer exists in the build:
#   ./deploy.sh --delete old-dir/index.php another/file.webp
# which sends DELETE {url-without-/tus}/resources/public_html/<path> with the same two auth headers.
set -u
: "${WIA_FB_URL:?set WIA_FB_URL}" "${WIA_FB_AUTH:?set WIA_FB_AUTH}" "${WIA_FB_REST:?set WIA_FB_REST}"
fb() { curl -sS --max-time 300 -H "X-Auth: $WIA_FB_AUTH" -H "X-Auth-Rest: $WIA_FB_REST" "$@"; }

if [ "${1:-}" = "--delete" ]; then
  shift
  base="${WIA_FB_URL%/tus}"
  for rel in "$@"; do
    c=$(fb -X DELETE "$base/resources/public_html/$rel" -o /dev/null -w "%{http_code}")
    echo "DELETE $c $rel"
  done
  exit 0
fi

cd "$(dirname "$0")/public" || exit 1
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(fb -X POST "$WIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$WIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && break
    sleep $((try * 2))
  done
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
