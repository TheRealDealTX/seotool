#!/bin/bash
# Deploy galvestonpublicadjuster.com to the Hostinger Agency website (UID lCCnMqaFW).
#
# Pushes files one by one through the website's File Browser TUS endpoint. Get the three
# credentials from the Hostinger API call `agency-hosting_generateUploadURLV1` (they expire):
#
#   export GPA_FB_URL='https://…/api/tus'   # "url"
#   export GPA_FB_AUTH='…'                  # "auth_key"
#   export GPA_FB_REST='…'                  # "rest_auth_key"
#   ./deploy.sh          # code, pages, assets and the blog queue
#   ./deploy.sh --init   # also runtime state (published.json, weather-*.json) — first deploy only,
#                        # later runs would overwrite what the weekly cron has written on the server
set -u
: "${GPA_FB_URL:?set GPA_FB_URL}" "${GPA_FB_AUTH:?set GPA_FB_AUTH}" "${GPA_FB_REST:?set GPA_FB_REST}"
cd "$(dirname "$0")" || exit 1
init=${1:-}

fb() { curl -sS --max-time 300 -H "X-Auth: $GPA_FB_AUTH" -H "X-Auth-Rest: $GPA_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  case "$rel" in
    data/published.json|data/weather-events.json|data/weather-status.json) [ "$init" = --init ] || continue ;;
  esac
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$GPA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$GPA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './tools' -o -path './data/private' -o -path './data/posts-generated' \) -prune -o -type f \
          ! -name '*.md' ! -name 'deploy.sh' ! -name '*.tmp' -print | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
