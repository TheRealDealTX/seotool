#!/bin/bash
# Upload the site to Hostinger (account u401386392, tinyhomesblueprint.com, public_html).
#
# Files go one by one through the File Browser TUS endpoint. Get the credentials from the
# Hostinger API call `hosting_files_generate-upload-url` (username u401386392,
# domain tinyhomesblueprint.com); they expire after a few hours:
#
#   export THB_FB_URL='https://.../api/tus'   # "url"
#   export THB_FB_AUTH='...'                  # "auth_key"
#   export THB_FB_REST='...'                  # "rest_auth_key"
#   php validate.php && ./deploy.sh
#
# Only site files are uploaded; the old WordPress files on the server are left in place
# (see README, "Rollback").
set -u
: "${THB_FB_URL:?set THB_FB_URL}" "${THB_FB_AUTH:?set THB_FB_AUTH}" "${THB_FB_REST:?set THB_FB_REST}"
cd "$(dirname "$0")" || exit 1

fb() { curl -sS --max-time 300 -H "X-Auth: $THB_FB_AUTH" -H "X-Auth-Rest: $THB_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$THB_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$THB_FB_URL/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './backup-wordpress' -o -name 'README.md' -o -name 'deploy.sh' -o -name 'validate.php' -o -name 'dev-router.php' -o -name 'build-plans.php' -o -name '.gitignore' \
            -o -path './index.php' -o -path './.htaccess' \) -prune -o -type f -print | sort; [ -z "${THB_NO_SWITCH:-}" ] && { echo ./index.php; echo ./.htaccess; })
# index.php and .htaccess go last (THB_NO_SWITCH=1 skips them, to stage files without going live) so the live site switches over only once every page is in place.
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
