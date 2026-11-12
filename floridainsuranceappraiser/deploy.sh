#!/bin/bash
# Upload dist/ to the Hostinger Agency website BHoKZ0Ik1 (floridainsuranceappraiser.com,
# temporary domain pink-tiger-234102.hostingersite.com) via the File Browser TUS endpoint.
# Credentials come from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid BHoKZ0Ik1); they expire after a few hours:
#   export FB_URL='https://…/api/tus' FB_AUTH='…' FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the cache (`agency-hosting_cache_clear-website`).
set -u
: "${FB_URL:?set FB_URL}" "${FB_AUTH:?set FB_AUTH}" "${FB_REST:?set FB_REST}"
# Every page goes up as dir/index.php behind _guard.php (www/http 301 + off-domain noindex), because the
# host serves dir/index.html without running index.php. guardify.py does that on a staging copy, so
# ./dist and validate.py keep plain index.html; afterwards the stale index.html pages are deleted remotely.
HERE="$(cd "$(dirname "$0")" && pwd)"
STAGE="$(mktemp -d)"; CONV="$(mktemp)"; trap 'rm -rf "$STAGE" "$CONV"' EXIT
cp -a "$HERE/dist/." "$STAGE/" || exit 1
python3 "$HERE/guardify.py" "$STAGE" floridainsuranceappraiser.com --list-converted > "$CONV" || exit 1
cd "$STAGE" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $FB_AUTH" -H "X-Auth-Rest: $FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
if [ "$fail" -eq 0 ]; then
  removed=0
  while IFS= read -r page; do
    [ -z "$page" ] && continue
    c=$(fb -X DELETE "${FB_URL%/tus}/resources/public_html/$page" -o /dev/null -w "%{http_code}")
    case "$c" in 200|204|404) removed=$((removed+1));; *) echo "could not delete stale $page ($c)"; fail=$((fail+1));; esac
  done < "$CONV"
  echo "stale page index.html removed=$removed"
fi
[ "$fail" -eq 0 ]
