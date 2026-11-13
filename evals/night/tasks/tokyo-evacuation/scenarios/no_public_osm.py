"""Check that HTML and linked JS do not refer to public OSM servers."""
import re
import sys

from _common import get

FORBIDDEN = ("tile.openstreetmap.org", "nominatim.openstreetmap.org", "overpass-api.de")
_, html = get("/")
if html is None:
    sys.exit(1)
texts = [html]
for m in re.finditer(r"""<script[^>]+src=["']([^"']+)["']""", html, re.I):
    src = m.group(1)
    if src.startswith("/"):
        _, js = get(src)
        if js:
            texts.append(js)
for host in FORBIDDEN:
    if any(host in t for t in texts):
        print(f"OBSERVED: 画面またはスクリプトに禁止した公開サーバー名 ({host}) が含まれている")
        sys.exit(1)
