#!/bin/bash
# Deploy public/ to the Hostinger Agency website (UID DlnCdXsX9, temp domain
# snow-mole-583626.hostingersite.com) through its File Browser TUS endpoint.
# Get the credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# with website_uid=DlnCdXsX9 (they expire after a few hours):
#
#   export AG_FB_URL='https://…/api/tus'   # "url"
#   export AG_FB_AUTH='…'                  # "auth_key"
#   export AG_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (agency-hosting clear cache, or hPanel).
set -u
: "${AG_FB_URL:?set AG_FB_URL}" "${AG_FB_AUTH:?set AG_FB_AUTH}" "${AG_FB_REST:?set AG_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $AG_FB_AUTH" -H "X-Auth-Rest: $AG_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(fb -X POST "$AG_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$AG_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && break
    sleep $((try * 2))
  done
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name '*.jsonl' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
