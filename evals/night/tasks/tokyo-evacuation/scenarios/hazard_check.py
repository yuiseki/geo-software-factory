"""Check point-in-polygon filtering: safe_only=true excludes inside-polygon shelters, keeps outside-polygon ones."""
import sys

from _common import get_json

status, doc = get_json("/api/shelters?safe_only=true")
if doc is None or status != 200:
    print(f"OBSERVED: /api/shelters?safe_only=true の状態が {status}")
    sys.exit(1)
names = {(f.get("properties") or {}).get("name") for f in (doc.get("features") or [])}
if "浅草寺境内広場" in names or "蔵前小学校" in names:
    print("OBSERVED: 浸水想定区域内の避難場所が safe_only=true に含まれている")
    sys.exit(1)
if "元浅草防災広場" not in names:
    print("OBSERVED: 浸水想定区域外の避難場所が safe_only=true から誤って除外されている (bbox 判定の疑い)")
    sys.exit(1)
if len(names) != 8:
    print(f"OBSERVED: safe_only=true の件数が {len(names)} 件 (期待 8 件)")
    sys.exit(1)
