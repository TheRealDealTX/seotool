#!/bin/bash
# Deploy the San Antonio build to the Hostinger Agency (H5G) website for conversepublicadjuster.com
# (website UID h1GbQ1rks). The platform ignores .htaccess, keeps a locked WordPress index.php, and routes
# "/" and unknown paths through wp-content/db.php, so the homepage ships as home.html (never index.html).
#
# Credentials come from the Hostinger API call `agency-hosting_files_generate-upload-url`
# (website_uid h1GbQ1rks); they expire after a few hours:
#   export HR_FB_URL='https://…/api/tus'   # "url"
#   export HR_FB_AUTH='…'                  # "auth_key"
#   export HR_FB_REST='…'                  # "rest_auth_key"
#   python3 -I tools/seo_check.py && ./deploy.sh            # upload only
#   ./deploy.sh --remove-old                                # upload, then delete the old flat pages
# Afterwards clear the site cache (`agency-hosting_cache_clear-website`, or hPanel).
set -u
: "${HR_FB_URL:?set HR_FB_URL}" "${HR_FB_AUTH:?set HR_FB_AUTH}" "${HR_FB_REST:?set HR_FB_REST}"
cd "$(dirname "$0")" || exit 1
REST=${HR_FB_URL%/api/tus}

fb() { curl -sS --max-time 300 -H "X-Auth: $HR_FB_AUTH" -H "X-Auth-Rest: $HR_FB_REST" "$@"; }

ok=0; fail=0
while IFS= read -r f; do
  rel=${f#./}
  size=$(stat -c%s "$f")
  c=$(fb -X POST "$HR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
  p=$(fb -X PATCH "$HR_FB_URL/public_html/$rel?override=true" -H "Tus-Resumable: 1.0.0" \
        -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
        --data-binary "@$f" -o /dev/null -w "%{http_code}")
  if [ "$c" = 201 ] && [ "$p" = 204 ]; then ok=$((ok+1)); else fail=$((fail+1)); echo "FAIL $c/$p $rel"; fi
done < <(find . \( -path './_old-site' -o -path './tools' -o -path './.git' \) -prune -o -type f \
          ! -name 'README.md' ! -name 'deploy.sh' ! -name 'index.html' -print | sort | grep -v '^\./index\.html$')
# (root index.html is excluded on purpose; subdirectory index.html files are included by the find above)
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ] || exit 1

if [ "${1:-}" = "--remove-old" ]; then
  # Old flat pages whose URLs now 301 from wp-content/db.php. Deleting them makes the redirects fire
  # (the platform serves an existing file before PHP sees the request).
  del=0; dfail=0
  for old in about.html contact.html converse-hail-storm-september-2026.html \
    blog/acv-vs-rcv-why-the-first-check-is-smaller-than-the-estimate.html \
    blog/appraisal-clause-explained-for-bexar-county-homeowners.html \
    blog/door-knockers-in-converse-what-texas-law-lets-a-roofer-do.html \
    blog/hail-damage-roof-inspection-converse-before-the-heat-bakes-it-in.html \
    blog/hail-history-of-converse-and-northeast-bexar-county.html \
    blog/how-to-get-insurance-to-pay-for-roof-replacement-after-the-converse-hail-storm.html \
    blog/seven-line-items-missing-from-your-hail-roof-estimate.html \
    assets/site.css assets/site.js; do
    d=$(fb -X DELETE "$REST/api/resources/public_html/$old" -o /dev/null -w "%{http_code}")
    if [ "$d" = 200 ] || [ "$d" = 204 ] || [ "$d" = 404 ]; then del=$((del+1)); else dfail=$((dfail+1)); echo "DELETE FAIL $d $old"; fi
  done
  echo "removed=$del failed=$dfail"
  [ "$dfail" -eq 0 ] || exit 1
fi
