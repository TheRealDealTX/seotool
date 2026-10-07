#!/bin/bash
# Deploy public/ to the cebudavao.com Hostinger Agency website through its
# File Browser TUS endpoint. Get credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export CD_FB_URL='https://…/api/tus' CD_FB_AUTH='…' CD_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh            # everything
#   ./deploy.sh changed                                               # only files changed since last deploy
#
# Then clear the site cache (`agency-hosting_clear-website-cache`, or hPanel).
set -u
: "${CD_FB_URL:?set CD_FB_URL}" "${CD_FB_AUTH:?set CD_FB_AUTH}" "${CD_FB_REST:?set CD_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
STAMP=../.last-deploy
fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $CD_FB_AUTH" -H "X-Auth-Rest: $CD_FB_REST" "$@"; }
up() {
  local f=$1 rel=${1#./} size
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$CD_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$CD_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo ok; else echo "FAIL $c/$p $rel" >&2; echo fail; fi
}
export -f up fb; export CD_FB_URL CD_FB_AUTH CD_FB_REST
if [ "${1:-}" = changed ] && [ -f "$STAMP" ]; then list=$(find . -type f -newer "$STAMP"); else list=$(find . -type f); fi
res=$(printf '%s\n' "$list" | sort | xargs -P 8 -I{} bash -c 'up "{}"')
ok=$(grep -c '^ok' <<<"$res"); fail=$(grep -c '^fail' <<<"$res")
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ] && touch "$STAMP"
[ "$fail" -eq 0 ]
