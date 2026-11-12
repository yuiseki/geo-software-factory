import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_isolation  # noqa: E402

COMPOSE = Path(__file__).parent.parent / "assets" / "isolation" / "compose.yaml"


def dirs(root: Path) -> dict:
    env = {}
    for name in ("APP_DIR", "HANDOFF_DIR", "FEEDBACK_DIR", "SCENARIOS_DIR", "REPORT_DIR"):
        d = root / name.lower()
        d.mkdir()
        env[name] = str(d)
    env["EVAL_SCRIPTS"] = str(Path(__file__).parent)
    return env


class FakeRunner:
    """Answers each probe the way an isolated (or a broken) setup would."""

    def __init__(self, leak=False, feedback_writable=False, socket=False, control_blind=False):
        self.leak, self.feedback_writable, self.socket, self.control_blind = leak, feedback_writable, socket, control_blind
        self.calls = []

    def __call__(self, service, script):
        self.calls.append((service, script))
        code, out = self.answer(service, script)
        return code, check_isolation.RAN + "\n" + out

    def answer(self, service, script):
        if "grep" in script:
            found = (service == "implementer" and self.leak) or (service == "evaluator" and not self.control_blind)
            return (0, "/eval/scenarios/.isolation-canary\n/eval/out/.isolation-canary\n") if found else (1, "")
        if "docker.sock" in script:
            return (0, "") if self.socket else (1, "")
        if "/work/feedback" in script:
            return (0, "") if self.feedback_writable else (1, "Read-only file system")
        if "/eval/scenarios" in script:
            return (1, "Read-only file system")
        return (0, "")


class ProbeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dirs(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def results(self, runner):
        r = check_isolation.check(self.env, runner)
        return r, {p["name"]: p["ok"] for p in r["probes"]}

    def test_isolated_setup_passes(self):
        r, by = self.results(FakeRunner())
        self.assertTrue(r["ok"], r)
        self.assertTrue(all(by.values()))

    def test_a_leak_fails(self):
        r, by = self.results(FakeRunner(leak=True))
        self.assertFalse(r["ok"])
        self.assertFalse(by["implementer cannot find the canary"])

    def test_a_blind_search_fails_even_without_a_leak(self):
        # If the evaluator's own search cannot find the canary, "not found" on the implementer proves nothing.
        r, by = self.results(FakeRunner(control_blind=True))
        self.assertFalse(r["ok"])
        self.assertFalse(by["evaluator finds the canary (control)"])

    def test_writable_feedback_and_docker_socket_fail(self):
        _, by = self.results(FakeRunner(feedback_writable=True, socket=True))
        self.assertFalse(by["implementer cannot write the feedback"])
        self.assertFalse(by["implementer has no Docker socket"])

    def test_the_runner_is_cleaned_up_even_on_failure(self):
        runner = FakeRunner(leak=True)
        runner.cleaned = 0
        runner.cleanup = lambda: setattr(runner, "cleaned", runner.cleaned + 1)
        check_isolation.check(self.env, runner)
        self.assertEqual(runner.cleaned, 1)

    def test_canaries_are_removed_and_the_token_is_not_reused(self):
        runner = FakeRunner()
        check_isolation.check(self.env, runner)
        check_isolation.check(self.env, runner)
        for d in ("SCENARIOS_DIR", "REPORT_DIR"):
            self.assertEqual(list(Path(self.env[d]).iterdir()), [])
        greps = [s for svc, s in runner.calls if svc == "implementer" and "grep" in s]
        self.assertNotEqual(greps[0], greps[1])

    def test_containers_that_never_started_fail_every_probe(self):
        # "cannot write" and "no socket" are expected failures; a container that did not start must not pass them.
        r, by = self.results(lambda service, script: (1, "failed to create network"))
        self.assertFalse(r["ok"])
        self.assertFalse(any(by.values()), by)

    def test_missing_directory_is_reported_before_any_probe(self):
        env = dict(self.env)
        del env["SCENARIOS_DIR"]
        runner = FakeRunner()
        with self.assertRaises(check_isolation.Misconfigured):
            check_isolation.check(env, runner)
        self.assertEqual(runner.calls, [])

    def test_scenarios_inside_the_app_dir_is_misconfigured(self):
        env = dict(self.env)
        inner = Path(env["APP_DIR"]) / "scenarios"
        inner.mkdir()
        env["SCENARIOS_DIR"] = str(inner)
        with self.assertRaises(check_isolation.Misconfigured):
            check_isolation.check(env, FakeRunner())


@unittest.skipUnless(os.environ.get("GSF_DOCKER_TESTS") == "1", "set GSF_DOCKER_TESTS=1 to run against Docker")
class DockerTest(unittest.TestCase):
    """The real thing: the probes in containers, then one evaluation round trip through the handoff."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = dirs(Path(self.tmp.name))
        self.env.update(RUN_NAME=f"gsf-isolation-test-{os.getpid()}", RUN_UID=str(os.getuid()),
                        RUN_GID=str(os.getgid()))
        # A Docker host whose default address pools are used up cannot create the network; GSF_DOCKER_SUBNET
        # names a free one, through an override file as the night would use.
        self.files = [COMPOSE]
        if subnet := os.environ.get("GSF_DOCKER_SUBNET"):
            override = Path(self.tmp.name) / "subnet.yaml"
            override.write_text(f"networks:\n  night:\n    ipam:\n      config:\n        - subnet: {subnet}\n",
                                encoding="utf-8")
            self.files.append(override)
        self.compose = ["docker", "compose"] + [x for f in self.files for x in ("-f", str(f))]

    def tearDown(self):
        subprocess.run(self.compose + ["down", "--remove-orphans", "-t", "1"],
                       env={**os.environ, **self.env}, capture_output=True)
        self.tmp.cleanup()

    def test_probes_pass(self):
        r = check_isolation.check(self.env, check_isolation.docker_runner(self.files, self.env))
        self.assertTrue(r["ok"], json.dumps(r, ensure_ascii=False, indent=1))

    def test_a_broken_mount_is_caught(self):
        # Eval of the eval: mount the scenarios into the implementer too, and the check must fail.
        broken = Path(self.tmp.name) / "broken.yaml"
        text = COMPOSE.read_text(encoding="utf-8").replace(
            "      - ${FEEDBACK_DIR:?FEEDBACK_DIR}:/work/feedback:ro\n",
            "      - ${FEEDBACK_DIR:?FEEDBACK_DIR}:/work/feedback:ro\n      - ${SCENARIOS_DIR}:/work/oops:ro\n", 1)
        broken.write_text(text, encoding="utf-8")
        r = check_isolation.check(self.env, check_isolation.docker_runner([broken] + self.files[1:], self.env))
        self.assertFalse(r["ok"])

    def test_round_trip(self):
        app, handoff, scen = (Path(self.env[k]) for k in ("APP_DIR", "HANDOFF_DIR", "SCENARIOS_DIR"))
        (app / "index.html").write_text("<html>© OpenStreetMap contributors</html>", encoding="utf-8")
        (scen / "S1.json").write_text(json.dumps({"id": "S1", "symptom": "帰属表示が見えない", "checks": [
            {"kind": "http", "path": "/", "contains": "SECRET-EXPECTED-TEXT"}]}), encoding="utf-8")
        env = {**os.environ, **self.env, "IMPLEMENTER_CMD": "python3 -m http.server 8787"}
        compose = self.compose
        subprocess.run(compose + ["up", "-d", "implementer"], env=env, check=True, capture_output=True)
        (handoff / "ready.json").write_text(json.dumps({"rev": "abc1234", "port": 8787}), encoding="utf-8")
        for _ in range(20):  # wait for the app to listen
            p = subprocess.run(compose + ["run", "--rm", "-T", "evaluator", "python3", "-I", "/eval/bin/eval_watch.py",
                                          "--handoff", "/eval/handoff", "--scenarios", "/eval/scenarios",
                                          "--report-dir", "/eval/out", "--feedback", "/eval/feedback/eval-feedback.md",
                                          "--once"], env=env, capture_output=True, text=True)
            fb = Path(self.env["FEEDBACK_DIR"]) / "eval-feedback.md"
            if fb.exists() and "応答なし" not in fb.read_text(encoding="utf-8"):
                break
            (handoff / "ready.json").write_text(json.dumps({"rev": "abc1234", "port": 8787, "nonce": time.time()}),
                                                encoding="utf-8")
            time.sleep(1)
        text = fb.read_text(encoding="utf-8")
        self.assertIn("帰属表示が見えない", text)
        self.assertIn("状態 200", text)
        self.assertNotIn("SECRET-EXPECTED-TEXT", text)
        # the implementer reads the symptoms, and cannot change them
        p = subprocess.run(compose + ["exec", "-T", "implementer", "sh", "-c",
                                      "cat /work/feedback/eval-feedback.md && touch /work/feedback/x"],
                           env=env, capture_output=True, text=True)
        self.assertIn("帰属表示が見えない", p.stdout)
        self.assertNotEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main()
