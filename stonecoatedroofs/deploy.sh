#!/bin/bash
# Deploy public/ to the Hostinger Agency website for stonecoatedroofs.com.
#
# Pushes each built file through the website's File Browser TUS endpoint. Get the
# three credentials from the Hostinger API call `agency-hosting_files_generate-upload-url`
# for the website UID in README.md (they expire after a few hours):
#
#   export SCR_FB_URL='https://…/api/tus'   # "url"
#   export SCR_FB_AUTH='…'                  # "auth_key"
#   export SCR_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh            # everything
#   ./deploy.sh --pages                                               # skip wp-content/ media
#
# Then clear the site cache (`agency-hosting_websites_clear-cache`, or hPanel).
set -u
: "${SCR_FB_URL:?set SCR_FB_URL}" "${SCR_FB_AUTH:?set SCR_FB_AUTH}" "${SCR_FB_REST:?set SCR_FB_REST}"
cd "$(dirname "$0")/public" || exit 1
skip_media=${1:-}

up() {
  local rel=$1 size c p
  size=$(stat -c%s "$rel")
  c=$(curl -sS --max-time 300 -H "X-Auth: $SCR_FB_AUTH" -H "X-Auth-Rest: $SCR_FB_REST" -X POST "$SCR_FB_URL/public_html/$rel?override=true" \
        -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(curl -sS --max-time 300 -H "X-Auth: $SCR_FB_AUTH" -H "X-Auth-Rest: $SCR_FB_REST" -X PATCH "$SCR_FB_URL/public_html/$rel?override=true" \
        -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$rel" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo ok; else echo "FAIL $c/$p $rel"; fi
}
export -f up; export SCR_FB_URL SCR_FB_AUTH SCR_FB_REST

if [ "$skip_media" = "--pages" ]; then list=$(find . -type f -not -path './wp-content/*' | sed 's#^\./##' | sort)
else list=$(find . -type f | sed 's#^\./##' | sort); fi
res=$(printf '%s\n' "$list" | xargs -P 6 -I{} bash -c 'up "$@"' _ {})
ok=$(grep -c '^ok$' <<<"$res"); fail=$(grep -c '^FAIL' <<<"$res")
grep '^FAIL' <<<"$res"
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
