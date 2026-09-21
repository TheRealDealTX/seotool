#!/bin/bash
# Deploy the rooftarp.com static build to its Hostinger Agency website.
#
# The platform's archive importer only accepts WordPress archives, so this
# pushes the built files one by one through the website's File Browser TUS
# endpoint -- the same path huttoroofs.com (repo root) deploys through. Get the
# three credentials from the Hostinger API call
# `agency-hosting_generateUploadURLV1` for this website's UID (they expire
# after a few hours):
#
#   export RT_FB_URL='https://…/api/tus'      # "url" from the response
#   export RT_FB_AUTH='…'                     # "auth_key"
#   export RT_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_clearWebsiteCacheV1`, or hPanel).
#
# Only servable files go up. Source (build.py, content/), the backup archive
# and the deploy tooling are excluded -- the backup must never be web-served.
set -u
: "${RT_FB_URL:?set RT_FB_URL}" "${RT_FB_AUTH:?set RT_FB_AUTH}" "${RT_FB_REST:?set RT_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $RT_FB_AUTH" -H "X-Auth-Rest: $RT_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$RT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$RT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f \( -path './.git/*' -o -path './content/*' -o -path './backup/*' \
          -o -name '*.py' -o -path '*/__pycache__/*' -o -name 'prune-list.txt' \
          -o -name 'README.md' -o -name '.gitignore' -o -name '*.sh' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
