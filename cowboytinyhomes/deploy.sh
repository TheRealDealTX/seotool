#!/bin/bash
# Deploy cowboytinyhomes.com to Hostinger (account u401386392).
#
#   python3 generator/build.py && php validate.php      # rebuild plan sets, check the catalog
#   export CTH_FB_URL='https://…/api/tus/public_html'    # "url" from hosting_files_generate-upload-url
#   export CTH_FB_AUTH='…'                               # "auth_key"
#   export CTH_FB_REST='…'                               # "rest_auth_key"
#   ./deploy.sh            # site files -> public_html/, plan zips -> cth-plan-files/ (outside the web root)
#   ./deploy.sh --site     # site files only
#   ./deploy.sh --files    # plan zips only
#
# The credentials come from the Hostinger API (hosting_files_generate-upload-url with username
# u401386392 and domain cowboytinyhomes.com) and expire after a few hours. Uploads overwrite
# files but never delete: inc/secrets.php, inc/data/ (contact-form leads), .private/ and the
# WordPress backup on the server are left alone. Secrets are never uploaded by this script.
set -u
: "${CTH_FB_URL:?set CTH_FB_URL}" "${CTH_FB_AUTH:?set CTH_FB_AUTH}" "${CTH_FB_REST:?set CTH_FB_REST}"
cd "$(dirname "$0")" || exit 1
BASE=${CTH_FB_URL%/public_html}
MODE=${1:-all}

fb() { curl -sS --max-time 300 -H "X-Auth: $CTH_FB_AUTH" -H "X-Auth-Rest: $CTH_FB_REST" "$@"; }
ok=0; fail=0
put() {   # put <local file> <remote path under the domain folder>
  local size c p
  size=$(stat -c%s "$1")
  c=$(fb -X POST "$BASE/$2?override=true" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$BASE/$2?override=true" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" \
        -H "Upload-Offset: 0" --data-binary "@$1" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $2"; fi
}

if [ "$MODE" != "--files" ]; then
  while IFS= read -r f; do put "$f" "public_html/${f#site/}"; done < <(
    find site -type f ! -path 'site/inc/secrets.php' ! -path 'site/inc/data/*' ! -path 'site/.private/*' ! -name '*-secrets.php' | sort)
fi
if [ "$MODE" != "--site" ]; then
  for z in dist/plan-files/*.zip; do put "$z" "cth-plan-files/$(basename "$z")"; done
fi
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
