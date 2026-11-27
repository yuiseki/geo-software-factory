"""Tests for first_seen.py. Run: python3 -m unittest discover -s .agents/skills/geo-software-research-competitor/scripts"""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import first_seen  # noqa: E402

CARD = """---
financial: non-commercial
organization: individual
---

# こにゃーきんぐ

- URL: https://spotsharemap.github.io/sharewitheveryone/
- ソース: https://github.com/spotsharemap/sharewitheveryone (ライセンスの表示なし)
- 観測した日: 2026-11-11

## 技術

- App Store: こにゃーきんぐ、無料、初出 2019-04-27、最新の更新 2026-08-10
- Google Play: こにゃーきんぐ、初出 2018-12-01
"""


class Parse(unittest.TestCase):
    def test_reads_url_repo_and_store_dates(self):
        c = first_seen.parse_card(CARD)
        self.assertEqual(c["url"], "https://spotsharemap.github.io/sharewitheveryone/")
        self.assertEqual(c["repo"], "spotsharemap/sharewitheveryone")
        self.assertEqual(c["store"], ["2019-04-27", "2018-12-01"])

    def test_no_repo_off_github(self):
        c = first_seen.parse_card(CARD.replace("https://github.com/spotsharemap/sharewitheveryone",
                                               "https://codeberg.org/comaps/comaps"))
        self.assertIsNone(c["repo"])

    def test_last_update_is_not_a_first_date(self):
        self.assertNotIn("2026-08-10", first_seen.parse_card(CARD)["store"])


class Earliest(unittest.TestCase):
    def test_takes_the_earliest_and_names_its_source(self):
        self.assertEqual(first_seen.earliest({"wayback": "2020-01-02", "github": "2019-05-06", "store": None}),
                         ("2019-05-06", "github"))

    def test_none_when_nothing_was_found(self):
        self.assertEqual(first_seen.earliest({"wayback": None, "github": None}), ("none", "none"))


class Wayback(unittest.TestCase):
    def test_site_root_is_matched_as_the_host(self):
        q = first_seen.cdx_query("https://castlemap.au/")
        self.assertIn("url=castlemap.au&", q)
        self.assertNotIn("matchType", q)

    def test_a_path_is_matched_as_a_prefix_without_index_html(self):
        q = first_seen.cdx_query("https://fukazawa-lab.github.io/japan-bear-map/index.html?x=1")
        self.assertIn("url=fukazawa-lab.github.io%2Fjapan-bear-map&", q)
        self.assertIn("matchType=prefix", q)

    def test_timestamp_becomes_a_date(self):
        self.assertEqual(first_seen.ts_date("20150302123456"), "2015-03-02")
        self.assertIsNone(first_seen.ts_date(""))


class Frontmatter(unittest.TestCase):
    def test_adds_fields_after_the_existing_ones(self):
        out = first_seen.set_first_seen(CARD, "2018-12-01", "store")
        self.assertTrue(out.startswith("---\nfinancial: non-commercial\norganization: individual\n"
                                       "first_seen: 2018-12-01\nfirst_seen_by: store\n---\n"))
        self.assertEqual(out.split("---", 2)[2], CARD.split("---", 2)[2])

    def test_replaces_old_values(self):
        once = first_seen.set_first_seen(CARD, "2018-12-01", "store")
        twice = first_seen.set_first_seen(once, "2017-01-01", "wayback")
        self.assertIn("first_seen: 2017-01-01\nfirst_seen_by: wayback\n", twice)
        self.assertEqual(twice.count("first_seen:"), 1)

    def test_reads_back_what_it_wrote(self):
        self.assertEqual(first_seen.frontmatter(first_seen.set_first_seen(CARD, "none", "none"))["first_seen"], "none")


if __name__ == "__main__":
    unittest.main()
