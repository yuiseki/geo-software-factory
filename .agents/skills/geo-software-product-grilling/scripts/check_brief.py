#!/usr/bin/env python3
"""Check that a product brief is ready to hand from the day to the night, before an unattended run starts.

    python3 check_brief.py path/to/product-brief.md

Errors: a required section missing, or still the template's placeholder (<...>) or 未定, in the one-line summary,
the most important value, a Must feature, the place of the evaluation scenarios, and the decision policy. Then,
from the 準備したもの table, every backticked name in the 鍵と環境変数 row must be set in the environment, and
every backticked name in the 認証済みの CLI row must be on PATH. Values of variables are never read into the
report, only whether they are set. Whether a CLI is logged in is not checked here: run the 確かめ方 commands.

Prints a JSON report. Exit 0: ready. Exit 1: not ready.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"<[^>]*>")
BACKTICKED = re.compile(r"`([^`]+)`")


def sections(text: str) -> dict[str, str]:
    out, name, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if name is not None:
                out[name] = "\n".join(buf)
            name, buf = line[3:].strip(), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out[name] = "\n".join(buf)
    return out


def undecided(value: str) -> bool:
    v = value.strip()
    return not v or bool(PLACEHOLDER.search(v)) or v.startswith("未定")


def field(body: str, label: str) -> str | None:
    """The value after `label:` on a list line, up to the next sentence break of a 。."""
    for line in body.splitlines():
        m = re.match(rf"^\s*(?:-|\d+\.)\s*{re.escape(label)}\s*:\s*(.*)$", line)
        if m:
            return m.group(1).split("。")[0]
    return None


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        if line.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def check(path: Path, env=None) -> dict:
    env = os.environ if env is None else env
    s = sections(path.read_text(encoding="utf-8"))
    errors = []

    def need(item: str, value: str | None, why: str):
        if value is None or undecided(value):
            errors.append({"item": item, "why": why})

    for name in ("一行で", "提供する価値", "機能", "完成の条件", "判断の方針", "準備したもの"):
        if name not in s:
            errors.append({"item": name, "why": "節が無い"})

    if "一行で" in s:
        need("一行で", s["一行で"].strip().split("\n")[0] if s["一行で"].strip() else "", "誰の何をどう解くかが未定")
    if "提供する価値" in s:
        need("最重要の価値", field(s["提供する価値"], "最重要"), "価値の芯が未定")
    if "機能" in s:
        musts = [r[1] for r in table_rows(s["機能"]) if r and r[0] == "Must" and len(r) > 1]
        if not any(not undecided(m) for m in musts):
            errors.append({"item": "機能 Must", "why": "Must の機能が 1 つも決まっていない"})
    if "完成の条件" in s:
        need("評価のシナリオの置き場所", field(s["完成の条件"], "評価のシナリオの置き場所"),
             "シナリオが無いと、夜の評価者が判定できない")
    if "判断の方針" in s:
        for label in ("費用", "迷ったときの既定"):
            need(f"判断の方針 {label}", field(s["判断の方針"], label), "夜に聞く相手がいない")

    envs, clis = {}, {}
    for row in table_rows(s.get("準備したもの", "")):
        if len(row) < 2:
            continue
        if row[0].startswith("鍵と環境変数"):
            for n in BACKTICKED.findall(row[1]):
                envs[n] = bool(env.get(n))
        elif row[0].startswith("認証済みの CLI"):
            for n in BACKTICKED.findall(row[1]):
                clis[n] = shutil.which(n) is not None
    errors += [{"item": f"環境変数 {n}", "why": "設定されていない"} for n, ok in envs.items() if not ok]
    errors += [{"item": f"CLI {n}", "why": "PATH に無い"} for n, ok in clis.items() if not ok]

    return {"brief": str(path), "ok": not errors, "errors": errors, "env": envs, "cli": clis}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("brief", type=Path)
    r = check(ap.parse_args(argv).brief)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
