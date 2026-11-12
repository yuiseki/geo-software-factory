"""search_check.py <query> <expected count>: every returned name contains the query, and the count matches."""
import sys

from _common import features, q

query, expected = sys.argv[1], int(sys.argv[2])
fs = features(f"/places.geojson?q={q(query)}")
if fs is None:
    sys.exit(1)
names = [(f.get("properties") or {}).get("name", "") for f in fs]
wrong = [n for n in names if query not in n]
if wrong:
    print(f"OBSERVED: 絞り込みの結果に、名前に合わないものが {len(wrong)} 件ある")
if len(names) != expected:
    print(f"OBSERVED: 絞り込みの結果が {len(names)} 件")
sys.exit(0 if not wrong and len(names) == expected else 1)
