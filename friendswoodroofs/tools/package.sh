#!/bin/bash
# Build upload zips in dist/:
#   friendswoodroofs-public_html.zip  extract INSIDE public_html (app/ ends up in
#                                     public_html/app, blocked by .htaccess).
#                                     Use this with hPanel File Manager.
#   friendswoodroofs-deploy.zip       public_html/ and app/ side by side, for hosts
#                                     that allow writing next to public_html.
# Secrets, logs and runtime files are never included.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
mkdir -p dist
rm -f dist/friendswoodroofs-public_html.zip dist/friendswoodroofs-deploy.zip
EXCL=(-x 'app/storage/logs/*.log' 'app/storage/ratelimit/*.json' 'app/storage/secret.key' 'app/config/mail.php' '*.DS_Store')

STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
cp -a public_html/. "$STAGE/"
cp -a app "$STAGE/app"
mkdir -p "$STAGE/app/docs"
cp README.md UPLOAD-INSTRUCTIONS.txt "$STAGE/app/docs/"
(cd "$STAGE" && zip -rq "$ROOT/dist/friendswoodroofs-public_html.zip" . "${EXCL[@]}")

zip -rq dist/friendswoodroofs-deploy.zip public_html app README.md UPLOAD-INSTRUCTIONS.txt "${EXCL[@]}"
ls -lh dist/*.zip
