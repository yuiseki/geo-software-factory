"""Check /api/shelters count, properties, and CRS conversion accuracy."""
import math
import sys

from _common import get_json

status, doc = get_json("/api/shelters")
if doc is None or status != 200:
    print(f"OBSERVED: /api/shelters の状態が {status}")
    sys.exit(1)
fs = doc.get("features") or []
if len(fs) != 12:
    print(f"OBSERVED: 全件取得で {len(fs)} 件 (12 件必要)")
    sys.exit(1)
hit = [f for f in fs if (f.get("properties") or {}).get("name") == "上野公園避難所"]
if not hit:
    print("OBSERVED: 名称で引ける避難場所が足りない")
    sys.exit(1)
try:
    lon, lat = hit[0]["geometry"]["coordinates"][:2]
    d = math.hypot((lon - 139.7759) * 111320 * math.cos(math.radians(35.7143)), (lat - 35.7143) * 110540)
except (KeyError, TypeError, ValueError):
    print("OBSERVED: 地物の座標が読めない")
    sys.exit(1)
if d > 30:
    print(f"OBSERVED: 避難場所の座標が本来の位置から約 {round(d, -1):.0f} m ずれている")
    sys.exit(1)
