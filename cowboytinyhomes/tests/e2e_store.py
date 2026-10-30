"""End-to-end test of the Cowboy Tiny Homes plan store against the fake Stripe API.
Usage (from cowboytinyhomes/, after generator/build.py): python3 tests/e2e_store.py site /tmp/cth-e2e
Starts the fake Stripe API (tests/mock_stripe.py) and a PHP dev server with CTH_PRIVATE_DIR pointing
at a scratch folder, then walks the whole purchase flow."""
import hashlib, hmac, http.cookiejar, json, os, re, shutil, subprocess, sys, time, urllib.parse, urllib.request

SITE, WORK = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
PRIV = os.path.join(WORK, "private")
WHSEC = "whsec_test_secret"
MOCK, WEB = 12111, 8092
BASE = f"http://127.0.0.1:{WEB}"
LOG = os.path.join(WORK, "stripe-requests.jsonl")
ok = fail = 0

def check(cond, msg):
    global ok, fail
    print(("PASS " if cond else "FAIL ") + msg)
    ok, fail = ok + bool(cond), fail + (not cond)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPCookieProcessor(jar))

def req(path, data=None, headers=None, raw=None):
    url = path if path.startswith("http") else BASE + path
    body = raw if raw is not None else (urllib.parse.urlencode(data).encode() if data is not None else None)
    r = urllib.request.Request(url, data=body, headers=headers or {})
    try:
        resp = opener.open(r, timeout=30)
    except urllib.error.HTTPError as e:
        resp = e
    return resp.status if hasattr(resp, "status") else resp.code, dict(resp.headers), resp.read()

def secrets_file(**extra):
    cfg = {"stripe_secret": "sk_test_fake", "stripe_webhook_secret": WHSEC, "stripe_api_base": f"http://127.0.0.1:{MOCK}/v1", **extra}
    php = "<?php return [" + ", ".join(f"'{k}' => " + ("true" if v is True else f"'{v}'") for k, v in cfg.items()) + "];\n"
    open(os.path.join(PRIV, "cth-secrets.php"), "w").write(php)

def signed(event):
    payload = json.dumps(event).encode()
    t = str(int(time.time()))
    sig = hmac.new(WHSEC.encode(), (t + ".").encode() + payload, hashlib.sha256).hexdigest()
    return payload, {"Stripe-Signature": f"t={t},v1={sig}", "Content-Type": "application/json"}

shutil.rmtree(WORK, ignore_errors=True)
os.makedirs(os.path.join(PRIV, "cth-plan-files"))
for z in ("bandera", "frio-park-model"):
    shutil.copy(os.path.join(SITE, "..", "dist", "plan-files", z + ".zip"), os.path.join(PRIV, "cth-plan-files"))
env = {**os.environ, "CTH_PRIVATE_DIR": PRIV}
procs = [subprocess.Popen([sys.executable, os.path.join(HERE, "mock_stripe.py"), str(MOCK), LOG]),
         subprocess.Popen(["php", "-S", f"127.0.0.1:{WEB}", "-t", SITE, os.path.join(SITE, "..", "dev-router.php")], env=env,
                          stdout=open(os.path.join(WORK, "php.log"), "w"), stderr=subprocess.STDOUT)]
