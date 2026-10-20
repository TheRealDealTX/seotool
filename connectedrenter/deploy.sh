#!/bin/bash
# Deploy the static build to the Hostinger Agency website (UID 59z2Fco9q, connectedrenter.com).
#
# Pushes the built files one by one through the website's File Browser TUS endpoint.
# Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export CR_FB_URL='https://…/api/tus'   # "url"
#   export CR_FB_AUTH='…'                  # "auth_key"
#   export CR_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${CR_FB_URL:?set CR_FB_URL}" "${CR_FB_AUTH:?set CR_FB_AUTH}" "${CR_FB_REST:?set CR_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $CR_FB_AUTH" -H "X-Auth-Rest: $CR_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$CR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$CR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './content' -o -path '*/__pycache__' \) -prune -o -type f \
          ! -name '*.py' ! -name 'README.md' ! -name 'deploy.sh' -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
