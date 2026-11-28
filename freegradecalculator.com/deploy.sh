#!/bin/bash
# Upload this site to Hostinger public_html via the File Browser TUS endpoint.
# Get credentials from the Hostinger API `hosting_files_generate-upload-url`
# (username + domain); they expire after a few hours:
#   export FGC_URL='https://…'  FGC_AUTH='…'  FGC_REST='…'
#   ./deploy.sh            # all files
#   ./deploy.sh path …     # only these files
set -u
: "${FGC_URL:?}" "${FGC_AUTH:?}" "${FGC_REST:?}"
cd "$(dirname "$0")" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $FGC_AUTH" -H "X-Auth-Rest: $FGC_REST" "$@"; }
up() {
  local rel=${1#./} size; size=$(stat -c%s "$1")
  local c p
  c=$(fb -X POST "$FGC_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FGC_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$1" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo ok; else echo "FAIL $c/$p $rel" >&2; echo fail; fi
}
export -f up fb; export FGC_URL FGC_AUTH FGC_REST
if [ $# -gt 0 ]; then files=$(printf '%s\n' "$@"); else
  files=$(find . -type f ! -name '*.md' ! -name 'deploy.sh' ! -name 'secrets.local.php' ! -path './.git/*' | sort); fi
res=$(printf '%s\n' "$files" | xargs -P 6 -I{} bash -c 'up "{}"')
echo "uploaded=$(grep -c '^ok' <<<"$res") failed=$(grep -c '^fail' <<<"$res")"
