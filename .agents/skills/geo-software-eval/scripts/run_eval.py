#!/usr/bin/env python3
"""Run held-out scenarios against a running app, and hand the implementer symptoms only.

    python3 run_eval.py --scenarios DIR --base http://127.0.0.1:8787 --app-repo PATH \
                        --report OUT/report.json [--feedback PATH/eval-feedback.md]

The evaluator runs this, never the implementer. Scenarios are JSON files outside the app repository:

    {"id": "S1", "name": "...", "symptom": "one line the implementer may read",
     "checks": [{"kind": "http", "path": "/", "status": 200, "contains": "OpenStreetMap"},
                {"kind": "geojson", "path": "/places.geojson", "bbox": [W, S, E, N], "min_features": 10,
                 "require": ["name"]},
                {"kind": "command", "run": ["npx", "playwright", "test", "s1.spec.ts"], "timeout": 300}]}

A command runs in the scenario directory with EVAL_BASE_URL set, passes on exit 0, and may print lines starting
with "OBSERVED:" for the implementer; the rest of its output stays in the report.

Separation is enforced, not promised (with --app-repo; in the isolated containers of assets/isolation/ the mounts
do it, and the version comes from --version): it refuses scenarios or a report inside the app repository (they hold the
thresholds), and a feedback file outside it. The feedback names the version judged, each failed scenario's
symptom line, the paths requested and what was observed there (status, feature count, error codes), and never
the scenario's name, expected values or thresholds. The report holds everything, for the morning.

Exit 0: every scenario passed. Exit 1: a scenario failed or could not be judged. Exit 2: refused.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import geocheck  # noqa: E402

OBSERVED = "OBSERVED:"


class Refused(Exception):
    pass


def inside(path: Path, root: Path) -> bool:
    path, root = path.resolve(), root.resolve()
    return path == root or root in path.parents


def fetch(url: str, timeout: float):
    req = urllib.request.Request(url, headers={"User-Agent": "geo-software-eval"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(20_000_000)
    except urllib.error.HTTPError as e:
        return e.code, e.read(1_000_000)
    except (urllib.error.URLError, OSError) as e:
        return None, str(e).encode()


def run_check(c: dict, base: str, cwd: Path, timeout: float) -> dict:
    """Returns {"ok": bool|None, "full": everything, "observed": what the implementer may read}."""
    kind = c.get("kind")
    if kind in ("http", "geojson"):
        path = c.get("path", "/")
        status, body = fetch(base + path, timeout)
        observed = {"kind": kind, "path": path, "status": status}
        if status is None:
            observed["status"] = "応答なし"
            return {"ok": False, "full": {**c, "error": body.decode(errors="replace")[:300]}, "observed": observed}
        if kind == "http":
            ok = status == c.get("status", 200)
            if ok and "contains" in c:
                ok = c["contains"].encode() in body
                if not ok:
                    observed["body"] = "期待した文言が無い"
            return {"ok": ok, "full": {**c, "got_status": status}, "observed": observed}
        if status != 200:
            return {"ok": False, "full": {**c, "got_status": status}, "observed": observed}
        try:
            doc = json.loads(body)
        except ValueError:
            observed["body"] = "JSON として読めない"
            return {"ok": False, "full": c, "observed": observed}
        rep = geocheck.check(doc, expect_bbox=c.get("bbox"), require_props=c.get("require", ()),
                             min_features=c.get("min_features", 0), allow_empty=c.get("allow_empty", False))
        observed.update(features=rep["features"], errors=[e["code"] for e in rep["errors"]])
        return {"ok": not rep["errors"], "full": {**c, "geocheck": rep}, "observed": observed}
    if kind == "command":
        try:
            p = subprocess.run(c["run"], cwd=cwd, capture_output=True, text=True,
                               timeout=c.get("timeout", 300), env={**os.environ, "EVAL_BASE_URL": base})
        except subprocess.TimeoutExpired:
            return {"ok": False, "full": {**c, "error": "timeout"}, "observed": {"kind": kind, "result": "時間切れ"}}
        except OSError as e:
            return {"ok": None, "full": {**c, "error": str(e)}, "observed": {"kind": kind}}
        lines = [ln[len(OBSERVED):].strip() for ln in p.stdout.splitlines() if ln.startswith(OBSERVED)]
        return {"ok": p.returncode == 0,
                "full": {**c, "exit": p.returncode, "stdout": p.stdout[-20_000:], "stderr": p.stderr[-20_000:]},
                "observed": {"kind": kind, "exit": p.returncode, "observed": lines}}
    return {"ok": None, "full": {**c, "error": f"unknown kind {kind!r}"}, "observed": {"kind": str(kind)}}


def git_rev(repo: Path) -> str:
    p = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    dirty = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout
    rev = p.stdout.strip() if p.returncode == 0 else "コミットなし"
    return rev + (" (未コミットの変更あり)" if dirty.strip() else "")


def describe(o: dict) -> str:
    if o["kind"] == "command":
        head = "時間切れ" if o.get("result") == "時間切れ" else f"終了コード {o.get('exit')}"
        return "; ".join([head] + o.get("observed", []))
    if "path" not in o:
        return f"判定できない確かめの種類 ({o['kind']})"
    parts = [f"{o['path']}: 状態 {o['status']}"]
    if "features" in o:
        parts.append(f"地物 {o['features']} 件")
    if o.get("errors"):
        parts.append("検出: " + ", ".join(o["errors"]))
    if "body" in o:
        parts.append(o["body"])
    return "、".join(parts)


def run(scenarios: Path, base: str, app_repo: Path | None, report: Path, feedback: Path | None = None,
        timeout: float = 15, version: str | None = None) -> dict:
    if app_repo is not None:
        if inside(scenarios, app_repo):
            raise Refused("シナリオが実装のリポジトリの中にある。外に置く")
        if inside(report, app_repo):
            raise Refused("報告には閾値が入るので、実装のリポジトリの外に書く")
        if feedback is not None and not inside(feedback, app_repo):
            raise Refused("症状の返し先は、実装のリポジトリの中にする")
    else:
        # Isolated containers: the feedback directory is the only one shared with the implementer.
        if version is None:
            raise Refused("実装のリポジトリが無いときは、判定する版を --version で渡す")
        if feedback is not None and (inside(feedback, scenarios) or inside(feedback, report.parent)):
            raise Refused("症状の返し先を、シナリオや報告と同じ場所に置かない")
    base = base.rstrip("/")
    rev = version if version is not None else git_rev(app_repo)
    results = []
    for f in sorted(scenarios.glob("*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        checks = [run_check(c, base, scenarios, timeout) for c in s.get("checks", [])]
        if not checks or any(c["ok"] is None for c in checks):
            result = "error"
        else:
            result = "pass" if all(c["ok"] for c in checks) else "fail"
        results.append({"id": s.get("id", f.stem), "name": s.get("name"), "symptom": s.get("symptom", ""),
                        "result": result, "checks": checks})
    ok = bool(results) and all(r["result"] == "pass" for r in results)
    when = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out = {"when": when, "base": base, "version": rev, "ok": ok, "scenarios": results}
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    if feedback is not None:
        feedback.write_text(render_feedback(out), encoding="utf-8")
    return out


def render_feedback(out: dict) -> str:
    lines = ["# 評価の症状", "", f"- 判定した版: {out['version']}", f"- 判定した時刻: {out['when']}",
             f"- 結果: {sum(r['result'] == 'pass' for r in out['scenarios'])}/{len(out['scenarios'])} 合格", ""]
    if not out["scenarios"]:
        lines.append("シナリオが 1 本も無かった。評価は済んでいない。")
    for r in out["scenarios"]:
        if r["result"] == "pass":
            continue
        lines.append(f"## {r['id']}: {r['symptom'] or '症状の説明なし'}")
        if r["result"] == "error":
            lines.append("- 評価そのものが動かなかった。実装の不具合とは限らない")
        for c in r["checks"]:
            if c["ok"] is not True:
                lines.append(f"- {describe(c['observed'])}")
        lines.append("")
    if out["ok"]:
        lines.append("全シナリオ合格。")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scenarios", type=Path, required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--app-repo", type=Path, help="omit only in the isolated containers, with --version")
    ap.add_argument("--version", help="the version judged, when there is no app repo to ask")
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--feedback", type=Path)
    ap.add_argument("--timeout", type=float, default=15)
    a = ap.parse_args(argv)
    try:
        out = run(a.scenarios, a.base, a.app_repo, a.report, a.feedback, a.timeout, a.version)
    except Refused as e:
        print(json.dumps({"refused": str(e)}, ensure_ascii=False))
        return 2
    print(json.dumps({"ok": out["ok"], "version": out["version"],
                      "results": {r["id"]: r["result"] for r in out["scenarios"]}}, ensure_ascii=False))
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
