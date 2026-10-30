"""Build every plan set.

    python3 generator/build.py            # all plans
    python3 generator/build.py plan-12-2429 plan-12-2423

For each plan in site/inc/plans.php this writes
  site/assets/plans/<slug>/   public previews: model.json (3D), floor/electrical/plumbing
                              plan previews (watermarked SVG), elevations, 3d.webp
  site/inc/plan-sets.json     estimate, materials summary and set contents for the plan pages
  dist/plan-files/<slug>.zip  the paid download: drawing set PDF, DXF, materials and cost
                              CSVs, OBJ 3D model, PNG images and a README

dist/ is not committed and is uploaded outside the web root (see deploy.sh).
"""
from __future__ import annotations

import csv
import io
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import thb_mesh as ME  # noqa: E402
import thb_model as M  # noqa: E402
import thb_qty as Q  # noqa: E402
import thb_sheets as SH  # noqa: E402
import thb_views as V  # noqa: E402

PR = M.PROFILE

SITE = os.path.join(ROOT, "site")
BUILD = os.path.join(ROOT, "build")
DIST = os.path.join(ROOT, "dist", "plan-files")
PUBLIC = os.path.join(SITE, "assets", "plans")
FACADES = ("front", "rear", "left", "right")


def write(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(data)


def file_base(p):
    return p["name"].replace(" ", "-")


def main(only):
    os.makedirs(BUILD, exist_ok=True)
    plans = json.loads(subprocess.check_output(["php", os.path.join(HERE, "export-plans.php")]))
    sets_path = os.path.join(SITE, "inc", "plan-sets.json")
    sets = json.load(open(sets_path)) if os.path.exists(sets_path) and only else {}
    jobs, ctx = [], {}

    # ---- phase 1: model, takeoff, previews ------------------------------------------
    for slug, p in plans.items():
        if only and slug not in only:
            continue
        m = M.build_model(slug, p)
        items, g = Q.takeoff(m)
        est = Q.estimate(m, items)
        me = ME.build_mesh(m)
        b = SH.SetBuilder(slug, p, m, items, est, me)
        pub = os.path.join(PUBLIC, slug)
        priv = os.path.join(BUILD, slug)
        write(os.path.join(pub, "model.json"), json.dumps(ME.to_json(m, me), separators=(",", ":")))
        modes = ("floor", "electrical", "plumbing") + (("floor2", "electrical2", "plumbing2") if m.upper else ())
        for mode in modes:
            write(os.path.join(pub, f"{mode}.svg"), b.preview(mode))
            write(os.path.join(priv, f"{mode}.svg"), b.preview(mode, watermark=False))
        for fac in FACADES:
            svg = b.preview_elevation(fac)
            write(os.path.join(pub, f"elevation-{fac}.svg"), svg)
            write(os.path.join(priv, f"elevation-{fac}.svg"), svg)
        model_url = f"/assets/plans/{slug}/model.json"
        views = {"3d-front": ({"theta": -0.62, "phi": 1.18, "zoom": 1.6}, True), "3d-rear": ({"theta": 2.45, "phi": 1.15, "zoom": 1.6}, True),
                 "3d-cutaway": ({"theta": -0.5, "phi": 0.78, "zoom": 1.35}, False), "3d-top": ({"theta": 0.0, "phi": 0.17, "zoom": 1.4}, False)}
        for name, (view, roof) in views.items():
            jobs.append({"type": "3d", "model": model_url, "out": os.path.join(priv, "img", f"{name}.png"), "width": 1600, "height": 1000, "view": view, "roof": roof})
        for mode in modes:
            name = mode.replace("2", "-second-floor")
            jobs.append({"type": "svg", "svg": os.path.join(priv, f"{mode}.svg"), "out": os.path.join(priv, "img", f"{name}-plan.png"), "width": 2400})
        for fac in FACADES:
            jobs.append({"type": "svg", "svg": os.path.join(priv, f"elevation-{fac}.svg"), "out": os.path.join(priv, "img", f"elevation-{fac}.png"), "width": 2000})
        ctx[slug] = (p, m, items, est, me, b)
        print(f"{slug}: model, takeoff ({len(items)} items) and previews")

    # ---- phase 2: renders ------------------------------------------------------------
    jp = os.path.join(BUILD, "render-jobs.json")
    write(jp, json.dumps(jobs))
    subprocess.check_call(["node", os.path.join(HERE, "render.js"), jp], env={**os.environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"]).decode().strip()})

    # ---- phase 3: drawing set, CAD, files, zip ---------------------------------------
    from PIL import Image
    os.makedirs(DIST, exist_ok=True)
    for slug, (p, m, items, est, me, _) in ctx.items():
        priv = os.path.join(BUILD, slug)
        img = os.path.join(priv, "img")
        cover = os.path.join(img, "3d-front.png")
        b = SH.SetBuilder(slug, p, m, items, est, me, cover_img=cover)
        Image.open(cover).convert("RGB").resize((1200, 750)).save(os.path.join(PUBLIC, slug, "3d.webp"), "WEBP", quality=82)
        Image.open(os.path.join(img, "3d-cutaway.png")).convert("RGB").resize((1200, 750)).save(os.path.join(PUBLIC, slug, "3d-cutaway.webp"), "WEBP", quality=82)
        base = file_base(p)
        pdf = os.path.join(priv, f"{base}-Construction-Drawings-24x36.pdf")
        b.pdf(pdf)
        dxf = b.dxf()
        obj, mtl = ME.to_obj(m, me, base)
        mat_csv = io.StringIO()
        w = csv.writer(mat_csv)
        w.writerow(["Category", "Item", "Quantity", "Unit", "Unit price (USD)", "Total (USD)"])
        for it in items:
            w.writerow([it.cat, it.name, round(it.qty, 2), it.unit, f"{it.price:.2f}", f"{it.total:.2f}"])
        w.writerow([])
        w.writerow(["", "Materials subtotal", "", "", "", f"{est['materials']:.2f}"])
        cost_csv = io.StringIO()
        w = csv.writer(cost_csv)
        w.writerow(["Category", "Materials (USD)", "Contractor labor (USD)", "Total (USD)"])
        for c in est["categories"]:
            w.writerow([c["name"], c["materials"], c["labor"], c["materials"] + c["labor"]])
        for k, lbl in (("overhead", "Contractor overhead & profit (18%)"), ("permits", "Permits & plan review"), ("contingency_gc", "Contingency (10%)"), ("gc_total", "TOTAL - contractor build")):
            w.writerow([lbl, "", "", est[k]])
        w.writerow([])
        for k, lbl in (("materials", "Materials"), ("diy_trade_help", "Licensed trade help (electrical, plumbing, HVAC)"), ("permits", "Permits & plan review"),
                       ("contingency_diy", "Contingency (12% of materials)"), ("diy_total", "TOTAL - owner-built")):
            w.writerow([lbl, "", "", est[k]])
        regions = "".join(f"\n    {n + ':':20s} contractor ${gc:,}   owner-built ${diy:,}" for n, f, gc, diy in est.get("regions", []))
        readme = README.format(name=p["name"], title=p["title"], base=base, sheets="\n".join(f"  {n:6s} {t}" for n, t, _ in b.sheets),
                               sqft=p["sqft"], diy=f"{est['diy_total']:,}", gc=f"{est['gc_total']:,}", brand=PR["brand_name"], site=PR["url"],
                               phone=PR["phone"], basis=PR.get("cost_basis", "2026 US national averages"),
                               regions=("\n  By region:" + regions) if regions else "", important=PR["readme_important"])
        zpath = os.path.join(DIST, f"{slug}.zip")
        files = []
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            def add(arc, data=None, path=None):
                if path:
                    z.write(path, f"{base}/{arc}")
                    files.append((arc, os.path.getsize(path)))
                else:
                    raw = data.encode() if isinstance(data, str) else data
                    z.writestr(f"{base}/{arc}", raw)
                    files.append((arc, len(raw)))
            add("README.txt", readme)
            add(os.path.basename(pdf), path=pdf)
            add(f"{base}-CAD-Drawings.dxf", dxf)
            add(f"{base}-Materials-List.csv", mat_csv.getvalue())
            add(f"{base}-Cost-Estimate.csv", cost_csv.getvalue())
            add(f"3D-Model/{base}.obj", obj)
            add(f"3D-Model/{base}.mtl", mtl)
            for f in sorted(os.listdir(img)):
                add(f"Images/{f}", path=os.path.join(img, f))
        # Summary for the plan page
        cats = {}
        for it in items:
            c = cats.setdefault(it.cat, {"name": it.cat, "lines": 0, "total": 0.0, "examples": []})
            c["lines"] += 1
            c["total"] += it.total
            if len(c["examples"]) < 4:
                c["examples"].append(it.name)
        kinds = {}
        for d in m.devices:
            kinds[d.kind] = kinds.get(d.kind, 0) + 1
        fx = {}
        for f in m.all("fixtures"):
            fx[f.kind] = fx.get(f.kind, 0) + 1
        sets[slug] = {
            "estimate": est,
            "materials": [{**c, "total": round(c["total"])} for c in cats.values()],
            "material_lines": len(items),
            "sheets": [[n, t] for n, t, _ in b.sheets],
            "files": [[a, s] for a, s in files],
            "zip_bytes": os.path.getsize(zpath),
            "electrical": {"circuits": len(m.circuits), "service": m.notes["load"]["service"],
                           "receptacles": sum(v for k, v in kinds.items() if k in ("rec", "gfci", "rec20", "rec240", "wp")),
                           "lights": sum(v for k, v in kinds.items() if k in ("light", "can", "sconce", "fan", "cfan")), "fans": kinds.get("cfan", 0),
                           "alarms": kinds.get("smoke", 0) + kinds.get("smokeco", 0), "hvac_heads": kinds.get("minisplit", 0)},
            "plumbing": {"fixtures": sum(v for k, v in fx.items() if k in M.DFU), "dfu": m.notes.get("dfu", 0), "drain": m.notes.get("main_drain", ""),
                         "water_heater": "tank" if "wh" in fx else "tankless"},
            "openings": {"windows": len([o for o in m.all("openings") if o.kind == "window"]), "doors": len([o for o in m.all("openings") if o.kind != "window"])},
            "hvac": m.notes.get("hvac", {}),
            "upper": bool(m.upper),
            "framing": {"walls": f"{m.stud} @ {24 if m.container else 16} in. o.c.", "foundation": m.foundation},
        }
        print(f"{slug}: {len(b.sheets)} sheets, zip {os.path.getsize(zpath) / 1e6:.1f} MB")
    write(sets_path, json.dumps(sets, indent=1, sort_keys=True))


README = """{name} - {title}
{brand}  |  {site}  |  {phone}

WHAT'S IN THIS FOLDER
  {base}-Construction-Drawings-24x36.pdf
      The full drawing set, sized for 24 x 36 in. (ARCH D) sheets. Prints legibly at
      half size on 11 x 17 in. paper (scales on the sheets then read at half value).
{sheets}

  {base}-CAD-Drawings.dxf
      AutoCAD R12 DXF in inches at full scale, with separate layers for walls, doors,
      glazing, fixtures, dimensions, electrical and plumbing. Opens in AutoCAD,
      DraftSight, LibreCAD, BricsCAD, SketchUp (import) and most CAD programs.

  {base}-Materials-List.csv     Line-item takeoff with quantities, units and prices
  {base}-Cost-Estimate.csv      Cost by trade, owner-built and contractor totals
  3D-Model/{base}.obj + .mtl    3D model (feet, Y up) for SketchUp, Blender, Revit, etc.
  Images/                       3D renders, floor / electrical / plumbing plans, elevations

QUICK NUMBERS
  Heated area: {sqft} sq ft
  Estimated cost, owner-built: ${diy}   With a general contractor: ${gc}
  ({basis}; see sheet G2.0 for what is included and excluded.){regions}

LICENSE
  Your purchase includes a license to build ONE home from this plan. You may print and
  copy the drawings as needed for that build (builder, lender, permit office). The
  drawings may not be resold, shared publicly or used for additional homes without a
  further license.

IMPORTANT
  {important}

Need changes (flip the layout, add a bedroom, change the foundation)? Reply to your
order email or call {phone} for a modification quote.
"""

if __name__ == "__main__":
    main(set(sys.argv[1:]))
