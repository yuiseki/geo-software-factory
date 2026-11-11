# 探す｜今からほんや

- URL: https://imahon.jp/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS 5.6.0 |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | Supabase |
| 配信 | Cloudflare |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/planet/20261101_080013_pt/{z}/{x}/{y}.pbf`

メモ:

- 全国の本屋を探す地図。画面に「この範囲 8673 軒」と出た。店とイベントの情報は AI で集めており、確かめきれていないところがあるとサイトで説明している
- 店のデータは `/real/index.json` 1 本 (展開して 2.2 MB、転送 627 KB)、イベントは `/real/events.json`。MapLibre GL JS 5.6.0 を cdnjs から読む
- Supabase の `data_edits_live` を開くたびに呼んでいた。利用者からの修正の受け付けに使っていると見られる (推測)
