# rooftarp.com WordPress backup — 2026-09-21

Content archive of the live WordPress site, taken before the static rebuild was
due to be deployed.

## What's here

| File | What it is |
| --- | --- |
| `pages.tar.gz` | Rendered HTML of all 176 live URLs (3.4 MB compressed, ~16 MB raw) |
| `archived-urls.json` | The URL list that was crawled |
| `post-sitemap.xml`, `page-sitemap.xml`, `category-sitemap.xml` | The live sitemaps as they stood |
| `htaccess.txt` | The live `.htaccess` (LiteSpeed cache + WordPress rewrite blocks) |

Extract with:

```sh
tar xzf pages.tar.gz
```

Filenames are the URL path with `/` replaced by `__`, so
`https://rooftarp.com/service-areas/roof-tarp-houston/` is saved as
`pages/service-areas__roof-tarp-houston.html`.

## What this covers

Every page's rendered content, including all 141 city pages the rebuild
removes. If any of that copy is ever wanted back, it is here.

## What this does NOT cover

This is a **content archive, not a restorable site backup.** It is not
sufficient to rebuild the WordPress install.

Missing:

- **The MySQL database** (`u401386392_BlNOR`, 93 MB). Holds posts, pages,
  Rank Math SEO settings, menus, users and plugin configuration. The Hostinger
  API exposed to this session has no database export endpoint, so this could
  not be taken programmatically.
- **`wp-content/`** — themes, plugins, and the uploads media library. The
  file-read endpoint returns one text file at a time and refuses binaries, so
  bulk download was not possible.
- **Elementor page data.** The page builder stores layouts as serialised JSON
  in the database, not in the rendered HTML. The archive preserves what the
  pages looked like, not how they were assembled.

## Taking a full backup

Before replacing the WordPress install, take a real backup from hPanel — that
is the only route that captures files and database together:

1. **hPanel → Files → Backups** — generate a full account backup, or
2. **hPanel → Databases → phpMyAdmin** → select `u401386392_BlNOR` → Export →
   Go, for the database alone, and **hPanel → Files → File Manager** →
   compress `/domains/rooftarp.com/public_html` → download, for the files.

## Important: shared hosting account

rooftarp.com is one of **47 websites** on hosting account `u401386392`
(order `64270646`, `cloud_enterprise` plan). Its document root is
`/home/u401386392/domains/rooftarp.com/public_html`.

Any deployment or backup operation must be scoped to that directory
specifically. The other 46 sites on the account include
`txpublicadjusting.com`, `houstonpublicadjusting.com`, `riseapartments.com`,
`namesfrog.com` and `360carseat.com`, and an account-level operation would
affect all of them.
