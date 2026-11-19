#!/bin/bash
# Deploy this site to the Hostinger Agency website (UID uiVmbjn30) through the
# File Browser TUS endpoint. Get the credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export HR_FB_URL='https://.../api/tus' HR_FB_AUTH='...' HR_FB_REST='...'
#   ./deploy.sh            # uploads every site file into public_html/
#
# Then clear the site cache (hPanel or the API).
set -u
: "${HR_FB_URL:?set HR_FB_URL}" "${HR_FB_AUTH:?set HR_FB_AUTH}" "${HR_FB_REST:?set HR_FB_REST}"
cd "$(dirname "$0")" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $HR_FB_AUTH" -H "X-Auth-Rest: $HR_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$HR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$HR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -path './scripts/*' ! -name 'deploy.sh' ! -name '*.md' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
