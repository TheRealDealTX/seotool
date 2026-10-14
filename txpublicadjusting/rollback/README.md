# Switch-over notes (2026-10-14)

- `dns-before-switch-2026-10-14.json`: the txpublicadjusting.com DNS zone before any change. Restore with the Hostinger API `dns_records_update` (overwrite) if anything goes wrong. Email records (MX, SPF, DKIM, autodiscover) must never change.
- `old-wordpress/txpa-old-host.php`: installed on the old WordPress site (hosting account u401386392) as `wp-content/mu-plugins/txpa-old-host.php`. It makes the old site work at https://old.txpublicadjusting.com, always noindexed. It does nothing on any other host. Delete the file to undo.
- The old site is still the WordPress addon website `txpublicadjusting.com` on hosting account `u401386392` (order 64270646). The new site is the Agency website `cR6CoQmvm`.
- The domain can't be attached to the new site ("Domain is already taken") until the old hosting account releases it.
