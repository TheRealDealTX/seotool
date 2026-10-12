#!/bin/bash
# Upload ./public to the Hostinger Agency website's public_html via the File Browser TUS API.
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website UID TgdLuLxCB); they expire after a few hours:
#
#   export MW_FB_URL='https://…/api/tus' MW_FB_AUTH='…' MW_FB_REST='…'
#   python3 build.py && ./deploy.sh
set -u
: "${MW_FB_URL:?set MW_FB_URL}" "${MW_FB_AUTH:?set MW_FB_AUTH}" "${MW_FB_REST:?set MW_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $MW_FB_AUTH" -H "X-Auth-Rest: $MW_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$MW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$MW_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
