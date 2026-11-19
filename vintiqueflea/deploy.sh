#!/bin/bash
# Deploy the Vintique Flea PHP site to Hostinger Agency website 67Tls7oNq (vintiqueflea.com).
#
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid 67Tls7oNq). They expire after a few hours.
#   export VF_FB_URL='https://…/api/tus'   VF_FB_AUTH='…'   VF_FB_REST='…'
#   ./deploy.sh            # upload the site
#   ./deploy.sh rollback   # put WordPress's index.php + .htaccess back
set -u
: "${VF_FB_URL:?set VF_FB_URL}" "${VF_FB_AUTH:?set VF_FB_AUTH}" "${VF_FB_REST:?set VF_FB_REST}"
cd "$(dirname "$0")" || exit 1

put() { # put <local file> <remote path under public_html>
  local size c p
  size=$(stat -c%s "$1")
  c=$(curl -sS --max-time 300 -X POST "$VF_FB_URL/public_html/$2?override=true" -H "X-Auth: $VF_FB_AUTH" -H "X-Auth-Rest: $VF_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --max-time 300 -X PATCH "$VF_FB_URL/public_html/$2?override=true" -H "X-Auth: $VF_FB_AUTH" -H "X-Auth-Rest: $VF_FB_REST" \
        -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$1" -o /dev/null -w "%{http_code}")
  [ "$c" = 201 ] && [ "$p" = 204 ] || { echo "FAIL $c/$p $2"; return 1; }
}

if [ "${1:-}" = rollback ]; then
  put rollback/index.php index.php && put rollback/.htaccess .htaccess && echo "WordPress entry files restored."
  exit
fi

ok=0; fail=0
# index.php and .htaccess go LAST so the live site switches over only once everything else is in place.
while IFS= read -r f; do
  rel=${f#./}
  if put "$f" "$rel"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done < <(find . -type f ! -path './rollback/*' ! -name deploy.sh ! -name README.md ! -name '*.jsonl' ! -name secret.key \
          ! -path './index.php' ! -path './.htaccess' | sort)
if [ "$fail" -eq 0 ]; then
  put index.php index.php && put .htaccess .htaccess && ok=$((ok+2)) || fail=$((fail+1))
fi
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
