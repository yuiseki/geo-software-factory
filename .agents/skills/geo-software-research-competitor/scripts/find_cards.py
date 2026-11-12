#!/usr/bin/env python3
"""Find the observed map services (assets/services/, assets/apps/) that match any of the given words.

Reading every card at once buries the one that matters; search them instead. Only the part that says what a
service is (title, search words, one line, value, users) is searched, not the technology section. Width and
case are folded (Ｗｉ－Ｆｉ, wifi, Wi-Fi all match "wifi"). Standard library only; no ripgrep needed.

    python3 find_cards.py 電源 Wi-Fi Web会議 作業場所 カフェ 通話 coworking

Prints one card per line, most matched words first: matched count, file, title, URL, one line.
"""
from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
FIELDS = ("探すときの語", "一行で", "提供する価値", "想定する利用者")


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).lower()
    return re.sub(r"[\s\-‐_・]", "", s)


def card_text(text: str) -> tuple[str, dict]:
    """The searchable part of a card, and its title, URL and one line."""
    head = text.split("\n## 技術", 1)[0]
    lines = head.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else ""
    url = next((l.split(":", 1)[1].strip() for l in lines if l.startswith("- URL:")), "")
    rows = {}
    for l in lines:
        m = re.match(r"^\| ([^|]+?) \|(.*?)\|", l)
        if m:
            rows[m[1]] = m[2].strip()
    words = next((l.split(":", 1)[1] for l in lines if l.startswith("- 探すときの語:")), "")
    searchable = " ".join([title, words] + [rows.get(f, "") for f in FIELDS[1:]])
    return searchable, {"title": title, "url": url, "one_line": rows.get("一行で", "")}


def find(root: pathlib.Path, words: list[str]) -> list[dict]:
    hits = []
    for card in sorted([*root.glob("services/*.md"), *root.glob("apps/*.md")]):
        if card.name == "README.md":
            continue
        searchable, info = card_text(card.read_text(encoding="utf-8"))
        hay = fold(searchable)
        matched = sorted({w for w in words if fold(w) and fold(w) in hay})
        if matched:
            hits.append({"file": card.relative_to(root).as_posix(), "matched": matched, **info})
    return sorted(hits, key=lambda h: (-len(h["matched"]), h["file"]))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    hits = find(ASSETS, argv)
    for h in hits:
        print(f"{len(h['matched'])}\t{h['file']}\t{h['title']}\t{h['url']}\t{h['one_line']}")
    if not hits:
        print("no card matched; try other words (synonyms, broader terms, English)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
