#!/usr/bin/env python3
"""Build the Bible data files the site serves.

Output (all under public/data/):
  books.json            book table: slug, names per version, chapter/verse counts
  versions.json         version table (prefix, names, language, copyright)
  votd.json             verse-of-the-day reference list
  <ver>/<book>.json     {"c": [[verse text | "" | null, ...], ...]} one file per book.
                        null = not available in this version; "" = this verse is
                        joined with the one before it (the translation renders a
                        range such as 14–16 as one verse).
  <ver>/search.tsv      one line per verse: book-index TAB chapter TAB verse TAB text

Sources:
  KJV (/ta/)            eBible.org eng-kjv VPL (public domain). Downloaded into
                        sources/cache/ on first run.
  Ang Biblia 2011 (/ml/) sources/ml-wordpress-export.json — the verses that were
                        published on the old WordPress site — plus, optionally,
                        any licensed text dropped into sources/ml-licensed/*.txt
                        as VPL lines ("GEN 1:1 Sa sinugdan ...", USFM book codes).
                        Licensed lines override the WordPress export.
  Ang Pulong sa Dios (/ceb/) eBible.org cebocb VPL — Biblica® Open Ang Pulong sa
                        Dios, CC BY-SA 4.0. Text is used unchanged.

Run:  python3 tools/build_data.py
"""
import html
import io
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
OUT = ROOT / "public" / "data"
KJV_URL = "https://ebible.org/Scriptures/eng-kjv_vpl.zip"
CEB_URL = "https://ebible.org/Scriptures/cebocb_vpl.zip"

