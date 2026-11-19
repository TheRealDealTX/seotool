#!/bin/bash
# Deploy public_html/ to the Hostinger Agency website for my1secret.com.
#
# Get the three File Browser credentials from the Hostinger API call
# `agency-hosting_files_generate-upload-url` (website UID in README; they expire after a few hours):
#   export FB_URL='https://…/api/tus'  FB_AUTH='…'  FB_REST='…'
#   ./deploy.sh            # upload everything
#   ./deploy.sh app assets # upload only these subfolders of public_html
# The site config (DB credentials) is NOT in the repo: it lives on the server at
# .h5g/my1secret-config.php (see config.sample.php).
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
cd "$(dirname "$0")/public_html" || exit 1
fb() { curl -sS --retry 3 --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" "$@"; }
ok=0; fail=0
targets=("${@:-.}")
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find "${targets[@]}" -type f ! -path '*/uploads/*' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
