#!/bin/bash
# Deploy the SmokeDamage.com build to its Hostinger Agency website (UID qpuHSMS5T).
#
#   public/   -> public_html/   (the site)
#   private/  -> .h5g/sd-private/    (admin manifest; never web-served)
#
# Get credentials from the Hostinger API call agency-hosting_files_generate-upload-url
# (they expire after a few hours):
#   export SD_FB_URL='https://…/api/tus' SD_FB_AUTH='…' SD_FB_REST='…'
#   python3 build.py && python3 validate.py && ./deploy.sh
# Then clear the site cache (agency-hosting_cache_clear-website).
#
# Leads, uploads, settings.json, redirects.json and admin.json live only on the
# server in sd-private/ and are never overwritten by a deploy.
set -u
: "${SD_FB_URL:?set SD_FB_URL}" "${SD_FB_AUTH:?set SD_FB_AUTH}" "${SD_FB_REST:?set SD_FB_REST}"
cd "$(dirname "$0")" || exit 1

upload() {  # $1 local file, $2 remote path
  local size c p
  size=$(stat -c%s "$1")
  for try in 1 2 3; do
    c=$(curl -sS --max-time 300 -H "X-Auth: $SD_FB_AUTH" -H "X-Auth-Rest: $SD_FB_REST" -X POST "$SD_FB_URL/$2?override=true" \
          -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -H "X-Auth: $SD_FB_AUTH" -H "X-Auth-Rest: $SD_FB_REST" -X PATCH "$SD_FB_URL/$2?override=true" \
          -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" \
          --data-binary "@$1" -o /dev/null -w "%{http_code}")
    [ "$c" = 201 ] && [ "$p" = 204 ] && { echo "ok $2"; return 0; }
    sleep $((try * 2))
  done
  echo "FAIL $c/$p $2"; return 1
}
export -f upload

{ (cd public && find . -type f | sed 's#^\./##' | awk '{print "public/"$0"\tpublic_html/"$0}')
  (cd private && find . -type f -name 'site-manifest.json' | sed 's#^\./##' | awk '{print "private/"$0"\t.h5g/sd-private/"$0}'); } \
  | xargs -P 8 -d '\n' -I{} bash -c 'IFS=$'"'"'\t'"'"' read -r l r <<< "{}"; upload "$l" "$r"' > /tmp/sd-deploy.log
ok=$(grep -c '^ok ' /tmp/sd-deploy.log); fail=$(grep -c '^FAIL' /tmp/sd-deploy.log)
grep '^FAIL' /tmp/sd-deploy.log
echo "uploaded=$ok failed=$fail"
[ "$fail" -eq 0 ]
