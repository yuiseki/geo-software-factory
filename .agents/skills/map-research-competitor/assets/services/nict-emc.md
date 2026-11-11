# 電界強度マップ - 電磁環境研究室モニタリングプロジェクト

- URL: https://emc.nict.go.jp/mnt/gis_map.html
- 観測した日: 2026-11-11
- 概要と収支を確かめた日: 2026-11-12

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 電測車で測った電界強度の結果を、メッシュごとに地図で公開する研究所のページ |
| 提供する価値 | 地域ごとの電波の強さの実測値を、詳細なデータまで確かめられる |
| 想定する利用者 | 電波や電磁環境の研究者と技術者 |
| 商用か非商用か | 非商用 (国の研究機関の公開) |
| 推定の売上 | なし (非商用) |
| 運営 | 公的機関 (国立研究開発法人 情報通信研究機構 NICT) |
| 推定の運用費 | 推測: サイトは月数千円規模 (Apache のサーバーと Esri のベースマップ)。主な費用は電測車での測定で、国の予算 |

## 技術 (2026-11-11 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 地図ライブラリの名前は見つからなかった |
| フレームワーク | React、Vue |
| 背景の地図とタイル | Esri (ArcGIS) のベースマップ |
| 投稿やデータの保存先 | 見えなかった |
| 配信 | Apache (配信先の事業者は不明) |

読み込んだタイルとスタイルの URL (一部):

- `https://basemaps.arcgis.com/arcgis/rest/services/World_Basemap_v2/VectorTileServer/tile/{z}/{x}/{y}.pbf`
- `https://cdn.arcgis.com/sharing/rest/content/items/97b0ea1cc8ca41028420dd4067873c53/resources/styles/root.json`
- `https://js.arcgis.com/5.2/esri/widgets/Legend/styles/support/relationshipUtils.js`
- `https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{x}/{y}`
- `https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{x}/{y}`