time.sleep(1.2)
try:
    # 1. No Stripe key yet: the plan page falls back to the order form, and checkout redirects to the contact form.
    s, h, b = req("/home-designs/bandera/")
    check(s == 200 and b"Order this plan" in b and b"/order/checkout/" not in b, "without Stripe keys the plan page shows the contact-form order button")
    s, h, b = req("/order/checkout/", {"plan": "bandera"})
    check(s == 303 and "/contact-us/" in h.get("Location", ""), f"without Stripe keys checkout redirects to the contact form ({h.get('Location', '')[:60]})")
    s, h, b = req(urllib.parse.urlparse(h.get("Location", "/")).path + "?" + urllib.parse.urlparse(h.get("Location", "/")).query)
    check(s == 200 and b"The Bandera" in b and b'selected>Design / plans only' in b, "contact form is prefilled with the plan and project type")

    # 2. Stripe key present, but a plan without uploaded files still falls back.
    secrets_file()
    s, h, b = req("/home-designs/mesquite/")
    check(b"Order this plan" in b, "plan without an uploaded zip still shows the order form")
    s, h, b = req("/home-designs/bandera/")
    check(b'action="/order/checkout/"' in b and b"Buy &amp; download now" in b, "plan with key + zip shows the Buy & download button")

    # 3. Checkout -> Stripe -> webhook -> success page -> download
    s, h, b = req("/order/checkout/", {"plan": "bandera"})
    loc = h.get("Location", "")
    check(s == 303 and loc.startswith(f"http://127.0.0.1:{MOCK}/pay/cs_test_"), "checkout creates a session and redirects to Stripe")
    sent = json.loads(open(LOG).read().strip().splitlines()[-1])["params"]
    check(sent.get("line_items[0][price_data][unit_amount]") == "104500" and sent.get("metadata[plan]") == "bandera", "session has the right price ($1,045) and plan")
    check(sent.get("success_url", "").endswith("/order/complete/?session_id={CHECKOUT_SESSION_ID}") and "/home-designs/bandera/" in sent.get("cancel_url", ""), "success and cancel URLs point back to the site")
    check("automatic_tax[enabled]" not in sent, "Stripe Tax is off by default")
    sid = loc.rsplit("/", 1)[1]
    s, h, b = req(loc)                                   # buyer pays
    session = json.loads(b)
    payload, hdr = signed({"id": "evt_1", "type": "checkout.session.completed", "data": {"object": session}})
    s, h, b = req("/order/webhook/", raw=payload, headers=hdr)
    check(s == 200 and b'"received":true' in b, "signed webhook is accepted")
    orders = os.listdir(os.path.join(PRIV, "cth-data", "orders"))
    check(len(orders) == 1, "webhook recorded one order outside the web root")
    order = json.load(open(os.path.join(PRIV, "cth-data", "orders", orders[0])))
    check(order["id"].startswith("CTH-") and order["amount"] == 1045 and order["plan"] == "bandera", f"order record {order['id']} for $1,045")
    s, h, b = req("/order/webhook/", raw=payload, headers=hdr)
    check(len(os.listdir(os.path.join(PRIV, "cth-data", "orders"))) == 1, "a repeated webhook does not create a second order")
    s, h, b = req("/order/complete/?session_id=" + sid)
    check(s == 200 and order["id"].encode() in b and b"/order/download/?o=" in b, "success page shows the order and download link")
    check(b"credit the full plan price" in b, "success page offers the build credit")
    m = re.search(rb'href="https://cowboytinyhomes.com(/order/download/\?o=[^"]+)"', b)
    dl = m.group(1).decode().replace("&amp;", "&")
    s, h, b = req(dl)
    size = os.path.getsize(os.path.join(PRIV, "cth-plan-files", "bandera.zip"))
    check(s == 200 and h.get("Content-Type") == "application/zip" and len(b) == size, f"download streams the zip ({len(b):,} bytes)")
    check("Cowboy-Tiny-Homes-The-Bandera-Complete-Plan-Set.zip" in h.get("Content-Disposition", ""), "download has a sensible filename")
    order = json.load(open(os.path.join(PRIV, "cth-data", "orders", orders[0])))
    check(order["downloads"] == 1, "download count is tracked")
    s, h, b = req(dl.replace(order["token"], "0" * 40))
    check(s == 404, "a wrong token returns 404")
    csv = open(os.path.join(PRIV, "cth-data", "orders.csv")).read()
    check(order["id"] in csv, "sale is in the CSV log")

    # 4. Success page before the webhook (the page itself fulfills from the Stripe API)
    s, h, b = req("/order/checkout/", {"plan": "frio-park-model", "email": "second@example.com"})
    sid2 = h["Location"].rsplit("/", 1)[1]
    req(h["Location"])
    s, h, b = req("/order/complete/?session_id=" + sid2)
    check(s == 200 and b"Your plan set is ready" in b and b"second@example.com" in b, "success page fulfills a paid session when it arrives before the webhook")
    s, h, b = req("/order/complete/?session_id=cs_test_doesnotexist000")
    check(b"could not find that order" in b, "unknown session shows the not-found message")

    # 5. Lookup re-sends links (same answer whether or not the address has orders)
    s, h, b = req("/order/lookup/")
    csrf = re.search(rb'name="csrf" value="([0-9a-f]+)"', b).group(1).decode()
    s, h, b = req("/order/lookup/", {"csrf": csrf, "email": "buyer@example.com", "website": ""})
    check(s == 200 and b"download links are on their way" in b, "lookup accepts an address and confirms")
    s, h, b = req("/order/lookup/", {"csrf": "bad", "email": "buyer@example.com"})
    check(b"reload the page" in b, "lookup rejects a bad CSRF token")

    # 6. Refund turns the link off; a bad signature is rejected
    payload, hdr = signed({"id": "evt_2", "type": "charge.refunded", "data": {"object": {"payment_intent": session["payment_intent"], "amount": 104500, "amount_refunded": 104500}}})
    s, h, b = req("/order/webhook/", raw=payload, headers=hdr)
    s, h, b = req(dl)
    check(s == 410 and b"refunded" in b, "full refund disables the download link (410)")
    bad = dict(hdr); bad["Stripe-Signature"] = hdr["Stripe-Signature"][:-4] + "beef"
    s, h, b = req("/order/webhook/", raw=payload, headers=bad)
    check(s == 400, "webhook with a bad signature is rejected (400)")

    # 7. 100%-off promotion code: no payment required still delivers
    s, h, b = req("/order/checkout/", {"plan": "bandera"})
    sid3 = h["Location"].rsplit("/", 1)[1]
    s, h, b = req(f"http://127.0.0.1:{MOCK}/__session/{sid3}")
    free = json.loads(b); free.update(status="complete", payment_status="no_payment_required", amount_total=0)
    payload, hdr = signed({"id": "evt_3", "type": "checkout.session.completed", "data": {"object": free}})
    req("/order/webhook/", raw=payload, headers=hdr)
    check(len(os.listdir(os.path.join(PRIV, "cth-data", "orders"))) == 3, "fully discounted order is delivered")

    # 8. Stripe Tax switch
    secrets_file(stripe_tax=True)
    req("/order/checkout/", {"plan": "bandera"})
    sent = json.loads(open(LOG).read().strip().splitlines()[-1])["params"]
    check(sent.get("automatic_tax[enabled]") == "true" and sent.get("billing_address_collection") == "required", "stripe_tax => automatic tax with a required billing address")

    # 9. Pages carry noindex and stay out of the sitemap
    s, h, b = req("/sitemap.xml")
    check(b"/order/" not in b and b"/home-designs/bandera/" in b and b"/terms-of-sale/" in b, "sitemap lists plans and terms but no order pages")
    log = open(os.path.join(WORK, "php.log")).read()
    check(not re.search(r"PHP (Warning|Notice|Fatal|Deprecated)", log), "no PHP warnings in the server log")
finally:
    for p in procs: p.terminate()
print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
