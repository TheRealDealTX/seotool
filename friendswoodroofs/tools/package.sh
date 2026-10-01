#!/bin/bash
# Build upload zips in dist/:
#   friendswoodroofs-public_html.zip  extract INSIDE public_html (app/ ends up in
#                                     public_html/app, blocked by .htaccess).
#                                     Use this with hPanel File Manager.
#   friendswoodroofs-deploy.zip       public_html/ and app/ side by side, for hosts
#                                     that allow writing next to public_html.
# Secrets, logs and runtime files are never included. Read UPLOAD-INSTRUCTIONS.txt
# from the repo (it is not inside the public_html zip).
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
mkdir -p dist
rm -f dist/friendswoodroofs-public_html.zip dist/friendswoodroofs-deploy.zip
EXCL=(-x 'app/storage/logs/*.log*' 'app/storage/ratelimit/*.json' 'app/storage/ratelimit/*.php' 'app/storage/secret.*' 'app/config/mail.php' '*.DS_Store')

STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
cp -a public_html/. "$STAGE/"
cp -a app "$STAGE/app"
# Hostinger's platform serves files directly and ignores .htaccess, so inside
# public_html the app folder must contain only PHP files (which exit when
# requested directly) plus empty storage folders. Drop everything else.
find "$STAGE/app" -type f ! -name '*.php' ! -name '.gitkeep' -delete
(cd "$STAGE" && zip -rq "$ROOT/dist/friendswoodroofs-public_html.zip" . "${EXCL[@]}")

zip -rq dist/friendswoodroofs-deploy.zip public_html app README.md UPLOAD-INSTRUCTIONS.txt "${EXCL[@]}"
ls -lh dist/*.zip
