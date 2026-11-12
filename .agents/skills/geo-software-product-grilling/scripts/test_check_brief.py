import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_brief  # noqa: E402

TEMPLATE = Path(__file__).parent.parent / "assets" / "product-brief-template.md"

FILLED = """# プロダクト概要: 旅の実績

## 一行で

旅好きの人の、行った場所を忘れる困りごとを、地図に解除の印を付けることで解く。

## 提供する価値

1. 最重要: 行った場所が一目で分かる
2. 重要: 次に行く場所を決められる
3. 副次的: 未定

## 機能

| 優先度 | 機能 | この機能が届ける価値 |
|---|---|---|
| Must | 現在地の近くの名所を解除する | 行った場所が一目で分かる |
| Should | | |

## 完成の条件

- 大枠: 旅先で名所を解除できる
- 評価のシナリオの置き場所: ~/eval/trip。本数: 6

## 判断の方針

- 費用: 無料枠の内側
- 迷ったときの既定: 取り消せる操作

## 準備したもの

| 種類 | 中身 | 確かめ方 |
|---|---|---|
| 鍵と環境変数 (名前だけ) | `GSF_TEST_TOKEN`、`GSF_TEST_MISSING` | 名前が設定されていること |
| 認証済みの CLI | `python3`、`gsf-no-such-cli` | 認証の状態の表示 |
"""


def run(text, env=None):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "brief.md"
        p.write_text(text, encoding="utf-8")
        return check_brief.check(p, env=env or {})


class TemplateTest(unittest.TestCase):
    def test_the_bare_template_is_not_ready(self):
        r = check_brief.check(TEMPLATE, env={})
        self.assertFalse(r["ok"])
        names = {e["item"] for e in r["errors"]}
        self.assertIn("一行で", names)
        self.assertIn("機能 Must", names)
        self.assertIn("評価のシナリオの置き場所", names)


class FilledTest(unittest.TestCase):
    def test_filled_brief_reports_only_missing_env_and_cli(self):
        r = run(FILLED, env={"GSF_TEST_TOKEN": "s3cret-value"})
        items = sorted(e["item"] for e in r["errors"])
        self.assertEqual(items, ["CLI gsf-no-such-cli", "環境変数 GSF_TEST_MISSING"])
        self.assertEqual(r["env"], {"GSF_TEST_TOKEN": True, "GSF_TEST_MISSING": False})
        self.assertEqual(r["cli"], {"python3": True, "gsf-no-such-cli": False})

    def test_values_of_secrets_never_appear_in_the_report(self):
        r = run(FILLED, env={"GSF_TEST_TOKEN": "s3cret-value"})
        self.assertNotIn("s3cret-value", json.dumps(r, ensure_ascii=False))

    def test_all_present_is_ok(self):
        text = FILLED.replace("、`GSF_TEST_MISSING`", "").replace("、`gsf-no-such-cli`", "")
        self.assertTrue(run(text, env={"GSF_TEST_TOKEN": "x"})["ok"])

    def test_undecided_must_is_an_error(self):
        text = FILLED.replace("| Must | 現在地の近くの名所を解除する |", "| Must | 未定 |")
        self.assertIn("機能 Must", {e["item"] for e in run(text, env={"GSF_TEST_TOKEN": "x"})["errors"]})

    def test_placeholder_in_one_line_is_an_error(self):
        text = FILLED.replace("旅好きの人の、", "<誰の>、")
        self.assertIn("一行で", {e["item"] for e in run(text, env={"GSF_TEST_TOKEN": "x"})["errors"]})

    def test_missing_section_is_an_error(self):
        text = FILLED.replace("## 判断の方針", "## ほかの節")
        self.assertIn("判断の方針", {e["item"] for e in run(text, env={"GSF_TEST_TOKEN": "x"})["errors"]})

    def test_undecided_secondary_value_is_fine(self):
        # 副次的: 未定 is allowed; only the most important value is required.
        self.assertTrue(run(FILLED.replace("、`GSF_TEST_MISSING`", "").replace("、`gsf-no-such-cli`", ""),
                            env={"GSF_TEST_TOKEN": "x"})["ok"])


class CliTest(unittest.TestCase):
    def test_exit_code_and_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "brief.md"
            p.write_text(FILLED, encoding="utf-8")
            out = io.StringIO()
            old = os.environ.get("GSF_TEST_TOKEN")
            os.environ["GSF_TEST_TOKEN"] = "x"
            try:
                with redirect_stdout(out):
                    code = check_brief.main([str(p)])
            finally:
                if old is None:
                    del os.environ["GSF_TEST_TOKEN"]
                else:
                    os.environ["GSF_TEST_TOKEN"] = old
            self.assertEqual(code, 1)
            self.assertFalse(json.loads(out.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main()
