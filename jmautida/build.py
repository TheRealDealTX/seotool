#!/usr/bin/env python3
"""Generate the static pages of jmautida.com into ./public.

Hand-written assets (CSS, tool scripts, PHP endpoints) live in public/ already;
this script writes the HTML pages, the tool catalog, icons, sitemap and .htaccess.
Standard library only:  python3 build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "public"
SITE = "https://jmautida.com"
NAME = "John Raymond Autida"
BRAND = "JM Autida"
EMAIL = "autida@jmautida.com"
VERSION = "5"
SOCIAL = ["https://www.instagram.com/jhnrymndatd/", "https://www.facebook.com/johnraymond.autida/"]
COMPANIES = [
    ("Rise Marketing LLC", "Web developer"),
    ("TX Rising LLC", "Web developer"),
    ("J & J Web Marketing LLC", "Co-founder"),
]

e = html.escape

# 24px stroke icons (Lucide-style geometry).
ICONS = {
    "image": '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "star": '<rect x="3" y="3" width="18" height="18" rx="5"/><path d="m12 7 1.6 3.1 3.4.5-2.5 2.4.6 3.4L12 14.8l-3.1 1.6.6-3.4L7 10.6l3.4-.5z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "braces": '<path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5c0 1.1.9 2 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5c0-1.1.9-2 2-2a2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "type": '<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "contrast": '<circle cx="12" cy="12" r="10"/><path d="M12 18a6 6 0 0 0 0-12v12z"/>',
    "arrow": '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2m-7.07-14.07 1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "gift": '<path d="M20 12v10H4V12"/><path d="M2 7h20v5H2z"/><path d="M12 22V7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "play": '<path d="M6 3 20 12 6 21Z"/>',
    "briefcase": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "trash": '<path d="M3 6h18M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "plus": '<path d="M5 12h14M12 5v14"/>',
    "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98M15.41 6.51l-6.82 3.98"/>',
    "maximize": '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "pipette": '<path d="m2 22 1-1h3l9-9"/><path d="M3 21v-3l9-9"/><path d="m15 6 3.4-3.4a2.1 2.1 0 1 1 3 3L18 9l.4.4a2.1 2.1 0 1 1-3 3l-3.8-3.8a2.1 2.1 0 1 1 3-3l.4.4Z"/>',
    "swap": '<path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/>',
    "wand": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"/><path d="m14 7 3 3"/><path d="M5 6v4M19 14v4M10 2v2M7 8H3M21 16h-4M11 3H9"/>',
    "tree": '<path d="M21 12h-8M21 6H8M21 18h-8M3 6v4c0 1.1.9 2 2 2h3M3 10v6c0 1.1.9 2 2 2h3"/>',
    "columns": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M12 3v18"/>',
    "rows": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 12h18"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "monitor": '<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2"/><path d="M12 18h.01"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "hash": '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# Tool catalog. Order here is the order on the toolbox page.
# ---------------------------------------------------------------------------
TOOLS = [
    dict(
        slug="image-converter", key="image", icon="image", hue="orange", cat="Design & Media",
        name="Image converter", h1="Image converter: WebP, AVIF, JPG & PNG",
        short="Convert and compress images to WebP, AVIF, JPG or PNG in bulk. Resize, hit a target file size and download everything as a ZIP.",
        tags=["WebP · AVIF", "Batch", "Compress"], badge="new",
        title="Free Image Converter — Convert to WebP, AVIF, JPG & PNG | JM Autida",
        desc="Convert JPG, PNG, GIF, SVG and HEIC images to WebP, AVIF, JPG or PNG in bulk. Compress, resize and download as ZIP. Runs in your browser — no uploads.",
        keywords="convert to webp webp converter avif jpg png compress image resize bulk batch",
        local=True, scripts=["vendor/jszip.min.js"],
        intro="Smaller images make faster websites. Drop in a batch of JPG, PNG, GIF, SVG or HEIC files and convert them to modern WebP or AVIF, or to classic JPG and PNG, with full control over quality, size and dimensions.",
        steps=[
            "Drag images onto the drop zone, click to browse, or paste a screenshot with Ctrl/⌘ + V. Add up to 100 files at once.",
            "Choose the output format and quality. WebP at 75–85% is a great default for websites; use AVIF for the smallest files where supported.",
            "Optionally resize to a maximum width or height, or set a target file size and the converter will find the best quality that fits.",
            "Compare before and after with the slider, then download files one by one or all together as a ZIP.",
        ],
        features=[
            "Converts JPG, PNG, GIF, BMP, WebP, AVIF, SVG, ICO and (in Safari) HEIC",
            "WebP, AVIF, JPG and PNG output with a quality slider",
            "Target file size mode for upload limits such as 100 KB or 500 KB",
            "Resize by max width, max height or percentage, keeping aspect ratio",
            "Before/after comparison slider and savings for every file",
            "Strips EXIF metadata, including GPS location, automatically",
            "Download individually or as a single ZIP — nothing is uploaded",
        ],
        faq=[
            ("Are my images uploaded to a server?", "No. Every conversion happens inside your browser using the canvas API. Your files never leave your device, which also makes the converter fast and private."),
            ("What quality should I use for WebP?", "For photos on websites, 75–85% usually looks identical to the original while saving 25–35% compared to JPG. Graphics with flat colors and text often compress better as lossless PNG or high-quality WebP."),
            ("Why is AVIF not available in my browser?", "AVIF encoding depends on your browser. Chrome and Edge can create AVIF files; other browsers can still convert to WebP, JPG and PNG. The option appears automatically when your browser supports it."),
            ("Does converting remove photo metadata?", "Yes. Re-encoding through the canvas drops EXIF data such as camera details and GPS location. Orientation is applied to the pixels first so photos stay upright."),
            ("Can I convert an animated GIF?", "The converter exports the first frame of an animated GIF as a still image. For animations, use a dedicated video or animated WebP encoder."),
        ],
        related=["favicon-checker", "meta-tags-checker", "html-playground"],
    ),
    dict(
        slug="meta-tags-checker", key="meta", icon="search", hue="green", cat="SEO & Marketing",
        name="SEO meta tags checker", h1="SEO meta tags checker & generator",
        short="Audit any page: title, description, canonical, robots, Open Graph, headings, schema and more — with a score, Google and social previews.",
        tags=["SEO audit", "SERP preview", "Generator"], badge="popular",
        title="SEO Meta Tags Checker — Audit, Score & Preview | JM Autida",
        desc="Check any page's title, meta description, canonical, robots, Open Graph, Twitter cards, headings, images and schema. Get an SEO score, SERP and social previews.",
        keywords="meta tags checker seo audit serp preview open graph twitter card canonical robots schema headings h1 generator",
        local=False, scripts=[],
        intro="See a page the way search engines and social networks do. The checker fetches the live HTML, scores the on-page essentials, previews the Google result and social cards, and tells you exactly what to fix. Switch to the generator to write perfect tags from scratch.",
        steps=[
            "Enter the full URL of a public page and choose Analyze.",
            "Review the score and the grouped checks — search basics, social sharing, content structure and technical signals.",
            "Use the Google and social previews to fine-tune titles and descriptions that earn the click.",
            "Open the Generator tab to write new tags with live previews, then copy the ready-to-paste HTML.",
        ],
        features=[
            "SEO score with prioritized pass, warning and fail checks",
            "Google desktop and mobile previews with pixel-based truncation",
            "Facebook, LinkedIn and X (Twitter) card previews",
            "Headings outline, H1 count, image alt coverage and word count",
            "Canonical, robots meta, X-Robots-Tag, robots.txt and hreflang checks",
            "JSON-LD structured data detection and Open Graph completeness",
            "Meta tag generator with copy-ready HTML and a downloadable report",
        ],
        faq=[
            ("Does this check JavaScript-generated metadata?", "No. The checker reads the server-delivered HTML, the same first view most crawlers and social networks get. Tags injected only after JavaScript runs will not appear — which is worth fixing for reliable sharing previews."),
            ("How long should a title and meta description be?", "Google truncates by pixel width rather than characters. Aim for titles under roughly 580 pixels (about 50–60 characters) and descriptions under roughly 920 pixels (about 140–160 characters). The previews show where your text would be cut."),
            ("Does a high score guarantee rankings?", "No. The score covers on-page metadata and structure that you control. Rankings also depend on content quality, links, intent and many other signals. Use the report as a technical checklist."),
            ("Why might a page fail to load?", "Some sites block automated requests, require login, or respond slowly. The checker only fetches public pages on standard ports and limits page size to keep checks fast and safe."),
        ],
        related=["favicon-checker", "word-counter", "url-encoder-decoder"],
    ),
    dict(
        slug="time-calculator", key="time", icon="clock", hue="violet", cat="Productivity",
        name="Work hours & logout calculator", h1="Work hours & logout time calculator",
        short="Know exactly when to log out. Decimal hours, unpaid breaks, overnight shifts, client time zones, a live countdown and a weekly timesheet with overtime.",
        tags=["Decimal hours", "Timesheet", "Overtime"], badge="popular",
        title="Logout Time & Work Hours Calculator with Breaks | JM Autida",
        desc="Calculate logout time from decimal hours with unpaid breaks and overnight shifts. See it in your client's time zone, track a live countdown and total a weekly timesheet.",
        keywords="time calculator logout time decimal hours breaks overnight shift timesheet overtime pay hours worked clock out",
        local=True, scripts=["js/time-math.js"],
        intro="Built for remote workers, night shifts and anyone paid by the hour. Enter your start time and target hours to get your exact logout time, or work backwards from logout to paid hours. Then total a whole week, overtime and pay in seconds.",
        steps=[
            "Enter your start time and target paid hours. Decimal hours work too — 9.3 hours is 9 hours and 18 minutes.",
            "Add each unpaid break in minutes. Your logout time moves to keep paid hours exact.",
            "Pick your client's time zone to see the same shift on their clock, and keep the live countdown open while you work.",
            "Switch to Weekly timesheet to total in/out times for every day, with overtime and pay based on your hourly rate.",
        ],
        features=[
            "Two-way calculation: target hours → logout, or logout → paid hours",
            "Unpaid breaks, overnight shifts and multi-day shifts",
            "Shows your shift in a second time zone (great for PH ⇄ US work)",
            "Live countdown to logout with an optional browser notification",
            "Weekly timesheet with overtime threshold, multiplier and pay",
            "Decimal ⇄ hours-and-minutes converter and quick reference table",
            "Remembers your usual settings on this device; export to CSV",
        ],
        faq=[
            ("If I start at 7:30 PM and need 9.3 hours, when should I log out?", "Without a break, log out at 4:48 AM the next day. A 30-minute unpaid break moves logout to 5:18 AM."),
            ("What is 0.3 hours in minutes?", "Multiply decimal hours by 60: 0.3 × 60 = 18 minutes. Likewise 0.25 hours is 15 minutes, 0.5 hours is 30 minutes and 0.75 hours is 45 minutes."),
            ("How does the time zone view work?", "Your start time is treated as today in your device's time zone. The calculator converts the start and logout moments into the zone you choose, including daylight-saving rules for today's date."),
            ("How is overtime calculated in the timesheet?", "Hours above the weekly threshold you set (40 by default) count as overtime and are paid at your multiplier (1.5× by default). Check your employer's or local rules, since some regions also use daily overtime."),
            ("Is my timesheet saved?", "Your entries are stored only in this browser's local storage so they are there next time. Use Clear to remove them, or export a CSV to keep a copy."),
        ],
        related=["word-counter", "json-formatter", "markdown-to-word"],
    ),
    dict(
        slug="html-playground", key="html", icon="code", hue="green", cat="Developer",
        name="HTML, CSS & JS playground", h1="HTML, CSS & JavaScript playground",
        short="Separate HTML, CSS and JavaScript editors with live preview, a console, device sizes, starter templates, autosave and shareable links.",
        tags=["Live preview", "Console", "Share"], badge="",
        title="Free HTML, CSS & JavaScript Playground — Live Editor | JM Autida",
        desc="Write HTML, CSS and JavaScript with instant live preview, console output, device sizes, templates and shareable links. A fast, free online code playground.",
        keywords="html playground online html editor css js live preview codepen alternative sandbox console",
        local=True, scripts=[],
        intro="Prototype a component, debug a snippet or teach a concept without setting up a project. Code in separate HTML, CSS and JavaScript tabs and watch the sandboxed preview update as you type, with console output right beside it.",
        steps=[
            "Pick a starter template or start blank. Write markup, styles and scripts in their own tabs.",
            "The preview refreshes automatically. Turn off Auto-run and press Ctrl/⌘ + Enter to run manually.",
            "Check console.log output and errors in the console panel, and switch device widths to test responsive layouts.",
            "Share a link that contains your code, or download a single self-contained HTML file.",
        ],
        features=[
            "Separate HTML, CSS and JS editors with tab indentation",
            "Auto-run live preview in an isolated sandbox",
            "Console panel capturing logs, warnings and runtime errors",
            "Responsive, laptop, tablet and mobile preview widths",
            "Starter templates: landing hero, card grid, flexbox, animation",
            "Autosaves locally; share links encode your code in the URL",
            "Download everything as one HTML file",
        ],
        faq=[
            ("Is my code uploaded?", "No. Code stays in your browser and autosaves to local storage on this device. Share links compress your code into the link itself — nothing is stored on a server."),
            ("Can I use external libraries?", "Yes. Add script or link tags pointing to a CDN in the HTML tab. The preview can load external assets referenced by your code."),
            ("Can I run PHP or server code?", "No. The playground runs front-end code in the browser. PHP, Node.js and other server languages need a server."),
            ("Why can't my script access cookies or the parent page?", "The preview runs in a sandboxed frame with a unique origin. It can run JavaScript and show alerts but cannot read this site's storage or navigate the page — a safety feature."),
        ],
        related=["json-formatter", "contrast-checker", "markdown-to-word"],
    ),
    dict(
        slug="json-formatter", key="json", icon="braces", hue="violet", cat="Developer",
        name="JSON formatter & viewer", h1="JSON formatter, validator & viewer",
        short="Format, validate and minify JSON with exact error locations, a collapsible tree, sorting, auto-repair and CSV, YAML or TypeScript conversion.",
        tags=["Tree view", "Repair", "Convert"], badge="",
        title="JSON Formatter & Validator — Tree View, Repair, Convert | JM Autida",
        desc="Format, validate and minify JSON. See exact error lines, browse a collapsible tree, sort keys, repair common mistakes and convert to CSV, YAML or TypeScript.",
        keywords="json formatter json validator json viewer tree beautify minify json to csv json to yaml json to typescript repair",
        local=True, scripts=[],
        intro="Make messy API responses readable, find the exact character that breaks your JSON, and convert data into the format you need next — all without pasting sensitive payloads into a server.",
        steps=[
            "Paste JSON, drop a .json file onto the editor, or load the sample.",
            "Choose Format or Minify. Errors show the exact line and column with a pointer to the problem.",
            "Use Repair to fix comments, trailing commas, single quotes and unquoted keys automatically.",
            "Explore the Tree view, copy any value's path, or convert the data to CSV, YAML or TypeScript.",
        ],
        features=[
            "Format with 2 spaces, 4 spaces or tabs; minify in one click",
            "Line and column error pointer for invalid JSON",
            "One-click repair for comments, trailing commas and quotes",
            "Collapsible tree view with JSON paths you can copy",
            "Sort keys alphabetically at every depth",
            "Convert to CSV (flattened), YAML or TypeScript interfaces",
            "File import, drag and drop, copy and download",
        ],
        faq=[
            ("Why are comments and trailing commas rejected?", "Standard JSON does not allow comments, trailing commas, single-quoted strings or unquoted keys. Use Repair to convert these JavaScript-style habits into valid JSON."),
            ("Will very large numbers stay exact?", "JavaScript numbers have finite precision, so integers beyond 2^53 may change. Keep large IDs as quoted strings when exact digits matter."),
            ("How does JSON to CSV handle nested objects?", "Nested objects are flattened into dotted column names such as address.city. Arrays of primitive values are joined with semicolons; the input should be an array of objects."),
            ("Is my JSON sent anywhere?", "No. Parsing, formatting and conversion run entirely in your browser."),
        ],
        related=["html-playground", "url-encoder-decoder", "meta-tags-checker"],
    ),
    dict(
        slug="url-encoder-decoder", key="encode", icon="link", hue="green", cat="SEO & Marketing",
        name="URL toolkit & UTM builder", h1="URL encoder, decoder & UTM builder",
        short="Encode or decode URLs, inspect and edit query parameters, build UTM campaign links with presets, and convert Base64.",
        tags=["Encode", "UTM links", "Base64"], badge="",
        title="URL Encoder/Decoder, Query Parser & UTM Builder | JM Autida",
        desc="Encode and decode URLs or form data, parse and edit query strings, build UTM campaign links with presets, and convert text to and from Base64. Free and private.",
        keywords="url encoder url decoder percent encoding query string parser utm builder campaign url builder base64 encode decode",
        local=True, scripts=[],
        intro="Everything you do with links in one place: encode values safely, break a URL into its parts, edit query parameters, and build consistent UTM-tagged campaign links your analytics team will thank you for.",
        steps=[
            "Encode/Decode converts as you type. Choose component, full URL or form encoding, and process line by line if needed.",
            "URL parser splits any link into protocol, host, path and an editable table of query parameters.",
            "UTM builder creates tracked links from your landing page, source, medium and campaign — or start from a preset.",
            "Base64 converts text (UTF-8 safe) and files to Base64 or data URIs, with a URL-safe option.",
        ],
        features=[
            "encodeURIComponent, encodeURI and form (+) encoding modes",
            "Live two-way conversion with line-by-line batch mode",
            "Query string parser with editable parameters",
            "UTM builder with Google Ads, Meta, email and Google Business Profile presets",
            "Recent campaign links history with CSV export",
            "Base64 and Base64URL encode/decode, file to data URI",
        ],
        faq=[
            ("Should I encode an entire URL?", "Use component encoding for individual values like a query parameter. Encoding a whole URL with component mode also encodes the :// and / separators. Full URL mode keeps them intact."),
            ("Why do spaces sometimes become + instead of %20?", "HTML forms use application/x-www-form-urlencoded, where spaces become +. Choose Form mode to match that behavior; component mode uses %20."),
            ("Which UTM parameters are required?", "utm_source, utm_medium and utm_campaign are the core three. utm_term and utm_content are optional for keywords and ad variations. Keep naming consistent and lowercase for clean reports."),
            ("Is Base64 encryption?", "No. Base64 is an encoding that anyone can reverse. Don't use it to protect secrets."),
        ],
        related=["meta-tags-checker", "json-formatter", "word-counter"],
    ),
    dict(
        slug="word-counter", key="words", icon="type", hue="orange", cat="Writing",
        name="Word counter & text analyzer", h1="Word counter & SEO text analyzer",
        short="Words, characters, sentences, readability, keyword density, platform limits and quick case conversion for any draft.",
        tags=["Readability", "Keyword density", "Limits"], badge="",
        title="Word Counter — Readability, Keyword Density & Limits | JM Autida",
        desc="Count words, characters and sentences. Check readability scores, keyword density and limits for meta titles, descriptions and social posts. Convert text case instantly.",
        keywords="word counter character counter readability flesch keyword density meta description length case converter",
        local=True, scripts=[],
        intro="More than a counter: see how readable your writing is, which keywords dominate, and whether your copy fits the title tag, meta description or social post it's destined for.",
        steps=[
            "Type or paste your text. Everything updates instantly as you write.",
            "Check the readability score and grade level, and review long sentences that could be split.",
            "Use keyword density to spot overused words and confirm your focus phrase appears naturally.",
            "Pick a platform limit to track, or clean up and convert text case with one click.",
        ],
        features=[
            "Words, characters (with and without spaces), sentences, paragraphs",
            "Reading and speaking time with adjustable speed",
            "Flesch reading ease and grade level",
            "Keyword density for single words and 2–3 word phrases",
            "Limits for SEO titles, meta descriptions, X, Instagram, Google Business posts",
            "UPPER, lower, Title and Sentence case; whitespace cleanup",
            "Find and replace, autosave and download",
        ],
        faq=[
            ("Do character counts include spaces?", "The tool shows both: characters including spaces and line breaks, and characters without spaces. Counts use Unicode code points, so emoji count as one character."),
            ("What is a good Flesch reading ease score?", "60–70 is plain English that most adults read easily. Web copy often aims for 60 or higher; technical or academic writing scores lower."),
            ("What keyword density should I aim for?", "There is no magic number. Use your main phrase naturally in the title, first paragraph and headings. If a single word is far above 3–4% of the text, it may read as repetitive."),
            ("Is my text saved or uploaded?", "Your draft autosaves to local storage on this device only, so a refresh won't lose it. Nothing is sent to a server. Use Clear to remove it."),
        ],
        related=["markdown-to-word", "meta-tags-checker", "time-calculator"],
    ),
    dict(
        slug="markdown-to-word", key="markdown", icon="file", hue="violet", cat="Writing",
        name="Markdown to Word", h1="Markdown to Word converter",
        short="Write or import Markdown with a formatting toolbar and live preview, then export a real Word document, HTML or rich text.",
        tags=["DOCX", "Live preview", "Rich copy"], badge="",
        title="Markdown to Word Converter — Free DOCX Export | JM Autida",
        desc="Convert Markdown to an editable Word document. Format with a toolbar, preview live, set fonts and page size, then export DOCX, HTML or copy rich text. No upload.",
        keywords="markdown to word markdown to docx md to docx converter markdown editor export html rich text google docs",
        local=True, scripts=["vendor/marked.js", "vendor/docx.js"],
        intro="Draft in Markdown, deliver in Word. Write with a formatting toolbar or import a .md file, preview the document as you type, and export a genuine .docx with your choice of font, page size and page numbers.",
        steps=[
            "Write Markdown, use the toolbar for headings, lists, links and tables, or drop a .md file onto the editor.",
            "Watch the document preview update as you type, including tables, quotes, code and task lists.",
            "Set the file name, font, size, page size and page numbers in Document settings.",
            "Export a .docx, a standalone HTML file, or copy rich text to paste into Google Docs or email.",
        ],
        features=[
            "Formatting toolbar and keyboard shortcuts (Ctrl/⌘ + B, I, K)",
            "Live preview with GitHub-flavored Markdown, tables and task lists",
            "Real .docx export with fonts, sizes, Letter/A4 and page numbers",
            "Standalone HTML export and rich-text copy for Google Docs",
            "Import or drag-and-drop .md and .txt files",
            "Autosaves your draft locally with word count and reading time",
        ],
        faq=[
            ("Does this create a real Word document?", "Yes. Export produces a genuine .docx file with Word document XML — headings map to Word heading styles so the navigation pane and table of contents work."),
            ("Can I paste the result into Google Docs?", "Yes. Use Copy rich text, then paste into Google Docs, Gmail or Outlook to keep headings, lists, links and tables."),
            ("Are images supported?", "Images are represented by their alt text in the document. Embedding remote images would require downloading them, which this private, in-browser tool avoids."),
            ("Are documents sent to a server?", "No. Conversion runs in your browser. Drafts autosave only to this device's local storage."),
        ],
        related=["word-counter", "html-playground", "json-formatter"],
    ),
    dict(
        slug="favicon-checker", key="favicon", icon="star", hue="orange", cat="SEO & Marketing",
        name="Favicon checker & generator", h1="Favicon checker & generator",
        short="Check a site's favicons, Apple touch icon and manifest with real icon previews — then generate a complete favicon pack from one image.",
        tags=["Audit", "ICO + PNG", "Manifest"], badge="",
        title="Favicon Checker & Generator — ICO, PNG, Manifest | JM Autida",
        desc="Check any website's favicon, Apple touch icon and web manifest with live previews and sizes. Generate favicon.ico, PNG icons and site.webmanifest from one image.",
        keywords="favicon checker favicon generator favicon.ico apple touch icon web manifest android chrome icon png ico",
        local=False, scripts=["vendor/jszip.min.js"],
        intro="Favicons are tiny, but missing or broken ones look unprofessional in tabs, bookmarks, search results and home screens. Audit what a site declares — with real previews and decoded sizes — and generate a complete, correctly sized icon pack in seconds.",
        steps=[
            "Enter a website URL to check its declared favicons, /favicon.ico, Apple touch icon and web manifest.",
            "Review each icon's preview, size, type and status, plus a score and the fixes to make.",
            "Switch to Generate, upload a square logo (SVG or PNG at 512px+), and adjust background, padding and corners.",
            "Download the ZIP with favicon.ico, PNG icons and site.webmanifest, and paste the HTML snippet into your <head>.",
        ],
        features=[
            "Checks declared icons, /favicon.ico, Apple touch icon and manifest",
            "Live icon previews with decoded pixel dimensions",
            "Score with clear recommendations",
            "Generator: multi-size favicon.ico, 16/32/180/192/512 PNGs",
            "Background, padding and rounded-corner controls with tab and home-screen previews",
            "Ready-to-paste HTML snippet and site.webmanifest in one ZIP",
        ],
        faq=[
            ("Which favicon sizes do I need?", "A practical modern set is favicon.ico (16, 32 and 48px inside), a 180×180 apple-touch-icon.png, and 192×192 plus 512×512 PNGs referenced from site.webmanifest. Add an SVG favicon if your logo is vector."),
            ("Why does my old favicon still show?", "Browsers cache favicons aggressively. After updating, hard-refresh, open the icon URL directly, or rename the file (for example favicon.ico?v=2) to bust the cache."),
            ("Does a missing manifest break my website?", "No. A web app manifest is optional for normal websites, but it provides icons for Android home screens and installable experiences."),
            ("Is my logo uploaded when generating?", "No. The generator draws and encodes every icon in your browser. Only the website checker contacts a server, to fetch the public URL you enter."),
        ],
        related=["meta-tags-checker", "image-converter", "contrast-checker"],
    ),
    dict(
        slug="contrast-checker", key="contrast", icon="contrast", hue="green", cat="Design & Media",
        name="Color contrast checker", h1="Color contrast checker (WCAG & APCA)",
        short="WCAG 2 and APCA contrast scores, one-click accessible color fixes, color-blindness previews and a full palette matrix.",
        tags=["WCAG AA/AAA", "APCA", "Palette"], badge="",
        title="Color Contrast Checker — WCAG AA/AAA & APCA | JM Autida",
        desc="Check text and background contrast against WCAG AA and AAA plus APCA. Get accessible color suggestions, color-blindness previews and a palette contrast matrix.",
        keywords="contrast checker wcag color contrast aa aaa apca accessibility color blindness palette matrix accessible colors",
        local=True, scripts=[],
        intro="Make text everyone can read. Check any color pair against WCAG 2 thresholds and the newer APCA model, get the nearest passing colors in one click, preview how the pair looks with color-vision deficiencies, and test a whole palette at once.",
        steps=[
            "Enter text and background colors as hex, rgb(), hsl() or a color name — or use the pickers and eyedropper.",
            "Read the contrast ratio, the AA/AAA results for normal text, large text and UI components, and the APCA Lc value.",
            "If a check fails, click a suggested color to apply the closest accessible alternative.",
            "Open Palette matrix to paste your brand colors and see every combination's contrast at a glance.",
        ],
        features=[
            "WCAG 2.x AA and AAA for normal text, large text and UI components",
            "APCA lightness contrast (Lc) for modern guidance",
            "Nearest accessible color suggestions for text or background",
            "Color-blindness simulations: protanopia, deuteranopia, tritanopia, achromatopsia",
            "Accepts hex, rgb(), hsl() and CSS names; eyedropper where supported",
            "Palette matrix for up to 12 colors; shareable links",
        ],
        faq=[
            ("What contrast ratio do I need?", "WCAG AA requires 4.5:1 for normal text and 3:1 for large text and UI components. AAA requires 7:1 for normal text and 4.5:1 for large text."),
            ("What counts as large text?", "WCAG defines large text as at least 18pt (24px), or at least 14pt (about 18.7px) when bold."),
            ("What is APCA?", "The Accessible Perceptual Contrast Algorithm is a newer contrast model that accounts for text polarity and how we perceive lightness. Lc 75+ suits body text and Lc 60+ suits larger text. It is informative; WCAG 2 ratios remain the legal standard in most places."),
            ("Does a passing pair make my page accessible?", "It's one important part. Accessibility also depends on structure, focus states, keyboard support, alternative text and more."),
        ],
        related=["html-playground", "favicon-checker", "image-converter"],
    ),
]
BY_SLUG = {t["slug"]: t for t in TOOLS}
CATEGORIES = ["SEO & Marketing", "Developer", "Writing", "Design & Media", "Productivity"]


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def person_schema():
    return {
        "@type": "Person", "@id": f"{SITE}/#person", "name": NAME, "url": f"{SITE}/about",
        "jobTitle": "Web Developer", "image": f"{SITE}/assets/img/portrait.webp",
        "address": {"@type": "PostalAddress", "addressRegion": "Bohol", "addressCountry": "PH"},
        "email": f"mailto:{EMAIL}",
        "worksFor": [{"@type": "Organization", "name": "Rise Marketing LLC"}, {"@type": "Organization", "name": "TX Rising LLC"}],
        "knowsAbout": ["Web development", "WordPress", "Technical SEO", "Front-end development", "Web performance"],
        "sameAs": SOCIAL,
    }


def jj_schema():
    return {
        "@type": "Organization", "@id": f"{SITE}/#jj-web-marketing", "name": "J & J Web Marketing LLC",
        "founder": [{"@id": f"{SITE}/#person"}, {"@type": "Person", "name": "Joseph Dittman"}],
    }


def page(path, title, desc, body, active="", schema=None, extra_head="", body_attrs="", scripts=(), og_type="website"):
    url = SITE + path
    graph = [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "name": BRAND, "url": f"{SITE}/", "publisher": {"@id": f"{SITE}/#person"}},
        person_schema(),
    ] + (schema or [])
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if active == key else ""}>{label}</a>'
        for key, href, label in [("home", "/", "Home"), ("tools", "/tools", "Tools"), ("about", "/about", "About"), ("contact", "/contact", "Contact")]
    )
    tool_links = "".join(f'<li><a href="/tools/{t["slug"]}">{e(t["name"])}</a></li>' for t in TOOLS[:6])
    more_links = "".join(f'<li><a href="/tools/{t["slug"]}">{e(t["name"])}</a></li>' for t in TOOLS[6:])
    script_tags = "".join(f'<script defer src="/assets/{s}?v={VERSION}"></script>' for s in scripts)
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="JM Autida — web developer and free online tools">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{SITE}/assets/img/social-card.png">
<meta name="theme-color" content="#06080c">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VERSION}">
<script>document.documentElement.classList.remove('no-js');try{{var t=localStorage.getItem('jm-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script defer src="/assets/js/catalog.js?v={VERSION}"></script><script defer src="/assets/js/site.js?v={VERSION}"></script>{script_tags}
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
{extra_head}</head>
<body{body_attrs}>
<a class="skip" href="#main">Skip to content</a>
<div class="bg-fx" aria-hidden="true"><div class="aurora a1"></div><div class="aurora a2"></div><div class="aurora a3"></div></div>
<div class="scroll-progress" aria-hidden="true"></div>
<header class="header" id="top"><div class="container header-inner">
<a class="brand" href="/" aria-label="JM Autida home"><span class="brand-mark">jm</span><span>autida<span class="brand-dot">.</span><small>Web developer &amp; toolmaker</small></span></a>
<nav class="nav" id="site-nav" aria-label="Main navigation">{nav}</nav>
<div class="header-actions">
<button class="kbd-btn" type="button" data-palette aria-label="Search tools">{icon("search")}<span class="label">Search tools</span><kbd>⌘K</kbd></button>
<button class="icon-btn theme-toggle" type="button" aria-label="Toggle light and dark theme">{icon("moon", "moon")}{icon("sun", "sun")}</button>
<a class="btn btn-primary btn-sm header-cta" href="/contact">Let’s talk {icon("arrow", "arrow-anim")}</a>
<button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav">{icon("menu")}</button>
</div></div></header>
<main id="main">
{body}
</main>
<footer class="footer"><div class="container">
<div class="footer-grid">
<div class="footer-about"><a class="brand" href="/"><span class="brand-mark">jm</span><span>autida<span class="brand-dot">.</span></span></a>
<p>Websites, SEO and free tools by John Raymond Autida — built in Bohol, Philippines, for teams across the US.</p>
<div class="chips"><a class="chip" href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a></div></div>
<div><h4>Popular tools</h4><ul>{tool_links}</ul></div>
<div><h4>More tools</h4><ul>{more_links}</ul></div>
<div><h4>Site</h4><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/contact?topic=tool">Suggest a tool</a></li><li><a href="/privacy">Privacy</a></li><li><a href="{SOCIAL[0]}" target="_blank" rel="noopener noreferrer">Instagram</a></li><li><a href="{SOCIAL[1]}" target="_blank" rel="noopener noreferrer">Facebook</a></li></ul></div>
</div>
<div class="footer-bottom"><span>© <span data-year>2026</span> {NAME}. Free tools, always.</span><span><a href="/privacy">Privacy</a> · <a href="#top">Back to top ↑</a></span></div>
</div></footer>
</body>
</html>
"""


