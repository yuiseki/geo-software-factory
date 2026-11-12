#!/usr/bin/env python3
"""Deterministic checks for a GeoJSON file, so that a map is not judged correct by how it looks.

A map can look right while its coordinates are projected metres, latitude and longitude are
swapped, rings are open or cross themselves, or half the features fell outside the area. These
are decided by a program here, not by an LLM. Standard library only.

    python3 geocheck.py data.geojson [--expect-bbox W,S,E,N] [--require-props a,b]
                                     [--min-features N] [--allow-empty]

Prints a JSON report. Exit 0: no errors. Exit 1: errors. Exit 2: the file could not be read.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

GEOMETRY_DEPTH = {"Point": 0, "MultiPoint": 1, "LineString": 1, "MultiLineString": 2, "Polygon": 2, "MultiPolygon": 3}
WORLD = (-180.0, -90.0, 180.0, 90.0)
# Errors are listed in this order so that the most explanatory one comes first.
ORDER = ["bad-type", "bad-feature", "bad-geometry", "bad-position", "empty", "too-few", "swapped-lon-lat",
         "out-of-range", "outside-bbox", "ring-not-closed", "ring-too-short", "line-too-short",
         "self-intersection", "missing-property"]
MAX_EXAMPLES = 5


class Report:
    def __init__(self) -> None:
        self.found: dict[tuple[str, str], dict] = {}

    def add(self, level: str, code: str, message: str, where: str | None = None) -> None:
        f = self.found.setdefault((level, code), {"code": code, "message": message, "count": 0, "examples": []})
        f["count"] += 1
        if where is not None and len(f["examples"]) < MAX_EXAMPLES:
            f["examples"].append(where)

    def level(self, level: str) -> list[dict]:
        items = [f for (lv, _), f in self.found.items() if lv == level]
        return sorted(items, key=lambda f: ORDER.index(f["code"]) if f["code"] in ORDER else len(ORDER))


def inside(pos: tuple[float, float], box: tuple[float, float, float, float]) -> bool:
    return box[0] <= pos[0] <= box[2] and box[1] <= pos[1] <= box[3]


def is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def signed_area(ring: list[tuple[float, float]]) -> float:
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:])) / 2.0


def orient(a, b, c) -> int:
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_segment(a, b, p) -> bool:
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_cross(a, b, c, d) -> bool:
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and on_segment(a, b, c)) or (o2 == 0 and on_segment(a, b, d))
            or (o3 == 0 and on_segment(c, d, a)) or (o4 == 0 and on_segment(c, d, b)))


def ring_self_intersects(ring: list[tuple[float, float]]) -> bool:
    n = len(ring) - 1  # segments; the ring is closed
    for i in range(n):
        for j in range(i + 1, n):
            if j == i + 1 or (i == 0 and j == n - 1):
                continue  # neighbours share an end point
            if segments_cross(ring[i], ring[i + 1], ring[j], ring[j + 1]):
                return True
    return False


def check(doc, expect_bbox=None, require_props=(), min_features=0, allow_empty=False,
          max_ring_for_intersection=2000) -> dict:
    rep = Report()
    positions: list[tuple[tuple[float, float], str]] = []
    stats = {"features": 0, "null_geometries": 0}

    def walk_positions(coords, depth: int, where: str) -> list | None:
        if depth == 0:
            if not (isinstance(coords, list) and len(coords) in (2, 3) and all(is_number(v) for v in coords)):
                rep.add("errors", "bad-position", "A position must be 2 or 3 finite numbers [lon, lat(, z)].", where)
                return None
            pos = (float(coords[0]), float(coords[1]))
            positions.append((pos, where))
            return pos
        if not isinstance(coords, list):
            rep.add("errors", "bad-geometry", "Coordinates are not nested as the geometry type requires.", where)
            return None
        return [walk_positions(c, depth - 1, where) for c in coords]

    def check_ring(ring, where: str, exterior: bool) -> None:
        if any(p is None for p in ring):
            return
        if len(ring) < 4:
            rep.add("errors", "ring-too-short", "A polygon ring needs at least 4 positions.", where)
            return
        if ring[0] != ring[-1]:
            rep.add("errors", "ring-not-closed", "A polygon ring must end where it starts.", where)
            return
        area = signed_area(ring)
        if (exterior and area < 0) or (not exterior and area > 0):
            rep.add("warnings", "winding",
                    "RFC 7946 says exterior rings should be counterclockwise and holes clockwise.", where)
        if len(ring) > max_ring_for_intersection:
            rep.add("warnings", "intersection-skipped",
                    f"Ring longer than {max_ring_for_intersection} positions; self-intersection not tested.", where)
        elif ring_self_intersects(ring):
            rep.add("errors", "self-intersection", "A polygon ring crosses or touches itself.", where)

    def check_geometry(geom, where: str) -> None:
        if not isinstance(geom, dict) or "type" not in geom:
            rep.add("errors", "bad-geometry", "Geometry must be an object with a type.", where)
            return
        gtype = geom["type"]
        if gtype == "GeometryCollection":
            for i, g in enumerate(geom.get("geometries") or []):
                check_geometry(g, f"{where}/geometries[{i}]")
            return
        if gtype not in GEOMETRY_DEPTH or "coordinates" not in geom:
            rep.add("errors", "bad-geometry", f"Unknown geometry type or no coordinates: {gtype!r}.", where)
            return
        coords = walk_positions(geom["coordinates"], GEOMETRY_DEPTH[gtype], where)
        if coords is None:
            return
        if gtype == "LineString":
            if len(coords) < 2:
                rep.add("errors", "line-too-short", "A LineString needs at least 2 positions.", where)
        elif gtype == "MultiLineString":
            for line in coords:
                if line is not None and len(line) < 2:
                    rep.add("errors", "line-too-short", "A LineString needs at least 2 positions.", where)
        elif gtype in ("Polygon", "MultiPolygon"):
            polygons = [coords] if gtype == "Polygon" else coords
            for poly in polygons:
                for k, ring in enumerate(poly or []):
                    if ring is not None:
                        check_ring(ring, where, exterior=(k == 0))

    def check_feature(feat, where: str) -> None:
        if not isinstance(feat, dict) or feat.get("type") != "Feature" or "geometry" not in feat:
            rep.add("errors", "bad-feature", "A Feature needs type 'Feature' and a geometry member.", where)
            return
        stats["features"] += 1
        props = feat.get("properties") or {}
        for name in require_props:
            if props.get(name) in (None, ""):
                rep.add("errors", "missing-property", f"Property {name!r} is missing or empty.", where)
        if feat["geometry"] is None:
            stats["null_geometries"] += 1
        else:
            check_geometry(feat["geometry"], where)

    dtype = doc.get("type") if isinstance(doc, dict) else None
    if dtype == "FeatureCollection" and isinstance(doc.get("features"), list):
        for i, feat in enumerate(doc["features"]):
            check_feature(feat, f"features[{i}]")
        if not doc["features"] and not allow_empty:
            rep.add("errors", "empty", "The FeatureCollection has no features.")
    elif dtype == "Feature":
        check_feature(doc, "feature")
    elif dtype in GEOMETRY_DEPTH or dtype == "GeometryCollection":
        check_geometry(doc, "geometry")
    else:
        rep.add("errors", "bad-type", f"Not a GeoJSON object: type {dtype!r}.")

    crs_name = str(((doc.get("crs") or {}).get("properties") or {}).get("name", "")) if isinstance(doc, dict) else ""
    if isinstance(doc, dict) and "crs" in doc and not crs_name.endswith("CRS84"):
        rep.add("warnings", "crs-member",
                "A 'crs' member is present; RFC 7946 GeoJSON is always WGS 84 lon/lat, so the data may be projected.")
    if stats["features"] < min_features:
        rep.add("errors", "too-few", f"{stats['features']} features, fewer than the expected {min_features}.")

    target = tuple(expect_bbox) if expect_bbox else WORLD
    outside_bbox = 0
    for pos, where in positions:
        if pos == (0.0, 0.0):
            rep.add("warnings", "null-island", "A position is exactly (0, 0); often a missing value.", where)
        if inside(pos, target):
            continue
        if inside((pos[1], pos[0]), target):
            rep.add("errors", "swapped-lon-lat", "Swapping this position puts it inside the expected area; "
                    "GeoJSON order is [lon, lat].", where)
        elif not inside(pos, WORLD):
            rep.add("errors", "out-of-range", "Not in degrees (lon -180..180, lat -90..90); "
                    "projected metres or a different CRS?", where)
        else:
            outside_bbox += 1
            rep.add("errors", "outside-bbox", "Outside the expected bounding box.", where)

    lons = [p[0] for p, _ in positions]
    lats = [p[1] for p, _ in positions]
    return {
        "features": stats["features"],
        "null_geometries": stats["null_geometries"],
        "positions": len(positions),
        "bbox": [min(lons), min(lats), max(lons), max(lats)] if positions else None,
        "outside_bbox": outside_bbox,
        "errors": rep.level("errors"),
        "warnings": rep.level("warnings"),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--expect-bbox", help="W,S,E,N in degrees; positions outside are errors")
    ap.add_argument("--require-props", default="", help="comma-separated property names every feature must have")
    ap.add_argument("--min-features", type=int, default=0)
    ap.add_argument("--allow-empty", action="store_true")
    ap.add_argument("--max-ring-for-intersection", type=int, default=2000)
    args = ap.parse_args(argv)
    try:
        with open(args.path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError) as e:
        print(f"geocheck: cannot read {args.path}: {e}", file=sys.stderr)
        return 2
    box = tuple(float(v) for v in args.expect_bbox.split(",")) if args.expect_bbox else None
    if box is not None and len(box) != 4:
        ap.error("--expect-bbox needs four numbers W,S,E,N")
    report = check(doc, expect_bbox=box, require_props=[p for p in args.require_props.split(",") if p],
                   min_features=args.min_features, allow_empty=args.allow_empty,
                   max_ring_for_intersection=args.max_ring_for_intersection)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
