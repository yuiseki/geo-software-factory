import datetime
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import hooks  # noqa: E402

NOW = datetime.datetime(2026, 11, 14, 3, 0, tzinfo=datetime.timezone.utc)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.state = self.root / "state"
        self.env = {"RUN_STATE_DIR": str(self.state)}

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, event, payload=None, now=NOW):
        out = io.StringIO()
        with redirect_stdout(out):
            code = hooks.main([event], stdin=io.StringIO(json.dumps(payload or {})), env=self.env, now=now)
        text = out.getvalue().strip()
        return code, (json.loads(text) if text else None)


class StopSwitchTest(Base):
    def test_no_switch_allows(self):
        self.env["AGENT_STOP_FILE"] = str(self.root / "STOP")
        self.assertEqual(self.call("stop-switch", {"tool_name": "Bash"}), (0, None))

    def test_switch_denies_every_tool(self):
        (self.root / "STOP").write_text("", encoding="utf-8")
        self.env["AGENT_STOP_FILE"] = str(self.root / "STOP")
        code, out = self.call("stop-switch", {"tool_name": "Edit"})
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_unset_switch_path_fails_closed(self):
        code, out = self.call("stop-switch", {"tool_name": "Edit"})
        self.assertEqual(out["hookSpecificOutput"]["permissionDecision"], "deny")


class DeliverTest(Base):
    def setUp(self):
        super().setUp()
        self.fb = self.root / "eval-feedback.md"
        self.env["EVAL_FEEDBACK"] = str(self.fb)

    def context(self, out):
        return out["hookSpecificOutput"]["additionalContext"] if out else None

    def test_nothing_to_deliver(self):
        self.assertEqual(self.call("deliver"), (0, None))

    def test_new_feedback_is_delivered_once(self):
        self.fb.write_text("# 評価の症状\n- /places.geojson: 状態 500\n", encoding="utf-8")
        ctx = self.context(self.call("deliver")[1])
        self.assertIn("状態 500", ctx)
        self.assertIsNone(self.call("deliver")[1])

    def test_changed_feedback_is_delivered_again(self):
        self.fb.write_text("一回目", encoding="utf-8")
        self.call("deliver")
        self.fb.write_text("二回目", encoding="utf-8")
        self.assertIn("二回目", self.context(self.call("deliver")[1]))

    def test_long_feedback_is_cut_but_says_where_the_rest_is(self):
        self.fb.write_text("あ" * 20000, encoding="utf-8")
        ctx = self.context(self.call("deliver")[1])
        self.assertLess(len(ctx), 9000)
        self.assertIn(str(self.fb), ctx)

    def test_deadline_reminders_fire_once_each(self):
        self.env["RUN_DEADLINE"] = (NOW + datetime.timedelta(minutes=25)).isoformat()
        ctx = self.context(self.call("deliver")[1])
        self.assertIn("30 分", ctx)
        self.assertIsNone(self.call("deliver")[1])
        later = NOW + datetime.timedelta(minutes=16)
        self.assertIn("10 分", self.context(self.call("deliver", now=later)[1]))

    def test_past_deadline_says_stop_background_work(self):
        self.env["RUN_DEADLINE"] = (NOW - datetime.timedelta(minutes=1)).isoformat()
        self.assertIn("裏で回している", self.context(self.call("deliver")[1]))


class StopGuardTest(Base):
    def setUp(self):
        super().setUp()
        self.env["RUN_DEADLINE"] = (NOW + datetime.timedelta(hours=2)).isoformat()
        cl = self.root / "checklist.txt"
        cl.write_text("評価を全シナリオで動かし直したか\n壊した版で評価が落ちるか\n", encoding="utf-8")
        self.env["STOP_GUARD_CHECKLIST"] = str(cl)
        self.env["STOP_GUARD_MAX"] = "3"

    def test_blocks_with_a_different_reason_each_time_then_gives_up(self):
        reasons = []
        for _ in range(4):
            code, out = self.call("stop-guard", {"stop_hook_active": True})
            reasons.append(out["reason"] if out else None)
        self.assertEqual(reasons[0], "評価を全シナリオで動かし直したか")
        self.assertEqual(reasons[1], "壊した版で評価が落ちるか")
        self.assertIsNone(reasons[2])  # checklist used up: never repeat a reason
        self.assertIsNone(reasons[3])

    def test_cap_holds_even_with_a_long_checklist(self):
        (self.root / "checklist.txt").write_text("\n".join(f"観点{i}" for i in range(10)), encoding="utf-8")
        blocked = sum(self.call("stop-guard")[1] is not None for _ in range(10))
        self.assertEqual(blocked, 3)

    def test_after_the_deadline_lets_it_stop(self):
        self.assertIsNone(self.call("stop-guard", now=NOW + datetime.timedelta(hours=3))[1])

    def test_without_a_deadline_lets_it_stop(self):
        del self.env["RUN_DEADLINE"]
        self.assertIsNone(self.call("stop-guard")[1])


class StateTest(Base):
    def test_state_dir_is_required(self):
        del self.env["RUN_STATE_DIR"]
        self.env["EVAL_FEEDBACK"] = str(self.root / "x.md")
        with self.assertRaises(SystemExit):
            self.call("deliver")


if __name__ == "__main__":
    unittest.main()
