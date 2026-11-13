"""Reference app for tokyo-evacuation: plane IX -> WGS84, point-in-polygon, haversine nearest, input guards."""
import csv
import html
import http.server
import json
import math
import os
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"
if not DATA_DIR.is_dir():
    DATA_DIR = HERE.parent / "task" / "data"

BREAK = os.environ.get("REF_BREAK", "none")


def _to_wgs84(x_north: float, y_east: float) -> tuple[float, float]:
    try:
        from pyproj import Transformer
        t = Transformer.from_crs("EPSG:6677", "EPSG:4326", always_xy=True)
        return t.transform(y_east, x_north)
    except ImportError:
        # Fallback for environments without pyproj (accurate to <5m around Tokyo EPSG:6677 origin 36N, 139d50mE)
        lat0 = 36.0
        lon0 = 139.0 + 50.0 / 60.0
        scale = 0.9999
        lat = lat0 + (x_north / scale) / 110955.0
        lon = lon0 + (y_east / scale) / (111320.0 * math.cos(math.radians(lat)))
        return lon, lat


def _point_in_ring(lon: float, lat: float, ring: list[list[float]]) -> bool:
    inside = False
    n = len(ring)
    for i in range(n - 1):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[i + 1][0], ring[i + 1][1]
        if (y1 > lat) != (y2 > lat):
            x_int = (x2 - x1) * (lat - y1) / (y2 - y1) + x1
            if lon < x_int:
                inside = not inside
    return inside


def _in_hazard(lon: float, lat: float, polygons: list[list[list[float]]]) -> bool:
    if BREAK == "bbox":
        for ring in polygons:
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            if min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys):
                return True
        return False
    return any(_point_in_ring(lon, lat, ring) for ring in polygons)


def _haversine_m(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_data():
    hz_doc = json.loads((DATA_DIR / "hazard_zones.geojson").read_text(encoding="utf-8"))
    polygons = []
    for feat in hz_doc.get("features", []):
        geom = feat.get("geometry") or {}
        if geom.get("type") == "Polygon":
            polygons.append(geom["coordinates"][0])
    shelters = []
    with open(DATA_DIR / "shelters.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            x, y = float(row["x"]), float(row["y"])
            lon, lat = _to_wgs84(y, x) if BREAK == "swap" else _to_wgs84(x, y)
            shelters.append({
                "type": "Feature",
                "properties": {
                    "id": row["id"],
                    "name": row["name"],
                    "ward": row["ward"],
                    "capacity": int(row["capacity"]),
                    "wheelchair": row["wheelchair"].lower() == "true",
                    "in_hazard": _in_hazard(lon, lat, polygons),
                },
                "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]},
            })
    return shelters


SHELTERS = load_data()


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send_body(self, status: int, body: str, ctype: str):
        b = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _filter(self, qs: dict[str, list[str]]):
        q = qs.get("q", [""])[0]
        if BREAK != "guard" and len(q) > 500:
            return None
        fs = list(SHELTERS)
        if q:
            fs = [f for f in fs if q in f["properties"]["name"]]
        if qs.get("wheelchair", [""])[0].lower() == "true":
            fs = [f for f in fs if f["properties"]["wheelchair"]]
        if qs.get("safe_only", [""])[0].lower() == "true":
            fs = [f for f in fs if not f["properties"]["in_hazard"]]
        return fs

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        qs = urllib.parse.parse_qs(u.query)
        if u.path == "/":
            q_val = qs.get("q", [""])[0]
            rendered_q = q_val if BREAK == "guard" else html.escape(q_val, quote=True)
            osm = "\n<!-- https://tile.openstreetmap.org/{z}/{x}/{y}.png -->" if BREAK == "osm" else ""
            body = (
                "<!doctype html><meta charset='utf-8'><title>台東区 浸水時避難場所マップ</title>"
                f"<input id='q' value='{rendered_q}'><div id='map'></div>"
                f"<p>避難場所データ: 評価用 (CC0)</p>{osm}"
            )
            return self.send_body(200, body, "text/html; charset=utf-8")

        if u.path == "/api/shelters":
            fs = self._filter(qs)
            if fs is None:
                return self.send_body(400, json.dumps({"error": "q too long"}), "application/json")
            return self.send_body(200, json.dumps({"type": "FeatureCollection", "features": fs}, ensure_ascii=False),
                                  "application/geo+json")

        if u.path == "/api/nearest":
            try:
                lon = float(qs["lon"][0])
                lat = float(qs["lat"][0])
            except (KeyError, ValueError, IndexError):
                if BREAK == "guard":
                    return self.send_body(500, json.dumps({"error": "bad"}), "application/json")
                return self.send_body(400, json.dumps({"error": "invalid coordinates"}), "application/json")
            if BREAK != "guard" and not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0):
                return self.send_body(400, json.dumps({"error": "out of range"}), "application/json")
            fs = self._filter(qs)
            if fs is None:
                return self.send_body(400, json.dumps({"error": "q too long"}), "application/json")
            if not fs:
                return self.send_body(404, json.dumps({"error": "no matching shelter"}), "application/json")
            scored = []
            for f in fs:
                flon, flat = f["geometry"]["coordinates"]
                d = (abs(flon - lon) + abs(flat - lat)) if BREAK == "nearest" else _haversine_m(lon, lat, flon, flat)
                scored.append((d, f))
            scored.sort(key=lambda item: item[0], reverse=(BREAK == "nearest"))
            dist, best = scored[0]
            return self.send_body(200, json.dumps({"shelter": best, "distance_m": round(dist, 1)}, ensure_ascii=False),
                                  "application/json")

        self.send_body(404, json.dumps({"error": "not found"}), "application/json")


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8787))), Handler).serve_forever()
