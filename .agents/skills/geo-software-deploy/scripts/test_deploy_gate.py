import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import deploy_gate  # noqa: E402


class DeployGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.app = self.root / "app"
        self.out = self.root / "out"
        self.app.mkdir()
        self.out.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.app)], check=True)
        (self.app / "index.html").write_text("<html></html>", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=a@example.invalid", "-c", "user.name=a", "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=a@example.invalid", "-c", "user.name=a", "commit", "-q", "-m", "init"], check=True)
        self.rev = subprocess.run(["git", "-C", str(self.app), "rev-parse", "--short", "HEAD"],
                                  capture_output=True, text=True, check=True).stdout.strip()
        self.eval_report = self.out / "final.json"
        self.eval_report.write_text(json.dumps({
            "when": "2026-11-13T00:00:00+00:00",
            "version": self.rev,
            "ok": True,
            "scenarios": [{"id": "S1", "result": "pass"}],
        }), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_passes_when_tree_is_clean_and_eval_matches_head(self):
        res = deploy_gate.check(app_repo=self.app, eval_report=self.eval_report)
        self.assertTrue(res["ok"], res)
        self.assertEqual(res["head"], self.rev)
        self.assertEqual(res["errors"], [])

    def test_refuses_when_working_tree_is_dirty(self):
        (self.app / "uncommitted.txt").write_text("dirty", encoding="utf-8")
        res = deploy_gate.check(app_repo=self.app, eval_report=self.eval_report)
        self.assertFalse(res["ok"])
        self.assertIn("dirty_tree", [e["code"] for e in res["errors"]])

    def test_refuses_when_eval_version_differs_from_head_or_failed(self):
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=a@example.invalid", "-c", "user.name=a",
                        "commit", "-q", "--allow-empty", "-m", "after-eval"], check=True)
        res = deploy_gate.check(app_repo=self.app, eval_report=self.eval_report)
        self.assertFalse(res["ok"])
        self.assertIn("version_mismatch", [e["code"] for e in res["errors"]])

        new_rev = subprocess.run(["git", "-C", str(self.app), "rev-parse", "--short", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.strip()
        self.eval_report.write_text(json.dumps({
            "version": new_rev, "ok": False, "scenarios": [{"id": "S1", "result": "fail"}]
        }), encoding="utf-8")
        res2 = deploy_gate.check(app_repo=self.app, eval_report=self.eval_report)
        self.assertFalse(res2["ok"])
        self.assertIn("eval_failed", [e["code"] for e in res2["errors"]])

    def test_refuses_when_audit_has_blocking_severity_or_destructive_sql_migration(self):
        audit_path = self.out / "audit.json"
        audit_path.write_text(json.dumps({
            "findings": [
                {"id": "A1", "status": "問題あり", "severity": "High", "title": "BBox DoS"},
                {"id": "A2", "status": "防御されている", "severity": "Critical", "title": "SQLi"},
            ]
        }, ensure_ascii=False), encoding="utf-8")
        mig = self.app / "0002_drop.sql"
        mig.write_text("ALTER TABLE places ADD COLUMN note TEXT;\nDROP TABLE old_places;\n", encoding="utf-8")
        # Commit migration so tree stays clean
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=a@example.invalid", "-c", "user.name=a", "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.app), "-c", "user.email=a@example.invalid", "-c", "user.name=a", "commit", "-q", "-m", "mig"], check=True)
        rev = subprocess.run(["git", "-C", str(self.app), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, check=True).stdout.strip()
        self.eval_report.write_text(json.dumps({"version": rev, "ok": True, "scenarios": [{"id": "S1", "result": "pass"}]}), encoding="utf-8")

        res = deploy_gate.check(app_repo=self.app, eval_report=self.eval_report, audit_report=audit_path,
                                block_severity="High", migrations=[mig])
        self.assertFalse(res["ok"])
        codes = [e["code"] for e in res["errors"]]
        self.assertIn("audit_blocked", codes)
        self.assertIn("destructive_migration", codes)

    def test_records_release_and_returns_previous_version_for_rollback(self):
        ledger = self.out / "releases.json"
        r1 = deploy_gate.record_release(ledger, version="v1", commit="aaa1111", url="https://example.invalid")
        r2 = deploy_gate.record_release(ledger, version="v2", commit="bbb2222", url="https://example.invalid")
        self.assertIsNone(r1["previous"])
        self.assertEqual(r2["previous"]["version"], "v1")
        prev = deploy_gate.rollback_target(ledger)
        self.assertEqual(prev["version"], "v1")
        self.assertEqual(prev["commit"], "aaa1111")


if __name__ == "__main__":
    unittest.main()
