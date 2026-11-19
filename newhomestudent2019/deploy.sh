#!/bin/bash
# Deploy newhomestudent2019.com to its Hostinger Agency php-fpm website.
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website UID in README.md); they expire after a few hours:
#   export NH_FB_URL='https://…/api/tus'  NH_FB_AUTH='…'  NH_FB_REST='…'
#   php validate.php && ./deploy.sh
# Never uploads storage/ (leads + form secret live there on the server only).
set -u
: "${NH_FB_URL:?set NH_FB_URL}" "${NH_FB_AUTH:?set NH_FB_AUTH}" "${NH_FB_REST:?set NH_FB_REST}"
cd "$(dirname "$0")" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $NH_FB_AUTH" -H "X-Auth-Rest: $NH_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  for try in 1 2 3; do
    c=$(fb -X POST "$NH_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$NH_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && break
    sleep $((try * 2))
  done
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path ./backup -o -path ./storage -o -name '*.md' -o -name deploy.sh -o -name validate.php -o -name dev-router.php \) -prune -o -type f -print | sort)
# storage/ must exist on the server for the lead form; upload its placeholder only.
fb -X POST "$NH_FB_URL/public_html/storage/index.php?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: 15" -H "Upload-Offset: 0" -o /dev/null
printf '<?php exit; ?>\n' | fb -X PATCH "$NH_FB_URL/public_html/storage/index.php?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary @- -o /dev/null
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
