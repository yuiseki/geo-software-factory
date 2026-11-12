#!/usr/bin/env python3
"""Hooks for an unattended coding agent (Claude Code hook protocol: JSON on stdin, JSON on stdout).

    python3 hooks.py stop-switch   # PreToolUse: deny every tool while the stop file exists
    python3 hooks.py deliver       # PostToolUse: hand over new evaluation feedback and deadline reminders
    python3 hooks.py stop-guard    # Stop: before the deadline, send it back with one unused checklist item

Configured by environment variables, so the same script serves every run:

    RUN_STATE_DIR         required; this run's own directory outside the work tree, for what was delivered
    AGENT_STOP_FILE       stop-switch: while this file exists, every tool is denied. Unset also denies (fail closed)
    EVAL_FEEDBACK         deliver: the symptoms file the evaluator writes (run_eval.py --feedback)
    RUN_DEADLINE          ISO 8601 end of the run; reminders at 60, 30 and 10 minutes left and after the end
    STOP_GUARD_CHECKLIST  stop-guard: a file of one item per line (past winning moves, unchecked angles)
    STOP_GUARD_MAX        stop-guard: the most times it sends the agent back in one run (default 3)

Why: an agent trims long command output and missed a summary appended there most of the time, while the same
summary injected after each tool call was read almost always; a Stop hook that sends the agent back for the same
reason again and again burns tokens fast. See references/unattended-runs.md.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

MAX_CONTEXT = 8000
REMINDERS = (60, 30, 10)


def state_dir(env) -> Path:
    d = env.get("RUN_STATE_DIR")
    if not d:
        raise SystemExit("RUN_STATE_DIR is not set: give each run its own state directory outside the work tree")
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    return p


def load(env) -> dict:
    f = state_dir(env) / "hooks-state.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def save(env, st: dict) -> None:
    (state_dir(env) / "hooks-state.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def deadline(env):
    d = env.get("RUN_DEADLINE")
    return datetime.datetime.fromisoformat(d) if d else None


def stop_switch(payload, env, now):
    f = env.get("AGENT_STOP_FILE")
    if f and not Path(f).exists():
        return None
    why = "停止スイッチが入っている" if f else "AGENT_STOP_FILE が設定されていないので、止めた側に倒している"
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                   "permissionDecisionReason": f"{why}。作業を止め、ここまでを記録して終える。"}}


def deliver(payload, env, now):
    st = load(env)
    parts = []
    fb = env.get("EVAL_FEEDBACK")
    if fb and Path(fb).is_file():
        text = Path(fb).read_text(encoding="utf-8")
        digest = hashlib.sha256(text.encode()).hexdigest()
        if digest != st.get("feedback"):
            st["feedback"] = digest
            if len(text) > MAX_CONTEXT - 300:
                text = text[: MAX_CONTEXT - 300] + f"\n(以下略。全文は {fb})"
            parts.append("評価者から新しい症状が届いた。直す前に読む。\n\n" + text)
    end = deadline(env)
    if end is not None:
        left = (end - now).total_seconds() / 60
        sent = set(st.get("reminders", []))
        if left <= 0 and "end" not in sent:
            sent.add("end")
            parts.append("終わりの時刻を過ぎた。裏で回している計測や定期の処理を止め、コミットし、朝の報告を書いて終える。")
        else:
            due = [m for m in REMINDERS if left <= m and str(m) not in sent]
            if due:
                sent.update(str(m) for m in due)
                m = min(due)
                parts.append(f"終わりまで残り {m} 分を切った (残り約 {int(left)} 分)。"
                             "大きな変更は始めず、評価を動かし直し、コミットし、裏の処理を止める準備をする。")
        st["reminders"] = sorted(sent)
    save(env, st)
    if not parts:
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "\n\n".join(parts)}}


def stop_guard(payload, env, now):
    end = deadline(env)
    if end is None or now >= end:
        return None
    st = load(env)
    used = st.get("stop_reasons", [])
    if len(used) >= int(env.get("STOP_GUARD_MAX", "3")):
        return None
    cl = env.get("STOP_GUARD_CHECKLIST")
    items = [x.strip() for x in Path(cl).read_text(encoding="utf-8").splitlines() if x.strip()] if cl else []
    unused = [x for x in items if x not in used]
    if not unused:
        return None
    st["stop_reasons"] = used + [unused[0]]
    save(env, st)
    return {"decision": "block", "reason": unused[0]}


EVENTS = {"stop-switch": stop_switch, "deliver": deliver, "stop-guard": stop_guard}


def main(argv=None, stdin=None, env=None, now=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    env = os.environ if env is None else env
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if len(argv) != 1 or argv[0] not in EVENTS:
        print(f"usage: hooks.py {{{','.join(EVENTS)}}}", file=sys.stderr)
        return 2
    raw = (stdin or sys.stdin).read()
    payload = json.loads(raw) if raw.strip() else {}
    out = EVENTS[argv[0]](payload, env, now)
    if out is not None:
        print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
