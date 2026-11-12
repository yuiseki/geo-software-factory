"""Shared by the evaluator-side checks. Only lines starting with OBSERVED: reach the implementer."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ["EVAL_BASE_URL"].rstrip("/")


def get(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=15) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        with e:
            return e.code, e.read()
    except (urllib.error.URLError, OSError):
        return None, b""


def features(path):
    status, body = get(path)
    if status != 200:
        print(f"OBSERVED: {path.split('?')[0]} の状態 {status}")
        return None
    try:
        doc = json.loads(body)
    except ValueError:
        print(f"OBSERVED: {path.split('?')[0]} の応答が JSON として読めない")
        return None
    if not isinstance(doc, dict) or doc.get("type") != "FeatureCollection":
        print("OBSERVED: 応答が FeatureCollection ではない")
        return None
    return doc.get("features", [])


def q(s):
    return urllib.parse.quote(s)