def tool_card(t, featured=False, cls="", visual=""):
    tags = "".join(f'<span class="tag">{e(x)}</span>' for x in t["tags"])
    if t["badge"] == "new":
        tags = '<span class="tag new">New</span>' + tags
    elif t["badge"] == "popular":
        tags = '<span class="tag hot">Popular</span>' + tags
    search = " ".join([t["name"], t["short"], t["keywords"], t["cat"]]).lower()
    return (f'<a class="tool-card{" featured" if featured else ""} {cls} reveal" href="/tools/{t["slug"]}" data-hue="{t["hue"]}" '
            f'data-category="{e(t["cat"])}" data-search="{e(search)}" data-tilt>'
            f'<div class="card-top"><span class="tool-icon">{icon(t["icon"])}</span><span class="go">{icon("arrow")}</span></div>'
            f'<h3>{e(t["name"])}</h3><p>{e(t["short"])}</p><div class="tags">{tags}</div>{visual}</a>')


IMAGE_VISUAL = ('<div class="card-visual" aria-hidden="true"><div class="mini-convert">'
                '<div class="mini-file"><b>hero.jpg</b><span class="bar" style="--w:82%"><i></i></span><span>2.4 MB</span></div>'
                '<div class="mini-file"><b>hero.webp</b><span class="bar" style="--w:24%"><i></i></span><span class="save">−76%</span></div>'
                '<div class="mini-file"><b>team.avif</b><span class="bar" style="--w:18%"><i></i></span><span class="save">−83%</span></div>'
                '</div></div>')
