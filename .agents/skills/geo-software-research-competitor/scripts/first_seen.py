"""Write `first_seen` into the frontmatter of the cards: the earliest date the service is known to have been public.

    python3 scripts/first_seen.py                    # cards that have no first_seen yet
    python3 scripts/first_seen.py --all              # every card again
    python3 scripts/first_seen.py assets/apps/x.md   # the named cards

The date is the earliest of:
- wayback: the first capture with status 200 in the Internet Archive (the host for a site root, the path as a prefix
  otherwise)
- github: the creation date of the repository on the card's "ソース" line
- store: an "初出" (first release) date written on the card from App Store or Google Play

Each is the day something was seen, not the day the service started, so the real launch is on or before it. A
capture can come long after the launch, and a repository can be made long before it. `first_seen: none` means none of
the three found anything; a lookup that failed leaves the card unchanged, so the next run tries it again.
Run from the skill directory. Needs `gh` (logged in) for the repositories.
"""
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
URL = re.compile(r"^- URL: (\S+)", re.M)
REPO = re.compile(r"^- ソース: https://github\.com/([^/\s()]+)/([^/\s()]+)", re.M)
STORE = re.compile(r"初出 (\d{4}-\d{2}-\d{2})")
AGENT = "geo-software-factory first_seen"


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    head = text[4:text.index("\n---", 4)]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


def parse_card(text: str) -> dict:
    u = URL.search(text)
    r = REPO.search(text)
    return {"url": u.group(1) if u else None,
            "repo": f"{r.group(1)}/{r.group(2).removesuffix('.git')}" if r else None,
            "store": STORE.findall(text)}


def earliest(found: dict) -> tuple[str, str]:
    got = [(d, k) for k, d in found.items() if d]
    return min(got) if got else ("none", "none")


def cdx_query(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    path = p.path.removesuffix("index.html").rstrip("/")
    q = {"url": p.netloc + path, "limit": "1", "fl": "timestamp", "filter": "statuscode:200"}
    if path:
        q["matchType"] = "prefix"
    return "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q)


def ts_date(ts: str):
    ts = ts.strip()
    return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}" if len(ts) >= 8 else None


def set_first_seen(text: str, date: str, by: str) -> str:
    end = text.index("\n---", 4)
    keep = [line for line in text[4:end].splitlines() if not line.startswith(("first_seen:", "first_seen_by:"))]
    return "---\n" + "\n".join(keep + [f"first_seen: {date}", f"first_seen_by: {by}"]) + text[end:]


def wayback_first(url: str):
    for wait in (0, 10, 30):
        time.sleep(wait)
        try:
            req = urllib.request.Request(cdx_query(url), headers={"User-Agent": AGENT})
            return ts_date(urllib.request.urlopen(req, timeout=60).read().decode())
        except Exception as e:  # noqa: BLE001 - retried, then reported
            err = e
    raise RuntimeError(f"wayback: {err}")


def github_created(repo: str):
    r = subprocess.run(["gh", "api", f"repos/{repo}", "--jq", ".created_at"], capture_output=True, text=True,
                       timeout=60)
    if r.returncode != 0:
        if "Not Found" in r.stderr:
            return None
        raise RuntimeError(f"github: {r.stderr.strip()}")
    return r.stdout.strip()[:10] or None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cards", nargs="*", type=Path)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    cards = a.cards or sorted(p for p in ASSETS.glob("*/*.md") if p.name != "README.md")
    failed = 0
    for path in cards:
        text = path.read_text()
        if not a.cards and not a.all and "first_seen" in frontmatter(text):
            continue
        c = parse_card(text)
        try:
            found = {"wayback": wayback_first(c["url"]) if c["url"] else None,
                     "github": github_created(c["repo"]) if c["repo"] else None,
                     "store": min(c["store"]) if c["store"] else None}
        except RuntimeError as e:
            failed += 1
            print(f"{path.name}\tFAILED\t{e}", flush=True)
            continue
        date, by = earliest(found)
        path.write_text(set_first_seen(text, date, by))
        print(f"{path.name}\t{date}\t{by}\t{json.dumps(found)}", flush=True)
        time.sleep(1.5)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