# slug (kept from the WordPress URLs), USFM code, English name, Cebuano name,
# extra search abbreviations
BOOKS = [
    ("genesis", "GEN", "Genesis", "Genesis", "gen ge gn"),
    ("exodus", "EXO", "Exodus", "Exodo", "exo ex exod"),
    ("leviticus", "LEV", "Leviticus", "Levitico", "lev le lv"),
    ("numbers", "NUM", "Numbers", "Numeros", "num nu nm numeros"),
    ("deuteronomy", "DEU", "Deuteronomy", "Deuteronomio", "deut deu dt"),
    ("joshua", "JOS", "Joshua", "Josue", "josh jos jsh"),
    ("judges", "JDG", "Judges", "Mga Maghuhukom", "judg jdg jg maghuhukom"),
    ("ruth", "RUT", "Ruth", "Ruth", "rut ru rth"),
    ("1samuel", "1SA", "1 Samuel", "1 Samuel", "1sam 1sa 1sm"),
    ("2samuel", "2SA", "2 Samuel", "2 Samuel", "2sam 2sa 2sm"),
    ("1kings", "1KI", "1 Kings", "1 Mga Hari", "1kgs 1ki 1kin 1hari"),
    ("2kings", "2KI", "2 Kings", "2 Mga Hari", "2kgs 2ki 2kin 2hari"),
    ("1chronicles", "1CH", "1 Chronicles", "1 Cronicas", "1chr 1ch 1chron 1cronicas"),
    ("2chronicles", "2CH", "2 Chronicles", "2 Cronicas", "2chr 2ch 2chron 2cronicas"),
    ("ezra", "EZR", "Ezra", "Esdras", "ezr esdras"),
    ("nehemiah", "NEH", "Nehemiah", "Nehemias", "neh ne"),
    ("esther", "EST", "Esther", "Ester", "esth est es"),
    ("job", "JOB", "Job", "Job", "jb"),
    ("psalms", "PSA", "Psalms", "Mga Salmo", "ps psa psalm pss salmo salmos"),
    ("proverbs", "PRO", "Proverbs", "Mga Proverbio", "prov pro prv pr proverbio"),
    ("ecclesiastes", "ECC", "Ecclesiastes", "Ecclesiastes", "eccl ecc ec qoh"),
    ("songofsongs", "SNG", "Song of Solomon", "Awit ni Solomon", "song sos sng so canticles awit"),
    ("isaiah", "ISA", "Isaiah", "Isaias", "isa is"),
    ("jeremiah", "JER", "Jeremiah", "Jeremias", "jer je jr"),
    ("lamentations", "LAM", "Lamentations", "Mga Lamentaciones", "lam la lamentaciones"),
    ("ezekiel", "EZK", "Ezekiel", "Ezequiel", "ezek eze ezk"),
    ("daniel", "DAN", "Daniel", "Daniel", "dan da dn"),
    ("hosea", "HOS", "Hosea", "Oseas", "hos ho"),
    ("joel", "JOL", "Joel", "Joel", "joe jl"),
    ("amos", "AMO", "Amos", "Amos", "am"),
    ("obadiah", "OBA", "Obadiah", "Abdias", "obad ob oba"),
    ("jonah", "JON", "Jonah", "Jonas", "jon jnh"),
    ("micah", "MIC", "Micah", "Miqueas", "mic mc"),
    ("nahum", "NAM", "Nahum", "Nahum", "nah na"),
    ("habakkuk", "HAB", "Habakkuk", "Habacuc", "hab hb"),
    ("zephaniah", "ZEP", "Zephaniah", "Sofonias", "zeph zep zp"),
    ("haggai", "HAG", "Haggai", "Hageo", "hag hg"),
    ("zechariah", "ZEC", "Zechariah", "Zacarias", "zech zec zc"),
    ("malachi", "MAL", "Malachi", "Malaquias", "mal ml"),
    ("matthew", "MAT", "Matthew", "Mateo", "matt mat mt"),
    ("mark", "MRK", "Mark", "Marcos", "mrk mk mr"),
    ("luke", "LUK", "Luke", "Lucas", "luk lk"),
    ("john", "JHN", "John", "Juan", "jhn jn joh"),
    ("acts", "ACT", "Acts", "Mga Buhat", "act ac buhat"),
    ("romans", "ROM", "Romans", "Mga Taga-Roma", "rom ro rm roma"),
    ("1corinthians", "1CO", "1 Corinthians", "1 Mga Taga-Corinto", "1cor 1co 1corinto"),
    ("2corinthians", "2CO", "2 Corinthians", "2 Mga Taga-Corinto", "2cor 2co 2corinto"),
    ("galatians", "GAL", "Galatians", "Mga Taga-Galacia", "gal ga galacia"),
    ("ephesians", "EPH", "Ephesians", "Mga Taga-Efeso", "eph ephes efeso"),
    ("philippians", "PHP", "Philippians", "Mga Taga-Filipos", "phil php pp filipos"),
    ("colossians", "COL", "Colossians", "Mga Taga-Colosas", "col colosas"),
    ("1thessalonians", "1TH", "1 Thessalonians", "1 Mga Taga-Tesalonica", "1thess 1th 1thes 1tesalonica"),
    ("2thessalonians", "2TH", "2 Thessalonians", "2 Mga Taga-Tesalonica", "2thess 2th 2thes 2tesalonica"),
    ("1timothy", "1TI", "1 Timothy", "1 Timoteo", "1tim 1ti 1timoteo"),
    ("2timothy", "2TI", "2 Timothy", "2 Timoteo", "2tim 2ti 2timoteo"),
    ("titus", "TIT", "Titus", "Tito", "tit ti"),
    ("philemon", "PHM", "Philemon", "Filemon", "philem phm phlm"),
    ("hebrews", "HEB", "Hebrews", "Mga Hebreohanon", "heb he hebreohanon"),
    ("james", "JAS", "James", "Santiago", "jas jm jam"),
    ("1peter", "1PE", "1 Peter", "1 Pedro", "1pet 1pe 1pt"),
    ("2peter", "2PE", "2 Peter", "2 Pedro", "2pet 2pe 2pt"),
    ("1john", "1JN", "1 John", "1 Juan", "1jn 1jo 1jhn"),
    ("2john", "2JN", "2 John", "2 Juan", "2jn 2jo 2jhn"),
    ("3john", "3JN", "3 John", "3 Juan", "3jn 3jo 3jhn"),
    ("jude", "JUD", "Jude", "Judas", "jud jd"),
    ("revelation", "REV", "Revelation", "Pinadayag", "rev re rv revelations apocalypse"),
]

# eBible's KJV VPL uses a few non-USFM codes.
EBIBLE_CODES = {"SOL": "SNG", "EZE": "EZK", "JOE": "JOL", "NAH": "NAM", "MAR": "MRK",
                "JOH": "JHN", "PHI": "PHP", "JAM": "JAS", "1JO": "1JN", "2JO": "2JN",
                "3JO": "3JN"}

