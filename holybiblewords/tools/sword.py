"""Minimal reader for SWORD zText/zCom Bible-commentary modules (KJV versification).

Layout (per testament): .bzs = block index (offset, csize, usize: 3x uint32),
.bzv = verse index (block uint32, offset uint32, size uint16 | uint32 for *4 drivers),
.bzz = zlib-compressed blocks. Index order: 0 module intro, 1 testament intro, then per
book: book intro, then per chapter: chapter intro followed by its verses."""
import struct
import zlib
from pathlib import Path


def read_module(path, books, size4=False):
    """books: list of (slug, [verse counts per chapter]) in canon order (39 OT + 27 NT).
    Returns {(slug, ch, v): (key, text)} where key identifies the stored entry, so
    verses linked to the same entry (a commented range) share a key."""
    path = Path(path)
    out = {}
    for t, part in (("ot", books[:39]), ("nt", books[39:])):
        bzs = (path / f"{t}.bzs").read_bytes()
        bzv = (path / f"{t}.bzv").read_bytes()
        bzz = (path / f"{t}.bzz").read_bytes()
        blocks = [struct.unpack_from("<III", bzs, i) for i in range(0, len(bzs), 12)]
        cache = {}
        step = 12 if size4 else 10

        def entry(i):
            if (i + 1) * step > len(bzv):
                return None
            if size4:
                b, off, size = struct.unpack_from("<III", bzv, i * step)
            else:
                b, off, size = struct.unpack_from("<IIH", bzv, i * step)
            if size == 0 or b >= len(blocks):
                return None
            if b not in cache:
                o, cs, _ = blocks[b]
                cache[b] = zlib.decompress(bzz[o:o + cs])
            return (t, b, off, size), cache[b][off:off + size].decode("utf-8", "replace")

        idx = 2
        for slug, counts in part:
            idx += 1                      # book intro
            for c, n in enumerate(counts, 1):
                idx += 1                  # chapter intro
                for v in range(1, n + 1):
                    e = entry(idx)
                    if e:
                        out[(slug, c, v)] = e
                    idx += 1
    return out
