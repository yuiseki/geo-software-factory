"""Measure whether the skills of this repository make coding agents build and decide better, against the same
agents without them.

    python3 evals/bench.py make                                              # tasks and truths, from bench.json
    python3 evals/bench.py run --agent opencode --cond skills --task B1-taito-plane-ix [--rep 1]
    python3 evals/bench.py score > results.tsv

Run from the repository root. Work goes to tmp/evals-bench/ (tasks/<id>/{task,truth}, runs/<agent>/<cond>/<id>-r<rep>/).
The agent sees only its workdir: the task material and, with the skills, a git archive of the repository without
evals/. Truths never enter it. The runners mount only that workdir into a container with fixed CPU, memory and
process limits and a time limit. `make` needs pyproj (uv run --with pyproj python3 evals/bench.py make).

Outcomes: accurate, inaccurate (with reasons), declared_failure, invalid_answer, no_answer, timeout (cut off with
nothing to grade); on a negative task correct_reject or false_accept. provider_error (the runner failed with
nothing to grade) is not the agent's outcome: run it again with another --rep, do not grade it.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = ROOT / "tmp" / "evals-bench"
sys.path.insert(0, str(ROOT / ".agents/skills/geo-software-eval/scripts"))
import geocheck  # noqa: E402

RUNNERS = {"opencode": HERE / "run_opencode_docker.sh", "codex": HERE / "run_codex_docker.sh"}
PUBLIC_OSM = re.compile(r"https?://((?:[a-z]\.)?tile\.openstreetmap\.org|nominatim\.openstreetmap\.org|overpass-api\.de|"
                        r"overpass\.kumi\.systems|api\.openstreetmap\.org)/")
ATTRIBUTION = re.compile(r"OpenStreetMap", re.I)


def load_spec() -> dict:
    return json.loads((HERE / "bench.json").read_text(encoding="utf-8"))


def fill_prompt(template: str, workdir: str, skills: bool, minutes: int) -> str:
    s = re.sub(r"\{\{#SKILLS\}\}\n?(.*?)\{\{/SKILLS\}\}\n?", (lambda m: m.group(1)) if skills else "", template, flags=re.S)
    return s.replace("{{WORKDIR}}", workdir).replace("{{MINUTES}}", str(minutes))


def prepare_workdir(repo: Path, rev: str, dest: Path, task_dir: Path, skills: bool) -> Path:
    """The agent's whole world: task/ and, with the skills, the repository at `rev` without evals/."""
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} is not empty; refusing to write into it")
    leaks = [p.name for p in Path(task_dir).rglob("*") if p.name in ("truth.json", "key.json", "truth")]
    if leaks:
        raise SystemExit(f"the task material holds evaluation material: {leaks}")
    dest.mkdir(parents=True, exist_ok=True)
    if skills:
        tar = subprocess.run(["git", "-C", str(repo), "archive", "--format=tar", rev], check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(dest)], input=tar, check=True)
        shutil.rmtree(dest / "evals", ignore_errors=True)  # even if export-ignore is lost
    shutil.copytree(task_dir, dest / "task")
    if (dest / "evals").exists() or (dest / ".git").exists():
        raise SystemExit("the workdir holds evals/ or .git")
    return dest


# --- making tasks -------------------------------------------------------------------------------------------

def random_points(bbox, n, seed):
    rng = random.Random(seed)
    w, s, e, nn = bbox
    return [{"name": f"地点{i + 1:02d}", "lon": round(rng.uniform(w, e), 6), "lat": round(rng.uniform(s, nn), 6)}
            for i in range(n)]


def to_plane_rows(points, epsg):
    """Japan plane rectangular coordinates as surveyors write them: X is northing, Y is easting (metres)."""
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:6668", f"EPSG:{epsg}", always_xy=True)
    rows = []
    for p in points:
        east, north = tr.transform(p["lon"], p["lat"])
        rows.append({"名称": p["name"], "X": round(north, 3), "Y": round(east, 3)})
    return rows