SERP_VISUAL = ('<div class="card-visual" aria-hidden="true"><div class="mini-serp"><span class="u">yoursite.com › services</span>'
               '<span class="t">Roof Repair in Austin, TX | Same-Week Service</span>'
               '<span class="d">Licensed roofers fixing leaks, storm and hail damage. Free inspection and written estimate…</span>'
               '<div class="score"><span>Title 54ch ✓</span><span>OG tags ✓</span><span class="w">1 × H1 missing</span></div></div></div>')


def bento():
    b = BY_SLUG
    return "".join([
        tool_card(b["image-converter"], True, "span-8", IMAGE_VISUAL),
        tool_card(b["time-calculator"]),
        tool_card(b["meta-tags-checker"], True, "span-8", SERP_VISUAL),
        tool_card(b["html-playground"]),
        tool_card(b["json-formatter"]),
        tool_card(b["url-encoder-decoder"]),
        tool_card(b["word-counter"]),
        tool_card(b["favicon-checker"]),
        tool_card(b["markdown-to-word"]),
        tool_card(b["contrast-checker"]),
    ])


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    chips = "".join(
        f'<a class="chip" href="/tools/{s}">{icon(BY_SLUG[s]["icon"])}{e(label)}</a>'
        for s, label in [("image-converter", "Convert to WebP"), ("meta-tags-checker", "Audit meta tags"),
                         ("time-calculator", "Logout time"), ("json-formatter", "Format JSON"), ("url-encoder-decoder", "UTM builder")]
    )
    stack = ["HTML5", "CSS3", "JavaScript", "PHP", "WordPress", "Elementor", "Technical SEO", "Core Web Vitals", "Schema markup", "Landing pages", "WebP & AVIF", "Accessibility"]
    marquee = "".join(f"<span>{s}</span>" for s in stack * 2)
    features = [
        ("shield", "Private by design", "Most tools run entirely in your browser. Images, code and drafts never touch a server."),
        ("zap", "Fast, no sign-ups", "Open a tool and get to work. No accounts, no paywalls, no email gates — ever."),
        ("trend", "Built for real work", "Made for the jobs developers, SEOs, marketers and remote teams do every single day."),
    ]
    feat_html = "".join(f'<div class="feature reveal" style="--d:{i*0.08}s"><span class="tool-icon">{icon(ic)}</span><h3>{e(h)}</h3><p>{e(p)}</p></div>' for i, (ic, h, p) in enumerate(features))
    body = f"""
<section class="hero">
<canvas id="hero-canvas" aria-hidden="true"></canvas>
<div class="container">
<div class="hero-copy">
<span class="status-pill reveal"><span class="pulse"></span>Web developer · Bohol, PH ⇄ Texas, US</span>
<h1 class="reveal" style="--d:.05s"><span class="row">Websites that perform.</span><span class="row"><span class="grad-text">Tools that</span> <span class="scramble" data-words="save hours.|ship faster.|rank higher.|just work.">save hours.</span></span></h1>
<p class="lead reveal" style="--d:.1s">I’m John Raymond Autida — I build fast, search-friendly websites for Rise Marketing, TX Rising and J &amp; J Web Marketing, and I make free tools for the work in between.</p>
<div class="launcher reveal" style="--d:.15s" data-launcher>
<div class="launcher-box">{icon("search")}<input type="search" placeholder="What do you need to do? Try “webp” or “utm”" aria-label="Find a tool" autocomplete="off" role="combobox" aria-expanded="false" aria-controls="launcher-results"><kbd>/</kbd></div>
<div class="launcher-results" id="launcher-results" role="listbox" hidden></div>
</div>
<div class="chips reveal" style="--d:.2s">{chips}</div>
</div>
<div class="hero-art reveal" style="--d:.15s">
<span class="float-badge b1">{icon("zap")}100% in-browser</span>
<span class="float-badge b2">{icon("image")}−76% image size</span>
<span class="float-badge b3">{icon("search")}SEO score 96</span>
<div class="terminal" data-tilt-strong>
<div class="term-bar"><i></i><i></i><i></i><span>~/jmautida — zsh</span></div>
<div class="term-body" id="terminal" aria-label="Animated terminal showing the toolbox" role="img">
<span class="ln"><span class="p">➜</span> <span class="k">jm</span> tools --list</span>
<span class="ln c">10 free tools · no sign-ups · private</span>
</div>
</div>
<div class="portrait-chip"><img src="/assets/img/portrait.webp" alt="John Raymond Autida" width="42" height="42"><div><strong>John Raymond Autida</strong><small>Web developer &amp; co-founder, J &amp; J Web Marketing</small></div></div>
</div>
</div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>
<section class="section" id="tools"><div class="container">
<div class="section-head reveal"><div><span class="eyebrow accent"><span class="line"></span>01 / The toolbox</span><h2>Free tools for the web work you do every day.</h2><p>Convert images, audit SEO, plan your shift, format data and more. Press <kbd>⌘K</kbd> anywhere to jump straight to one.</p></div>
<a class="btn" href="/tools">Browse all {len(TOOLS)} tools {icon("arrow", "arrow-anim")}</a></div>
<div class="bento">{bento()}</div>
</div></section>
<section class="section-tight"><div class="container">
<div class="stats-band reveal">
<div><strong><span data-count="{len(TOOLS)}">{len(TOOLS)}</span></strong><span>free tools, and counting</span></div>
<div><strong><span data-count="0">0</span></strong><span>sign-ups, paywalls or ads</span></div>
<div><strong><span data-count="8">8</span>/{len(TOOLS)}</strong><span>run fully in your browser</span></div>
<div><strong><span data-count="11">11</span>+</strong><span>years building for the web</span></div>
</div></div></section>
<section class="section"><div class="container">
<div class="section-head reveal"><div><span class="eyebrow accent"><span class="line"></span>02 / Why these tools</span><h2>Useful first. Fast always. Private by default.</h2></div></div>
<div class="features">{feat_html}</div>
</div></section>
<section class="section"><div class="container two-col">
<div class="reveal"><span class="eyebrow accent"><span class="line"></span>03 / The developer behind it</span>
<h2 style="font-size:clamp(32px,4.4vw,54px);margin:14px 0 18px">Code, SEO and marketing — under one roof.</h2>
<p class="lead">By day I build and grow websites with the teams at Rise Marketing LLC and TX Rising LLC, and I co-founded J &amp; J Web Marketing LLC with Joseph Dittman. This toolbox is where I share the utilities we rely on.</p>
<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="/about">More about me {icon("arrow", "arrow-anim")}</a><a class="btn btn-ghost" href="/contact">Start a project</a></div></div>
<div class="roles" style="grid-template-columns:1fr">{"".join(f'<div class="role reveal" style="--d:{i*0.08}s"><span class="eyebrow">{e(r)}</span><h3>{e(c)}</h3></div>' for i, (c, r) in enumerate(COMPANIES))}</div>
</div></section>
<section class="section-tight"><div class="container"><div class="cta reveal">
<div><span class="eyebrow accent"><span class="line"></span>Have a project or a tool idea?</span><h2>Let’s build something <span class="grad-text">fast &amp; useful.</span></h2></div>
<div class="btn-row"><a class="btn btn-primary" href="/contact" data-magnetic>Start a conversation {icon("arrow", "arrow-anim")}</a><a class="btn btn-ghost" href="/contact?topic=tool">Suggest a tool</a></div>
</div></div></section>
"""
    schema = [{"@type": "WebPage", "@id": f"{SITE}/#page", "url": f"{SITE}/", "name": "John Raymond Autida — Web Developer & Free Online Tools", "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": f"{SITE}/#person"}},
              {"@type": "ItemList", "name": "Free online tools", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/tools/{t['slug']}", "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    return page("/", "John Raymond Autida — Web Developer & Free Online Tools",
                "Free image converter (WebP/AVIF), SEO meta tags checker, logout time calculator, JSON formatter, UTM builder and more — by web developer John Raymond Autida.",
                body, "home", schema, scripts=["js/fx.js"])


def tools_index():
    filters = '<button class="filter" data-filter="all" aria-pressed="true">All tools</button>' + "".join(
        f'<button class="filter" data-filter="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in CATEGORIES)
    cards = "".join(tool_card(t) for t in TOOLS)
    body = f"""
<section class="page-intro"><div class="container">
<span class="eyebrow accent"><span class="line"></span>The toolbox / free forever</span>
<h1>Ten tools. <span class="grad-text">Zero busywork.</span></h1>
<p class="lead">Practical, private tools for developers, SEOs, marketers, writers and remote teams. No accounts, no limits — just open one and go.</p>
</div></section>
<section class="section-tight" style="padding-top:10px"><div class="container">
<div class="tool-filter"><div class="filters" role="group" aria-label="Filter tools by category">{filters}</div>
<label class="search">{icon("search")}<input id="tool-search" type="search" placeholder="Search tools…" aria-label="Search tools"></label></div>
<p id="tool-count" class="muted" aria-live="polite">{len(TOOLS)} tools, ready when you are.</p>
<div class="bento" id="tool-grid">{cards}</div>
<div class="empty" id="no-tools" hidden><h3>No tool matches that yet.</h3><p>Try another keyword — or <a class="text-link" href="/contact?topic=tool">suggest the tool you need</a>.</p></div>
</div></section>
<section class="section-tight"><div class="container"><div class="cta reveal">
<div><span class="eyebrow accent"><span class="line"></span>Missing something?</span><h2>Tell me the tool you wish existed.</h2></div>
<a class="btn btn-primary" href="/contact?topic=tool" data-magnetic>Suggest a tool {icon("arrow", "arrow-anim")}</a>
</div></div></section>
"""
    schema = [{"@type": "CollectionPage", "@id": f"{SITE}/tools#page", "url": f"{SITE}/tools", "name": "Free Online Tools for Web, SEO & Productivity", "isPartOf": {"@id": f"{SITE}/#website"},
               "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/tools/{t['slug']}", "name": t["name"]} for i, t in enumerate(TOOLS)]}}]
    return page("/tools", "Free Online Tools — Image Converter, SEO Checker & More | JM Autida",
                "Ten free, private tools: WebP/AVIF image converter, SEO meta tags checker, favicon generator, logout time calculator, JSON formatter, UTM builder, word counter and more.",
                body, "tools", schema)


