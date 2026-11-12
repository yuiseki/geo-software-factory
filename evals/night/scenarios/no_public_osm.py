"""no_public_osm.py: the page and the same-origin scripts and styles it loads name no public OSM server."""
import re
import sys

from _common import get

FORBIDDEN = ("tile.openstreetmap.org", "nominatim.openstreetmap.org", "overpass-api.de")
status, body = get("/")
if status != 200:
    print(f"OBSERVED: / の状態 {status}")
    sys.exit(1)
texts = [body]
for ref in re.findall(rb'(?:src|href)=["\']([^"\']+\.(?:js|css|json))["\']', body):
    ref = ref.decode(errors="replace")
    if ref.startswith(("http://", "https://", "//")):
        continue
    s, b = get("/" + ref.lstrip("./").lstrip("/"))
    if s == 200:
        texts.append(b)
found = sorted({h for h in FORBIDDEN for t in texts if h.encode() in t})
for h in found:
    print(f"OBSERVED: 画面が {h} を参照している")
sys.exit(1 if found else 0)
