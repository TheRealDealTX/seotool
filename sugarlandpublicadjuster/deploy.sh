#!/bin/bash
# Deploy public_html/ to sugarlandpublicadjuster.com (Hostinger Cloud Enterprise,
# account u401386392) through the File Browser TUS upload API.
#
# Get credentials from the Hostinger API call `hosting_files_generate-upload-url`
# (username u401386392, domain sugarlandpublicadjuster.com); they expire after a few hours:
#
#   export SL_FB_URL='https://…'   # "url"
#   export SL_FB_AUTH='…'          # "auth_key"
#   export SL_FB_REST='…'          # "rest_auth_key"
#   ./deploy.sh            # everything except wp-content/uploads (already on the server)
#   ./deploy.sh --all      # include wp-content/uploads
#
# index.php and .htaccess are uploaded last so the switch-over happens in one step.
# Afterwards clear the cache (`hosting_cache_clear-website`), which also purges the CDN.
set -u
: "${SL_FB_URL:?set SL_FB_URL}" "${SL_FB_AUTH:?set SL_FB_AUTH}" "${SL_FB_REST:?set SL_FB_REST}"
cd "$(dirname "$0")/public_html" || exit 1
ALL=${1:-}

up() {
  local f=$1 rel=${1#./} size c p
  size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(curl -sS --max-time 300 -X POST "$SL_FB_URL/$rel?override=true" -H "X-Auth: $SL_FB_AUTH" -H "X-Auth-Rest: $SL_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -X PATCH "$SL_FB_URL/$rel?override=true" -H "X-Auth: $SL_FB_AUTH" -H "X-Auth-Rest: $SL_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$f" -o /dev/null -w "%{http_code}")
    if [ "$c" = 201 ] && [ "$p" = 204 ]; then return 0; fi
    sleep $((try * 2))
  done
  echo "FAIL $c/$p $rel"; return 1
}

skip=(! -path './index.php' ! -path './.htaccess')
[ "$ALL" = --all ] || skip+=(! -path './wp-content/*')
ok=0; fail=0
while IFS= read -r f; do
  if up "$f"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done < <(find . -type f "${skip[@]}" | sort)
for f in ./index.php ./.htaccess; do
  if up "$f"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
