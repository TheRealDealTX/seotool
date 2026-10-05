#!/bin/bash
# Deploy the build to the Hostinger Agency website (UID duFSuwfQj, beltonbanners.com).
#
# The platform's archive importer only accepts WordPress archives, so this
# pushes the built files one by one through the website's File Browser TUS
# endpoint. Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export BB_FB_URL='https://…/api/tus'      # "url" from the response
#   export BB_FB_AUTH='…'                     # "auth_key"
#   export BB_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_cache_clear-website`, or hPanel).
# Pass a path prefix as $1 to upload only part of the tree (e.g. ./deploy.sh assets).
set -u
: "${BB_FB_URL:?set BB_FB_URL}" "${BB_FB_AUTH:?set BB_FB_AUTH}" "${BB_FB_REST:?set BB_FB_REST}"
cd "$(dirname "$0")" || exit 1
PREFIX=${1:-.}

fb() { curl -sS --max-time 300 -H "X-Auth: $BB_FB_AUTH" -H "X-Auth-Rest: $BB_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$BB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$BB_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find "$PREFIX" -type f \( -path './.git/*' -o -path './backup/*' -o -path './content/*' \
          -o -name '*.py' -o -path '*/__pycache__/*' -o -name 'README.md' -o -name '.gitignore' \
          -o -name 'deploy.sh' \) -prune -o -type f -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
