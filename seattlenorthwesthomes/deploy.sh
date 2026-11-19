#!/bin/bash
# Deploy to a Hostinger Agency php-fpm website through its File Browser TUS API.
#
#   public_html/*  -> public_html/
#   app/*          -> public_html/app/
# The File Browser only exposes public_html, so app/ lives inside it; every file
# in app/ starts with `defined('SNW') || exit;`, so requesting one directly prints nothing.
#
# Get credentials from the Hostinger API `agency-hosting_files_generate-upload-url`
# (website UID D5jnILeBy = staging/new site); they expire after a few hours:
#   export SNW_FB_URL='https://…/api/tus' SNW_FB_AUTH='…' SNW_FB_REST='…'
#   ./deploy.sh            # everything
#   ./deploy.sh app        # only paths starting with app/
# Then clear the site cache (agency-hosting cache clear, or hPanel).
set -u
: "${SNW_FB_URL:?}" "${SNW_FB_AUTH:?}" "${SNW_FB_REST:?}"
cd "$(dirname "$0")" || exit 1
only=${1:-}
fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $SNW_FB_AUTH" -H "X-Auth-Rest: $SNW_FB_REST" "$@"; }
up() {
  local f=$1 size c p
  size=$(stat -c%s "$f")
  local dest=$f; case $f in app/*) dest="public_html/$f";; esac
  c=$(fb -X POST "$SNW_FB_URL/$dest?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$SNW_FB_URL/$dest?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo ok; else echo "FAIL $c/$p $f"; fi
}
export -f up fb
find public_html app -type f ! -path 'app/storage/*' ! -name '.DS_Store' | sort | grep "^${only}" \
  | xargs -P 8 -I{} bash -c 'up "$1"' _ {} | sort | uniq -c
