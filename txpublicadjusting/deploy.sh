#!/bin/bash
# Upload site/ to a Hostinger Agency website's public_html through its File
# Browser TUS endpoint (the plain-PHP platform has no git or SFTP deploy).
#
# 1. Get credentials with the Hostinger API call `agency-hosting_files_generate-upload-url`
#    (website_uid: cR6CoQmvm for the preview; they expire after a few hours):
#      export TX_FB_URL='https://…/api/tus'   # "url"
#      export TX_FB_AUTH='…'                  # "auth_key"
#      export TX_FB_REST='…'                  # "rest_auth_key"
# 2. ./deploy.sh            # uploads every file under site/
#    ./deploy.sh path …     # or only the given paths, relative to site/
# 3. Clear the site cache (`agency-hosting_cache_clear-website` or hPanel).
#
# Never uploaded: anything under site/storage except its guard files (leads and
# the form secret live on the server only).
set -u
: "${TX_FB_URL:?set TX_FB_URL}" "${TX_FB_AUTH:?set TX_FB_AUTH}" "${TX_FB_REST:?set TX_FB_REST}"
cd "$(dirname "$0")/site" || exit 1

fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $TX_FB_AUTH" -H "X-Auth-Rest: $TX_FB_REST" "$@"; }

if [ $# -gt 0 ]; then
  files=$(printf '%s\n' "$@")
else
  files=$(find . -type f ! -path './storage/*' -print | sed 's#^\./##' | sort; printf 'storage/index.php\nstorage/.htaccess\n')
fi

ok=0; fail=0
while IFS= read -r rel; do
  [ -f "$rel" ] || { echo "skip (missing) $rel"; continue; }
  size=$(stat -c%s "$rel")
  url="$TX_FB_URL/public_html/$(printf '%s' "$rel" | sed 's/ /%20/g')?override=true"
  c=$(fb -X POST "$url" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$url" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done <<< "$files"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
