"""Resources published on stormclaims.org/resources/.

One dict per entry, newest first. `body` is HTML for the article. `file` is a
path under /resources/ (the PDF or document the entry is about), or None for a
write-up with no attachment. Run ../build.py after editing.
"""

RESOURCES = [
    {
        "slug": "obsolete-concrete-roof-tiles-florida",
        "title": "Obsolete Concrete Roof Tiles Formerly Produced in Florida",
        "category": "Tile roofing",
        "source": "Tile Roofing Industry Alliance, Technical Brief #2022-002",
        "date": "2022-10-05",
        "published": "2026-10-17",
        "file": "tri-alliance-obsolete-concrete-roof-tiles-florida-2022-002.pdf",
        "file_label": "1 page PDF · 113 KB",
        "summary": (
            "The industry's own list of discontinued Pioneer, Hanson, Entegra, Boral and Wallin "
            "concrete tiles that no longer interlock with any profile in production. The document "
            "to attach when a tile roof can't be repaired because matching tile no longer exists."
        ),
        "body": """
<p>When a hail or wind claim lands on a concrete tile roof, the first question the carrier asks is whether the damaged tiles can be replaced individually. On a lot of Florida roofs the honest answer is no: the tile was made by a manufacturer that has since closed or been absorbed, and nothing made today locks into it. This brief from the Tile Roofing Industry Alliance (TRI) is the manufacturers' own statement of which profiles those are.</p>

<h2>What the brief says</h2>
<p>TRI revised its earlier list (#2020-03) in October 2022 to focus on the tiles people actually ask about. It states plainly that the tiles below "are obsolete and do not interlock with the profiles currently offered by our existing member roof tile manufacturers." Identifying marks on the back of a tile may read Pioneer, Currier, Entegra, Wallin, Bender or Hanson.</p>
<ul class="tile-list">
  <li>Any tile with Wallin/Pioneer Cottage Shingle</li>
  <li>Any tile with Pioneer flat</li>
  <li>Any tile with Hanson/Pioneer/Bender Palema</li>
  <li>Any tile with Hanson/Pioneer/Bender Nordic flat</li>
  <li>Any flat or "S" tile labeled "Pioneer"</li>
  <li>Any tile with Hanson flat, including Horizon, Slate, Southern Shake, Victorian Slate and Old World</li>
  <li>Any tile with Hanson/Pioneer Hacienda</li>
  <li>Any flat or "S" tile labeled "Lifetile"</li>
  <li>Any tile with Hanson Regal</li>
  <li>Any tile with Entegra Valencia</li>
  <li>Any tile with Entegra Skandia flat</li>
  <li>Any tile with Entegra Estate manufactured in Indiantown or Pompano Beach</li>
  <li>Any flat tile labeled Boral Lifetile "BUSA"</li>
  <li>Any tile with Entegra Europa (WAVE) tile</li>
  <li>Any tile with Entegra Bella S Tile</li>
  <li>Any tile with Boral Spanish S Nuevo</li>
</ul>
<p>The brief also notes that when a full replacement is required, member manufacturers will try to offer similar colors, but "an exact color replacement is highly unlikely."</p>

<h2>How to use it on a claim</h2>
<ol>
  <li><b>Photograph the back of a tile.</b> Pull one damaged tile and shoot the stamp or embossed brand on the underside. That mark is what ties the roof to this list.</li>
  <li><b>Match it to the list.</b> If the brand and profile appear above, note the exact line item from the brief in your estimate narrative.</li>
  <li><b>Attach the brief.</b> Upload it with your estimate under "Carrier letters &amp; estimates" or "Your estimate &amp; measurements" so it's in the claim file from day one.</li>
  <li><b>Write the scope accordingly.</b> If no interlocking replacement exists, a repair that leaves mismatched, non-interlocking tile in the field isn't a repair. Scope what the roof actually needs and let the document do the explaining.</li>
</ol>
<p>Policy language on matching and "like kind and quality" varies by carrier and state, so this brief supports the argument; it doesn't make it by itself. Send us the claim and we'll handle that part.</p>

<h2>Source</h2>
<p>Tile Roofing Industry Alliance, 2150 N 107th Street, Suite 205, Seattle, WA 98133. <a href="https://tileroofing.org" target="_blank" rel="noopener">tileroofing.org</a>. The alliance also publishes installation manuals and the earlier bulletin #2020-03 covering older tiles.</p>
""",
    },
]
