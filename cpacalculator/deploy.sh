#!/bin/bash
# Deploy cpacalculator.com to its Hostinger Agency website (UID 17XGw98Uo) through the
# File Browser TUS endpoint. Get credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export FB_URL='https://…/api/tus' FB_AUTH='…' FB_REST='…'
#   ./deploy.sh            # uploads every site file into public_html/
#
# The SMTP password is NOT in this repo. It lives on the server, outside the web root, at
# .private/cpacalculator-mail.php (see README "Contact form").
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
cd "$(dirname "$0")" || exit 1
fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f ! -name 'deploy.sh' ! -name 'dev-router.php' ! -name 'README.md' ! -name 'config.local.php' ! -name '*.md' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
