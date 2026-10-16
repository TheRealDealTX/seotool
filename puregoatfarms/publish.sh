#!/bin/bash
# Publish the Milking & Dairy cluster to puregoatfarms.com (Hostinger Agency
# WordPress website UID VSUHIRjmA).
#
# Needs the three File Browser credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` for website VSUHIRjmA (they
# expire after a few hours):
#
#   export PGF_FB_URL='https://…/api/tus'   # "url"
#   export PGF_FB_AUTH='…'                  # "auth_key"
#   export PGF_FB_REST='…'                  # "rest_auth_key"
#   ./publish.sh            # dry run: uploads, reports, changes nothing
#   ./publish.sh --live     # publishes, then the importer deletes itself
#
# Afterwards clear the site cache (`agency-hosting_cache_clear-website`).
set -euo pipefail
: "${PGF_FB_URL:?set PGF_FB_URL}" "${PGF_FB_AUTH:?set PGF_FB_AUTH}" "${PGF_FB_REST:?set PGF_FB_REST}"
cd "$(dirname "$0")"
LIVE=${1:-}

python3 build_posts.py
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
python3 make_images.py payload.json "$STAGE/pgf-img"
TOKEN=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
sed "s/__TOKEN__/$TOKEN/" publish.php > "$STAGE/pgf-publish.php"
cp payload.json "$STAGE/pgf-payload.json"
php -l "$STAGE/pgf-publish.php" >/dev/null

fb() { curl -sS --max-time 300 -H "X-Auth: $PGF_FB_AUTH" -H "X-Auth-Rest: $PGF_FB_REST" "$@"; }
upload() {  # upload <local file> <path inside public_html>
  local f=$1 rel=$2 size c p
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$PGF_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$PGF_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "uploaded $rel"; else echo "FAILED $c/$p $rel" >&2; exit 1; fi
}

upload "$STAGE/pgf-payload.json" pgf-payload.json
for img in "$STAGE"/pgf-img/*.webp; do upload "$img" "pgf-img/$(basename "$img")"; done
upload "$STAGE/pgf-publish.php" pgf-publish.php

echo "--- dry run"
curl -sS "https://puregoatfarms.com/pgf-publish.php?token=$TOKEN&dry=1"
echo
if [ "$LIVE" = "--live" ]; then
  echo "--- live run"
  curl -sS "https://puregoatfarms.com/pgf-publish.php?token=$TOKEN"
  echo
else
  echo "Dry run only. Re-run with --live to publish, or remove pgf-publish.php, pgf-payload.json and pgf-img/ from public_html."
fi
