#!/bin/bash
# Upload public/ to the Hostinger Agency website's public_html over the File
# Browser TUS endpoint. Get the credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export HR_FB_URL='https://…/api/tus' HR_FB_AUTH='…' HR_FB_REST='…'
#   ./deploy.sh            # code + assets (skips old WP uploads)
#   ./deploy.sh --all      # also public/wp-content/uploads (first deploy)
#
# config.local.php, app/data and media/ (listing photos the sync downloads on
# the server) are never uploaded.
set -u
: "${HR_FB_URL:?set HR_FB_URL}" "${HR_FB_AUTH:?set HR_FB_AUTH}" "${HR_FB_REST:?set HR_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

up() {
  local f=${1#./} size c p
  size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(curl -sS --max-time 300 -X POST "$HR_FB_URL/public_html/$f?override=true" -H "X-Auth: $HR_FB_AUTH" -H "X-Auth-Rest: $HR_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -X PATCH "$HR_FB_URL/public_html/$f?override=true" -H "X-Auth: $HR_FB_AUTH" -H "X-Auth-Rest: $HR_FB_REST" \
          -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$f" -o /dev/null -w "%{http_code}")
    if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "ok $f"; return 0; fi
    sleep $((try * 2))
  done
  echo "FAIL $c/$p $f"
}
export -f up

skip=(-path ./app/data -o -path ./media -o -name config.local.php -o -name '*.sqlite*')
[ "${1:-}" = "--all" ] || skip+=(-o -path ./wp-content/uploads)
find . \( "${skip[@]}" \) -prune -o -type f -print | sort | xargs -P 8 -I{} bash -c 'up "$@"' _ {} > /tmp/ha-deploy.log
echo "uploaded=$(grep -c '^ok' /tmp/ha-deploy.log) failed=$(grep -c '^FAIL' /tmp/ha-deploy.log)"
grep '^FAIL' /tmp/ha-deploy.log
! grep -q '^FAIL' /tmp/ha-deploy.log
