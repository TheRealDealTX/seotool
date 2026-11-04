#!/bin/bash
# Deploy enforceinterest.com to the Hostinger Agency website UID 1WCLLtRIk.
#
#   ./public -> public_html/  (pages + RSS feed in _pages/, served only via index.php;
#                              plus assets, icons, contact.php, sitemap, robots, llms.txt, GSC file)
#
# Uses the website's File Browser TUS endpoint. Get the three credentials from the Hostinger API
# call `agency-hosting_files_generate-upload-url` (they expire after a few hours):
#
#   export EI_FB_URL='https://…/api/tus'   # "url"
#   export EI_FB_AUTH='…'                  # "auth_key"
#   export EI_FB_REST='…'                  # "rest_auth_key"
#   python3 build.py && python3 validate.py && ./deploy.sh [--prune]
#
# --prune deletes top-level entries in public_html/ and public_html/_pages/ that the build no longer
# produces (never _private/ or Search Console google*.html verification files). Then clear the site cache (`agency-hosting_cache_clear-website`).
set -u
: "${EI_FB_URL:?set EI_FB_URL}" "${EI_FB_AUTH:?set EI_FB_AUTH}" "${EI_FB_REST:?set EI_FB_REST}"
cd "$(dirname "$0")" || exit 1
API=${EI_FB_URL%/tus}

fb() { curl -sS --max-time 300 -H "X-Auth: $EI_FB_AUTH" -H "X-Auth-Rest: $EI_FB_REST" "$@"; }

ok=0; fail=0
upload_dir() {  # $1 local dir, $2 remote dir
  while IFS= read -r f; do
    rel=${f#./}
    size=$(stat -c%s "$1/$rel")
    c=$(fb -X POST "$EI_FB_URL/$2/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(fb -X PATCH "$EI_FB_URL/$2/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
          -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$1/$rel" -o /dev/null -w "%{http_code}")
    if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $2/$rel"; fi
  done < <(cd "$1" && find . -path ./_pages -prune -o -type f -print | sort)
}

prune_dir() {  # $1 local dir, $2 remote dir: delete remote top-level entries absent locally
  fb "$API/resources/$2/" | python3 -c 'import json,sys; [print(i["name"]) for i in json.load(sys.stdin).get("items", [])]' |
  while IFS= read -r name; do
    case "$name" in _private|.h5g|.htaccess|google*.html) continue;; esac  # never prune verification files
    if [ ! -e "$1/$name" ]; then
      echo "prune $2/$name: $(fb -X DELETE "$API/resources/$2/$name" -o /dev/null -w '%{http_code}')"
    fi
  done
}

# Pages first, so the new index.php never points at missing files.
upload_dir public/_pages public_html/_pages
upload_dir public public_html
echo "uploaded=$ok failed=$fail"
if [ "${1:-}" = "--prune" ] && [ "$fail" -eq 0 ]; then
  prune_dir public/_pages public_html/_pages
  prune_dir public public_html
fi
[ "$fail" -eq 0 ]
