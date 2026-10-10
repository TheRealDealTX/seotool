#!/bin/bash
# Deploy ./public to the Hostinger Agency website BzzTLgzXV (heathergreenstudios.com;
# temporary domain lightcoral-mole-192256.hostingersite.com) through its File
# Browser TUS endpoint. Get credentials from `agency-hosting_files_generate-upload-url`
# (they expire after a few hours):
#
#   export HG_FB_URL='https://…/api/tus' HG_FB_AUTH='…' HG_FB_REST='…'
#   python3 build.py && ./deploy.sh
set -u
: "${HG_FB_URL:?set HG_FB_URL}" "${HG_FB_AUTH:?set HG_FB_AUTH}" "${HG_FB_REST:?set HG_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $HG_FB_AUTH" -H "X-Auth-Rest: $HG_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$HG_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$HG_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
