#!/bin/bash
# Upload this folder to the Hostinger Agency website's public_html through the
# File Browser TUS endpoint. Get credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export LLT_FB_URL='https://…/api/tus'  LLT_FB_AUTH='…'  LLT_FB_REST='…'
#   python3 tests/validate.py && ./deploy.sh [file ...]
#
# With no arguments every site file is uploaded; pass paths to upload only those.
set -u
: "${LLT_FB_URL:?set LLT_FB_URL}" "${LLT_FB_AUTH:?set LLT_FB_AUTH}" "${LLT_FB_REST:?set LLT_FB_REST}"
cd "$(dirname "$0")" || exit 1
fb() { curl -sS --max-time 300 --retry 3 -H "X-Auth: $LLT_FB_AUTH" -H "X-Auth-Rest: $LLT_FB_REST" "$@"; }
list() {
  if [ $# -gt 0 ]; then printf '%s\n' "$@"; else
    find . -type f ! -path './tests/*' ! -path './.git*' ! -name 'deploy.sh' ! -name '*.md' ! -name '.gitignore' ! -path './storage/quote-*' | sed 's#^\./##' | sort
  fi
}
ok=0; fail=0
while IFS= read -r rel; do
  size=$(stat -c%s "$rel")
  c=$(fb -X POST "$LLT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$LLT_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(list "$@")
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
