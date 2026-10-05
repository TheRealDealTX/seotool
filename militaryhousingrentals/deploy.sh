#!/bin/bash
# Deploy militaryhousingrentals.com to Hostinger (account u401386392).
#
# Uploads the site through the File Browser TUS endpoint. Get the three
# credentials from the Hostinger API call `hosting_files_generate-upload-url`
# (username u401386392, domain militaryhousingrentals.com); they expire after a
# few hours:
#
#   export MHR_FB_URL='https://…'     # "url"
#   export MHR_FB_AUTH='…'            # "auth_key"
#   export MHR_FB_REST='…'            # "rest_auth_key"
#   ./deploy.sh            # upload everything
#   ./deploy.sh app/data   # upload only files under these paths
#
# The WordPress install is left in place on the server, so rolling back means
# re-uploading backup/wp-index.php.txt as index.php and backup/wp-htaccess.txt
# as .htaccess.
set -u
: "${MHR_FB_URL:?set MHR_FB_URL}" "${MHR_FB_AUTH:?set MHR_FB_AUTH}" "${MHR_FB_REST:?set MHR_FB_REST}"
cd "$(dirname "$0")" || exit 1

# llms.txt is a real file on the server, so regenerate it from the data.
php -r 'chdir("."); $_SERVER["REQUEST_URI"]="/llms.txt"; require "index.php";' > llms.txt 2>/dev/null

fb() { curl -sS --max-time 300 -H "X-Auth: $MHR_FB_AUTH" -H "X-Auth-Rest: $MHR_FB_REST" "$@"; }

if [ $# -gt 0 ]; then paths=("$@"); else paths=(.); fi
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$MHR_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$MHR_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find "${paths[@]}" -type f \
          -not -path './backup/*' -not -path 'backup/*' -not -path '*/app/storage/*' -not -path 'app/storage/*' \
          -not -name 'deploy.sh' -not -name 'README.md' -not -name '.gitignore' -not -path '*/.git/*' | sort)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
