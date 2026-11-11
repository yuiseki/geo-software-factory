# uMap - Online map creator

- URL: https://umap.hotosm.org/en/
- 観測した日: 2026-11-11

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet |
| フレームワーク | 見つからなかった |
| 背景の地図とタイル | OSM 財団の公開タイル、OpenStreetMap France のタイル、Esri (ArcGIS) のベースマップ、OpenTopoMap、自前のタイル (サイトと同じドメイン) |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | nginx/1.31.6 (配信先の事業者は不明) |

読み込んだタイルとスタイルの URL (一部):

- `https://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png%20https://b.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png`
- `https://c.tile.opentopomap.org/{z}/{x}/{y}.png`
- `https://services.arcgisonline.com/ArcGis/rest/services/World_Imagery/MapServer/tile/{z}/{x}/{y}.png`
- `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
- `https://titiler.hotosm.org/cog/tiles/WebMercatorQuad/{z}/{x}/{y}@1x`

メモ:

- 地図を作れるサービス。既定の背景として OSM France の HOT スタイル、OpenTopoMap、Esri などを選べる
