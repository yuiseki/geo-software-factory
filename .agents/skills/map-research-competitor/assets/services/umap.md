# uMap - Online map creator

- URL: https://umap.hotosm.org/en/
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12
- 探すときの語: 地図作成、マイマップ、OSM、埋め込み、人道支援、HOT

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | OpenStreetMap のレイヤーの上に点、線、面を置いて、自分の地図を作ってサイトに埋め込める地図作成サービス (HOT が運営するインスタンス) |
| 提供する価値 | 登録して数分で、データの読み込みとライセンスの指定までした地図を作って共有できる |
| 想定する利用者 | 人道支援や防災、教育、公共の分野で地図を作る人と団体 |
| 商用か非商用か | 非商用 (オープンソースの uMap を、非営利の Humanitarian OpenStreetMap Team が運営。広告、有料プランは見えなかった) |
| 推定の売上 | なし (非商用。HOT は寄付と助成で運営されている団体) |
| 運営 | 団体 (Humanitarian OpenStreetMap Team) |
| 推定の運用費 | 推測: 月数万円。nginx のサーバーと地図のデータベース、自前のタイル。背景には OSM 財団や OSM France の公開タイルも使う |

## 技術 (2026-11-11 の観測)

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

データの出どころ (地図の帰属表示と画面の最下部 500 字、2026-11-12):

- フッターに「uMap An OpenStreetMap project」「Hosted by Humanitarian OpenStreetMap Team」。背景のタイルの帰属表示は、各地図の画面に出る (トップページでは見ていない)
