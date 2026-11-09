#!/usr/bin/env python3
"""THE FACTORY UPDATES ITSELF (9 Nov 2026).

Until today a member's copy only got a fix when the member typed `update`. Nobody
does: the test copy sat on 1.3.0 while the kit reached 1.4.0. Kamay: "any fix we push
must reach every affiliate's version. An absolute yes."

This file is the ONE way a copy is updated. It runs in two places:

  python3 kit_update.py           on the member's computer: at every `plan` (the weekly
                                  Monday task) and when they say `update`. Installs everything.
  python3 kit_update.py --cloud   on GitHub (kit_update.yml, a few times a day). GitHub's own
                                  key may not write workflow files, so a version that changes
                                  one waits for the computer run; every other version is
                                  installed here, with nobody at the keyboard.

A new version is announced by the number in the original's KIT.json. What is the
member's own is never replaced (MINE below). Their keys are never touched.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
if "--root" in sys.argv:
    HERE = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
CLOUD = "--cloud" in sys.argv

# What belongs to the member. An update never replaces any of it.
MINE = re.compile(r"^(my_brand/|state/|docs/|factory/plans/|factory/reports/"
                  r"|factory/source_plan\.json$|factory/kt_series\.json$|factory/MASTERY\.md$)")
WORKFLOWS = ".github/workflows/"
# personalize.py writes the member's repo name over these two strings in every file,
# this one included, so they are spelled in two halves here.
P_REPO = "YOUR-GITHUB-" + "NAME/YOUR-REPO"
P_PAGES = "YOUR-GITHUB-" + "NAME.github.io/YOUR-REPO"


def git(*args, check=True, text=True):
    r = subprocess.run(["git", "-C", HERE, *args], capture_output=True, text=text)
    if check and r.returncode:
        err = r.stderr if text else r.stderr.decode("utf-8", "replace")
        sys.exit(f"git {' '.join(args[:3])} failed: {err.strip()[:400]}")
    return r


def my_repo():
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"]
    url = git("remote", "get-url", "origin").stdout.strip()
    m = re.search(r"github\.com[:/]+([^/]+/[^/.]+?)(?:\.git)?/?$", url) or re.search(r"/([^/]+/[^/.]+?)(?:\.git)?/?$", url)
    return m.group(1) if m else ""


def ver(s):
    return tuple(int(x) for x in re.findall(r"\d+", s or "0"))


def say(line):
    print(line)
    if CLOUD and os.environ.get("GITHUB_STEP_SUMMARY"):
        open(os.environ["GITHUB_STEP_SUMMARY"], "a").write(line + "\n")


def main():
    kit = json.load(open(os.path.join(HERE, "KIT.json")))
    upstream = kit.get("upstream") or "kamaycampos/affiliate-factory"
    repo = my_repo()
    if not repo:
        sys.exit("Could not tell this repository's name.")
    if repo.lower() == upstream.lower():
        say("This is the original kit: nothing to update.")
        return

    git("fetch", "-q", "--no-tags", f"https://github.com/{upstream}.git", "main")
    new_sha = git("rev-parse", "FETCH_HEAD").stdout.strip()
    new_kit = json.loads(git("show", f"{new_sha}:KIT.json").stdout)
    if ver(new_kit["version"]) <= ver(kit["version"]):
        say(f"Already on the newest version ({kit['version']}).")
        return

    # Always install with the NEWEST updater, so a fix to this file reaches a copy too.
    if "--fresh" not in sys.argv:
        newest = git("show", f"{new_sha}:kit_update.py", check=False)
        if newest.returncode == 0 and newest.stdout != open(os.path.abspath(__file__)).read():
            tmp = os.path.join(tempfile.mkdtemp(), "kit_update.py")
            open(tmp, "w").write(newest.stdout)
            args = [a for a in sys.argv[1:] if a not in ("--root",) and a != HERE]
            sys.exit(subprocess.run([sys.executable, tmp, "--fresh", "--root", HERE, *args]).returncode)

    owner, name = repo.split("/", 1)
    pages = f"{owner.lower()}.github.io/{name}"
    files = [f for f in git("ls-tree", "-r", "--name-only", new_sha).stdout.splitlines() if f and not MINE.match(f)]

    if CLOUD:
        changed = []
        for f in [x for x in files if x.startswith(WORKFLOWS)]:
            want = git("show", f"{new_sha}:{f}", text=False).stdout.replace(P_PAGES.encode(), pages.encode()).replace(P_REPO.encode(), repo.encode())
            p = os.path.join(HERE, f)
            if not os.path.exists(p) or open(p, "rb").read() != want:
                changed.append(f)
        if changed:
            say(f"Version {new_kit['version']} changes {len(changed)} workflow file(s) ({', '.join(os.path.basename(c) for c in changed)}). "
                "GitHub's own key may not write those, so this version is installed from the member's computer, "
                "at the next weekly plan or the next time they open Claude and type: update")
            return
        files = [f for f in files if not f.startswith(WORKFLOWS)]

    for i in range(0, len(files), 200):
        git("checkout", new_sha, "--", *files[i:i + 200])
    r = subprocess.run([sys.executable, os.path.join(HERE, "personalize.py"), "--repo", repo] + (["--no-keys"] if CLOUD else []),
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"personalize.py failed: {(r.stdout + r.stderr).strip()[:400]}")

    for i in range(0, len(files), 200):
        git("add", "--", *files[i:i + 200])
    git("add", "-u")
    if git("diff", "--staged", "--quiet", check=False).returncode == 0:
        say(f"Already on the newest version ({new_kit['version']}).")
        return
    git("commit", "-q", "-m", f"update to {new_kit['version']}")

    ok = False
    why = ""
    for attempt in range(1, 6):
        pull = git("pull", "-q", "--rebase", "--autostash", check=False)
        if pull.returncode == 0:
            push = git("push", "-q", check=False)
            if push.returncode == 0:
                ok = True
                break
            why = push.stderr.strip()
        else:
            why = pull.stderr.strip()
            git("rebase", "--abort", check=False)
        subprocess.run(["sleep", str(attempt * 5)])
    if not ok:
        if "workflow" in why.lower():
            sys.exit("The update is ready on this computer but GitHub refused the push: the GitHub login lacks the "
                     "'workflow' permission. Run:  gh auth refresh -h github.com -s workflow   (the member approves it "
                     "in Chrome), then:  git push")
        sys.exit(f"The update is committed here but did not reach GitHub: {why[:300]}")

    old = set(kit.get("changes", []))
    fresh = [c for c in new_kit.get("changes", []) if c not in old]
    say(f"UPDATED: {kit['version']} -> {new_kit['version']}. Everything that is the member's own was kept.")
    for c in fresh[:8]:
        say(f"  new: {c}")


if __name__ == "__main__":
    main()
