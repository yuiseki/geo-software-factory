import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from functools import partial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dark_factory  # noqa: E402

BRIEF = """# プロダクト概要: 台東区テストマップ

## 一行で

旅行者の、名所の場所が分からない困りごとを、地図に名所を表示することで解く。

## 提供する価値

1. 最重要: 名所の位置が正しく分かる
2. 重要: 名前で絞り込める
3. 副次的: 未定

## 機能

| 優先度 | 機能 | この機能が届ける価値 |
|---|---|---|
| Must | 名所を地図に表示する | 名所の位置が正しく分かる |

## 完成の条件

- 大枠: `sh start.sh` で起動し、`/` と `/places.geojson` を返す
- 評価のシナリオの置き場所: 外の scenarios ディレクトリ。本数: 2

## 判断の方針

- 費用: 無料枠の内側
- 迷ったときの既定: 外部のサービスに頼らない

## 準備したもの

| 種類 | 中身 | 確かめ方 |
|---|---|---|
| 鍵と環境変数 (名前だけ) | 要らない | |
| 認証済みの CLI | `python3`、`git` | |

## 夜に決めたこと

- 

## 止まったこと

- 
"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class DarkFactoryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.app = self.root / "app"
        self.scen = self.root / "scenarios"
        self.work = self.root / "work"
        self.app.mkdir()
        self.scen.mkdir()
        (self.app / "product-brief.md").write_text(BRIEF, encoding="utf-8")
        (self.scen / "S1.json").write_text(json.dumps({
            "id": "S1", "name": "出典表示", "symptom": "トップページに出典が無い",
            "checks": [{"kind": "http", "path": "/", "status": 200, "contains": "CC0"}],
        }, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_preflight_passes_when_brief_and_scenarios_are_valid(self):
        r = dark_factory.preflight(self.app, self.scen, self.work)
        self.assertTrue(r["ok"], r)

    def test_preflight_refuses_scenarios_or_workdir_inside_app_or_stop_switch(self):
        inner_scen = self.app / "scenarios"
        inner_scen.mkdir()
        self.assertFalse(dark_factory.preflight(self.app, inner_scen, self.work)["ok"])
        self.assertFalse(dark_factory.preflight(self.app, self.scen, self.app / "work")["ok"])
        self.work.mkdir(exist_ok=True)
        (self.work / "STOP").write_text("", encoding="utf-8")
        self.assertFalse(dark_factory.preflight(self.app, self.scen, self.work)["ok"])

    def test_eval_of_eval_checks_good_passes_and_broken_fails(self):
        good_dir, bad_dir = self.root / "good", self.root / "bad"
        good_dir.mkdir()
        bad_dir.mkdir()
        (good_dir / "index.html").write_text("<html>CC0</html>", encoding="utf-8")
        (bad_dir / "index.html").write_text("<html>no attribution</html>", encoding="utf-8")
        s_good = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(good_dir)))
        s_bad = http.server.ThreadingHTTPServer(("127.0.0.1", 0), partial(Quiet, directory=str(bad_dir)))
        threading.Thread(target=s_good.serve_forever, daemon=True).start()
        threading.Thread(target=s_bad.serve_forever, daemon=True).start()
        try:
            g_url = f"http://127.0.0.1:{s_good.server_address[1]}"
            b_url = f"http://127.0.0.1:{s_bad.server_address[1]}"
            rep = dark_factory.eval_of_eval(self.scen, g_url, {"no-attr": b_url}, self.work / "out" / "eval-of-eval.json")
            self.assertTrue(rep["ok"])
            self.assertEqual(rep["breaks"]["no-attr"]["failed_scenarios"], ["S1"])
        finally:
            s_good.shutdown()
            s_good.server_close()
            s_bad.shutdown()
            s_bad.server_close()

    def test_end_to_end_local_night_loop_and_morning_report(self):
        port = dark_factory.free_port()
        impl_script = self.root / "impl.py"
        impl_script.write_text(f"""import json, os, subprocess, time
from pathlib import Path

app = Path.cwd()
handoff = Path(os.environ["EVAL_HANDOFF"])
feedback = Path(os.environ["EVAL_FEEDBACK"])
port = int(os.environ["APP_PORT"])

(app / "index.html").write_text("<html>CC0</html>", encoding="utf-8")
(app / "start.sh").write_text("exec python3 -m http.server ${{PORT:-{port}}}\\n", encoding="utf-8")
brief = (app / "product-brief.md").read_text(encoding="utf-8").replace(
    "## 夜に決めたこと\\n\\n- ", "## 夜に決めたこと\\n\\n- 静的配信にした")
(app / "product-brief.md").write_text(brief, encoding="utf-8")
subprocess.run(["git", "-c", "user.email=a@example.invalid", "-c", "user.name=a", "add", "-A"], check=True)
subprocess.run(["git", "-c", "user.email=a@example.invalid", "-c", "user.name=a", "commit", "-q", "-m", "impl"], check=True)
rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
srv = subprocess.Popen(["sh", "start.sh"], env={{**os.environ, "PORT": str(port)}})
try:
    time.sleep(0.2)
    handoff.write_text(json.dumps({{"rev": rev, "port": port}}), encoding="utf-8")
    for _ in range(30):
        if feedback.is_file() and rev in feedback.read_text(encoding="utf-8"):
            break
        time.sleep(0.1)
finally:
    srv.terminate()
    srv.wait(timeout=5)
""", encoding="utf-8")

        summary = dark_factory.run_factory(
            app_dir=self.app, scenarios_dir=self.scen, work_dir=self.work, mode="local",
            agent="custom", implementer_cmd=[sys.executable, "-I", str(impl_script)],
            port=port, minutes=1.0, watch_interval=0.05, startup_timeout=5.0,
        )
        self.assertTrue(summary["ok"], summary)
        self.assertTrue(summary["final_ok"])
        self.assertTrue(summary["deploy_ready"])
        self.assertEqual(summary["eval_requests"], 1)
        morning = (self.work / "out" / "morning-report.md").read_text(encoding="utf-8")
        self.assertIn("1/1 合格", morning)
        self.assertIn("静的配信にした", morning)
        eval_rep = (self.work / "out" / "eval-report.md").read_text(encoding="utf-8")
        self.assertIn("# 評価の報告: 台東区テストマップ", eval_rep)


if __name__ == "__main__":
    unittest.main()
