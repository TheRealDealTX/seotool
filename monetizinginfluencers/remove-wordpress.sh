#!/bin/bash
# One-off: permanently delete the old WordPress install from public_html
# (monetizinginfluencers.com, Hostinger user u401386392). Uses the same three
# File Browser credentials as deploy.sh (from `hosting_files_generate-upload-url`):
#
#   export MI_FB_URL='https://srvNNNN-files.hstgr.io/rest/<id>/api/tus/public_html'
#   export MI_FB_AUTH='…' MI_FB_REST='…'
#   ./remove-wordpress.sh
#
# The WordPress database is removed separately (Hostinger API `hosting_databases_*`, or hPanel).
set -u
: "${MI_FB_URL:?set MI_FB_URL}" "${MI_FB_AUTH:?set MI_FB_AUTH}" "${MI_FB_REST:?set MI_FB_REST}"
API="${MI_FB_URL%/tus/public_html}"
fb() { curl -sS --max-time 300 -H "X-Auth: $MI_FB_AUTH" -H "X-Auth-Rest: $MI_FB_REST" "$@"; }

WP_PATHS=(
  wp-admin wp-includes wp-content _wp-backup
  wp-activate.php wp-blog-header.php wp-comments-post.php wp-config.php wp-config-sample.php
  wp-cron.php wp-links-opml.php wp-load.php wp-login.php wp-mail.php wp-settings.php
  wp-signup.php wp-trackback.php xmlrpc.php license.txt readme.html default.php .htaccess.bk
)
fail=0
for p in "${WP_PATHS[@]}"; do
  c=$(fb -X DELETE "$API/resources/public_html/$p" -o /dev/null -w "%{http_code}")
  case "$c" in 200|204) echo "deleted $p";; 404) echo "absent  $p";; *) echo "FAIL $c $p"; fail=1;; esac
done
echo "--- remaining in public_html:"
fb "$API/resources/public_html/" | python3 -c 'import json,sys; print("\n".join(sorted(i["name"] for i in json.load(sys.stdin)["items"])))'
exit $fail
