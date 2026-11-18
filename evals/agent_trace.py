"""What an agent read in a bench run, and how large its context was at each model call.

    python3 evals/agent_trace.py                     # one row per run of every agent
    python3 evals/agent_trace.py --task L4-plateau-light --files

The model reads its whole context again at every call, so the tokens a run reads are the sum of the context sizes of
its calls. The first call's context is the fixed part (system prompt, tool definitions, the task prompt); what the
agent reads afterwards (SKILL.md, references) grows the context and is read again at every later call.

What each log gives:
- OpenCode: tokens per step (input + cache read + cache write). A request larger than the server's context window
  does not reach the model; OpenCode logs it in stderr (`request (N tokens) exceeds the available context size`).
- Gemini (Antigravity CLI): tokens per agent response (input + cache read).
- Qoder: no token counts (they are 0); only the share of the context window (`context_usage_ratio`), whose size is
  not recorded with the Auto model.

A file counts as read when a tool input names it: a read tool's path, or a shell command that names the path, or
that changes into a skill directory and names the rest of the path. A grep over a directory does not count.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKILLS = ROOT / ".agents" / "skills"
OVERFLOW = re.compile(r"request \((\d+) tokens\) exceeds the available context size")
CD = re.compile(r"\bcd\s+[\"']?(\S*?\.agents/skills/[^\s;&|\"']+)")


def _events(text):
    for line in text.splitlines():
        try:
            yield json.loads(line)
        except ValueError:
            continue


def _text(x) -> str:
    return x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)


def parse(agent: str, text: str) -> dict:
    """{"context": [tokens per model call], "ratio": [share of the window per call], "tools": [{"tool", "input"}]}."""
    out = {"context": [], "ratio": [], "tools": []}
    if agent == "opencode":
        for e in _events(text):
            p = e.get("part") or {}
            if e.get("type") == "step_finish" and "tokens" in p:
                tk = p["tokens"]
                c = tk.get("cache") or {}
                out["context"].append(tk.get("input", 0) + c.get("read", 0) + c.get("write", 0))
            elif e.get("type") == "tool_use":
                out["tools"].append({"tool": p.get("tool"), "input": _text((p.get("state") or {}).get("input", {}))})
    elif agent == "gemini":
        seen = set()
        for e in _events(text):
            su = e.get("step_update") or {}
            if su.get("step_type") == "agent_response" and "usage" in su:
                u = su["usage"]
                out["context"].append(u.get("input_tokens", 0) + u.get("cache_read_tokens", 0))
            elif su.get("step_type") == "tool" and su.get("step_index") not in seen:
                seen.add(su.get("step_index"))
                out["tools"].append({"tool": su.get("tool_name"),
                                     "input": _text((su.get("tool_info") or {}).get("parameters", {}))})
    elif agent in ("qoder", "claude"):
        for e in _events(text):
            if e.get("type") != "assistant":
                continue
            m = e.get("message") or {}
            u = m.get("usage") or {}
            if "context_usage_ratio" in u:
                out["ratio"].append(u["context_usage_ratio"])
            elif u.get("input_tokens") or u.get("cache_read_input_tokens"):
                out["context"].append(u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                                      + u.get("cache_creation_input_tokens", 0))
            for b in m.get("content") or []:
                if b.get("type") == "tool_use":
                    out["tools"].append({"tool": b.get("name"), "input": _text(b.get("input", {}))})
    else:
        raise ValueError(f"no trace for agent {agent}")
    return out


def overflows(stderr: str) -> list[int]:
    """Sizes of the requests the server refused as larger than its context window, each size once, in order."""
    seen = []
    for m in OVERFLOW.finditer(stderr):
        n = int(m.group(1))
        if n not in seen:
            seen.append(n)
    return seen


def _names(text: str, path: str) -> bool:
    return re.search(r"(?<![\w.-])" + re.escape(path) + r"(?![\w.-])", text) is not None


def refs_read(inputs, known) -> list[str]:
    """Which of `known` (paths relative to .agents/skills) the tool inputs name, in the order first named."""
    got = []
    for text in inputs:
        bases = [m.group(1).split(".agents/skills/", 1)[1].rstrip("/") for m in CD.finditer(text)]
        for rel in known:
            if rel in got:
                continue
            hit = ("skills/" + rel) in text
            for b in bases:
                if not hit and rel.startswith(b + "/") and _names(text, rel[len(b) + 1:]):
                    hit = True
            if hit:
                got.append(rel)
    return got


def summary(context: list[int]) -> dict:
    if not context:
        return {"calls": 0, "fixed": 0, "peak": 0, "read": 0}
    return {"calls": len(context), "fixed": context[0], "peak": max(context), "read": sum(context)}


def known_paths(root: Path = SKILLS) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*.md"))


def main():
    sys.path.insert(0, str(HERE))
    import bench

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--agent")
    ap.add_argument("--cond")
    ap.add_argument("--task")
    ap.add_argument("--model")
    ap.add_argument("--files", action="store_true", help="list the skill files each run read")
    a = ap.parse_args()
    spec = bench.load_spec()
    known = known_paths()
    cols = ["agent", "model", "cond", "task", "rep", "outcome", "calls", "fixed", "peak", "read", "ratio_first",
            "ratio_peak", "overflow", "n_files"]
    print("\t".join(cols))
    for m in sorted((bench.WORK / "runs").glob("*/*/*/meta.json")):
        meta = json.loads(m.read_text())
        if any(v and meta.get(k) != v for k, v in (("agent", a.agent), ("cond", a.cond), ("task", a.task),
                                                     ("model", a.model))):
            continue
        d = m.parent
        log = (d / "log.jsonl").read_text(errors="replace") if (d / "log.jsonl").exists() else ""
        err = (d / "stderr.log").read_text(errors="replace") if (d / "stderr.log").exists() else ""
        try:
            t = parse(meta["agent"], log)
        except ValueError:
            continue
        s = summary(t["context"])
        files = refs_read([x["input"] for x in t["tools"]], known)
        row = [meta["agent"], meta.get("model", "-"), meta["cond"], meta["task"], meta["rep"],
               bench.outcome_of(spec, d, meta)[0], s["calls"], s["fixed"], s["peak"], s["read"],
               f"{t['ratio'][0]:.3f}" if t["ratio"] else "-", f"{max(t['ratio']):.3f}" if t["ratio"] else "-",
               ",".join(map(str, overflows(err))) or "-", len(files)]
        print("\t".join(str(v) for v in row))
        if a.files:
            for f in files:
                print(f"\t{f}")


if __name__ == "__main__":
    main()