# Order = order of the header switcher. "fallback" is the chain used for verses a
# version doesn't have yet. "italics": [brackets] in the text mean italics (KJV only).
VERSIONS = {
    "ta": {
        "prefix": "ta", "short": "KJV", "name": "King James Version",
        "label": "King James Version (KJV)", "lang": "en", "nameKey": "en",
        "desc": "English · complete Old and New Testament",
        "copyright": "Public domain.", "italics": True, "fallback": [],
    },
    "ml": {
        "prefix": "ml", "short": "AB", "name": "Ang Biblia, 2011",
        "label": "Ang Biblia, 2011", "lang": "ceb", "nameKey": "ceb",
        "desc": "Cebuano",
        "copyright": "Ang Biblia © 2011 Philippine Bible Society. Used with permission.",
        "italics": False, "fallback": ["ceb", "ta"],
    },
    "ceb": {
        "prefix": "ceb", "short": "APSD", "name": "Ang Pulong sa Dios",
        "label": "Ang Pulong sa Dios", "lang": "ceb", "nameKey": "ceb",
        "fullTitle": "Biblica® Open Ang Pulong sa Dios™",
        "desc": "Cebuano · complete modern translation (Biblica® Open)",
        "copyright": "Biblica® Open Ang Pulong sa Dios™ Katungod sa pagmantala © 2009, 2010, 2014, 2024 Biblica, Inc. "
                     "Biblica® Open Cebuano Contemporary Bible™ Copyright © 2009, 2010, 2014, 2024 by Biblica, Inc. "
                     "“Biblica” is a trademark registered in the United States Patent and Trademark Office by Biblica, Inc. "
                     "Used with permission. Licensed under CC BY-SA 4.0.",
        "notice": "The original Work by its copyright holders is available for free at www.biblica.com and open.bible.",
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "italics": False, "fallback": ["ta"],
    },
}

# Verse of the day: popular, self-contained verses. The site picks one per
# calendar day by cycling through this list (see votdIndex in app.js / bible.php).
VOTD = """
john 3 16; jeremiah 29 11; philippians 4 13; romans 8 28; proverbs 3 5; proverbs 3 6;
psalms 23 1; isaiah 41 10; joshua 1 9; matthew 11 28; romans 12 2; philippians 4 6;
2timothy 1 7; psalms 46 1; isaiah 40 31; matthew 6 33; hebrews 11 1; galatians 5 22;
1corinthians 13 4; ephesians 2 8; psalms 119 105; romans 5 8; 2corinthians 5 17;
psalms 37 4; lamentations 3 22; lamentations 3 23; 1peter 5 7; james 1 5; psalms 27 1;
john 14 6; matthew 28 19; romans 15 13; hebrews 12 1; psalms 34 8; numbers 6 24;
numbers 6 25; numbers 6 26; deuteronomy 31 6; deuteronomy 31 8; psalms 91 1; psalms 91 2;
psalms 121 1; psalms 121 2; isaiah 26 3; isaiah 43 2; isaiah 53 5; micah 6 8;
zephaniah 3 17; nahum 1 7; habakkuk 3 19; matthew 5 14; matthew 5 16; matthew 7 7;
matthew 22 37; mark 10 27; mark 11 24; luke 1 37; luke 6 31; john 1 1; john 8 12;
john 10 10; john 11 25; john 13 34; john 14 27; john 15 5; john 15 13; john 16 33;
acts 1 8; romans 6 23; romans 8 1; romans 8 31; romans 8 38; romans 10 9; romans 12 12;
1corinthians 10 13; 1corinthians 16 14; 2corinthians 4 16; 2corinthians 12 9;
galatians 2 20; galatians 6 9; ephesians 3 20; ephesians 4 32; ephesians 6 10;
philippians 1 6; philippians 4 7; philippians 4 8; philippians 4 19; colossians 3 2;
colossians 3 23; 1thessalonians 5 16; 1thessalonians 5 17; 1thessalonians 5 18;
2timothy 3 16; hebrews 4 12; hebrews 13 5; hebrews 13 8; james 1 2; james 1 12;
james 4 8; 1peter 2 9; 2peter 3 9; 1john 1 9; 1john 4 7; 1john 4 18; 1john 4 19;
revelation 3 20; revelation 21 4; genesis 1 1; genesis 1 27; genesis 28 15;
genesis 50 20; exodus 14 14; exodus 15 2; exodus 20 12; exodus 33 14; leviticus 19 18;
deuteronomy 6 5; deuteronomy 7 9; joshua 24 15; ruth 1 16; 1samuel 16 7; 1samuel 12 24;
2samuel 22 31; 2samuel 22 2; 1kings 8 61; 2kings 6 16; 1chronicles 16 11;
1chronicles 16 34; 2chronicles 7 14; nehemiah 8 10; esther 4 14; job 19 25;
psalms 1 1; psalms 4 8; psalms 16 8; psalms 16 11; psalms 18 2; psalms 19 14;
psalms 23 4; psalms 28 7; psalms 30 5; psalms 31 24; psalms 32 8; psalms 34 18;
psalms 37 5; psalms 40 1; psalms 42 11; psalms 46 10; psalms 51 10; psalms 55 22;
psalms 56 3; psalms 62 1; psalms 73 26; psalms 84 11; psalms 90 12; psalms 100 4;
psalms 103 1; psalms 103 12; psalms 107 1; psalms 118 24; psalms 119 11;
psalms 136 1; psalms 138 8; psalms 139 14; psalms 143 8; psalms 145 18; psalms 147 3;
proverbs 4 23; proverbs 16 3; proverbs 16 9; proverbs 17 17; proverbs 18 10;
proverbs 22 6; proverbs 27 17; proverbs 31 25; ecclesiastes 3 1; ecclesiastes 3 11;
isaiah 9 6; isaiah 12 2; isaiah 30 15; isaiah 40 8; isaiah 40 29; isaiah 54 10;
isaiah 55 8; isaiah 58 11; isaiah 61 1; jeremiah 17 7; jeremiah 31 3; jeremiah 33 3;
ezekiel 36 26; daniel 2 20; hosea 6 3; joel 2 13; amos 5 24; malachi 3 10;
matthew 5 3; matthew 5 9; matthew 6 34; matthew 18 20; matthew 19 26; mark 12 30;
luke 12 32; john 3 17; john 6 35; john 14 1; john 14 2; romans 1 16; romans 3 23;
romans 5 1; romans 8 18; romans 12 10; 1corinthians 2 9; 1corinthians 15 58;
2corinthians 9 7; ephesians 1 7; ephesians 5 2; philippians 3 14; colossians 3 15;
2thessalonians 3 3; 1timothy 4 12; titus 3 5; hebrews 10 23; hebrews 11 6; james 5 16;
1peter 3 15; 1peter 4 8; 1john 3 1; 1john 5 14; jude 1 24; revelation 22 13
"""


