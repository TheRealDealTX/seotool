#!/bin/bash
# Deploy Purely Wholesome Farm to its Hostinger Agency website (UID ZST1Yj5FK).
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (they expire after a few hours):
#   export PW_FB_URL='https://…/api/tus'  PW_FB_AUTH='…'  PW_FB_REST='…'
#   ./deploy.sh              # everything
#   ./deploy.sh app assets   # only these paths
set -u
: "${PW_FB_URL:?set PW_FB_URL}" "${PW_FB_AUTH:?set PW_FB_AUTH}" "${PW_FB_REST:?set PW_FB_REST}"
cd "$(dirname "$0")" || exit 1
export PW_FB_URL PW_FB_AUTH PW_FB_REST
up() {
  f=${1#./}; size=$(stat -c%s "$f"); enc=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$f")
  for try in 1 2 3; do
    c=$(curl -sS --max-time 300 -X POST "$PW_FB_URL/public_html/$enc?override=true" -H "X-Auth: $PW_FB_AUTH" -H "X-Auth-Rest: $PW_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -X PATCH "$PW_FB_URL/public_html/$enc?override=true" -H "X-Auth: $PW_FB_AUTH" -H "X-Auth-Rest: $PW_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && { echo "ok $f"; return; }
    sleep $((try * 2))
  done
  echo "FAIL $c/$p $f"
}
export -f up
find "${@:-.}" -type f ! -path './_build/*' ! -path '_build/*' ! -name 'README.md' ! -name 'deploy.sh' ! -path '*/app/storage/messages.php' ! -path '*/app/storage/subscribers.php' ! -name '.DS_Store' \
  | sort | xargs -P 8 -I{} bash -c 'up "{}"' > /tmp/pw-deploy.log
grep -c '^ok' /tmp/pw-deploy.log | sed 's/^/uploaded=/'; grep '^FAIL' /tmp/pw-deploy.log; ! grep -q '^FAIL' /tmp/pw-deploy.log
