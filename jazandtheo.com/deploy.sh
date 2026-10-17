#!/bin/bash
# Deploy the build to the Hostinger Agency website (UID tjhqL1FqG).
# Temporary domain: darkseagreen-wildcat-209722.hostingersite.com
#
# The platform's archive importer only accepts WordPress archives, so this
# pushes the built files one by one through the website's File Browser TUS
# endpoint. Get the three credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export JT_FB_URL='https://…/api/tus'      # "url" from the response
#   export JT_FB_AUTH='…'                     # "auth_key"
#   export JT_FB_REST='…'                     # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh
#
# Then clear the site cache (`agency-hosting_cache_clear-website`, or hPanel).
# Pass a path prefix as $1 to upload only part of the tree (e.g. ./deploy.sh assets).
set -u
: "${JT_FB_URL:?set JT_FB_URL}" "${JT_FB_AUTH:?set JT_FB_AUTH}" "${JT_FB_REST:?set JT_FB_REST}"
cd "$(dirname "$0")" || exit 1
PREFIX=${1:-.}

fb() { curl -sS --max-time 300 -H "X-Auth: $JT_FB_AUTH" -H "X-Auth-Rest: $JT_FB_REST" "$@"; }

upload() {
  local f=$1 rel=${1#./} size c p
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$JT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$JT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "ok"; else echo "FAIL $c/$p $rel"; fi
}
export -f upload fb
export JT_FB_URL JT_FB_AUTH JT_FB_REST

find "$PREFIX" \( -path './.git' -o -path './content' -o -path './__pycache__' -o -path '*/__pycache__' \) -prune -o -type f \
  ! -name '*.py' ! -name 'README.md' ! -name 'deploy.sh' ! -name '.generated' ! -name 'manifest.json' -print \
  | sort | xargs -P 6 -I{} bash -c 'upload "$1"' _ {} > /tmp/jt-deploy.log
ok=$(grep -c '^ok$' /tmp/jt-deploy.log); fail=$(grep -c '^FAIL' /tmp/jt-deploy.log)
grep '^FAIL' /tmp/jt-deploy.log
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
