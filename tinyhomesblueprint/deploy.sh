#!/bin/bash
# Deploy tinyhomesblueprint.com to Hostinger (account u401386392).
#
#   python3 generator/build.py          # rebuild plan sets (previews + dist/plan-files/*.zip)
#   export THB_FB_URL='https://…/api/tus/public_html'   # "url" from hosting_files_generate-upload-url
#   export THB_FB_AUTH='…'                              # "auth_key"
#   export THB_FB_REST='…'                              # "rest_auth_key"
#   ./deploy.sh            # site files -> public_html/, plan zips -> thb-plan-files/ (outside the web root)
#   ./deploy.sh --site     # site files only
#   ./deploy.sh --files    # plan zips only
#
# The credentials come from the Hostinger API (hosting_files_generate-upload-url with
# username u401386392 and domain tinyhomesblueprint.com) and expire after a few hours.
# Secrets (thb-secrets.php) are never uploaded by this script; see README.md.
set -u
: "${THB_FB_URL:?set THB_FB_URL}" "${THB_FB_AUTH:?set THB_FB_AUTH}" "${THB_FB_REST:?set THB_FB_REST}"
cd "$(dirname "$0")" || exit 1
BASE=${THB_FB_URL%/public_html}
MODE=${1:-all}

fb() { curl -sS --max-time 300 -H "X-Auth: $THB_FB_AUTH" -H "X-Auth-Rest: $THB_FB_REST" "$@"; }
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
  while IFS= read -r f; do put "$f" "public_html/${f#site/}"; done < <(find site -type f | sort)
fi
if [ "$MODE" != "--site" ]; then
  for z in dist/plan-files/*.zip; do put "$z" "thb-plan-files/$(basename "$z")"; done
fi
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
