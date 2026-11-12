#!/usr/bin/env python3
"""YouTube key for a factory repo, with no copy-paste of tokens through a chat.

    python3 yt_key.py <CLIENT_ID>        (proven on WB Organics, 15 Oct 2026)

Asks for the OAuth client SECRET in a paste box in the browser (key_box.py), waits for the Google "Allow" click at
http://127.0.0.1:8765, then stores YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN in
the repo's GitHub secrets and prints the channel name it can upload to.
"""
import http.server
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

import re
import key_box
HERE = os.path.dirname(os.path.abspath(__file__))
_u = subprocess.run(["git", "-C", HERE, "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
_m = re.search(r"github\.com[:/]+([^/]+/[^/.]+?)(?:\.git)?/?$", _u) or re.search(r"/([^/]+/[^/.]+?)(?:\.git)?/?$", _u)
REPO, CID = _m.group(1), sys.argv[1]
GH = "gh"
PORT = 8765
REDIRECT = f"http://127.0.0.1:{PORT}/"
SCOPES = " ".join([
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
])

SECRET = key_box.ask("Paste your YouTube key", [
    {"name": "secret", "label": "Client secret", "min": 10,
     "help": "On the Google Cloud page: click the copy icon next to Client secret."}])["secret"]

url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": CID, "redirect_uri": REDIRECT, "response_type": "code",
    "scope": SCOPES, "access_type": "offline", "prompt": "consent"})
open(os.path.join(HERE, ".yt_auth_url"), "w").write(url)
print("\n  The secret is in. The Google page to open is in .yt_auth_url.", flush=True)
print("\n  Now click Allow in Chrome (Claude opens the page). If Google says it hasn't verified the app: Advanced -> Go to (your app). Waiting...")

code = {}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        code.update({k: v[0] for k, v in q.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>Done. You can close this tab and go back to Claude.</h2>")

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", PORT), H)
while "code" not in code and "error" not in code:
    srv.handle_request()
if "error" in code:
    sys.exit(f"  Google said: {code['error']}")

data = urllib.parse.urlencode({"code": code["code"], "client_id": CID, "client_secret": SECRET,
                               "redirect_uri": REDIRECT, "grant_type": "authorization_code"}).encode()
tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))
if "refresh_token" not in tok:
    sys.exit("  Google gave no refresh token. Re-run and click Allow again.")
for name, val in (("YT_CLIENT_ID", CID), ("YT_CLIENT_SECRET", SECRET), ("YT_REFRESH_TOKEN", tok["refresh_token"])):
    subprocess.run([GH, "secret", "set", name, "-R", REPO], input=val.encode(), check=True)
req = urllib.request.Request("https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true",
                             headers={"Authorization": "Bearer " + tok["access_token"]})
ch = json.load(urllib.request.urlopen(req)).get("items", [{}])[0].get("snippet", {}).get("title", "?")
os.remove(os.path.join(HERE, ".yt_auth_url"))
print(f"\n  Done. YouTube key stored for {REPO}. Channel: {ch}")