def clean(text):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def ebible_lines(url, name):
    cache = SRC / "cache" / name
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        print("downloading", url)
        raw = urllib.request.urlopen(url, timeout=120).read()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            cache.write_bytes(z.read(name))
    return cache.read_text(encoding="utf-8-sig").splitlines()


def fit_versification(name, text, shape):
    """Map a modern translation onto KJV verse numbers without altering its text.

    Verses beyond the KJV count are appended to the last KJV verse of the chapter
    (e.g. 3 John 1:15). Verses the translation joined with the previous one become
    "" so the reader can show a range (e.g. 1 Chronicles 8:14–16)."""
    out = {}
    for (slug, c, v), t in sorted(text.items()):
        if slug not in shape or c not in shape[slug]:
            print(f"warning: {name} {slug} {c}:{v} has no KJV chapter, dropped")
            continue
        last = shape[slug][c]
        if v > last:
            out[(slug, c, last)] = (out.get((slug, c, last)) or "") + " " + t
            print(f"note: {name} {slug} {c}:{v} appended to {c}:{last}")
        else:
            out[(slug, c, v)] = t
    joined = 0
    for slug, chs in shape.items():
        for c, n in chs.items():
            seen = False
            for v in range(1, n + 1):
                if (slug, c, v) in out:
                    seen = True
                elif seen:
                    out[(slug, c, v)] = ""
                    joined += 1
    return out, joined


VPL = re.compile(r"^([1-3A-Z]{3}) (\d+):(\d+) (.*)$")


def parse_vpl(lines, by_code):
    """VPL lines -> {(slug, ch, v): text}; non-canonical books are skipped."""
    out = {}
    for line in lines:
        m = VPL.match(line.strip())
        if not m:
            continue
        code = EBIBLE_CODES.get(m.group(1), m.group(1))
        if code in by_code:
            # "¶" marks paragraph starts in the KJV source; the reader doesn't use them
            text = re.sub(r"\s+", " ", m.group(4).replace("¶", "")).strip()
            out[(by_code[code], int(m.group(2)), int(m.group(3)))] = text
    return out


