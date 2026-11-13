"""Shared helpers for tokyo-evacuation scenarios."""
import json
import os
import urllib.error
import urllib.request

BASE = os.environ["EVAL_BASE_URL"].rstrip("/")


def get(path: str):
    try:
        with urllib.request.urlopen(BASE + path, timeout=5) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, OSError):
        print("OBSERVED: サーバーに接続できない")
        return None, None


def get_json(path: str):
    status, body = get(path)
    if body is None:
        return status, None
    try:
        return status, json.loads(body)
    except ValueError:
        print(f"OBSERVED: {path} が正しい JSON ではない")
        return status, None
