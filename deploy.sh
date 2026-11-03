#!/bin/bash
# Deploy public/ to the Hostinger Agency website for solarcctvcamera.com.
#
# The platform has no git/SSH deploy for Agency php-fpm sites, so this pushes
# every file through the website's File Browser TUS endpoint. Get the three
# credentials from the Hostinger API operation
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export FB_URL='https://…/api/tus'   # "url"
#   export FB_AUTH='…'                  # "auth_key"
#   export FB_REST='…'                  # "rest_auth_key"
#   python3 tools/validate.py && ./deploy.sh            # everything
#   ./deploy.sh public/assets/css/site.css              # or just some files
#
# Then clear the cache (`agency-hosting_cache_clear-website`).
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
cd "$(dirname "$0")" || exit 1

up() {
  local f=$1 rel=${1#public/} size c p
  size=$(stat -c%s "$f")
  c=$(curl -sS --max-time 120 -X POST "$FB_URL/public_html/$rel?override=true" -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" \
      -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --max-time 300 -X PATCH "$FB_URL/public_html/$rel?override=true" -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" \
      -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
      --data-binary "@$f" -o /dev/null -w "%{http_code}")
  [ "$c" = 201 ] && [ "$p" = 204 ] && return 0
  echo "FAIL $c/$p $rel"; return 1
}

if [ $# -gt 0 ]; then files=("$@"); else mapfile -t files < <(find public -type f ! -name 'config.local.php' | sort); fi
ok=0; fail=0
for f in "${files[@]}"; do if up "$f"; then ok=$((ok+1)); else fail=$((fail+1)); fi; done
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
