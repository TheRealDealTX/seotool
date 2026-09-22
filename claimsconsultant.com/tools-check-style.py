"""Count the stylistic tics that make copy read as machine-written."""
import glob
import html
import re
from collections import Counter

ROOT = "/home/user/seotool/claimsconsultant.com"

def text_of(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
    body = re.search(r"<main.*?</main>", s, flags=re.S)
    s = body.group(0) if body else s
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()

pages = {}
for f in sorted(glob.glob(ROOT + "/**/*.html", recursive=True)):
    if "/assets/" in f:
        continue
    pages[f.replace(ROOT, "")] = text_of(f)

corpus = " ".join(pages.values())
words = re.findall(r"[A-Za-z']+", corpus)
n = len(words)
print("pages: %d   words: %s\n" % (len(pages), format(n, ",")))

def per1k(c):
    return c / n * 1000

PATTERNS = [
    ("em dash", r"—"),
    ("'It is not X, it is Y'", r"\b(?:is|was|are|were) not [^.;—]{3,60}?\.? It is\b|\bnot (?:whether|because|that)\b[^.]{0,80}?\b(?:it is|but)\b"),
    ("sentence-initial 'Which is'", r"(?:^|[.;] )Which is\b"),
    ("'That is the …'", r"\bThat is (?:the|what|why|exactly)\b"),
    ("'which is (why|the|exactly)'", r"\bwhich is (?:why|the point|exactly|precisely)\b"),
    ("'not because … but'", r"\bnot because\b[^.]{0,80}\bbut\b"),
    ("'worth <x>ing'", r"\bworth \w+ing\b"),
    ("'and correctly so' / 'rightly so'", r"\b(?:and correctly so|rightly so)\b"),
    ("'the whole (point|problem|argument)'", r"\bthe whole (?:point|problem|argument|thing)\b"),
    ("'in practice'", r"\bin practice\b"),
    ("'genuinely'", r"\bgenuinely\b"),
    ("'actually'", r"\bactually\b"),
    ("'frequently'", r"\bfrequently\b"),
    ("'routinely'", r"\broutinely\b"),
    ("'deliberately'", r"\bdeliberately\b"),
    ("'precisely'", r"\bprecisely\b"),
    ("'simply'", r"\bsimply\b"),
    ("'entirely'", r"\bentirely\b"),
    ("'materially'", r"\bmaterially\b"),
    ("'considerably'", r"\bconsiderably\b"),
    ("'unusually'", r"\bunusually\b"),
    ("'nearly always/almost always'", r"\b(?:nearly|almost) always\b"),
    ("'is not a … it is a'", r"\bis not an? [^.]{2,40}\.? It is an?\b"),
    ("'rather than' ", r"\brather than\b"),
    ("colon-dramatic ': the'", r": the \w+"),
]

print("%-38s %6s %8s" % ("tic", "count", "per 1k"))
print("-" * 54)
for label, pat in PATTERNS:
    c = len(re.findall(pat, corpus, flags=re.I if "'" in label else 0))
    if c:
        print("%-38s %6d %8.2f" % (label, c, per1k(c)))

# sentence length distribution
sents = [s.strip() for s in re.split(r"(?<=[.!?]) +", corpus) if len(s.strip()) > 1]
lens = [len(re.findall(r"[A-Za-z']+", s)) for s in sents]
lens = [l for l in lens if l > 0]
avg = sum(lens) / len(lens)
var = (sum((l - avg) ** 2 for l in lens) / len(lens)) ** 0.5
short = sum(1 for l in lens if l <= 8)
long_ = sum(1 for l in lens if l >= 35)
print("\nsentences: %s   mean %.1f words   sd %.1f" % (format(len(lens), ","), avg, var))
print("  <=8 words: %.1f%%    >=35 words: %.1f%%" % (short / len(lens) * 100, long_ / len(lens) * 100))

# repeated long phrases across different pages (boilerplate / self-plagiarism)
grams = Counter()
where = {}
for path, t in pages.items():
    w = re.findall(r"[A-Za-z']+", t.lower())
    seen = set()
    for i in range(len(w) - 7):
        g = " ".join(w[i:i + 8])
        if g in seen:
            continue
        seen.add(g)
        grams[g] += 1
        where.setdefault(g, set()).add(path)

print("\nphrases repeated across 3+ different pages (excluding site chrome):")
shown = 0
for g, c in grams.most_common(400):
    if c < 3:
        break
    if len(where[g]) < 3:
        continue
    if shown >= 14:
        break
    print("  %2d pages  %s" % (len(where[g]), g))
    shown += 1
