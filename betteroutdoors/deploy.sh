#!/bin/bash
# Deploy Better Outdoors to its Hostinger Agency website through the File
# Browser TUS endpoint. Get the credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export BO_FB_URL='https://…/api/tus'   # "url"
#   export BO_FB_AUTH='…'                  # "auth_key"
#   export BO_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh            # everything
#   ./deploy.sh --code     # skip wp-content images (code-only redeploy)
set -u
: "${BO_FB_URL:?set BO_FB_URL}" "${BO_FB_AUTH:?set BO_FB_AUTH}" "${BO_FB_REST:?set BO_FB_REST}"
cd "$(dirname "$0")" || exit 1
skip_media=0; [ "${1:-}" = "--code" ] && skip_media=1

fb() { curl -sS --max-time 300 -H "X-Auth: $BO_FB_AUTH" -H "X-Auth-Rest: $BO_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  [ $skip_media = 1 ] && [[ $rel == wp-content/* ]] && continue
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$BO_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$BO_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name '*.py' ! -name 'deploy.sh' ! -name 'README.md' ! -path '*/__pycache__/*' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
