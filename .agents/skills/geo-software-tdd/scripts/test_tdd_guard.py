import datetime
import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tdd_guard  # noqa: E402

TODAY = datetime.date(2026, 11, 13)


class TddGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_quarantine_ledger_validates_fields_expiry_and_unexpected_passes(self):
        ledger = self.root / "quarantine.json"
        ledger.write_text(json.dumps({
            "quarantined": [
                {"test": "test_webgl_context_lost", "reason": "SwiftShader flake", "owner": "alice", "expires": "2026-12-01"},
                {"test": "test_expired_flake", "reason": "old", "owner": "bob", "expires": "2026-11-01"},
                {"test": "test_missing_owner", "reason": "r", "owner": "", "expires": "2026-12-01"},
            ]
        }), encoding="utf-8")
        res = tdd_guard.check_quarantine(ledger, passed_tests=["test_webgl_context_lost"], today=TODAY)
        self.assertFalse(res["ok"])
        codes = [e["code"] for e in res["errors"]]
        self.assertIn("expired_quarantine", codes)
        self.assertIn("missing_quarantine_metadata", codes)
        self.assertIn("quarantined_test_passed", codes)

    def test_quarantine_passes_when_valid_and_not_unexpectedly_passing(self):
        ledger = self.root / "quarantine.json"
        ledger.write_text(json.dumps({
            "quarantined": [
                {"test": "test_webgl_context_lost", "reason": "SwiftShader flake", "owner": "alice", "expires": "2026-12-01"},
            ]
        }), encoding="utf-8")
        res = tdd_guard.check_quarantine(ledger, passed_tests=["test_other"], today=TODAY)
        self.assertTrue(res["ok"], res)

    def test_ratchet_allows_decrease_and_updates_cap_but_rejects_increase(self):
        caps_file = self.root / "caps.json"
        caps_file.write_text(json.dumps({"todo_count": 5}), encoding="utf-8")
        src = self.root / "src"
        src.mkdir()
        (src / "a.py").write_text("# TODO: one\n# TODO: two\n", encoding="utf-8")

        # 2 TODOs <= cap 5 -> passes and ratchets cap down to 2
        r1 = tdd_guard.check_ratchet(src, caps_file, update=True)
        self.assertTrue(r1["ok"], r1)
        self.assertEqual(json.loads(caps_file.read_text(encoding="utf-8"))["todo_count"], 2)

        # Adding a 3rd TODO now exceeds ratcheted cap 2 -> fails
        (src / "a.py").write_text("# TODO: one\n# TODO: two\n# TODO: three\n", encoding="utf-8")
        r2 = tdd_guard.check_ratchet(src, caps_file, update=False)
        self.assertFalse(r2["ok"])
        self.assertEqual(r2["errors"][0]["code"], "ratchet_exceeded")

    def test_network_guard_allows_loopback_and_blocks_external_hosts(self):
        with tdd_guard.block_external_network():
            with self.assertRaises(RuntimeError) as ctx:
                socket.create_connection(("tile.openstreetmap.org", 80), timeout=1)
            self.assertIn("tile.openstreetmap.org", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