def main():
    by_code = {b[1]: b[0] for b in BOOKS}
    kjv = parse_vpl(ebible_lines(KJV_URL, "eng-kjv_vpl.txt"), by_code)
    # KJV marks translator-supplied words with [brackets]; keep them as the
    # convention for italics (rendered as <i> by the site).
    if len(kjv) != 31102:
        sys.exit(f"KJV verse count {len(kjv)} != 31102")

    # Versification comes from the KJV.
    shape = {}
    for (slug, c, v) in kjv:
        shape.setdefault(slug, {}).setdefault(c, 0)
        shape[slug][c] = max(shape[slug][c], v)

    ml = {}
    export = json.loads((SRC / "ml-wordpress-export.json").read_text(encoding="utf-8"))
    # WordPress gave duplicate posts suffixed slugs ("genesis/13-2/7-2"); the
    # plain slug wins when both exist.
    for key in sorted(export["verses"], key=lambda k: "-" in k):
        slug, c, v = key.split("/")
        ref = (slug, int(c.split("-")[0]), int(v.split("-")[0]))
        t = clean(export["verses"][key]["html"])
        if t and ref not in ml:
            ml[ref] = t
    from_site = len(ml)
    licensed = 0
    for f in sorted((SRC / "ml-licensed").glob("*.txt")) if (SRC / "ml-licensed").exists() else []:
        rows = parse_vpl(f.read_text(encoding="utf-8-sig").splitlines(), by_code)
        licensed += len(rows)
        ml.update(rows)

    extra = [k for k in ml if k[0] not in shape or k[1] not in shape[k[0]] or k[2] > shape[k[0]][k[1]]]
    for k in extra:
        print("warning: Ang Biblia verse outside KJV versification, dropped:", "/".join(map(str, k)))
        del ml[k]

    ceb_text, ceb_joined = fit_versification("Ang Pulong sa Dios", parse_vpl(ebible_lines(CEB_URL, "cebocb_vpl.txt"), by_code), shape)
    ceb_gaps = sum(n for chs in shape.values() for n in chs.values()) - len(ceb_text)

    texts = {"ta": kjv, "ml": ml, "ceb": ceb_text}
    OUT.mkdir(parents=True, exist_ok=True)
    books_meta = []
    for i, (slug, code, en, ceb, abbr) in enumerate(BOOKS):
        counts = [shape[slug][c] for c in range(1, len(shape[slug]) + 1)]
        avail = {}
        for ver, t in texts.items():
            chapters = [[t.get((slug, c, v)) for v in range(1, n + 1)] for c, n in enumerate(counts, 1)]
            have = sum(1 for ch in chapters for x in ch if x is not None)
            avail[ver] = have
            d = OUT / ver
            d.mkdir(exist_ok=True)
            (d / f"{slug}.json").write_text(json.dumps({"b": slug, "c": chapters}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        books_meta.append({
            "slug": slug, "code": code, "t": "ot" if i < 39 else "nt",
            "names": {"en": en, "ceb": ceb},
            "abbr": sorted(set(abbr.split())),
            "verses": counts,
            "available": {ver: avail[ver] for ver in texts},
        })

    for ver, t in texts.items():
        idx = {b[0]: i for i, b in enumerate(BOOKS)}
        lines = [f"{idx[s]}\t{c}\t{v}\t{x}" for (s, c, v), x in sorted(t.items(), key=lambda kv: (idx[kv[0][0]], kv[0][1], kv[0][2])) if x]
        (OUT / ver / "search.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (OUT / "books.json").write_text(json.dumps(books_meta, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "versions.json").write_text(json.dumps(VERSIONS, ensure_ascii=False, indent=1), encoding="utf-8")

    votd = []
    for ref in VOTD.replace("\n", " ").split(";"):
        slug, c, v = ref.split()
        c, v = int(c), int(v)
        if slug not in shape or c not in shape[slug] or v > shape[slug][c]:
            sys.exit(f"bad VOTD ref {ref}")
        if [slug, c, v] in votd:
            sys.exit(f"duplicate VOTD ref {ref}")
        votd.append([slug, c, v])
    (OUT / "votd.json").write_text(json.dumps(votd, separators=(",", ":")), encoding="utf-8")

    print(f"KJV verses: {len(kjv)}")
    print(f"Ang Biblia verses: {len(ml)} (WordPress export {from_site}, licensed files {licensed}) of 31102")
    print(f"Ang Pulong sa Dios verses: {len(ceb_text) - ceb_joined} (+{ceb_joined} joined into ranges, {ceb_gaps} missing)")
    print(f"verse-of-the-day refs: {len(votd)}")


if __name__ == "__main__":
    main()
