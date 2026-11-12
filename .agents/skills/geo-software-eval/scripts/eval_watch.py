#!/usr/bin/env python3
"""The evaluator's loop in the isolated containers (assets/isolation/): wait for the implementer's request, judge,
answer with symptoms.

    python3 eval_watch.py --handoff /eval/handoff --scenarios /eval/scenarios --report-dir /eval/out \
                          --feedback /eval/feedback/eval-feedback.md [--app-host implementer] [--interval 10]

The implementer asks for an evaluation by writing handoff/ready.json:

    {"rev": "<git commit, 7 to 40 hex>", "port": 8787}     (add "nonce": n to ask again for the same version)

The evaluator decides where to look: http://<app-host>:<port>. Anything else in the request is ignored, so the
implementer cannot point the evaluator at another place. Each new request (by content) is judged once with
run_eval.py; the full report goes to the report directory, the symptoms to the feedback file. A malformed request
is answered in the feedback file and not judged.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import run_eval  # noqa: E402

REV = re.compile(r"^[0-9a-f]{7,40}$")


def once(handoff: Path, scenarios: Path, report_dir: Path, feedback: Path, app_host: str = "implementer"):
    req_file = handoff / "ready.json"
    if not req_file.is_file():
        return None
    raw = req_file.read_bytes()
    key = hashlib.sha256(raw).hexdigest()
    state_file = report_dir / "watch-state.json"
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
    if state.get("last") == key:
        return None
    state["last"] = key
    state_file.write_text(json.dumps(state), encoding="utf-8")
    try:
        req = json.loads(raw)
        rev, port = req["rev"], req["port"]
        if not (isinstance(rev, str) and REV.match(rev)) or not (isinstance(port, int) and 0 < port < 65536):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        if run_eval.inside(feedback, scenarios) or run_eval.inside(feedback, report_dir):
            raise run_eval.Refused("症状の返し先を、シナリオや報告と同じ場所に置かない")
        feedback.write_text("# 評価の症状\n\n依頼の形が違うので評価していない。handoff/ready.json は "
                            '{"rev": "<7〜40 桁の 16 進のコミット>", "port": <1〜65535 の整数>} にする。\n',
                            encoding="utf-8")
        return {"refused": True}
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return run_eval.run(scenarios=scenarios, base=f"http://{app_host}:{port}", app_repo=None,
                        report=report_dir / f"{stamp}-{rev}.json", feedback=feedback, version=rev)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--handoff", type=Path, required=True)
    ap.add_argument("--scenarios", type=Path, required=True)
    ap.add_argument("--report-dir", type=Path, required=True)
    ap.add_argument("--feedback", type=Path, required=True)
    ap.add_argument("--app-host", default="implementer")
    ap.add_argument("--interval", type=float, default=10)
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args(argv)
    while True:
        r = once(a.handoff, a.scenarios, a.report_dir, a.feedback, a.app_host)
        if r is not None:
            print(json.dumps({k: r.get(k) for k in ("version", "ok", "refused")}, ensure_ascii=False), flush=True)
        if a.once:
            return 0
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