def make(spec):
    for t in spec["tasks"]:
        d = WORK / "tasks" / t["id"]
        if d.exists():
            continue
        (d / "task").mkdir(parents=True)
        (d / "truth").mkdir()
        (d / "task" / "README.md").write_text(t["brief"].strip() + "\n", encoding="utf-8")
        if t["kind"] == "build":
            pts = random_points(t["bbox"], t["n"], t["seed"])
            rows = to_plane_rows(pts, t["epsg"])
            lines = ["名称,X,Y"] + [f"{r['名称']},{r['X']},{r['Y']}" for r in rows]
            (d / "task" / "data.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
            (d / "truth" / "truth.json").write_text(json.dumps(pts, ensure_ascii=False, indent=0), encoding="utf-8")
        else:
            (d / "truth" / "key.json").write_text(json.dumps(sorted(t["key"])), encoding="utf-8")
        print(t["id"], "made", file=sys.stderr)


# --- scoring ------------------------------------------------------------------------------------------------

def metres(a, b):
    p1, p2 = math.radians(a[1]), math.radians(b[1])
    dl = math.radians(b[0] - a[0])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371008.8 * math.asin(min(1.0, math.sqrt(h)))


def match(pred, ref, tol_m):
    pairs = sorted((metres(p, r), i, j) for i, p in enumerate(pred) for j, r in enumerate(ref))
    used_p, used_r = set(), set()
    for dist, i, j in pairs:
        if dist > tol_m:
            break
        if i not in used_p and j not in used_r:
            used_p.add(i)
            used_r.add(j)
    return len(used_p)


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return "unreadable"


def score_build(work: Path, truth, expect_bbox, tol_m) -> dict:
    answer = read_json(work / "answer.json")
    if isinstance(answer, dict) and answer.get("status") == "failed":
        return {"outcome": "declared_failure", "reason": answer.get("reason", "")}
    data = read_json(work / "out" / "places.geojson")
    if data is None:
        return {"outcome": "no_answer" if answer is None else "invalid_answer"}
    if not isinstance(data, dict):
        return {"outcome": "invalid_answer"}
    rep = geocheck.check(data, expect_bbox=expect_bbox, require_props=["name", "source"])
    reasons = [e["code"] for e in rep["errors"]]
    pred = [tuple(f["geometry"]["coordinates"][:2]) for f in data.get("features", [])
            if isinstance(f, dict) and (f.get("geometry") or {}).get("type") == "Point"]
    ref = [(p["lon"], p["lat"]) for p in truth]
    matched = match(pred, ref, tol_m)
    if matched < len(ref):
        reasons.append("positions")
    texts = "".join(p.read_text(errors="replace") for p in (work / "out").rglob("*") if p.suffix in (".html", ".js"))
    if not ATTRIBUTION.search(texts):
        reasons.append("attribution")
    return {"outcome": "inaccurate" if reasons else "accurate", "reasons": reasons, "matched": matched,
            "n_pred": len(pred), "n_ref": len(ref)}


def score_decide(answer, key) -> dict:
    if answer is None:
        return {"outcome": "no_answer"}
    if not isinstance(answer, dict) or not isinstance(answer.get("constraints", []), list):
        return {"outcome": "invalid_answer"}
    if answer.get("status") == "failed":
        return {"outcome": "declared_failure"}
    got, want = set(answer.get("constraints", [])), set(key)
    hit = len(got & want)
    precision = hit / len(got) if got else 0.0
    recall = hit / len(want) if want else 1.0
    return {"outcome": "accurate" if got == want else "inaccurate", "precision": precision, "recall": recall,
            "reasons": sorted(got ^ want)}


def final_outcome(outcome: str, negative: bool, exit_code: int, has_answer: bool) -> str:
    if not has_answer:
        if exit_code == 124:
            return "timeout"
        return "no_answer" if exit_code == 0 else "provider_error"
    if negative:
        if outcome == "declared_failure":
            return "correct_reject"
        if outcome in ("accurate", "inaccurate"):
            return "false_accept"
    return outcome


def public_osm_hits(text: str) -> list[str]:
    """Public OSM servers in URLs of an agent's log. Names alone do not count: the prompt names them to forbid them."""
    return sorted(set(PUBLIC_OSM.findall(text)))


# --- running ------------------------------------------------------------------------------------------------

def run(spec, agent, cond, task_id, rep, minutes, rev):
    t = next(x for x in spec["tasks"] if x["id"] == task_id)
    d = WORK / "runs" / agent / cond / f"{task_id}-r{rep}"
    if (d / "meta.json").exists():
        raise SystemExit(f"{d} has already run; use another --rep")
    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", rev], capture_output=True, text=True, check=True).stdout.strip()
    wd = prepare_workdir(ROOT, commit, d / "work", WORK / "tasks" / task_id / "task", cond == "skills")
    prompt = fill_prompt((HERE / "prompts" / f"{t['kind']}.md").read_text(encoding="utf-8"), "/work", cond == "skills", minutes)
    (d / "prompt.md").write_text(prompt, encoding="utf-8")
    env = {**os.environ, "EVAL_MINUTES": str(minutes)}
    t0 = time.time()
    with open(d / "log.jsonl", "w") as log, open(d / "stderr.log", "w") as err:
        r = subprocess.run([str(RUNNERS[agent]), "--prompt", str(d / "prompt.md"), str(wd)], stdout=log, stderr=err, env=env)
    meta = {"agent": agent, "cond": cond, "task": task_id, "rep": rep, "exit": r.returncode, "rev": commit,
            "seconds": round(time.time() - t0), "minutes": minutes,
            "model": os.environ.get("EVAL_MODEL", "runner default"), "image": os.environ.get("EVAL_IMAGE", "runner default")}
    (d / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(d, r.returncode, meta["seconds"])


def score_all(spec):
    tasks = {t["id"]: t for t in spec["tasks"]}
    cols = ["agent", "cond", "task", "rep", "outcome", "reasons", "matched", "precision", "recall", "exit", "seconds",
            "public_osm"]
    print("\t".join(cols))
    for m in sorted((WORK / "runs").glob("*/*/*/meta.json")):
        meta = json.loads(m.read_text())
        d, t = m.parent, tasks[meta["task"]]
        work = d / "work"
        truth_dir = WORK / "tasks" / t["id"] / "truth"
        if t["kind"] == "build":
            truth = json.loads((truth_dir / "truth.json").read_text(encoding="utf-8"))
            s = score_build(work, truth, tuple(t["bbox_expect"]), t.get("tol_m", 1.0))
            has = (work / "answer.json").exists() or (work / "out" / "places.geojson").exists()
        else:
            key = json.loads((truth_dir / "key.json").read_text(encoding="utf-8"))
            s = score_decide(read_json(work / "answer.json"), key)
            has = (work / "answer.json").exists()
        o = final_outcome(s["outcome"], t.get("negative", False), meta["exit"], has)
        logs = "".join(p.read_text(errors="replace") for p in (d / "log.jsonl", d / "stderr.log") if p.exists())
        row = [meta["agent"], meta["cond"], meta["task"], meta["rep"], o, ",".join(s.get("reasons", [])) or "-",
               f"{s['matched']}/{s['n_ref']}" if "matched" in s else "-",
               f"{s['precision']:.2f}" if "precision" in s else "-", f"{s['recall']:.2f}" if "recall" in s else "-",
               meta["exit"], meta["seconds"], ",".join(public_osm_hits(logs)) or "-"]
        print("\t".join(str(v) for v in row))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("make")
    r = sub.add_parser("run")
    r.add_argument("--agent", choices=sorted(RUNNERS), required=True)
    r.add_argument("--cond", choices=["skills", "baseline"], required=True)
    r.add_argument("--task", required=True)
    r.add_argument("--rep", type=int, default=1)
    r.add_argument("--minutes", type=int, default=30)
    r.add_argument("--rev", default="HEAD")
    sub.add_parser("score")
    a = ap.parse_args()
    spec = load_spec()
    if a.cmd == "make":
        make(spec)
    elif a.cmd == "run":
        run(spec, a.agent, a.cond, a.task, a.rep, a.minutes, a.rev)
    else:
        score_all(spec)


if __name__ == "__main__":
    main()
