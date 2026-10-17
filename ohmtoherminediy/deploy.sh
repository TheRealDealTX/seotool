#!/bin/bash
# Deploy ./public to the Hostinger Agency website WSPEsjCDT (ohmtoherminediy.com,
# temporary domain mediumseagreen-wallaby-208321.hostingersite.com).
#
# Uploads every built file through the website's File Browser TUS endpoint.
# Get the credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export OMM_FB_URL='https://…/api/tus'   # "url"
#   export OMM_FB_AUTH='…'                  # "auth_key"
#   export OMM_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
set -u
: "${OMM_FB_URL:?set OMM_FB_URL}" "${OMM_FB_AUTH:?set OMM_FB_AUTH}" "${OMM_FB_REST:?set OMM_FB_REST}"
cd "$(dirname "$0")/public" || exit 1

fb() { curl -sS --max-time 300 --retry 3 --retry-delay 2 -H "X-Auth: $OMM_FB_AUTH" -H "X-Auth-Rest: $OMM_FB_REST" "$@"; }
up() {
  local f=$1 rel=${1#./} size
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$OMM_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$OMM_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "ok $rel"; else echo "FAIL $c/$p $rel"; fi
}
export -f up fb
export OMM_FB_URL OMM_FB_AUTH OMM_FB_REST
# index.php and home.html go last so the new homepage only switches over once assets are in place
find . -type f ! -name index.php ! -name home.html -print0 | sort -z | xargs -0 -n1 -P6 bash -c 'up "$0"' > /tmp/omm-deploy.log
up ./home.html >> /tmp/omm-deploy.log; up ./index.php >> /tmp/omm-deploy.log
ok=$(grep -c '^ok' /tmp/omm-deploy.log); fail=$(grep -c '^FAIL' /tmp/omm-deploy.log)
grep '^FAIL' /tmp/omm-deploy.log
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
