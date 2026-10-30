"""Minimal fake Stripe API for the checkout flow: create and retrieve Checkout Sessions.
POST /v1/checkout/sessions    -> session (unpaid) with a hosted 'url'
GET  /v1/checkout/sessions/ID -> the session; /pay/ID marks it paid (simulates the buyer paying)
Every request is logged to requests.jsonl so the test can inspect the parameters sent."""
import json, sys, secrets, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
SESS = {}
LOG = sys.argv[2]
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode()
        params = dict(urllib.parse.parse_qsl(body, keep_blank_values=True))
        open(LOG, "a").write(json.dumps({"method": "POST", "path": self.path, "auth": self.headers.get("Authorization"), "params": params}) + "\n")
        if self.path == "/v1/checkout/sessions":
            if not (self.headers.get("Authorization") or "").startswith("Basic "):
                return self.send(401, {"error": {"message": "No API key"}})
            sid = "cs_test_" + secrets.token_hex(12)
            amount = int(params["line_items[0][price_data][unit_amount]"])
            tax = round(amount * 0.0825) if params.get("automatic_tax[enabled]") == "true" else 0
            SESS[sid] = {"id": sid, "object": "checkout.session", "url": f"http://127.0.0.1:{PORT}/pay/{sid}", "status": "open",
                         "payment_status": "unpaid", "amount_total": amount + tax, "currency": "usd", "total_details": {"amount_tax": tax},
                         "metadata": {"plan": params.get("metadata[plan]")}, "client_reference_id": params.get("client_reference_id"),
                         "customer_details": {"email": params.get("customer_email") or "buyer@example.com", "name": "Test Buyer"},
                         "payment_intent": "pi_test_" + secrets.token_hex(8)}
            return self.send(200, SESS[sid])
        self.send(404, {"error": {"message": "not found"}})
    def do_GET(self):
        open(LOG, "a").write(json.dumps({"method": "GET", "path": self.path}) + "\n")
        if self.path.startswith("/pay/"):
            s = SESS[self.path[5:]]; s.update(status="complete", payment_status="paid")
            return self.send(200, s)
        if self.path.startswith("/v1/checkout/sessions/"):
            s = SESS.get(self.path.rsplit("/", 1)[1])
            return self.send(200, s) if s else self.send(404, {"error": {"message": "No such checkout.session"}})
        if self.path.startswith("/__session/"):
            return self.send(200, SESS[self.path.rsplit("/", 1)[1]])
        self.send(404, {"error": {"message": "not found"}})
PORT = int(sys.argv[1])
HTTPServer(("127.0.0.1", PORT), H).serve_forever()
