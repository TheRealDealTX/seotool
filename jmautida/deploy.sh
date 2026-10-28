#!/usr/bin/env bash
# Upload jmautida/public to the jmautida.com document root through Hostinger's File Browser (TUS).
# Get credentials from the Hostinger API operation hosting_files_generate-upload-url
# (username u401386392, domain jmautida.com), then:
#   BASE=https://srvNNNN-files.hstgr.io/rest/<id>/api AK=<auth_key> RK=<rest_auth_key> ./jmautida/deploy.sh [files...]
# With no file arguments every file under public/ is uploaded (api/config.php included if present locally).
set -euo pipefail
cd "$(dirname "$0")/public"
: "${BASE:?set BASE}" "${AK:?set AK}" "${RK:?set RK}"
if [ $# -gt 0 ]; then files=("$@"); else mapfile -t files < <(find . -type f ! -name 'config.sample.php' | sed 's|^\./||' | sort); fi
fail=0
for f in "${files[@]}"; do
  size=$(stat -c%s "$f")
  url="$BASE/tus/public_html/$f?override=true"
  code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "$url" -H "X-Auth: $AK" -H "X-Auth-Rest: $RK" -H 'Tus-Resumable: 1.0.0' -H "Upload-Length: $size" -H 'Upload-Offset: 0')
  if [ "$code" != 201 ] && [ "$code" != 200 ]; then echo "FAIL create $f ($code)"; fail=1; continue; fi
  if [ "$size" -gt 0 ]; then
    code=$(curl -s -o /dev/null -w '%{http_code}' -X PATCH "$url" -H "X-Auth: $AK" -H "X-Auth-Rest: $RK" -H 'Tus-Resumable: 1.0.0' -H 'Content-Type: application/offset+octet-stream' -H 'Upload-Offset: 0' --data-binary "@$f")
    if [ "$code" != 204 ] && [ "$code" != 200 ]; then echo "FAIL upload $f ($code)"; fail=1; continue; fi
  fi
  echo "ok $f"
done
exit $fail
