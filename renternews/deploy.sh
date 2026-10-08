#!/bin/bash
# Upload the built site (public/) to renternews.net on Hostinger (u401386392).
#
# Get fresh credentials from the Hostinger API operation
# `hosting_files_generate-upload-url` (username u401386392, domain renternews.net):
#   export RN_FB_URL='https://…/api/tus/public_html'   # "url"
#   export RN_FB_AUTH='…'                             # "auth_key"
#   export RN_FB_REST='…'                             # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the cache with `hosting_cache_clear-website`.
#
# Uploads everything except the unchanged WordPress media library
# (wp-content/) and the bundled ZIP lists. Pass --all to include them.
set -u
: "${RN_FB_URL:?set RN_FB_URL}" "${RN_FB_AUTH:?set RN_FB_AUTH}" "${RN_FB_REST:?set RN_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $RN_FB_AUTH" -H "X-Auth-Rest: $RN_FB_REST" -H "Tus-Resumable: 1.0.0" "$@"; }
if [ "${1:-}" = "--all" ]; then list=$(find . -type f | sort)
else list=$(find . -type f ! -path './wp-content/*' ! -path './assets/data/zips-*' | sort); fi
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$RN_FB_URL/$rel?override=true" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$RN_FB_URL/$rel?override=true" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done <<< "$list"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
