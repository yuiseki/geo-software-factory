# ArcGIS Online

- URL: https://www.arcgis.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ArcGIS Online、Esri、Web GIS、空間解析、クラウド GIS、Field Maps、ArcGIS Maps SDK、デジタルツイン

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ブラウザ上で地図の作成・共有、空間データの管理・解析、フィールド調査アプリとの連携を行える Esri のクラウド型 Web GIS プラットフォーム |
| 提供する価値 | 専門的な GIS 解析機能や豊富な統計・地理データ、組織内の権限管理、2D/3D 可視化、現地調査モバイルアプリとの同期をクラウド上で一元運用できる |
| 想定する利用者 | 自治体・政府機関、インフラ・建設・不動産・小売企業、大学・研究機関、GIS 専門家、ArcGIS 開発者 |
| 商用か非商用か | 商用 (組織向けの User Type 別年間サブスクリプション課金、および ArcGIS Location Platform による無料枠付きの従量課金モデルを提供) |
| 推定の売上 | 約 13 億米ドル規模 (非上場企業 Esri 全体の年間売上は業界分析で $1.1B〜$1.3B 超と報じられている。ArcGIS Online 単体の売上は非公開) |
| 運営 | 企業 (Environmental Systems Research Institute, Inc. / Esri、米国) |
| 推定の運用費 | 推測: 年数百億円規模。世界中の官公庁・企業向けに高可用な GIS クラウド、空間解析サーバー、大量のベースマップと衛星画像を配信している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | ArcGIS Maps SDK for JavaScript (応答 HTML 内に `ArcGIS` の記述および `./js/app/config.js`・`./js/app/build/main.js` を確認) |
| フレームワーク | 独自構成 (`./js/app/build/main.js` によるアプリバンドル) |
| 背景の地図とタイル | Esri Basemaps (Living Atlas of the World 等) |
| 投稿やデータの保存先 | ArcGIS Online ホステッドフィーチャーレイヤー等のクラウド GIS ストレージ |
| 配信 | ArcGIS Online サーバー + Amazon CloudFront (`server: ArcGIS Online`、`via: ...cloudfront.net` を応答ヘッダーで確認) |

メモ:

- ウェブ版と連携する公式 iOS / Android アプリ（ArcGIS Field Maps、ArcGIS Survey123 等）が提供されている（利用には組織アカウントが必要）。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| ベースマップ・Living Atlas | Esri 独自整備データ、公的統計・政府機関データ、商用衛星画像プロバイダ、OpenStreetMap 等 | ArcGIS 公式サイト |
