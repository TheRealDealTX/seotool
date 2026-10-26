#!/bin/bash
# Deploy bastroproofs.com to the Hostinger Agency website (UID wIZQiliPf).
#
# Pushes every site file through the website's File Browser TUS endpoint.
# Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export BR_FB_URL='https://…/api/tus'   # "url"
#   export BR_FB_AUTH='…'                  # "auth_key"
#   export BR_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh
#
# Then clear the site cache (`agency-hosting_cache_clear-website`).
set -u
: "${BR_FB_URL:?set BR_FB_URL}" "${BR_FB_AUTH:?set BR_FB_AUTH}" "${BR_FB_REST:?set BR_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $BR_FB_AUTH" -H "X-Auth-Rest: $BR_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$BR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$BR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './bin' -o -name 'README.md' -o -name 'deploy.sh' -o -name '__pycache__' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
