#!/bin/bash
# Upload public/ to arriveoutdoors.com (Hostinger web hosting, account u401386392).
#
# Get fresh credentials (they expire after a few hours) from the Hostinger API call
# `hosting_files_generate-upload-url` with username=u401386392, domain=arriveoutdoors.com:
#
#   export AO_FB_URL='https://…'   # "url"
#   export AO_FB_AUTH='…'          # "auth_key"
#   export AO_FB_REST='…'          # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Uploads overwrite files of the same name. WordPress files are left in place
# (see backup-wordpress/README.md for rollback).
set -u
: "${AO_FB_URL:?set AO_FB_URL}" "${AO_FB_AUTH:?set AO_FB_AUTH}" "${AO_FB_REST:?set AO_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $AO_FB_AUTH" -H "X-Auth-Rest: $AO_FB_REST" "$@"; }
ok=0; fail=0
upload() {
  local rel=$1 size; size=$(stat -c%s "$rel")
  local c p
  c=$(fb -X POST "$AO_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$AO_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
}
# Content first; .htaccess and index.php last so the switch-over happens only once everything is there.
while IFS= read -r f; do upload "${f#./}"; done < <(find . -type f ! -name .htaccess ! -path ./index.php ! -path ./index.html | sort)
upload index.html; upload index.php; upload .htaccess
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
