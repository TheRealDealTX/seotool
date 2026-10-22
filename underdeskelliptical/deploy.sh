#!/bin/bash
# Deploy to the Hostinger Agency website for underdeskelliptical.com (plain php-fpm site, UID FQYNNuIDk).
#
# Pushes the site files one by one through the website's File Browser TUS endpoint.
# Get the three credentials from the Hostinger API call that generates a File Browser
# upload URL for the website (they expire after a few hours):
#
#   export UDE_FB_URL='https://…/api/tus'      # "url" from the response
#   export UDE_FB_AUTH='…'                     # "auth_key"
#   export UDE_FB_REST='…'                     # "rest_auth_key"
#   ./deploy.sh
#
# Afterwards clear the site cache.
set -u
: "${UDE_FB_URL:?set UDE_FB_URL}" "${UDE_FB_AUTH:?set UDE_FB_AUTH}" "${UDE_FB_REST:?set UDE_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $UDE_FB_AUTH" -H "X-Auth-Rest: $UDE_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$UDE_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$UDE_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './dev' -o -path './data/messages.php' -o -name 'README.md' -o -name 'deploy.sh' -o -name '.git*' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
