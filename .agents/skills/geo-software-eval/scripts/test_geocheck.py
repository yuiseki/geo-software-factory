"""Tests for geocheck.py. Run: python3 -m unittest discover -s .agents/skills/geo-software-eval/scripts"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import geocheck  # noqa: E402

JAPAN = (122.0, 20.0, 154.0, 46.0)


def point(lon, lat, **props):
    return {"type": "Feature", "properties": props, "geometry": {"type": "Point", "coordinates": [lon, lat]}}


def fc(*features):
    return {"type": "FeatureCollection", "features": list(features)}


def square(x, y, d=0.01):
    return [[x, y], [x + d, y], [x + d, y + d], [x, y + d], [x, y]]


def codes(report, level):
    return sorted({f["code"] for f in report[level]})


class Structure(unittest.TestCase):
    def test_valid_collection_has_no_findings(self):
        r = geocheck.check(fc(point(139.77, 35.68, name="東京")))
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["warnings"], [])
        self.assertEqual(r["features"], 1)

    def test_unknown_type_is_an_error(self):
        r = geocheck.check({"type": "Thing"})
        self.assertIn("bad-type", codes(r, "errors"))

    def test_feature_without_geometry_member_is_an_error(self):
        r = geocheck.check(fc({"type": "Feature", "properties": {}}))
        self.assertIn("bad-feature", codes(r, "errors"))

    def test_null_geometry_is_allowed_but_counted(self):
        r = geocheck.check(fc({"type": "Feature", "properties": {}, "geometry": None}))
        self.assertEqual(r["errors"], [])
        self.assertEqual(r["null_geometries"], 1)

    def test_empty_collection_is_an_error_unless_allowed(self):
        self.assertIn("empty", codes(geocheck.check(fc()), "errors"))
        self.assertEqual(geocheck.check(fc(), allow_empty=True)["errors"], [])

    def test_non_numeric_and_non_finite_positions_are_errors(self):
        r = geocheck.check(fc(point("139", 35.6)))
        self.assertIn("bad-position", codes(r, "errors"))
        r = geocheck.check({"type": "Point", "coordinates": [float("nan"), 35.0]})
        self.assertIn("bad-position", codes(r, "errors"))


class Coordinates(unittest.TestCase):
    def test_projected_metres_are_reported_as_not_degrees(self):
        # Japan plane rectangular zone IX, metres: far outside any degree range.
        r = geocheck.check(fc(point(-5000.0, -35000.0)))
        self.assertIn("out-of-range", codes(r, "errors"))

    def test_swapped_lat_lon_is_detected_with_an_expected_bbox(self):
        r = geocheck.check(fc(point(35.68, 139.77), point(34.69, 135.50)), expect_bbox=JAPAN)
        self.assertIn("swapped-lon-lat", codes(r, "errors"))

    def test_points_outside_the_expected_bbox_are_errors(self):
        r = geocheck.check(fc(point(139.77, 35.68), point(-0.12, 51.5)), expect_bbox=JAPAN)
        self.assertIn("outside-bbox", codes(r, "errors"))
        self.assertEqual(r["outside_bbox"], 1)

    def test_null_island_is_a_warning(self):
        r = geocheck.check(fc(point(0, 0)))
        self.assertIn("null-island", codes(r, "warnings"))

    def test_legacy_crs_member_is_a_warning(self):
        doc = fc(point(139.77, 35.68))
        doc["crs"] = {"type": "name", "properties": {"name": "EPSG:6677"}}
        self.assertIn("crs-member", codes(geocheck.check(doc), "warnings"))

    def test_crs84_member_is_not_a_warning(self):
        doc = fc(point(139.77, 35.68))
        doc["crs"] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}
        self.assertEqual(geocheck.check(doc)["warnings"], [])

    def test_bbox_of_the_data_is_reported(self):
        r = geocheck.check(fc(point(139.0, 35.0), point(140.0, 36.0)))
        self.assertEqual(r["bbox"], [139.0, 35.0, 140.0, 36.0])


class Polygons(unittest.TestCase):
    def poly(self, ring):
        return fc({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [ring]}})

    def test_closed_square_is_fine(self):
        self.assertEqual(geocheck.check(self.poly(square(139.0, 35.0)))["errors"], [])

    def test_unclosed_ring_is_an_error(self):
        self.assertIn("ring-not-closed", codes(geocheck.check(self.poly(square(139.0, 35.0)[:-1])), "errors"))

    def test_short_ring_is_an_error(self):
        self.assertIn("ring-too-short", codes(geocheck.check(self.poly([[139, 35], [139.1, 35], [139, 35]])), "errors"))

    def test_bow_tie_is_self_intersecting(self):
        ring = [[139.0, 35.0], [139.1, 35.1], [139.1, 35.0], [139.0, 35.1], [139.0, 35.0]]
        self.assertIn("self-intersection", codes(geocheck.check(self.poly(ring)), "errors"))

    def test_clockwise_exterior_is_a_warning(self):
        ring = list(reversed(square(139.0, 35.0)))
        self.assertIn("winding", codes(geocheck.check(self.poly(ring)), "warnings"))

    def test_large_rings_skip_the_intersection_test_with_a_warning(self):
        ring = [[139.0 + i * 1e-5, 35.0] for i in range(50)] + [[139.0, 35.01], [139.0, 35.0]]
        r = geocheck.check(self.poly(ring), max_ring_for_intersection=10)
        self.assertIn("intersection-skipped", codes(r, "warnings"))


class Properties(unittest.TestCase):
    def test_missing_required_property_is_an_error(self):
        r = geocheck.check(fc(point(139.77, 35.68, name="a"), point(139.7, 35.6)), require_props=["name"])
        self.assertIn("missing-property", codes(r, "errors"))

    def test_min_features(self):
        self.assertIn("too-few", codes(geocheck.check(fc(point(139.77, 35.68)), min_features=2), "errors"))


class Cli(unittest.TestCase):
    def run_cli(self, doc, *args):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "x.geojson"
            p.write_text(json.dumps(doc))
            return subprocess.run([sys.executable, "-I", str(pathlib.Path(geocheck.__file__)), str(p), *args],
                                  capture_output=True, text=True)

    def test_exit_status_follows_errors(self):
        self.assertEqual(self.run_cli(fc(point(139.77, 35.68))).returncode, 0)
        bad = self.run_cli(fc(point(35.68, 139.77)), "--expect-bbox", "122,20,154,46")
        self.assertEqual(bad.returncode, 1)
        self.assertEqual(json.loads(bad.stdout)["errors"][0]["code"], "swapped-lon-lat")

    def test_unreadable_json_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / "x.geojson"
            p.write_text("{not json")
            r = subprocess.run([sys.executable, "-I", str(pathlib.Path(geocheck.__file__)), str(p)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
