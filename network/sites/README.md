# Built sites

One folder per domain, created by the setup task:

```
network/sites/<domain>/
  persona.md        author persona, voice notes, about-page copy
  template.html     this site's page shell (unique per site: palette, type, layout)
  disavow.txt       Google disavow file for the spam referring domains
  redirects.csv     legacy URL -> new URL map for pages that still carry real links
  index.html        home page
  about/index.html  contact/index.html
  posts/<slug>/index.html   one folder per post, built from the calendar
  posts/<slug>.md           the post source (front matter: week, keyword, links)
```

Every site must differ in template, palette, author, footer text and publishing weekday. No shared analytics IDs.
