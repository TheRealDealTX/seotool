#!/bin/bash
# Upload the site to Hostinger (luxuryapartmentdesign.com, account u401386392).
#
# Get the three credentials from the Hostinger API operation
# `hosting_files_generate-upload-url` (username u401386392, domain
# luxuryapartmentdesign.com); they expire after a few hours:
#
#   export LAD_FB_URL='https://…'   # "url"
#   export LAD_FB_AUTH='…'          # "auth_key"
#   export LAD_FB_REST='…'          # "rest_auth_key"
#   ./deploy.sh                     # upload straight into public_html (normal updates)
#   ./deploy.sh _lad_new            # upload into a staging folder (first switchover only)
set -u
: "${LAD_FB_URL:?set LAD_FB_URL}" "${LAD_FB_AUTH:?set LAD_FB_AUTH}" "${LAD_FB_REST:?set LAD_FB_REST}"
cd "$(dirname "$0")" || exit 1
prefix=${1:+$1/}

fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $LAD_FB_AUTH" -H "X-Auth-Rest: $LAD_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$LAD_FB_URL/$prefix$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$LAD_FB_URL/$prefix$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path ./deploy -o -name '*.md' -o -name '*.py' -o -name 'deploy.sh' -o -name 'router.php' -o -name '.git*' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
