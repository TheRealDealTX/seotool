#!/bin/bash
# Deploy the dukoraidea.com build to its Hostinger Agency website (UID 5Iuo12rhh).
#
# Files are pushed one by one through the website's File Browser TUS endpoint.
# Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (website_uid 5Iuo12rhh; they expire after a few hours):
#
#   export DK_FB_URL='https://…/api/tus'      # "url" from the response
#   export DK_FB_AUTH='…'                     # "auth_key"
#   export DK_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (hPanel, or the Agency cache-clear API call).
set -u
: "${DK_FB_URL:?set DK_FB_URL}" "${DK_FB_AUTH:?set DK_FB_AUTH}" "${DK_FB_REST:?set DK_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $DK_FB_AUTH" -H "X-Auth-Rest: $DK_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  dest="public_html/$rel"
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$DK_FB_URL/$dest?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$DK_FB_URL/$dest?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './content' -o -path '*/__pycache__' -o -name '*.py' -o -name 'README.md' -o -name '.gitignore' \
          -o -name 'deploy.sh' -o -name 'sizes.json' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
