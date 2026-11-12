#!/usr/bin/env python3
"""Checks the skill collection before it is published.

Errors fail the run; warnings (old "確かめた日" dates) are printed only.
Run from the repository root:  python3 scripts/check.py [--max-age-days N]
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import sys
import urllib.parse

SKIP_DIRS = {".git", "tmp", "node_modules"}
MAX_SKILL_LINES = 200
LINK = re.compile(r"\]\(([^)\s]+)\)")
LOCAL_PATH = re.compile(r"(?<![\w.])/(home|Workspaces|sata_hdd\w*)/")
DISCLOSURE_PREFIX = "- 利害関係の開示:"
CHECKED = re.compile(r"^\| 確かめた日 \| (\d{4}-\d{2}-\d{2})")
TODO_SKILL = re.compile(r"^- \[( |x)\] (\S+) \((\d+)/(\d+)\)$")
TODO_FILE = re.compile(r"^  - \[( |x)\] (\S+)$")
# What a competitor card must say beyond the technology: what the service is, for whom, and how it pays.
CARD_ROWS = ("一行で", "提供する価値", "想定する利用者", "商用か非商用か", "推定の売上", "運営", "推定の運用費")
SEARCH_WORDS = re.compile(r"^- 探すときの語: *(.*)$", re.M)
CARD_ROW = re.compile(r"^\| ([^|]+?) \|(.*?)\|")


def markdown_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(p for p in root.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(root).parts))


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    head = text[4:].split("\n---", 1)[0]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


def check_skills(root: pathlib.Path, errors: list[str]) -> None:
    for skill_md in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        rel = skill_md.relative_to(root).as_posix()
        text = skill_md.read_text()
        meta = frontmatter(text)
        name = meta.get("name")
        if name != skill_md.parent.name:
            errors.append(f"{rel}: name '{name}' does not match directory '{skill_md.parent.name}'")
        if not meta.get("description", "").strip():
            errors.append(f"{rel}: missing description")
        lines = text.count("\n")
        if lines > MAX_SKILL_LINES:
            errors.append(f"{rel}: {lines} lines, over {MAX_SKILL_LINES} lines")


def check_text(root: pathlib.Path, errors: list[str]) -> None:
    for md in markdown_files(root):
        rel = md.relative_to(root).as_posix()
        text = md.read_text()
        for n, line in enumerate(text.splitlines(), 1):
            if "—" in line:
                errors.append(f"{rel}:{n}: em dash")
            if LOCAL_PATH.search(line):
                errors.append(f"{rel}:{n}: local path")
        for target in LINK.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = urllib.parse.unquote(target.split("#")[0])
            if path and not (md.parent / path).exists():
                errors.append(f"{rel}: broken link {target}")


def check_disclosure(root: pathlib.Path, errors: list[str]) -> None:
    agents = root / "AGENTS.md"
    canon = next((l for l in agents.read_text().splitlines() if l.startswith(DISCLOSURE_PREFIX)), None) if agents.exists() else None
    if canon is None:
        errors.append("AGENTS.md: no disclosure line")
        return
    for skill_md in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        for line in skill_md.read_text().splitlines():
            # A skill may add a sentence after the shared one, never change it.
            if line.startswith(DISCLOSURE_PREFIX) and not line.startswith(canon):
                errors.append(f"{skill_md.relative_to(root).as_posix()}: disclosure differs from AGENTS.md")


def check_todo(root: pathlib.Path, errors: list[str]) -> None:
    todo = root / ".agents/skills/TODO.md"
    if not todo.exists():
        errors.append("TODO.md: missing")
        return
    listed: dict[str, dict] = {}
    current = None
    for line in todo.read_text().splitlines():
        if m := TODO_SKILL.match(line):
            current = listed.setdefault(m[2], {"box": m[1], "said": (int(m[3]), int(m[4])), "files": {}})
        elif (m := TODO_FILE.match(line)) and current is not None:
            current["files"][m[2]] = m[1] == "x"
        elif not line.startswith("  "):
            current = None
    for name, entry in listed.items():
        skill_dir = root / ".agents/skills" / name
        on_disk = {p.relative_to(skill_dir).as_posix() for p in skill_dir.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts} if skill_dir.is_dir() else set()
        # An entry ending in "/" (a directory of data, such as cards) covers every file under it.
        dirs = [p for p in entry["files"] if p.endswith("/")]
        covered = {p for p in on_disk if any(p.startswith(d) for d in dirs)}
        for path in sorted(on_disk - entry["files"].keys() - covered):
            errors.append(f"TODO.md: {name} is missing {path}")
        for path in sorted(entry["files"].keys() - on_disk):
            if path.endswith("/") and any(p.startswith(path) for p in on_disk):
                continue
            errors.append(f"TODO.md: {name} lists {path}, which does not exist")
        done = sum(entry["files"].values())
        total = len(entry["files"])
        if entry["said"] != (done, total):
            errors.append(f"TODO.md: {name} says ({entry['said'][0]}/{entry['said'][1]}) but has {done}/{total}")
        if (entry["box"] == "x") != (done == total):
            errors.append(f"TODO.md: {name} box does not match {done}/{total}")
    for skill_dir in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        if skill_dir.parent.name not in listed:
            errors.append(f"TODO.md: {skill_dir.parent.name} is not listed")


def check_cards(root: pathlib.Path, errors: list[str]) -> None:
    cards = [*(root / ".agents/skills").glob("*/assets/services/*.md"), *(root / ".agents/skills").glob("*/assets/apps/*.md")]
    for card in sorted(cards):
        if card.name == "README.md":
            continue
        rel = card.relative_to(root).as_posix()
        text = card.read_text()
        rows = {m[1]: m[2].strip() for line in text.splitlines() if (m := CARD_ROW.match(line))}
        # Names differ from the words people search with (生活利便性 vs 生活便利), so each card lists them.
        words = SEARCH_WORDS.search(text)
        if not words or not words[1].strip():
            errors.append(f"{rel}: card has no words to search it by (- 探すときの語:)")
        for name in CARD_ROWS:
            if name not in rows:
                errors.append(f"{rel}: card has no row '{name}'")
            elif not rows[name]:
                errors.append(f"{rel}: card row '{name}' is empty")


def check_dates(root: pathlib.Path, today: datetime.date, max_age_days: int, warnings: list[str]) -> None:
    for md in markdown_files(root / ".agents/skills"):
        for line in md.read_text().splitlines():
            if m := CHECKED.match(line):
                age = (today - datetime.date.fromisoformat(m[1])).days
                if age > max_age_days:
                    warnings.append(f"{md.relative_to(root).as_posix()}: checked {m[1]}, {age} days ago")


def check(root: pathlib.Path, today: datetime.date, max_age_days: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    check_skills(root, errors)
    check_text(root, errors)
    check_disclosure(root, errors)
    check_todo(root, errors)
    check_cards(root, errors)
    check_dates(root, today, max_age_days, warnings)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-age-days", type=int, default=90, help="warn when a reference was checked longer ago than this")
    args = parser.parse_args()
    errors, warnings = check(pathlib.Path.cwd(), datetime.date.today(), args.max_age_days)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
