"""Upload the two images and create the article as a DRAFT on riseapartments.com.

Needs WP_USER and WP_APP_PASSWORD (a WordPress application password) in the
environment. Never publishes: status is always "draft".
"""
import base64, json, os, re, sys, urllib.request

SITE = "https://riseapartments.com/wp-json/wp/v2"
HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "How to Tell Whether an Apartment Cooling Problem Needs Maintenance or Professional Repair"
EXCERPT = ("Is your Texas apartment AC a quick filter fix or a job for a pro? Learn which cooling "
           "problems renters can check, which need an HVAC technician, and how to report them.")
CATEGORY_RENT_TIPS = 1

auth = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()


def call(path, data, headers):
    req = urllib.request.Request(f"{SITE}/{path}", data=data, method="POST",
                                 headers={"Authorization": f"Basic {auth}", **headers})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


# Alt text lives in the post's <img> tags; this site's REST API refuses media edits.
def upload(filename, slug, alt):
    with open(os.path.join(HERE, "images", filename), "rb") as f:
        media = call("media", f.read(), {"Content-Type": "image/png",
                                         "Content-Disposition": f'attachment; filename="{slug}.png"'})
    return media


html = open(os.path.join(HERE, "post-body.html")).read()
images = {
    "images/image1.png": ("image1.png", "apartment-ac-not-cooling-texas", "Woman sitting on a sofa in a warm apartment living room"),
    "images/image2.png": ("image2.png", "hvac-technician-apartment-ac-repair", "Technician drilling into an air conditioner casing"),
}
featured = None
# EXISTING_MEDIA="image1.png=123,..." reuses images already uploaded.
existing = dict(kv.split("=") for kv in os.environ.get("EXISTING_MEDIA", "").split(",") if kv)
for src, (fn, slug, alt) in images.items():
    if fn in existing:
        m = json.load(urllib.request.urlopen(f"{SITE}/media/{existing[fn]}"))
    else:
        m = upload(fn, slug, alt)
    featured = featured or m["id"]
    html = html.replace(f'src="{src}"', f'class="wp-image-{m["id"]}" src="{m["source_url"]}"')

post = call("posts", json.dumps({
    "title": TITLE, "content": html, "excerpt": EXCERPT, "status": "draft",
    "slug": "apartment-ac-maintenance-or-professional-repair",
    "categories": [CATEGORY_RENT_TIPS], "featured_media": featured,
}).encode(), {"Content-Type": "application/json"})
print(post["id"], post["status"], f"https://riseapartments.com/wp-admin/post.php?post={post['id']}&action=edit")
