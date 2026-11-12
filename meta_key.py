#!/usr/bin/env python3
"""Instagram + Facebook key, pasted by the member into a box in their browser - never a chat,
never the Terminal (key_box.py; `--terminal` asks here as before).

    python3 meta_key.py <APP_ID>

Asks for the App secret (Meta app -> App settings -> Basic) and the token from
Graph API Explorer (Generate Access Token, with their Page and Instagram ticked). Swaps it
for a long-lived user token, then for their Page token, which does not expire, and stores
FB_PAGE_ID, FB_ACCESS_TOKEN, IG_USER_ID, IG_ACCESS_TOKEN in their repository's secrets.
Prints only the Page and Instagram names it reached. Proven pattern: WB Organics, 15 Oct 2026.
"""
import json, os, re, subprocess, sys, urllib.parse, urllib.request

import key_box

HERE = os.path.dirname(os.path.abspath(__file__))
u = subprocess.run(["git", "-C", HERE, "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
m = re.search(r"github\.com[:/]+([^/]+/[^/.]+?)(?:\.git)?/?$", u) or re.search(r"/([^/]+/[^/.]+?)(?:\.git)?/?$", u)
REPO, APP = m.group(1), sys.argv[1]
G = "https://graph.facebook.com/v21.0"


def get(path, **q):
    try:
        return json.load(urllib.request.urlopen(f"{G}/{path}?" + urllib.parse.urlencode(q), timeout=30))
    except urllib.error.HTTPError as e:
        sys.exit("  Meta refused: " + json.load(e).get("error", {}).get("message", str(e)))


_got = key_box.ask("Paste your two Meta keys", [
    {"name": "secret", "label": "1. App secret", "min": 10,
     "help": "On your Meta app page: App settings, then Basic. Click Show next to App secret and copy it."},
    {"name": "token", "label": "2. Access token", "min": 50,
     "help": "In Graph API Explorer: the long key in the Access Token box at the top. Copy all of it."}])
SECRET, USER = _got["secret"], _got["token"]

long_user = get("oauth/access_token", grant_type="fb_exchange_token", client_id=APP,
                client_secret=SECRET, fb_exchange_token=USER)["access_token"]
pages = get("me/accounts", fields="name,id,access_token,instagram_business_account{username}",
            access_token=long_user).get("data", [])
if not pages:
    # A Page held through a business portfolio can be missing from me/accounts (Meta lists
    # only Pages the person holds directly). The portfolio still lists it.
    try:
        for b in get("me/businesses", fields="id", access_token=long_user).get("data", []):
            pages += get(f"{b['id']}/owned_pages", fields="name,id,access_token,instagram_business_account{username}",
                         access_token=long_user).get("data", [])
        pages = [p for p in pages if p.get("access_token")]
    except SystemExit:
        pass
pages = [p for p in pages if p.get("instagram_business_account")] or pages
if not pages:
    sys.exit("  No Facebook Page came with this token. Generate it again and tick your Page.")
if len(pages) > 1:
    pages = [pages[key_box.choose("Which Page is yours?", [
        f"{p['name']}  (Instagram: @{(p.get('instagram_business_account') or {}).get('username', 'none linked')})" for p in pages])]]
p = pages[0]
ig = p.get("instagram_business_account") or {}
if not ig:
    sys.exit(f"  {p['name']} has no Instagram linked. Link it (Page settings -> Linked accounts) and re-run.")
for k, v in (("FB_PAGE_ID", p["id"]), ("FB_ACCESS_TOKEN", p["access_token"]),
             ("IG_USER_ID", ig["id"]), ("IG_ACCESS_TOKEN", p["access_token"])):
    subprocess.run(["gh", "secret", "set", k, "-R", REPO], input=v.encode(), check=True)
print(f"\n  Done. Meta key stored for {REPO}. Page: {p['name']} · Instagram: @{ig.get('username')}")
