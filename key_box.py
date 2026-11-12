#!/usr/bin/env python3
"""THE PASTE BOX: a key goes in through a page in the member's browser, never the Terminal.

10 Nov 2026. The first member could not paste into the Terminal tab at all ("the paste and
Enter didn't work"), on three key steps in a row. Everybody knows how to paste into a box
on a web page and click a button, so that is what a key step is now.

meta_key.py, yt_key.py and tiktok_key.py call ask() / choose(). Each opens a small page
that lives on this computer only (http://127.0.0.1:<port>/...), waits for the member to
paste and click Save, and hands the values to the script. Nothing is printed, nothing goes
through the chat, and the page is gone the moment it is used.

The page's address is also written to .key_box_url beside this file, so the member's Claude
can open it in the Chrome window they are already looking at.

Every script still takes --terminal, which asks in the Terminal as before.
"""
import html
import http.server
import os
import secrets
import sys
import time
import urllib.parse
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
URLFILE = os.path.join(HERE, ".key_box_url")
TERMINAL = "--terminal" in sys.argv
WAIT_MINUTES = 30

CSS = """*{box-sizing:border-box}html,body{background:#fff;color:#000}
body{margin:0;font:20px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.w{max-width:640px;margin:0 auto;padding:28px 16px 60px}
.b{font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
h1{font-size:30px;line-height:1.15;margin:10px 0 14px}p{margin:0 0 14px}
label{display:block;font-weight:700;margin:20px 0 6px}small{display:block;font-weight:400;font-size:16px;color:#444}
input[type=password],input[type=text]{width:100%;font:inherit;padding:14px;border:2px solid #000;border-radius:12px}
button{display:block;width:100%;font:inherit;font-weight:700;margin-top:22px;padding:16px;border:2px solid #000;
border-radius:12px;background:#000;color:#fff;cursor:pointer}
button.o{background:#fff;color:#000;text-align:left;margin-top:10px}
.e{border:2px solid #000;border-left-width:8px;border-radius:12px;padding:12px;margin:0 0 14px;font-weight:700}
.n{font-size:16px;color:#444;margin-top:22px}.ok{font-size:56px;line-height:1;margin:0}"""


def _page(body):
    return ("<!doctype html><html lang=en><meta charset=utf-8><meta name=viewport content='width=device-width,"
            "initial-scale=1'><meta name=color-scheme content='light only'><title>Paste your key</title>"
            f"<style>{CSS}</style><div class=w><div class=b>The Affiliate Factory</div>{body}</div></html>").encode()


def _serve(render, accept, watch=None, open_now=True):
    """One page, on this computer only, until accept() returns a result (or watch() does)."""
    token = secrets.token_urlsafe(16)
    box = {}

    class H(http.server.BaseHTTPRequestHandler):
        def _send(self, body, code=200):
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.split("?")[0] != f"/{token}":
                return self._send(_page("<h1>This page is no longer in use</h1><p>Go back to Claude.</p>"), 404)
            self._send(_page(render("")))

        def do_POST(self):
            if self.path.split("?")[0] != f"/{token}":
                return self._send(_page("<h1>This page is no longer in use</h1><p>Go back to Claude.</p>"), 404)
            n = min(int(self.headers.get("Content-Length") or 0), 200000)
            form = {k: v[0].strip() for k, v in urllib.parse.parse_qs(self.rfile.read(n).decode("utf-8", "replace")).items()}
            result, problem = accept(form)
            if problem:
                return self._send(_page(render(problem)))
            box["result"] = result
            self._send(_page("<p class=ok>&#10003;</p><h1>Saved</h1><p>You can close this tab and go back to Claude.</p>"))

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    srv.timeout = 1
    url = f"http://127.0.0.1:{srv.server_address[1]}/{token}"
    open(URLFILE, "w").write(url)
    print(f"  A page with a paste box is open on this computer: {url}", flush=True)
    if open_now and not os.environ.get("KEY_BOX_NO_OPEN"):
        try:
            webbrowser.open(url)
        except Exception:
            pass
    end = time.time() + WAIT_MINUTES * 60
    try:
        while "result" not in box:
            if watch:
                seen = watch()
                if seen is not None:
                    box["result"] = seen
                    break
            if time.time() > end:
                sys.exit(f"  Nobody used the paste box for {WAIT_MINUTES} minutes. Run this again when ready.")
            srv.handle_request()
    finally:
        srv.server_close()
        os.path.exists(URLFILE) and os.remove(URLFILE)
    return box["result"]


def ask(title, fields, intro="", watch=None, open_now=True):
    """fields: [{"name", "label", "help", "min": shortest real value, "secret": True}] -> {name: value}"""
    if TERMINAL:
        import getpass
        out = {}
        for f in fields:
            print(f"\n  {f['label']}. {f.get('help', '')}")
            out[f["name"]] = (getpass.getpass("  (nothing shows) > ") if f.get("secret", True) else input("  > ")).strip()
            if len(out[f["name"]]) < f.get("min", 1):
                sys.exit("  That was empty or too short. Run this again.")
        return out

    def render(problem):
        rows = "".join(
            f"<label for={f['name']}>{html.escape(f['label'])}<small>{html.escape(f.get('help', ''))}</small></label>"
            f"<input id={f['name']} name={f['name']} type={'password' if f.get('secret', True) else 'text'} "
            f"autocomplete=off autocapitalize=off spellcheck=false required>" for f in fields)
        return (f"<h1>{html.escape(title)}</h1>" + (f"<div class=e>{html.escape(problem)}</div>" if problem else "")
                + (f"<p>{html.escape(intro)}</p>" if intro else "")
                + f"<form method=post>{rows}<button type=submit>Save</button></form>"
                "<p class=n>Click in a box and paste (Mac: Cmd+V, Windows: Ctrl+V). Dots show instead of the key: "
                "that is normal. This page is on your own computer. What you paste goes straight into your factory's "
                "locked storage. Claude does not see it.</p>")

    def accept(form):
        for f in fields:
            if len(form.get(f["name"], "")) < f.get("min", 1):
                return None, f"\"{f['label']}\" is empty or too short. Copy it again, paste it, and click Save."
        return {f["name"]: form[f["name"]] for f in fields}, ""

    return _serve(render, accept, watch, open_now)


def choose(title, options, intro=""):
    """options: list of labels -> the index the member clicked."""
    if TERMINAL:
        for i, o in enumerate(options, 1):
            print(f"  {i}. {o}")
        return int(input("  Which number is yours? ").strip()) - 1

    def render(problem):
        return (f"<h1>{html.escape(title)}</h1>" + (f"<p>{html.escape(intro)}</p>" if intro else "")
                + "<form method=post>" + "".join(f"<button class=o name=pick value={i}>{html.escape(o)}</button>"
                                                 for i, o in enumerate(options)) + "</form>")

    def accept(form):
        try:
            i = int(form.get("pick", ""))
            return (i, "") if 0 <= i < len(options) else (None, "Click one of the buttons.")
        except ValueError:
            return None, "Click one of the buttons."

    return _serve(render, accept)


if __name__ == "__main__":   # python3 key_box.py : try the box with a pretend key
    got = ask("Try the paste box", [{"name": "a", "label": "Any word", "help": "This is only a test.", "min": 3}])
    print(f"  The box works. It received {len(got['a'])} characters.")
