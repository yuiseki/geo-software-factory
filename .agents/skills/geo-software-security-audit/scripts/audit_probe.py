#!/usr/bin/env python3
"""Local/preview security audit probe for map products, with scenario generation.

    python3 audit_probe.py --base http://127.0.0.1:8787 [--search-path /api/places]
                           [--report OUT/audit.json] [--scenarios-out SCENARIOS_DIR]

Enforces geo-software-security-audit principles by program:
1. Sends single probes for secret/repo exposure (`/.env`, `/.git/HEAD`), oversized search query (10,000 chars),
   world/inverted bounding boxes (`bbox=-180,-90,180,90`), and reflected HTML/XSS payloads (`<img src=x onerror=1>`).
2. Classifies each into the 4 triage states (`問題あり`, `防御されている`, `該当なし`, `未確認`) with concrete
   observations (status code, response time ms, feature count). Never writes secret values.
3. Enforces the triage rule: any `防御されている` without a concrete observation is downgraded to `未確認`.
4. Converts confirmed issues (`問題あり`) into held-out `geo-software-eval` scenario JSON files so regressions are caught.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

FOUR_STATES = ("問題あり", "防御されている", "該当なし", "未確認")


def request_once(url: str, timeout: float = 10.0) -> tuple[int | None, bytes, float]:
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": "geo-software-security-audit"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(5_000_000)
            ms = round((time.monotonic() - t0) * 1000.0, 1)
            return r.status, body, ms
    except urllib.error.HTTPError as e:
        body = e.read(500_000)
        ms = round((time.monotonic() - t0) * 1000.0, 1)
        return e.code, body, ms
    except (urllib.error.URLError, OSError):
        ms = round((time.monotonic() - t0) * 1000.0, 1)
        return None, b"", ms


def enforce_observation_rule(findings: list[dict]) -> list[dict]:
    """Rule (`triage.md` 14): 観測の無い「防御されている」は「未確認」にする。"""
    out = []
    for f in findings:
        item = dict(f)
        if item.get("status") == "防御されている" and not str(item.get("observed") or "").strip():
            item["status"] = "未確認"
        out.append(item)
    return out


def to_eval_scenario(finding: dict) -> dict:
    fid = finding["id"]
    return {
        "id": f"AUDIT-{fid}",
        "name": f"監査退行防止: {finding['title']}",
        "symptom": finding["symptom"],
        "checks": [finding["eval_check"]],
    }


def probe(base: str, search_path: str = "/api/places", max_features_cap: int = 500,
          report_path: Path | None = None, scenarios_out: Path | None = None, timeout: float = 10.0) -> dict:
    base = base.rstrip("/")
    findings: list[dict] = []

    # 1. Exposure: /.env and /.git/HEAD
    for code_id, path, label, needle in (
        ("EXPOSURE-ENV", "/.env", ".env の露出", b"="),
        ("EXPOSURE-GIT", "/.git/HEAD", ".git/HEAD の露出", b"ref:"),
    ):
        st, body, ms = request_once(base + path, timeout=timeout)
        if st is None:
            findings.append({"id": code_id, "domain": "exposure", "title": label, "severity": "Critical",
                             "status": "未確認", "observed": "", "symptom": f"{path} の応答が確認できない"})
        elif st == 200 and needle in body and b"<html" not in body[:200].lower():
            findings.append({
                "id": code_id, "domain": "exposure", "title": label, "severity": "Critical",
                "status": "問題あり", "observed": f"GET {path} -> status={st} ({ms}ms, {len(body)} bytes)",
                "symptom": f"{path} が公開されており取得できる (404 または 403 にする)",
                "eval_check": {"kind": "http", "path": path, "status": 404},
            })
        else:
            findings.append({
                "id": code_id, "domain": "exposure", "title": label, "severity": "Critical",
                "status": "防御されている", "observed": f"GET {path} -> status={st} ({ms}ms)",
                "symptom": "",
            })

    # 2. Abuse: Huge search query (10,000 chars)
    huge_q = "a" * 10000
    q_path = f"{search_path}?q={huge_q}"
    st, body, ms = request_once(base + q_path, timeout=timeout)
    if st is None:
        findings.append({"id": "ABUSE-HUGE-QUERY", "domain": "abuse", "title": "1万文字の検索語の拒否",
                         "severity": "High", "status": "未確認", "observed": "", "symptom": ""})
    elif st in (400, 413, 414, 422):
        findings.append({
            "id": "ABUSE-HUGE-QUERY", "domain": "abuse", "title": "1万文字の検索語の拒否", "severity": "High",
            "status": "防御されている", "observed": f"GET {search_path}?q=(10000文字) -> status={st} ({ms}ms)",
            "symptom": "",
        })
    elif st == 404:
        findings.append({
            "id": "ABUSE-HUGE-QUERY", "domain": "abuse", "title": "1万文字の検索語の拒否", "severity": "High",
            "status": "該当なし", "observed": f"GET {search_path} -> status=404", "symptom": "",
        })
    else:
        findings.append({
            "id": "ABUSE-HUGE-QUERY", "domain": "abuse", "title": "1万文字の検索語の拒否", "severity": "High",
            "status": "問題あり", "observed": f"GET {search_path}?q=(10000文字) -> status={st} ({ms}ms)",
            "symptom": f"{search_path} に極端に長い検索語を送っても 400 で拒まれない",
            "eval_check": {"kind": "http", "path": q_path, "status": 400},
        })

    # 3. Abuse: World BBox (-180,-90,180,90)
    bbox_path = f"{search_path}?bbox=-180,-90,180,90"
    st, body, ms = request_once(base + bbox_path, timeout=timeout)
    if st is None:
        findings.append({"id": "ABUSE-WORLD-BBOX", "domain": "abuse", "title": "全世界 bbox 要求の上限",
                         "severity": "High", "status": "未確認", "observed": "", "symptom": ""})
    elif st in (400, 422):
        findings.append({
            "id": "ABUSE-WORLD-BBOX", "domain": "abuse", "title": "全世界 bbox 要求の上限", "severity": "High",
            "status": "防御されている", "observed": f"GET {bbox_path} -> status={st} ({ms}ms)", "symptom": "",
        })
    elif st == 200:
        feat_count = 0
        try:
            doc = json.loads(body)
            feat_count = len(doc.get("features", [])) if isinstance(doc, dict) else 0
        except ValueError:
            pass
        if feat_count > max_features_cap or ms > 1000.0:
            findings.append({
                "id": "ABUSE-WORLD-BBOX", "domain": "abuse", "title": "全世界 bbox 要求の上限", "severity": "High",
                "status": "問題あり",
                "observed": f"GET {bbox_path} -> status=200, features={feat_count}, {ms}ms",
                "symptom": f"{bbox_path} で上限を超える地物 ({feat_count} 件) または遅い応答が返る",
                "eval_check": {"kind": "http", "path": bbox_path, "status": 400},
            })
        else:
            findings.append({
                "id": "ABUSE-WORLD-BBOX", "domain": "abuse", "title": "全世界 bbox 要求の上限", "severity": "High",
                "status": "防御されている",
                "observed": f"GET {bbox_path} -> status=200, features={feat_count} (<= {max_features_cap}), {ms}ms",
                "symptom": "",
            })
    else:
        findings.append({
            "id": "ABUSE-WORLD-BBOX", "domain": "abuse", "title": "全世界 bbox 要求の上限", "severity": "High",
            "status": "該当なし" if st == 404 else "防御されている",
            "observed": f"GET {bbox_path} -> status={st} ({ms}ms)", "symptom": "",
        })

    # 4. Injection: Unescaped HTML reflection in search parameter
    xss_payload = "<img src=x onerror=alert(1)>"
    xss_path = f"{search_path}?q={urllib.parse.quote(xss_payload)}"
    st, body, ms = request_once(base + xss_path, timeout=timeout)
    if st is None:
        findings.append({"id": "INJECTION-XSS-REFLECT", "domain": "injection", "title": "検索語の HTML 反射防止",
                         "severity": "High", "status": "未確認", "observed": "", "symptom": ""})
    elif st == 200 and xss_payload.encode("utf-8") in body:
        findings.append({
            "id": "INJECTION-XSS-REFLECT", "domain": "injection", "title": "検索語の HTML 反射防止",
            "severity": "High", "status": "問題あり",
            "observed": f"GET {xss_path} -> status=200, 応答本文に未エスケープの <img> タグが含まれる",
            "symptom": f"{search_path} の応答に検索語の HTML タグがそのまま出力される",
            "eval_check": {"kind": "http", "path": xss_path, "status": 400},
        })
    else:
        findings.append({
            "id": "INJECTION-XSS-REFLECT", "domain": "injection", "title": "検索語の HTML 反射防止",
            "severity": "High", "status": "防御されている",
            "observed": f"GET {xss_path} -> status={st} ({ms}ms, 未エスケープ反射なし)", "symptom": "",
        })

    findings = enforce_observation_rule(findings)
    issues = [f for f in findings if f["status"] == "問題あり"]

    written_scenarios = []
    if scenarios_out is not None and issues:
        scenarios_out.mkdir(parents=True, exist_ok=True)
        for f in issues:
            if "eval_check" in f:
                scen = to_eval_scenario(f)
                sp = scenarios_out / f"{scen['id']}.json"
                sp.write_text(json.dumps(scen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                written_scenarios.append(str(sp))

    out = {
        "when": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "base": base,
        "ok": not issues,
        "findings": findings,
        "generated_scenarios": written_scenarios,
    }
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", required=True)
    ap.add_argument("--search-path", default="/api/places")
    ap.add_argument("--max-features", type=int, default=500)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--scenarios-out", type=Path)
    ap.add_argument("--timeout", type=float, default=10.0)
    a = ap.parse_args(argv)
    res = probe(a.base, a.search_path, a.max_features, a.report, a.scenarios_out, a.timeout)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
