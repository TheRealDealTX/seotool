# Switch-over notes (2026-10-14)

- `dns-before-switch-2026-10-14.json`: the txpublicadjusting.com DNS zone before any change. Restore with the Hostinger API `dns_records_update` (overwrite) if anything goes wrong. Email records (MX, SPF, DKIM, autodiscover) must never change.
- `old-wordpress/txpa-old-host.php`: installed on the old WordPress site (hosting account u401386392) as `wp-content/mu-plugins/txpa-old-host.php`. It makes the old site work at https://old.txpublicadjusting.com, always noindexed. It does nothing on any other host. Delete the file to undo.
- The old site is still the WordPress addon website `txpublicadjusting.com` on hosting account `u401386392` (order 64270646). The new site is the Agency website `cR6CoQmvm`.
- The domain can't be attached to the new site ("Domain is already taken") until the old hosting account releases it.

## 2026-10-14 switch: what happened

1. The old WordPress website (u401386392) was deleted with `hosting_websites_delete`, as the owner asked (rollback is Hostinger's daily backup).
2. `txpublicadjusting.com` was attached to the new Agency website `cR6CoQmvm`, and its SSL certificate is active.
3. **Deleting the old website also deleted the domain's DNS zone** in the Hostinger account. The API can't recreate a zone, so it has to be recreated in hPanel. Once the zone exists, restore these records:

| Type | Name | Value | TTL |
| --- | --- | --- | --- |
| ALIAS | @ | txpublicadjusting.com.cdn.hstgr.net | 300 |
| CNAME | www | www.txpublicadjusting.com.cdn.hstgr.net | 300 |
| MX | @ | mx1.hostinger.com (priority 5) | 14400 |
| MX | @ | mx2.hostinger.com (priority 10) | 14400 |
| TXT | @ | v=spf1 include:_spf.mail.hostinger.com ~all | 3600 |
| TXT | _dmarc | v=DMARC1; p=none | 3600 |
| CNAME | hostingermail-a._domainkey | hostingermail-a.dkim.mail.hostinger.com | 300 |
| CNAME | hostingermail-b._domainkey | hostingermail-b.dkim.mail.hostinger.com | 300 |
| CNAME | hostingermail-c._domainkey | hostingermail-c.dkim.mail.hostinger.com | 300 |
| CNAME | autodiscover | autodiscover.mail.hostinger.com | 300 |
| CNAME | autoconfig | autoconfig.mail.hostinger.com | 300 |

The old `ftp` A record (193.203.178.215) and the `old` ALIAS belonged to the deleted website, so don't restore them.