def lower_first(name):
    # "Image converter" -> "image converter", but keep acronyms such as "SEO" or "JSON".
    return name[0].lower() + name[1:] if len(name) > 1 and name[1].islower() and not name.startswith("Markdown") else name


def tool_page(t):
    path = f"/tools/{t['slug']}"
    steps = "".join(f"<li>{e(s)}</li>" for s in t["steps"])
    feats = "".join(f"<li>{icon('check')}<span>{e(f)}</span></li>" for f in t["features"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in t["faq"])
    related = "".join(f'<a href="/tools/{r}" data-hue="{BY_SLUG[r]["hue"]}"><span class="tool-icon">{icon(BY_SLUG[r]["icon"])}</span>{e(BY_SLUG[r]["name"])}</a>' for r in t["related"])
    privacy = (f'{icon("lock")}Runs in your browser' if t["local"] else f'{icon("globe")}Checks public URLs')
    body = f"""
<section class="tool-hero"><div class="container">
<nav aria-label="Breadcrumb"><ol class="breadcrumbs"><li><a href="/">Home</a></li><li><a href="/tools">Tools</a></li><li aria-current="page">{e(t["name"])}</li></ol></nav>
<div class="tool-hero-grid"><div><span class="eyebrow accent"><span class="line"></span>{e(t["cat"])}</span><h1>{e(t["h1"])}</h1><p>{e(t["intro"])}</p></div>
<div class="badges"><span class="badge-soft">{privacy}</span><span class="badge-soft">{icon("gift")}Free · no sign-up</span></div></div>
</div></section>
<section><div class="container">
<div class="workspace" id="tool-app" data-tool="{t["key"]}"><div class="tool-loading">Loading {e(lower_first(t["name"]))}…</div></div>
<p class="status-line" id="status" role="status" aria-live="polite"></p>
<noscript><p class="status-line error">This tool needs JavaScript. The guide below still explains how it works.</p></noscript>
<div class="guide">
<div><span class="eyebrow accent"><span class="line"></span>How it works</span><h2>How to use the {e(lower_first(t["name"]))}</h2><ol>{steps}</ol>
<h3 style="font-size:20px;margin:30px 0 14px">What it can do</h3><ul class="features-list">{feats}</ul></div>
<div><span class="eyebrow accent"><span class="line"></span>FAQ</span><h2>Common questions</h2><div class="faq">{faq}</div>
<h3 style="font-size:20px;margin:36px 0 0">More useful tools</h3><div class="related" style="grid-template-columns:1fr">{related}</div>
<p class="muted" style="margin-top:22px;font-size:14px">Found a bug or want a feature? <a class="text-link" href="/contact?topic=tool">Tell me →</a></p></div>
</div>
</div></section>
"""
    schema = [
        {"@type": "WebPage", "@id": f"{SITE}{path}#page", "url": f"{SITE}{path}", "name": t["title"], "description": t["desc"], "isPartOf": {"@id": f"{SITE}/#website"}, "mainEntity": {"@id": f"{SITE}{path}#tool"}},
        {"@type": "WebApplication", "@id": f"{SITE}{path}#tool", "name": t["name"], "url": f"{SITE}{path}", "description": t["desc"], "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any modern web browser", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "featureList": t["features"], "creator": {"@id": f"{SITE}/#person"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}, {"@type": "ListItem", "position": 2, "name": "Tools", "item": f"{SITE}/tools"}, {"@type": "ListItem", "position": 3, "name": t["name"], "item": f"{SITE}{path}"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
    ]
    scripts = t["scripts"] + ["js/tools/common.js", f"js/tools/{t['slug']}.js"]
    return page(path, t["title"], t["desc"], body, "tools", schema, scripts=scripts)


def about():
    roles = [
        ("Web developer", "Rise Marketing LLC", "Building and maintaining websites and landing pages for Rise Marketing and the brands it supports — clean code, fast load times and on-page SEO that helps pages earn traffic and leads.", "building"),
        ("Web developer", "TX Rising LLC", "Developing and supporting TX Rising’s web projects in Texas, from new builds and redesigns to performance tuning, technical SEO and the everyday updates that keep sites healthy.", "trend"),
        ("Co-founder", "J & J Web Marketing LLC", "Co-founded with Joseph Dittman. Together we design, build and grow websites for businesses, combining development, SEO and digital marketing so clients get one team that does it all.", "users"),
    ]
    roles_html = "".join(
        f'<div class="role reveal" style="--d:{i*0.08}s" data-tilt><span class="tool-icon" style="margin-bottom:18px">{icon(ic)}</span><span class="eyebrow">{e(r)}</span><h3 style="margin-top:10px">{e(c)}</h3><p>{e(p)}</p></div>'
        for i, (r, c, p, ic) in enumerate(roles))
    skills = [
        ("Development", ["HTML5", "CSS3", "JavaScript", "PHP", "WordPress", "Elementor", "Responsive design", "Web performance"]),
        ("SEO & marketing", ["On-page SEO", "Technical audits", "Schema markup", "Landing pages", "Local SEO", "Analytics & UTM tracking"]),
        ("Design & content", ["Photoshop", "Image optimization", "UI layout", "Blog publishing", "Promotional graphics"]),
        ("How I work", ["Clear communication", "PH ⇄ US time zones", "Fast turnaround", "Documentation", "Long-term support"]),
    ]
    skills_html = "".join(f'<div class="skill-group reveal"><h3>{e(h)}</h3><div class="chips">{"".join(f"<span class=chip>{e(s)}</span>" for s in items)}</div></div>' for h, items in skills)
    timeline = [
        ("NOW", "Rise Marketing LLC · TX Rising LLC", "Web development, landing pages and technical SEO for marketing teams and their clients in Texas."),
        ("NOW", "Co-founder, J & J Web Marketing LLC", "Building a web marketing company with Joseph Dittman — websites, SEO and growth for small businesses."),
        ("2021–2022", "Website projects", "RiseLocate, TX Real Buyer, OnWards World and Realty.IO — real estate and lead-generation sites, redesigns and blogs."),
        ("EDUCATION", "Technical foundations", "Associate’s degree in Computer Science and a BS in Electrical Engineering."),
    ]
    tl_html = "".join(f'<div class="reveal"><span>{e(a)}</span><h3>{e(b)}</h3><p>{e(c)}</p></div>' for a, b, c in timeline)
    body = f"""
<section class="page-intro"><div class="container about-hero">
<div><span class="eyebrow accent"><span class="line"></span>Hello, I’m John Raymond</span>
<h1>I build websites that <span class="grad-text">work as hard as you do.</span></h1>
<p class="lead">I’m a web developer based in Bohol, Philippines, working with marketing teams in Texas. Since 2015 I’ve lived where design, code and marketing meet — building websites that load fast, rank well and turn visitors into customers.</p>
<p>Today I develop websites for <strong>Rise Marketing LLC</strong> and <strong>TX Rising LLC</strong>, and I’m the co-founder of <strong>J &amp; J Web Marketing LLC</strong> with Joseph Dittman. Whether it’s a landing page that needs to convert, a WordPress site that needs to be faster, or an SEO fix that needs to ship today, I like solving problems end to end.</p>
<div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="/contact" data-magnetic>Work with me {icon("arrow", "arrow-anim")}</a><a class="btn btn-ghost" href="/tools">Try the tools</a></div></div>
</div></section>
<section class="section"><div class="container">
<div class="section-head reveal"><div><span class="eyebrow accent"><span class="line"></span>Where I work now</span><h2>Three teams, one goal: websites that grow businesses.</h2></div></div>
<div class="roles">{roles_html}</div>
</div></section>
<section class="section"><div class="container two-col">
<div class="reveal"><span class="eyebrow accent"><span class="line"></span>Why the toolbox exists</span><h2 style="font-size:clamp(30px,4vw,48px);margin:14px 0 18px">The tools I wished were one click away.</h2>
<p class="lead">Every week our work involves the same small jobs: converting images to WebP, checking meta tags before launch, building UTM links for a campaign, formatting an API response, or figuring out exactly when a night shift ends.</p>
<p class="muted">So I built them properly — fast, private and free — and put them here for anyone who needs them. If there’s a tool your team keeps wishing for, <a class="text-link" href="/contact?topic=tool">tell me</a>.</p></div>
<div class="timeline">{tl_html}</div>
</div></section>
<section class="section"><div class="container">
<div class="section-head reveal"><div><span class="eyebrow accent"><span class="line"></span>What I work with</span><h2>Skills &amp; stack</h2></div></div>
<div class="skills">{skills_html}</div>
</div></section>
<section class="section-tight"><div class="container"><div class="cta reveal">
<div><span class="eyebrow accent"><span class="line"></span>Let’s work together</span><h2>Need a website that performs?</h2></div>
<a class="btn btn-primary" href="/contact" data-magnetic>Get in touch {icon("arrow", "arrow-anim")}</a>
</div></div></section>
"""
    schema = [{"@type": "ProfilePage", "@id": f"{SITE}/about#page", "url": f"{SITE}/about", "name": "About John Raymond Autida", "isPartOf": {"@id": f"{SITE}/#website"}, "mainEntity": {"@id": f"{SITE}/#person"}}, jj_schema()]
    return page("/about", "About John Raymond Autida — Web Developer, Rise Marketing & J & J Web Marketing",
                "John Raymond Autida is a web developer in Bohol, Philippines, working with Rise Marketing LLC and TX Rising LLC, and co-founder of J & J Web Marketing LLC with Joseph Dittman.",
                body, "about", schema, og_type="profile")


def contact():
    topics = [("project", "Website project"), ("seo", "SEO & marketing"), ("tool", "Tool idea or bug"), ("other", "Something else")]
    pills = "".join(f'<input type="radio" name="topic" id="topic-{k}" value="{k}"{" checked" if i == 0 else ""}><label for="topic-{k}">{e(v)}</label>' for i, (k, v) in enumerate(topics))
    body = f"""
<section class="page-intro"><div class="container contact-grid">
<div><span class="eyebrow accent"><span class="line"></span>Let’s make something useful</span>
<h1>Good things start <span class="grad-text">with a hello.</span></h1>
<p class="lead">Planning a website, need SEO help, or have an idea for a new tool? Send a message — I read every one and usually reply within one business day.</p>
<div class="contact-list">
<a href="mailto:{EMAIL}"><span class="tool-icon">{icon("mail")}</span><div><small>Email</small>{EMAIL}</div></a>
<div><span class="tool-icon">{icon("pin")}</span><div><small>Based in</small>Bohol, Philippines · working with US teams</div></div>
<a href="{SOCIAL[0]}" target="_blank" rel="noopener noreferrer"><span class="tool-icon">{icon("instagram")}</span><div><small>Instagram</small>@jhnrymndatd</div></a>
<a href="{SOCIAL[1]}" target="_blank" rel="noopener noreferrer"><span class="tool-icon">{icon("facebook")}</span><div><small>Facebook</small>johnraymond.autida</div></a>
</div></div>
<form class="contact-form reveal" id="contact-form" novalidate>
<div id="form-body" style="display:grid;gap:16px">
<h2>Send a message</h2>
<fieldset style="border:0;padding:0;margin:0"><legend class="field" style="margin-bottom:8px">What’s it about?</legend><div class="topic-pills">{pills}</div></fieldset>
<div class="form-grid">
<label class="field">Your name<input class="input" name="name" required maxlength="100" autocomplete="name"></label>
<label class="field">Email<input class="input" name="email" type="email" required maxlength="200" autocomplete="email"></label>
<label class="field full">Website <small>(optional)</small><input class="input" name="site" type="url" maxlength="300" placeholder="https://" autocomplete="url"></label>
<label class="field full">Message<textarea class="input" name="message" required minlength="10" maxlength="5000" rows="6" placeholder="Tell me about your project, timeline or idea…"></textarea></label>
</div>
<label class="hp" aria-hidden="true">Leave this empty<input name="company" tabindex="-1" autocomplete="off"></label>
<input type="hidden" name="ts" value="">
<button class="btn btn-primary" type="submit" id="contact-submit">{icon("send")}Send message</button>
<p class="form-note">Your message goes straight to {EMAIL}. Your details are used only to reply — see the <a class="text-link" href="/privacy">privacy note</a>.</p>
<p class="status-line" id="contact-status" role="status" aria-live="polite"></p>
</div>
<div class="form-success" id="form-success" hidden><span class="tool-icon">{icon("check")}</span><h2>Message sent!</h2><p class="muted">Thanks for reaching out. I’ll get back to you at the email you provided, usually within one business day.</p><a class="btn btn-ghost" href="/tools">Explore the tools meanwhile</a></div>
</form>
</div></section>
"""
    schema = [{"@type": "ContactPage", "@id": f"{SITE}/contact#page", "url": f"{SITE}/contact", "name": "Contact John Raymond Autida", "isPartOf": {"@id": f"{SITE}/#website"}}]
    return page("/contact", "Contact John Raymond Autida — Websites, SEO & Tool Ideas",
                "Contact web developer John Raymond Autida about a website project, SEO and marketing help, or an idea for a new free tool. Email autida@jmautida.com.",
                body, "contact", schema)


def privacy():
    body = f"""
<section class="page-intro"><div class="container prose">
<span class="eyebrow accent"><span class="line"></span>Privacy</span>
<h1>Your work stays yours.</h1>
<p class="lead">This site is built to collect as little as possible. Here is exactly what happens to your data.</p>
<h2>Browser-based tools</h2>
<p>The image converter, HTML playground, JSON formatter, URL toolkit, word counter, Markdown to Word, contrast checker, favicon generator and time calculator process everything in your browser. Images, code, documents and text are not uploaded to or stored on this website’s server.</p>
<p>Some tools save your latest input or settings in your browser’s local storage so they are there when you come back (for example drafts, timesheets and playground code). This data stays on your device; clear it with each tool’s Clear button or your browser settings.</p>
<h2>Website checks</h2>
<p>The meta tags checker and favicon checker send the public URL you enter to this website’s server. The server requests that page and related public resources (such as icons, the manifest and robots.txt), returns the results to you and does not save them. A temporary hash of your network address is used to limit requests for a few minutes.</p>
<h2>Contact form</h2>
<p>When you send a message, your name, email address, optional website and message are emailed to {EMAIL} so I can reply. They are not added to any mailing list or shared with third parties. A temporary hash of your network address is used to prevent spam.</p>
<h2>Fonts, hosting and external sites</h2>
<p>Pages load fonts from Google Fonts, which receives your IP address as part of the request. The hosting provider may keep standard access logs, including IP addresses and requested URLs. HTML playground previews may request external files your code references. Links to social profiles lead to sites with their own privacy policies.</p>
<h2>Contact</h2>
<p>Questions about privacy? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p class="muted">Last updated October 28, 2026.</p>
</div></section>
"""
    return page("/privacy", "Privacy — JM Autida", "How jmautida.com handles your data: browser-based tools that keep your files private, website checks, the contact form and hosting logs.", body)


def not_found():
    body = f"""
<section class="page-intro"><div class="container" style="text-align:center;padding-block:60px">
<span class="eyebrow accent">404 / page not found</span>
<h1 style="margin-inline:auto"><span class="scramble" data-words="404|lost?|0x194">404</span></h1>
<p class="lead" style="margin-inline:auto">This address doesn’t lead anywhere. Maybe one of these tools is what you were after?</p>
<div class="btn-row" style="justify-content:center;margin:30px 0"><a class="btn btn-primary" href="/tools">Browse tools {icon("arrow", "arrow-anim")}</a><a class="btn btn-ghost" href="/">Back home</a><button class="btn btn-ghost" type="button" data-palette>{icon("search")}Search</button></div>
</div></section>
"""
    return page("/404", "Page not found — JM Autida", "The page you were looking for could not be found.", body, scripts=["js/fx.js"]).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')


def htaccess():
    slugs = "|".join(t["slug"] for t in TOOLS)
    legacy = "\n".join(
        f"RewriteCond %{{QUERY_STRING}} (^|&)tool={t['key']}(&|$) [NC]\nRewriteRule ^tool(?:\\.html)?/?$ /tools/{t['slug']} [R=301,L,QSD]"
        for t in TOOLS if t["key"] != "image")
    return f"""DirectoryIndex index.html index.php
Options -Indexes -MultiViews
ErrorDocument 404 /404.html
AddType application/manifest+json .webmanifest
AddType image/avif .avif
<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
<FilesMatch "\\.(html)$">
Header set Cache-Control "no-cache"
</FilesMatch>
</IfModule>
<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript application/json application/manifest+json image/svg+xml application/xml text/xml
</IfModule>
<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/css "access plus 30 days"
ExpiresByType application/javascript "access plus 30 days"
ExpiresByType text/javascript "access plus 30 days"
ExpiresByType image/webp "access plus 90 days"
ExpiresByType image/png "access plus 90 days"
ExpiresByType image/svg+xml "access plus 90 days"
ExpiresByType image/x-icon "access plus 90 days"
</IfModule>
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteCond %{{HTTP_HOST}} ^www\\.jmautida\\.com$ [NC]
RewriteRule ^ https://jmautida.com%{{REQUEST_URI}} [R=301,L,NE]
RewriteCond %{{HTTP_HOST}} ^jmautida\\.com$ [NC]
RewriteCond %{{HTTPS}} !=on
RewriteCond %{{HTTP:X-Forwarded-Proto}} !^https$ [NC]
RewriteRule ^ https://jmautida.com%{{REQUEST_URI}} [R=301,L,NE]
# Never serve server-side helpers, private config or the WordPress-era backup.
RewriteRule ^api/(?:lib|mailer|config[^/]*)\\.php$ - [F,L]
RewriteRule ^(?:backup|_private)(?:/|$) - [F,L]
# Legacy query-based tool URLs.
{legacy}
RewriteRule ^tool(?:\\.html)?/?$ /tools [R=301,L,QSD]
# Friendly aliases for the image converter.
RewriteRule ^tools/(?:webp-converter|convert-to-webp|image-compressor)/?$ /tools/image-converter [R=301,L]
RewriteCond %{{THE_REQUEST}} \\s/+index\\.(?:html|php)(?:[?\\s]) [NC]
RewriteRule ^index\\.(?:html|php)$ / [R=301,L]
RewriteRule ^(?:portfolio|work)(?:\\.html)?/?$ / [R=301,L,QSD]
RewriteRule ^resume(?:\\.html)?/?$ /about [R=301,L,QSD]
RewriteCond %{{THE_REQUEST}} \\s/+(tools|about|contact|privacy)\\.html(?:[?\\s]) [NC]
RewriteRule ^(tools|about|contact|privacy)\\.html$ /$1 [R=301,L]
RewriteCond %{{THE_REQUEST}} \\s/+pages/({slugs})\\.html(?:[?\\s]) [NC]
RewriteRule ^pages/({slugs})\\.html$ /tools/$1 [R=301,L]
RewriteRule ^(tools/(?:{slugs})|tools|about|contact|privacy)/+$ /$1 [R=301,L]
RewriteRule ^tools/({slugs})$ pages/$1.html [L]
RewriteRule ^(tools|about|contact|privacy)$ $1.html [L]
</IfModule>
"""


def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    write("index.html", home())
    write("tools.html", tools_index())
    for t in TOOLS:
        write(f"pages/{t['slug']}.html", tool_page(t))
    write("about.html", about())
    write("contact.html", contact())
    write("privacy.html", privacy())
    write("404.html", not_found())
    write(".htaccess", htaccess())
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["/", "/tools"] + [f"/tools/{t['slug']}" for t in TOOLS] + ["/about", "/contact", "/privacy"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-28</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("site.webmanifest", json.dumps({
        "name": "JM Autida — Web Developer & Free Tools", "short_name": "JM Tools", "start_url": "/tools", "scope": "/",
        "display": "standalone", "background_color": "#06080c", "theme_color": "#06080c",
        "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    }, indent=2))
    write("index.php", "<?php\n// Fallback entry point for hosts that prefer index.php.\nreadfile(__DIR__ . '/index.html');\n")
    catalog = [{"slug": t["slug"], "key": t["key"], "name": t["name"], "short": t["short"], "icon": t["icon"], "hue": t["hue"],
                "cat": t["cat"], "keywords": t["keywords"], "badge": t["badge"]} for t in TOOLS]
    write("assets/js/catalog.js", "/* Generated by build.py. */\nwindow.JM_TOOLS = " + json.dumps(catalog, ensure_ascii=False)
          + ";\nwindow.JM_ICONS = " + json.dumps(ICONS) + ";\n")
    print(f"Built {len(TOOLS)} tool pages and 6 site pages into {OUT}")


if __name__ == "__main__":
    main()
