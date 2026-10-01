#!/bin/bash
# Create dist/friendswoodroofs-deploy.zip for upload through hPanel File Manager.
# The zip contains two folders that go side by side in the domain directory:
#   public_html/   -> contents go into the domain's public_html
#   app/           -> goes NEXT TO public_html (outside the web root)
# app/config/mail.php is included only if you created it locally.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/friendswoodroofs-deploy.zip
zip -rq dist/friendswoodroofs-deploy.zip public_html app \
  -x 'app/storage/logs/*.log' 'app/storage/ratelimit/*.json' 'app/storage/secret.key' '*.DS_Store'
echo "Created dist/friendswoodroofs-deploy.zip ($(du -h dist/friendswoodroofs-deploy.zip | cut -f1))"
[ -f app/config/mail.php ] && echo "Included app/config/mail.php (contains SMTP password - keep the zip private)." \
  || echo "NOTE: app/config/mail.php not found - create it on the server from mail.example.php."
