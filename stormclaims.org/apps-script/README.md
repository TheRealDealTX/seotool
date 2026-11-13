# Apps Script: one-time update for the new upload form

The form on stormclaims.org talks to the "Rise Document Portal" Apps Script
through a `doPost` function. `Code.gs` here is your current script with that
one function added near the top (search for `function doPost`). Nothing else
changed: Drive filing, Trello matching, the log sheet and the email notice are
untouched, and the old upload page keeps working.

## Steps (about two minutes)

1. Open the script: https://script.google.com/d/1ebtNgqQ1XEMq7e0LISodNKtO7GEkTLb83rPE4UPzqzIIvctkY9P90nLT/edit
2. In `Code.gs`, paste the `doPost` function from this folder's `Code.gs`
   (or replace the whole file with it; it is identical apart from `doPost`).
3. Click **Deploy > Manage deployments**, click the pencil (Edit) on the
   existing deployment, set **Version** to **New version**, then **Deploy**.
   Editing the existing deployment keeps the same `/exec` URL. Do not use
   "New deployment", which would create a different URL.

That's it. stormclaims.org/upload checks for `doPost` on load: until it is
there, partners are sent to the old upload page, so nothing breaks in between.
