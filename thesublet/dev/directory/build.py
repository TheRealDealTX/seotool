#!/usr/bin/env python3
"""Merge DataForSEO business-listing results into dev/directory/directory.json.

Inputs (git-ignored): paths-*.txt ("<city-key> <saved tool-result file>") and raw-*.jsonl.
Filters out closed businesses, university dorms (.edu / student_dormitory), and
entries with no phone and no website. Output fields are only public business info.
"""
import glob, json, math, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FURNISHED = {"furnished_apartment_building", "serviced_apartment", "serviced_accommodation",
             "extended_stay_hotel", "corporate_housing", "short_term_apartment_rental_agency", "corporate_campus"}


def load_file(path):
    try:
        raw = json.load(open(path))
    except Exception as e:
        print("skip unreadable", path, e, file=sys.stderr)
        return []
    if isinstance(raw, list) and raw and isinstance(raw[0], dict) and "text" in raw[0]:
        raw = json.loads(raw[0]["text"])
    return raw.get("items") or []


def norm_item(it, key):
    ai = it.get("address_info") or {}
    attrs = ((it.get("attributes") or {}).get("available_attributes") or {})
    flat = set(sum([v for v in attrs.values() if isinstance(v, list)], []))
    status = (((it.get("work_time") or {}).get("work_hours") or {}).get("current_status"))
    return {
        "key": key, "cid": str(it.get("cid") or ""), "place_id": it.get("place_id") or "",
        "title": it.get("title") or "", "category": it.get("category") or "",
        "category_ids": it.get("category_ids") or [], "address": ai.get("address") or "",
        "city": ai.get("city") or "", "zip": ai.get("zip") or "", "region": ai.get("region") or "",
        "borough": ai.get("borough") or "", "lat": it.get("latitude"), "lng": it.get("longitude"),
        "phone": it.get("phone") or "", "url": it.get("url") or "", "domain": it.get("domain") or "",
        "rating": (it.get("rating") or {}).get("value"), "votes": (it.get("rating") or {}).get("votes_count"),
        "status": status, "attrs": sorted(flat),
    }


def centers():
    php = "define('APP',1); foreach (glob('%s/../../app/content/cities/*.php') as $f) foreach (require $f as $k=>$c) echo $k,' ',$c['lat'],' ',$c['lng'],PHP_EOL;" % HERE
    out = subprocess.run(["php", "-r", php], capture_output=True, text=True).stdout
    return {k: (float(a), float(b)) for k, a, b in (l.split() for l in out.splitlines() if l.strip())}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def main():
    C = centers()
    rows = []
    for pf in glob.glob(os.path.join(HERE, "paths-*.txt")):
        for line in open(pf):
            parts = line.strip().split(None, 1)
            if len(parts) != 2:
                continue
            key, path = parts
            rows += [norm_item(it, key) for it in load_file(path.strip())]
    for rf in glob.glob(os.path.join(HERE, "raw-*.jsonl")):
        for line in open(rf):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            r.setdefault("attrs", [])
            r["cid"] = str(r.get("cid") or "")
            rows.append(r)

    out, seen, dropped = [], set(), {}
    def drop(reason):
        dropped[reason] = dropped.get(reason, 0) + 1
    for r in rows:
        ids = set(r.get("category_ids") or [])
        dom = (r.get("domain") or r.get("url") or "").lower()
        ref = r.get("cid") or r.get("place_id") or (r["title"] + r.get("address", ""))
        if not r.get("title") or r.get("lat") is None:
            drop("incomplete"); continue
        if r["key"] not in C or km(C[r["key"]], (float(r["lat"]), float(r["lng"]))) > 45:
            drop("far from city"); continue
        if ref in seen:
            drop("duplicate"); continue
        if r.get("status") in ("closed_forever", "temporarily_closed"):
            drop("closed"); continue
        if "student_dormitory" in ids or re.search(r"\.edu(/|$)", dom) or ".edu/" in (r.get("url") or ""):
            drop("university"); continue
        if re.search(r"\b(residence hall|quadrangle|dormitory|housing office)\b", r["title"], re.I):
            drop("university"); continue
        if not r.get("phone") and not r.get("url"):
            drop("no contact"); continue
        seen.add(ref)
        if "extended_stay_hotel" in ids or "hotel" in (r.get("category") or "").lower():
            ptype = "extended_stay"
        elif (r.get("category") or "").lower().startswith("student") or ("student_housing_center" in ids and not ids & FURNISHED):
            ptype = "student_housing"
        else:
            ptype = "furnished_community"
        attrs = set(r.get("attrs") or [])
        amen = []
        for a, k in [("has_fitness_center", "gym"), ("has_swimming_pool", "pool"), ("has_in_unit_washer_dryer", "laundry_in_unit"),
                     ("has_elevator", "elevator"), ("has_onsite_parking", "parking"), ("has_business_center", "workspace")]:
            if a in attrs:
                amen.append(k)
        if ptype in ("extended_stay", "furnished_community"):
            amen.append("kitchen")
        votes = r.get("votes") or 0
        rating = r.get("rating") or 0
        out.append({
            "key": r["key"], "ref": ref, "title": r["title"][:140], "category": (r.get("category") or "")[:80],
            "ptype": ptype, "furnished": 1 if (ids & FURNISHED or ptype != "student_housing") else 0,
            "address": (r.get("address") or "")[:190], "address_city": (r.get("city") or "")[:80],
            "zip": re.sub(r"[^0-9]", "", r.get("zip") or "")[:5], "borough": (r.get("borough") or "")[:80],
            "lat": round(float(r["lat"]), 5), "lng": round(float(r["lng"]), 5),
            "phone": (r.get("phone") or "")[:40], "url": (r.get("url") or "")[:300],
            "pets": "yes" if attrs & {"welcomes_pets", "welcomes_dogs"} else "ask",
            "amenities": sorted(set(amen)),
            "score": int(min(votes, 5000) * (rating or 3) / 5),
        })
    json.dump(out, open(os.path.join(HERE, "directory.json"), "w"), indent=0, ensure_ascii=False)
    by = {}
    for o in out:
        by[o["key"]] = by.get(o["key"], 0) + 1
    print(f"rows={len(rows)} kept={len(out)} cities={len(by)} dropped={dropped}")


if __name__ == "__main__":
    main()
