# ゴミ箱マップ | 街中のゴミ箱情報をシェアしよう！

- URL: https://gomibako-map.com/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet |
| フレームワーク | WordPress |
| 背景の地図とタイル | OSM 財団の公開タイル、Mapbox の API への通信 (用途は未確認) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | nginx (配信先の事業者は不明) |

読み込んだタイルとスタイルの URL (一部):

- `https://a.tile.osm.org/{z}/{x}/{y}.png`
- `https://b.tile.osm.org/{z}/{x}/{y}.png`
- `https://c.tile.osm.org/{z}/{x}/{y}.png`

メモ:

- 背景は `tile.osm.org` (OSM 財団の公開タイルの別名) を Leaflet で読む
