Drop licensed Ang Biblia, 2011 text here as `*.txt` files in VPL format, one verse per line:

    GEN 1:1 Sa sinugdan gibuhat sa Dios ang kalangitan ug ang yuta.
    MAT 1:1 ...

Book codes are USFM (GEN, EXO, … MAT, MRK, LUK, JHN, … REV). Then run
`python3 tools/build_data.py`. These lines override the verses exported from the
old WordPress site, and fill in the books that were never published there.
