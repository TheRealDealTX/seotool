#!/bin/bash
# Deploy ./public to monetizinginfluencers.com (Hostinger web hosting, user u401386392,
# Cloud Enterprise order 64270646) through the File Browser TUS upload API.
#
# Get credentials from the Hostinger API call `hosting_files_generate-upload-url`
# (username u401386392, domain monetizinginfluencers.com). They expire after a few hours.
#
#   export MI_FB_URL='https://srvNNNN-files.hstgr.io/rest/<id>/api/tus/public_html'   # "url"
#   export MI_FB_AUTH='…'   # "auth_key"
#   export MI_FB_REST='…'   # "rest_auth_key"
#   python3 validate.py && ./deploy.sh
#
# .htaccess is uploaded last so the new pages exist before the rewrite rules switch over.
set -u
: "${MI_FB_URL:?set MI_FB_URL}" "${MI_FB_AUTH:?set MI_FB_AUTH}" "${MI_FB_REST:?set MI_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $MI_FB_AUTH" -H "X-Auth-Rest: $MI_FB_REST" "$@"; }

upload() {
  local rel=$1 size c p
  size=$(stat -c%s "$rel")
  c=$(fb -X POST "$MI_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$MI_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
}

ok=0; fail=0
while IFS= read -r f; do upload "${f#./}"; done < <(find . -type f ! -name '.htaccess' | sort)
find . -mindepth 2 -name '.htaccess' | sort | while IFS= read -r f; do echo "${f#./}"; done > /tmp/mi_ht.$$
while IFS= read -r f; do upload "$f"; done < /tmp/mi_ht.$$
rm -f /tmp/mi_ht.$$
[ "$fail" -eq 0 ] && upload ".htaccess"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
