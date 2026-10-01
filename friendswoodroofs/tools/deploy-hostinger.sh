#!/bin/bash
# Upload the site to a Hostinger Agency-plan website through its File Browser
# TUS endpoint (same method as the repository's Hutto deploy.sh).
#
# Get short-lived credentials from the Hostinger API call
# `agency-hosting_generateUploadURLV1` for the friendswoodroofs.com website:
#   export FR_FB_URL='https://…/api/tus'   # "url"
#   export FR_FB_AUTH='…'                  # "auth_key"
#   export FR_FB_REST='…'                  # "rest_auth_key"
#   ./tools/deploy-hostinger.sh
#
# public_html/* is uploaded to /public_html/ and app/* to /app/ (next to
# public_html, outside the web root). If your File Browser root turns out to
# BE public_html, set FR_APP_REMOTE=public_html/app - the bundled
# app/.htaccess then blocks web access to it.
# Afterwards clear the site cache (`agency-hosting_clearWebsiteCacheV1` or hPanel).
set -u
: "${FR_FB_URL:?set FR_FB_URL}" "${FR_FB_AUTH:?set FR_FB_AUTH}" "${FR_FB_REST:?set FR_FB_REST}"
APP_REMOTE="${FR_APP_REMOTE:-app}"
cd "$(dirname "$0")/.." || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $FR_FB_AUTH" -H "X-Auth-Rest: $FR_FB_REST" "$@"; }
upload() { # local remote
  local size; size=$(stat -c%s "$1")
  local c p
  c=$(fb -X POST "$FR_FB_URL/$2?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FR_FB_URL/$2?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$1" -o /dev/null -w "%{http_code}")
  [ "$c" = 201 ] && [ "$p" = 204 ]
}

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  case "$rel" in
    public_html/*) remote="$rel" ;;
    app/*)         remote="$APP_REMOTE/${rel#app/}" ;;
  esac
  if upload "$f" "$remote"; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $rel"; fi
done < <(find ./public_html ./app -type f ! -name '*.log' ! -path './app/storage/ratelimit/*.json' ! -name 'secret.key' | sort)
echo "uploaded=$ok failed=$fail"
[ -f app/config/mail.php ] || echo "NOTE: app/config/mail.php was not uploaded (not present locally). Create it on the server."
[ "$fail" -eq 0 ]
