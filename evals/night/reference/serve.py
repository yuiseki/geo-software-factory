"""Reference app for evals/night: converts data/places.csv (plane IX, X = northing) once and serves it."""
import csv
import http.server
import json
import os
import urllib.parse
from pathlib import Path

from pyproj import Transformer

HERE = Path(__file__).parent
SWAP = os.environ.get("REF_BREAK") == "swap"          # broken variants, to check that the scenarios fail
TILES = os.environ.get("REF_BREAK") == "osm"
SEARCH = os.environ.get("REF_BREAK") == "search"

to_wgs = Transformer.from_crs("EPSG:6677", "EPSG:4326", always_xy=True)
FEATURES = []
with open(HERE / "data" / "places.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        x, y = float(row["X"]), float(row["Y"])
        lon, lat = to_wgs.transform(x, y) if SWAP else to_wgs.transform(y, x)
        FEATURES.append({"type": "Feature", "properties": {"name": row["名称"], "kind": row["種別"]},
                         "geometry": {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]}})

PAGE = """<!doctype html><meta charset="utf-8"><title>台東区の名所マップ</title>
<input id="q" placeholder="名前で絞り込む"><div id="map" style="height:80vh"></div>
<p>地点データ: 評価用 (CC0)</p><script src="app.js"></script>"""
APP = "fetch('/places.geojson').then(r => r.json()).then(d => console.log(d.features.length));" + (
    "\n// https://tile.openstreetmap.org/{z}/{x}/{y}.png" if TILES else "")


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, body, ctype):
        b = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        if u.path == "/":
            return self.send(PAGE, "text/html; charset=utf-8")
        if u.path == "/app.js":
            return self.send(APP, "text/javascript")
        if u.path == "/places.geojson":
            q = urllib.parse.parse_qs(u.query).get("q", [""])[0]
            fs = [f for f in FEATURES if q in f["properties"]["name"]] if not SEARCH else FEATURES[:3]
            return self.send(json.dumps({"type": "FeatureCollection", "features": fs}, ensure_ascii=False),
                             "application/geo+json")
        self.send_error(404)


http.server.ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", 8787))), H).serve_forever()
