"""Check input validation (400 instead of 500) and HTML escaping."""
import sys
import urllib.parse

from _common import get

for path in (
    "/api/nearest?lon=999&lat=35.71",
    "/api/nearest?lon=abc&lat=35.71",
    "/api/shelters?q=" + ("a" * 600),
):
    status, _ = get(path)
    if status != 400:
        print(f"OBSERVED: 不正または過大な入力に対して状態 {status} を返した (400 が必要)")
        sys.exit(1)

status, body = get("/?q=" + urllib.parse.quote("<script>alert(1)</script>"))
if status != 200 or body is None:
    print(f"OBSERVED: トップページの状態が {status}")
    sys.exit(1)
if "<script>alert(1)</script>" in body:
    print("OBSERVED: クエリの <script> がそのまま HTML に反射されている")
    sys.exit(1)
