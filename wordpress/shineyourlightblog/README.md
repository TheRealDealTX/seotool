# shineyourlightblog.com — ad placement (must-use plugin)

`syl-ad-placement.php` places the four AdSense units on shineyourlightblog.com and keeps them
at least two content blocks away from affiliate/shopping links, disclosures and embeds.

| Unit | Slot | Where |
| --- | --- | --- |
| Display (responsive) | 8096221599 | After the post intro (first clean gap after ~50 words) |
| In-article | 1960371044 | Every ~350 words further down, max 4, never under a heading |
| Multiplex | 8746967795 | After the post body |
| In-feed | 5524169668 | Home/archive/search grid, after posts 3 and 9 (full row) |

## Install

1. hPanel → shineyourlightblog.com → File Manager → `public_html/wp-content/mu-plugins/`
2. Upload `syl-ad-placement.php` (no activation needed — mu-plugins are always on).
3. WP Admin → LiteSpeed Cache → Toolbox → **Purge All**.

To turn ads off on one post, add the custom field `syl_no_ads` = `1`.
To remove everything, delete the file from `mu-plugins/`.
