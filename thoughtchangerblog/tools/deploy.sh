#!/bin/bash
# Upload public/ to Hostinger through the File Browser TUS API.
#
#   Get credentials from the Hostinger API `hosting_files_generate-upload-url`
#   (username u401386392, domain thoughtchangerblog.com); they expire after a few hours.
#   export TC_FB_URL='https://…/api/tus/public_html'  TC_FB_AUTH='…'  TC_FB_REST='…'
#   tools/deploy.sh staging     # -> public_html/staging (staging.thoughtchangerblog.com, noindex)
#   tools/deploy.sh production  # -> public_html (the live site)
#   SKIP_MEDIA=1 tools/deploy.sh staging   # code-only update (skips wp-content/uploads)
#   FILES='content/posts.json llms.txt …' tools/deploy.sh production  # upload only these paths (relative to public/)
#
# Files only ever get added/overwritten; nothing on the server is deleted.
set -u
: "${TC_FB_URL:?}" "${TC_FB_AUTH:?}" "${TC_FB_REST:?}"
target=${1:?staging|production}
cd "$(dirname "$0")/.." || exit 1
build=$(mktemp -d)
cp -a public/. "$build/"
prefix=""
if [ "$target" = staging ]; then
  prefix="staging/"
  printf 'User-agent: *\nDisallow: /\n' > "$build/robots.txt"
  # The staging folder sits inside the live public_html: refuse to serve it under the main domain.
  python3 - "$build/.htaccess" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace("RewriteBase /\n", "RewriteBase /\nRewriteCond %{HTTP_HOST} !^staging\\. [NC]\nRewriteRule ^ - [R=404,L]\n",1)
s+='\n<IfModule mod_headers.c>\nHeader always set X-Robots-Tag "noindex, nofollow"\n</IfModule>\n'
open(p,'w').write(s)
PY
elif [ "$target" != production ]; then echo "unknown target"; exit 1; fi
export prefix build
up() {
  rel=${1#./}; f="$build/$rel"; size=$(stat -c%s "$f")
  url="$TC_FB_URL/${prefix}$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$rel")?override=true"
  for try in 1 2 3; do
    c=$(curl -sS --max-time 300 -X POST "$url" -H "X-Auth: $TC_FB_AUTH" -H "X-Auth-Rest: $TC_FB_REST" -H "Tus-Resumable: 1.0.0" -H "Upload-Length: $size" -H "Upload-Offset: 0" -o /dev/null -w "%{http_code}")
    p=$(curl -sS --max-time 300 -X PATCH "$url" -H "X-Auth: $TC_FB_AUTH" -H "X-Auth-Rest: $TC_FB_REST" -H "Tus-Resumable: 1.0.0" -H "Content-Type: application/offset+octet-stream" -H "Upload-Offset: 0" --data-binary "@$f" -o /dev/null -w "%{http_code}")
    if [ "$c" = 201 ] && [ "$p" = 204 ]; then echo "OK $rel"; return 0; fi
    sleep $((try * 2))
  done
  echo "FAIL $c/$p $rel"
}
export -f up
cd "$build" && { if [ -n "${FILES:-}" ]; then for x in $FILES; do echo "./$x"; done; else find . -type f; fi; } | { if [ -n "${SKIP_MEDIA:-}" ]; then grep -v '^./wp-content/'; else cat; fi; } | sort | xargs -P 8 -I{} bash -c 'up "$@"' _ {} > /tmp/tc-deploy.log
echo "ok=$(grep -c '^OK' /tmp/tc-deploy.log) fail=$(grep -c '^FAIL' /tmp/tc-deploy.log)"
grep '^FAIL' /tmp/tc-deploy.log | head
rm -rf "$build"
