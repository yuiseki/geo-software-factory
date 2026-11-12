"""Tests for find_cards.py. Run: python3 -m unittest discover -s .agents/skills/geo-software-research-competitor/scripts"""
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import find_cards  # noqa: E402

CARD = """# こにゃーきんぐ

- URL: https://spotsharemap.github.io/sharewitheveryone/
- 探すときの語: 作業場所、カフェ作業、Web 会議、電源、Wi-Fi、通話できる場所

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 会話してよいか、電源や Wi-Fi があるかで選ぶ、作業と通話の場所の地図 |
| 提供する価値 | オンライン面接や Web 会議ができる場所を探せる |

## 技術

| 描画 | MapLibre GL JS |
"""
OTHER = CARD.replace("こにゃーきんぐ", "本屋の地図").replace("作業場所、カフェ作業、Web 会議、電源、Wi-Fi、通話できる場所", "本屋、書店") \
    .replace("会話してよいか、電源や Wi-Fi があるかで選ぶ、作業と通話の場所の地図", "全国の本屋の地図") \
    .replace("オンライン面接や Web 会議ができる場所を探せる", "本屋を探せる")


class FindCards(unittest.TestCase):
    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        (self.root / "services").mkdir()
        (self.root / "apps").mkdir()
        (self.root / "services" / "konyaking.md").write_text(CARD)
        (self.root / "apps" / "books.md").write_text(OTHER)
        (self.root / "services" / "README.md").write_text("# index\n電源\n")

    def test_finds_by_any_word_and_ranks_by_how_many_match(self):
        hits = find_cards.find(self.root, ["電源", "wifi", "会議", "本屋"])
        self.assertEqual([h["file"] for h in hits], ["services/konyaking.md", "apps/books.md"])
        self.assertEqual(hits[0]["url"], "https://spotsharemap.github.io/sharewitheveryone/")
        self.assertEqual(hits[0]["matched"], ["wifi", "会議", "電源"])

    def test_width_and_case_are_folded(self):
        self.assertTrue(find_cards.find(self.root, ["ＷＩ-ＦＩ"]))

    def test_technology_section_is_not_searched(self):
        self.assertEqual(find_cards.find(self.root, ["MapLibre"]), [])

    def test_readme_is_not_a_card(self):
        self.assertTrue(all(h["file"] != "services/README.md" for h in find_cards.find(self.root, ["電源"])))


if __name__ == "__main__":
    unittest.main()
