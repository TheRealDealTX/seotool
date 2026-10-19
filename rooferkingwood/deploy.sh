#!/bin/bash
# Deploy dist/ to the Hostinger Agency website jhGHXYw37 (rooferkingwood.com) via the File Browser TUS endpoint.
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url` (they expire):
#   export KW_FB_URL='https://…'  KW_FB_AUTH='…'  KW_FB_REST='…'
#   python3 build.py && python3 check.py && ./deploy.sh
# Then clear the cache (`agency-hosting_cache_clear-website`).
set -u
: "${KW_FB_URL:?set KW_FB_URL}" "${KW_FB_AUTH:?set KW_FB_AUTH}" "${KW_FB_REST:?set KW_FB_REST}"
cd "$(dirname "$0")/dist" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $KW_FB_AUTH" -H "X-Auth-Rest: $KW_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(fb -X POST "$KW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$KW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && break
    sleep $((try * 2))
  done
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
