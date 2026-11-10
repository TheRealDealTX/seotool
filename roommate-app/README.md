# Rise Roommates — roommate.riseapartments.com

A social roommate-finder for renters: profiles, compatibility matching, friends, real-time-ish messaging,
a community feed, and preferred apartment properties (synced from riseapartments.com) so renters get matched
with people interested in the same place. Includes a full admin panel at `/admin`.

Plain PHP 8.1+ and MySQL with no framework, no Composer, and no build step. Upload the files and it runs.

## Features

| Area | What it does |
| --- | --- |
| Accounts | Sign up, log in, password reset by email, rate-limited logins, CSRF on every form, honeypot on sign-up |
| Profiles | Photo, bio, age, gender, job, city, budget, move-in date, lease length, lifestyle (cleanliness, sleep, smoking, pets, guests, WFH), roommate gender preference, interests, Instagram |
| Properties | ~5,000 listings imported from riseapartments.com (name, address, city, photo, link). Renters mark properties they're interested in (up to 25), can add missing ones (admin approval), and see everyone interested in each property |
| Matching | 0–100% compatibility score with reasons: shared properties (strongest signal), budget overlap, city, move-in timing, have/need a place, lifestyle, gender preference (dealbreaker), shared interests (`app/match.php`) |
| Discover | Search and filter renters by property, city, budget, gender, have/need a place, non-smoker, pets, sorted by best match / recently active / newest |
| Friends | Requests, accept/decline/cancel, unfriend, mutual friends, block/unblock |
| Messages | 1:1 chat with live polling, unread badges, "Seen" receipts, Enter-to-send; optional "friends only" mode |
| Feed | Posts with photos, optional property tag, likes, comments; tabs for Everyone / Friends / My properties |
| Notifications | Friend requests and accepts, messages, likes, comments, property approvals |
| Safety | Report users, posts, comments; block; safety tips, terms and privacy pages |
| Admin (`/admin`) | Dashboard and sign-up chart, members (search, suspend, verify, promote to admin, set password, delete, CSV export), properties (approve, feature, edit, photo, delete), reports queue (remove content, suspend), posts moderation, site settings (name, announcement banner, sign-ups on/off, messaging rules, property submission rules), listing sync, audit log |

## Layout

```
index.php            front controller + route table
.htaccess            HTTPS, blocks app/ and dotfiles, routes everything to index.php
app/bootstrap.php    config, PDO, migrations, session
app/lib.php          helpers (auth, CSRF, rendering, uploads, social graph, Rise sync)
app/match.php        compatibility scoring
app/schema.sql       database schema (idempotent; migrate() also adds new columns)
app/pages/*.php      request handlers
app/views/**.php     templates
app/cli/sync.php     daily listing sync (cron)
app/config.php       SERVER ONLY, not in git (DB credentials). See config.sample.php
assets/              app.css, app.js, icon.svg
uploads/             user images (PHP execution disabled)
setup.php            one-time installer (deleted from the server after install)
```

## Hosting (Hostinger Cloud Enterprise)

- Account `u401386392`, subdomain document root `/home/u401386392/domains/riseapartments.com/public_html/roommate`
- Database `u401386392_roommates` (user `u401386392_roommates`, host `127.0.0.1`). The password is only in `app/config.php` on the server
- Cron (daily 04:17): `/usr/bin/php …/roommate/app/cli/sync.php` re-syncs listings from riseapartments.com. Admins can also run it from **Admin → Sync listings**
- The previous WordPress install was moved (not deleted) to `/home/u401386392/domains/riseapartments.com/roommate_wordpress_backup_20261109_201857`. Its database was left untouched

## Making changes later (people or Claude)

1. Edit the code in this folder and test locally:
   ```sh
   cp app/config.sample.php app/config.php   # point at a local MySQL
   php -S 127.0.0.1:8080 index.php           # static files: use a small router or Apache
   ```
2. Deploy with the Hostinger API: `hosting_files_generate-upload-url` (username `u401386392`, domain
   `roommate.riseapartments.com`) returns a TUS URL plus `auth_key` and `rest_auth_key`. Upload each changed file to
   `{url}/{path}?override=true` (POST to create, then PATCH with the bytes). Paths are relative to the roommate root.
   The same credentials also let you read files (`GET {url minus /tus}/raw/{path}`) and delete them
   (`DELETE …/resources/{path}`), including `app/config.php`.
3. Schema changes: add them to `schema.sql` (new tables) or to the `$addCols` list in `migrate()` (new columns).
   `migrate()` runs from `setup.php`; to run it again, re-upload `setup.php`, POST `token=<setup_token from app/config.php>&action=install`,
   then POST `action=selfdestruct`.
4. Lost the admin password? Any admin can reset it under Admin → Members. If no admin can log in, re-upload `setup.php`
   and call `action=install` with `admin_email`, `admin_username` and `admin_password`: it promotes or resets that account.
