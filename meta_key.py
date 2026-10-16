#!/usr/bin/env python3
"""Instagram + Facebook key, pasted by the member into THIS prompt - never into a chat.

    python3 meta_key.py <APP_ID>

Asks (hidden) for the App secret (Meta app -> App settings -> Basic) and the token from
Graph API Explorer (Generate Access Token, with their Page and Instagram ticked). Swaps it
for a long-lived user token, then for their Page token, which does not expire, and stores
FB_PAGE_ID, FB_ACCESS_TOKEN, IG_USER_ID, IG_ACCESS_TOKEN in their repository's secrets.
Prints only the Page and Instagram names it reached. Proven pattern: WB Organics, 15 Oct 2026.
"""
import getpass, json, os, re, subprocess, sys, urllib.parse, urllib.request

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


print("\n  PASTE THE APP SECRET (Meta app -> App settings -> Basic -> Show), then Enter.")
SECRET = getpass.getpass("  (nothing shows) > ").strip()
print("\n  PASTE THE TOKEN from Graph API Explorer (the long key at the top), then Enter.")
USER = getpass.getpass("  (nothing shows) > ").strip()
if len(SECRET) < 10 or len(USER) < 50:
    sys.exit("  One of them was empty. Run this again.")

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
    for i, p in enumerate(pages, 1):
        print(f"  {i}. {p['name']}  (@{(p.get('instagram_business_account') or {}).get('username', '-')})")
    pages = [pages[int(input("  Which number is yours? ").strip()) - 1]]
p = pages[0]
ig = p.get("instagram_business_account") or {}
if not ig:
    sys.exit(f"  {p['name']} has no Instagram linked. Link it (Page settings -> Linked accounts) and re-run.")
for k, v in (("FB_PAGE_ID", p["id"]), ("FB_ACCESS_TOKEN", p["access_token"]),
             ("IG_USER_ID", ig["id"]), ("IG_ACCESS_TOKEN", p["access_token"])):
    subprocess.run(["gh", "secret", "set", k, "-R", REPO], input=v.encode(), check=True)
print(f"\n  Done. Meta key stored for {REPO}. Page: {p['name']} · Instagram: @{ig.get('username')}")
