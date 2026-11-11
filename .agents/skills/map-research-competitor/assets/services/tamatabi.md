# 世界のライブカメラ地図｜いま見れるライブ映像 - たま旅ライブ

- URL: https://tamatabi.world/ja/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | MapLibre GL JS 4.7.1、D3 |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OpenFreeMap |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Vercel |

読み込んだタイルとスタイルの URL (一部):

- `https://tiles.openfreemap.org/styles/dark`

メモ:

- 世界のライブカメラを地図で見るサービス。カメラは YouTube の埋め込み
- カメラのデータは `/api/livecams` 1 本 (展開して 8.7 MB、転送 1.3 MB)。配信中かを確かめた時刻 (`checkedAt`) が数分前になっていた
- MapLibre GL JS 4.7.1 と OpenFreeMap の dark スタイルのほか、d3-geo と topojson で Natural Earth の陸地 (`land-50m.json`) を点で描いている
