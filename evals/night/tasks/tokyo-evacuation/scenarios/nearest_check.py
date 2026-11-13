"""Check /api/nearest returns correct shelter and geodesic distance_m."""
import sys

from _common import get_json

status, doc = get_json("/api/nearest?lon=139.7774&lat=35.7138&safe_only=true")
if doc is None or status != 200:
    print(f"OBSERVED: /api/nearest の状態が {status}")
    sys.exit(1)
shelter = doc.get("shelter") or {}
name = (shelter.get("properties") or {}).get("name")
dist = doc.get("distance_m")
if name != "上野公園避難所":
    print(f"OBSERVED: 最寄り避難場所が {name!r} になった")
    sys.exit(1)
if not isinstance(dist, (int, float)) or not (100 <= dist <= 200):
    print(f"OBSERVED: distance_m={dist!r} が実際の測地距離 (約 147 m) と合っていない")
    sys.exit(1)
