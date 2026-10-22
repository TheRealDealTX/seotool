#!/bin/bash
# Deploy site/ to the Hostinger Agency website (plain php-fpm, H5G platform).
#
# The H5G platform ignores .htaccess and the File Browser can only write inside
# public_html/, so the whole site goes there. Private PHP files exit unless loaded
# by the app (defined('CCPA_ROOT') guard), and logs/secret are .php files whose
# first line exits, so nothing private is readable over HTTP.
#
# Credentials come from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid j0WNY4Y29; they expire after a few hours):
#   export FB_URL='https://…/api/tus' FB_AUTH='…' FB_REST='…'
#   sh tools/deploy.sh            # everything
#   sh tools/deploy.sh path ...   # only these site/-relative files
# Then clear the cache (`agency-hosting_cache_clear-website`).
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
cd "$(dirname "$0")/../site" || exit 1

dest() { echo "public_html/$1"; }
up() {
  local f=$1 d size c p
  d=$(dest "$f"); size=$(stat -c%s "$f")
  c=$(curl -sS --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" -X POST "$FB_URL/$d?override=true" \
      -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" -X PATCH "$FB_URL/$d?override=true" \
      -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
      --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && { [ "$p" = 204 ] || [ "$size" = 0 ]; }; then echo "ok $d"; else echo "FAIL $c/$p $d"; return 1; fi
}

if [ $# -gt 0 ]; then files=$(printf '%s\n' "$@"); else
  # Skip local-only files: secrets, caches, logs, rate-limit state.
  files=$(find . -type f ! -name '*.tmp' ! -name '*.lock' ! -path './includes/config.local.php' ! -path './data/secret.php' ! -name '.secret' \
            ! \( -path './data/cache/*' ! -name .htaccess \) ! \( -path './data/logs/*' ! -name .htaccess \) \
            ! \( -path './data/ratelimit/*' ! -name .htaccess \) | sed 's#^\./##' | sort)
fi
ok=0; fail=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if up "$f" >/dev/null; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $f"; fi
done <<< "$files"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
