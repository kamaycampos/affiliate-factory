#!/usr/bin/env python3
"""TikTok: clips land in the member's TikTok INBOX (drafts); they paste the caption and tap Post.

Proven on WB Organics, 15 Oct 2026. TikTok does not approve personal posting apps, so the
member's own TikTok developer app stays in SANDBOX, with their own TikTok account added
as a sandbox "target user". Sandbox + "Upload to TikTok" (video.upload) = inbox drafts.

    python3 tiktok_key.py <SANDBOX_CLIENT_KEY>

1. Asks for the SANDBOX client secret (TikTok for Developers -> app -> Sandbox ->
   Credentials) in a paste box in the browser (key_box.py) - never the Terminal.
2. Writes the consent link to .tt_auth_url (their Claude opens it in their Chrome).
3. They tap Authorize and land on their control panel. Their Claude reads that tab's address
   and writes it to .tt_landed (a one-time code, useless without the secret); if it cannot,
   a second paste box asks the member for that address.
4. Stores TT_CLIENT_KEY, TT_CLIENT_SECRET, TT_REFRESH_TOKEN in their repository's secrets
   and prints the TikTok account it reached. Nothing secret is ever printed.

The redirect is their control panel (https://OWNER.github.io/REPO/). It must be listed
under Sandbox -> Login Kit -> Redirect URI before running this.
"""
import hashlib, json, os, re, secrets, subprocess, sys, urllib.parse, urllib.request

import key_box

HERE = os.path.dirname(os.path.abspath(__file__))
LANDED = os.path.join(HERE, ".tt_landed")
URLFILE = os.path.join(HERE, ".tt_auth_url")
SCOPES = "user.info.basic,user.info.profile,user.info.stats,video.list,video.upload"

url = subprocess.run(["git", "-C", HERE, "remote", "get-url", "origin"],
                     capture_output=True, text=True).stdout.strip()
m = re.search(r"github\.com[:/]+([^/]+)/([^/.]+?)(?:\.git)?/?$", url) or re.search(r"/([^/]+)/([^/.]+?)(?:\.git)?/?$", url)
if not m:
    sys.exit("  Could not tell this repository's name from git.")
OWNER, NAME = m.group(1), m.group(2)
REPO = f"{OWNER}/{NAME}"
REDIRECT = f"https://{OWNER.lower()}.github.io/{NAME}/"

print(f"\n  TikTok inbox for {REPO}. Redirect URI to register in the Sandbox: {REDIRECT}")
_args = [a for a in sys.argv[1:] if not a.startswith("--")]
_fields = [{"name": "cs", "label": "Client secret", "min": 8,
            "help": "TikTok for Developers: your app, Sandbox, Credentials. Click the small arrow or copy icon next to Client secret."}]
if not _args:
    _fields.insert(0, {"name": "ck", "label": "Client key", "min": 8, "secret": False,
                       "help": "Same place, the line above: Client key. It starts with sb."})
_got = key_box.ask("Paste your TikTok key", _fields)
CK, CS = (_args[0] if _args else _got["ck"]), _got["cs"]
os.path.exists(LANDED) and os.remove(LANDED)

ver = secrets.token_urlsafe(48)
state = "tt" + secrets.token_hex(5)
open(URLFILE, "w").write("https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
    "client_key": CK, "response_type": "code", "scope": SCOPES, "redirect_uri": REDIRECT,
    "state": state, "code_challenge": hashlib.sha256(ver.encode()).hexdigest(),
    "code_challenge_method": "S256"}))
print("\n  The secret is in. The TikTok page to open is in .tt_auth_url.", flush=True)
print("  After Authorize they land on their control panel: write that tab's full address to .tt_landed", flush=True)


def _landed():
    if os.path.exists(LANDED):
        t = open(LANDED).read().strip()
        return {"landed": t} if "code=" in t else None


landed = key_box.ask("One last step for TikTok", [
    {"name": "landed", "label": "The address of the page you landed on", "min": 20, "secret": False,
     "help": "After you tap Authorize on TikTok you land on your control panel. Click its address bar at the top, "
             "select all (Cmd+A, Windows Ctrl+A), copy, and paste it here."}],
    watch=_landed, open_now=False)["landed"]   # opened only if Claude could not read the address itself
os.path.exists(URLFILE) and os.remove(URLFILE)
os.path.exists(LANDED) and os.remove(LANDED)
q = urllib.parse.parse_qs(urllib.parse.urlparse(landed).query)
if q.get("state", [""])[0] != state or "code" not in q:
    sys.exit("  That address has no fresh TikTok code. Run this again.")
req = urllib.request.Request("https://open.tiktokapis.com/v2/oauth/token/",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data=urllib.parse.urlencode({
                                 "client_key": CK, "client_secret": CS, "code": q["code"][0],
                                 "grant_type": "authorization_code", "redirect_uri": REDIRECT,
                                 "code_verifier": ver}).encode())
r = json.loads(urllib.request.urlopen(req, timeout=30).read())
if not r.get("refresh_token"):
    sys.exit(f"  TikTok refused: {r.get('error')} {r.get('error_description')}")
if "video.upload" not in (r.get("scope") or ""):
    sys.exit("  TikTok did not grant video.upload: add Content Posting API to the Sandbox and re-run.")
for k, v in (("TT_CLIENT_KEY", CK), ("TT_CLIENT_SECRET", CS), ("TT_REFRESH_TOKEN", r["refresh_token"])):
    subprocess.run(["gh", "secret", "set", k, "-R", REPO], input=v.encode(), check=True)
u = urllib.request.Request("https://open.tiktokapis.com/v2/user/info/?fields=display_name,username",
                           headers={"Authorization": "Bearer " + r["access_token"]})
who = json.loads(urllib.request.urlopen(u, timeout=30).read()).get("data", {}).get("user", {})
print(f"\n  Done. TikTok key stored for {REPO}. Account: {who.get('display_name')} (@{who.get('username')})")
