#!/bin/bash
# The plan generator, 3D viewer and store engine are shared by the plan-store sites in this
# repo (tinyhomesblueprint/, cowboytinyhomes/). Edit them in either site, then copy them
# across so the copies never drift. Site-specific settings stay out of these files:
# generator/profile.json, site/inc/plans.php, site/inc/config.php and the page templates.
#
#   ./sync-shared.sh --check                          # list shared files that differ
#   ./sync-shared.sh tinyhomesblueprint cowboytinyhomes   # copy from one site to the other
set -u
cd "$(dirname "$0")" || exit 1
FILES=(
  generator/build.py generator/export-plans.php generator/render.js
  generator/thb_draw.py generator/thb_mesh.py generator/thb_model.py
  generator/thb_qty.py generator/thb_sheets.py generator/thb_views.py
  site/assets/js/plan-3d.js site/assets/js/plan-page.js
  site/assets/js/vendor/three-0.160.0.module.min.js
  site/inc/store.php site/inc/plan-svg.php site/inc/mailer.php site/pages/order/webhook.php
  dev-router.php
)
SITES=(tinyhomesblueprint cowboytinyhomes)
if [ "${1:-}" = "--check" ]; then
  rc=0
  for f in "${FILES[@]}"; do
    if ! cmp -s "${SITES[0]}/$f" "${SITES[1]}/$f"; then echo "differs: $f"; rc=1; fi
  done
  [ $rc -eq 0 ] && echo "shared files are identical"
  exit $rc
fi
from=${1:?source site}; to=${2:?target site}
for f in "${FILES[@]}"; do
  [ -f "$from/$f" ] || { echo "missing: $from/$f"; continue; }
  mkdir -p "$(dirname "$to/$f")"
  cmp -s "$from/$f" "$to/$f" || { cp "$from/$f" "$to/$f"; echo "copied: $f"; }
done
