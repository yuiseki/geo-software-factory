"""geo_check.py <path> <count> <name> <lon> <lat>: exact count, and one known place within 30 m."""
import math
import sys

from _common import features

path, count, name, lon, lat = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
fs = features(path)
if fs is None:
    sys.exit(1)
ok = True
if len(fs) != count:
    print(f"OBSERVED: 全件の取得で {len(fs)} 件")
    ok = False
hit = [f for f in fs if (f.get("properties") or {}).get("name") == name]
if not hit:
    print("OBSERVED: 名称で引ける名所が足りない")
    sys.exit(1)
try:
    x, y = hit[0]["geometry"]["coordinates"][:2]
    d = math.hypot((x - lon) * 111320 * math.cos(math.radians(lat)), (y - lat) * 110540)
except (KeyError, TypeError, ValueError):
    print("OBSERVED: 地物の座標が読めない")
    sys.exit(1)
if d > 30:
    print(f"OBSERVED: 位置を知っている名所が、本来の位置から約 {round(d, -1):.0f} m ずれている")
    ok = False
sys.exit(0 if ok else 1)
