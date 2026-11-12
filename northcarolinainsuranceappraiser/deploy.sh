#!/bin/bash
# Push ./public to the Hostinger Agency website's public_html via the File Browser TUS API.
# Get credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid 45jUap7vr, see README; they expire after a few hours):
#   export NCIA_FB_URL='https://…'  NCIA_FB_AUTH='…'  NCIA_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the site cache (`agency-hosting_cache_clear-website`).
set -u
: "${NCIA_FB_URL:?set NCIA_FB_URL}" "${NCIA_FB_AUTH:?set NCIA_FB_AUTH}" "${NCIA_FB_REST:?set NCIA_FB_REST}"
# Every page goes up as dir/index.php behind _guard.php (www/http 301 + off-domain noindex), because the
# host serves dir/index.html without running index.php. guardify.py does that on a staging copy, so
# ./public and validate.py keep plain index.html; afterwards the stale index.html pages are deleted remotely.
HERE="$(cd "$(dirname "$0")" && pwd)"
STAGE="$(mktemp -d)"; CONV="$(mktemp)"; trap 'rm -rf "$STAGE" "$CONV"' EXIT
cp -a "$HERE/public/." "$STAGE/" || exit 1
python3 "$HERE/guardify.py" "$STAGE" northcarolinainsuranceappraiser.com --list-converted > "$CONV" || exit 1
cd "$STAGE" || exit 1
fb() { curl -sS --max-time 300 -H "X-Auth: $NCIA_FB_AUTH" -H "X-Auth-Rest: $NCIA_FB_REST" "$@"; }
ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}; size=$(stat -c%s "$f")
  c=$(fb -X POST "$NCIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$NCIA_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . -type f | sort)
echo "uploaded=$ok failed=$fail"
if [ "$fail" -eq 0 ]; then
  removed=0
  while IFS= read -r page; do
    [ -z "$page" ] && continue
    c=$(fb -X DELETE "${NCIA_FB_URL%/tus}/resources/public_html/$page" -o /dev/null -w "%{http_code}")
    case "$c" in 200|204|404) removed=$((removed+1));; *) echo "could not delete stale $page ($c)"; fail=$((fail+1));; esac
  done < "$CONV"
  echo "stale page index.html removed=$removed"
fi
[ "$fail" -eq 0 ]
