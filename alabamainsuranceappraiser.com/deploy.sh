#!/bin/bash
# Deploy ./public_html to the Hostinger Agency website for alabamainsuranceappraiser.com
# (website UID rMIbFS7kW) through its File Browser TUS endpoint.
#
# Get fresh credentials (they expire after a few hours) from the Hostinger API
# call `agency-hosting_files_generate-upload-url` with website_uid=rMIbFS7kW:
#
#   export AIA_FB_URL='https://…/api/tus'   # "url"
#   export AIA_FB_AUTH='…'                  # "auth_key"
#   export AIA_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the cache (`agency-hosting_cache_clear-website`).
#
# The SMTP config (.h5g/aia-config.php) lives beside public_html, outside the
# web root, and is never part of this upload; see README "Contact form".
set -u
: "${AIA_FB_URL:?set AIA_FB_URL}" "${AIA_FB_AUTH:?set AIA_FB_AUTH}" "${AIA_FB_REST:?set AIA_FB_REST}"
cd "$(dirname "$0")/public_html" || exit 1

fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $AIA_FB_AUTH" -H "X-Auth-Rest: $AIA_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$AIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$AIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name 'leads.log.php' ! -name 'config.local.php' | sort)

# Remove the platform's placeholder page if it is still there.
fb -X DELETE "${AIA_FB_URL%/tus}/resources/public_html/default.php" -o /dev/null || true

echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
