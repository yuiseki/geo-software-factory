#!/usr/bin/env python3
"""Pre-deploy gate and release rollback ledger for Dark Factory deployments.

    python3 deploy_gate.py check    --app-repo PATH --eval-report OUT/final.json [--audit-report OUT/audit.json]
                                    [--block-severity High] [--migration FILE ...]
    python3 deploy_gate.py record   --ledger OUT/releases.json --version VER --commit SHA [--url URL]
    python3 deploy_gate.py rollback --ledger OUT/releases.json

Enforces geo-software-deploy/SKILL.md and references/preflight.md by program:
1. Refuses deployment if the git working tree has uncommitted changes ("戻る点を仕組みで作る").
2. Refuses deployment unless `eval_report` has `ok: true` and its `version` matches `HEAD` of `app_repo`.
3. Refuses deployment if `audit_report` has any finding with status `問題あり` at or above `block_severity`.
4. Refuses destructive SQL migrations (`DROP`, `DELETE FROM`, `TRUNCATE`, `ALTER ... DROP`) unless explicitly approved.
5. Pairs each deployed version ID with its git commit SHA in a ledger so rollback knows the exact prior version.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}
DESTRUCTIVE_SQL = re.compile(
    r"\b(DROP\s+TABLE|DROP\s+COLUMN|DROP\s+INDEX|TRUNCATE\s+TABLE|DELETE\s+FROM|ALTER\s+TABLE\s+\S+\s+DROP)\b",
    re.IGNORECASE,
)


def git_state(app_repo: Path) -> tuple[str | None, str | None, bool]:
    if not (app_repo / ".git").exists():
        return None, None, True
    short = subprocess.run(["git", "-C", str(app_repo), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True)
    full = subprocess.run(["git", "-C", str(app_repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    dirty = subprocess.run(["git", "-C", str(app_repo), "status", "--porcelain"],
                           capture_output=True, text=True)
    if short.returncode != 0:
        return None, None, True
    return short.stdout.strip(), full.stdout.strip(), bool(dirty.stdout.strip())


def check(app_repo: Path, eval_report: Path, audit_report: Path | None = None,
          block_severity: str = "High", migrations: list[Path] | None = None) -> dict:
    errors: list[dict] = []
    short_head, full_head, dirty = git_state(app_repo)
    if short_head is None:
        errors.append({"code": "no_git_head", "message": "app_repo に git の HEAD コミットが無い"})
    if dirty:
        errors.append({"code": "dirty_tree", "message": "作業ツリーに未コミットの変更がある (コミットしてからデプロイする)"})

    if not eval_report.is_file():
        errors.append({"code": "missing_eval", "message": f"評価の報告が無い: {eval_report}"})
    else:
        try:
            ev = json.loads(eval_report.read_text(encoding="utf-8"))
        except ValueError as e:
            errors.append({"code": "invalid_eval", "message": f"評価の報告が JSON として読めない: {e}"})
            ev = {}
        ev_ver = str(ev.get("version") or "").strip()
        if short_head and ev_ver and not (ev_ver == short_head or ev_ver == full_head or (full_head and full_head.startswith(ev_ver))):
            errors.append({
                "code": "version_mismatch",
                "message": f"評価した版 ({ev_ver}) と出す版 ({short_head}) が一致しない。評価をやり直してから出す",
            })
        if not ev.get("ok"):
            errors.append({"code": "eval_failed", "message": "評価の全シナリオが合格していない (ok=false)"})

    if audit_report is not None and audit_report.is_file():
        threshold = SEVERITY_RANK.get(block_severity.lower(), 3)
        aud = json.loads(audit_report.read_text(encoding="utf-8"))
        for f in aud.get("findings", []):
            status = str(f.get("status") or "")
            sev = str(f.get("severity") or "High")
            if status in ("問題あり", "open", "vulnerable") and SEVERITY_RANK.get(sev.lower(), 3) >= threshold:
                errors.append({
                    "code": "audit_blocked",
                    "message": f"公開を止める深刻度 ({sev}) の監査指摘が残っている: {f.get('id', '')} {f.get('title', '')}",
                })

    for mig in migrations or []:
        if mig.is_file():
            sql = mig.read_text(encoding="utf-8", errors="replace")
            m = DESTRUCTIVE_SQL.search(sql)
            if m:
                errors.append({
                    "code": "destructive_migration",
                    "message": f"{mig.name}: 取り消せない SQL ({m.group(1)}) を含む。昼の承認が無ければ当てない",
                })

    return {
        "ok": not errors,
        "head": short_head,
        "dirty": dirty,
        "errors": errors,
    }


def record_release(ledger_path: Path, version: str, commit: str, url: str = "") -> dict:
    releases = json.loads(ledger_path.read_text(encoding="utf-8")) if ledger_path.is_file() else []
    previous = releases[-1] if releases else None
    entry = {
        "version": version,
        "commit": commit,
        "url": url,
        "deployed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    releases.append(entry)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(releases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"current": entry, "previous": previous}


def rollback_target(ledger_path: Path) -> dict | None:
    if not ledger_path.is_file():
        return None
    releases = json.loads(ledger_path.read_text(encoding="utf-8"))
    if len(releases) < 2:
        return None
    return releases[-2]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="subcmd", required=True)

    p_chk = sub.add_parser("check", help="verify clean git tree, matching passing eval report, and audit/migrations")
    p_chk.add_argument("--app-repo", type=Path, required=True)
    p_chk.add_argument("--eval-report", type=Path, required=True)
    p_chk.add_argument("--audit-report", type=Path)
    p_chk.add_argument("--block-severity", default="High")
    p_chk.add_argument("--migration", dest="migrations", type=Path, action="append", default=[])

    p_rec = sub.add_parser("record", help="record a deployed version ID and commit SHA pair")
    p_rec.add_argument("--ledger", type=Path, required=True)
    p_rec.add_argument("--version", required=True)
    p_rec.add_argument("--commit", required=True)
    p_rec.add_argument("--url", default="")

    p_rb = sub.add_parser("rollback", help="print the previous release version and commit SHA for rollback")
    p_rb.add_argument("--ledger", type=Path, required=True)

    a = ap.parse_args(argv)
    if a.subcmd == "check":
        res = check(a.app_repo, a.eval_report, a.audit_report, a.block_severity, a.migrations)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res["ok"] else 1
    if a.subcmd == "record":
        res = record_release(a.ledger, a.version, a.commit, a.url)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    if a.subcmd == "rollback":
        target = rollback_target(a.ledger)
        print(json.dumps({"rollback": target}, ensure_ascii=False, indent=2))
        return 0 if target else 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
