---
financial: commercial
organization: corp-smb
first_seen: 2006-08-13
first_seen_by: wayback
---

# GraphHopper

- URL: https://www.graphhopper.com
- ソース: https://github.com/graphhopper/graphhopper (Apache-2.0)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: GraphHopper、ルート検索、配送最適化、jsprit、Photon、OpenStreetMap、Apache-2.0、Directions API

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 高速なオープンソースの Java 製ルーティングエンジンと、配車・配送最適化・等時間圏 API を提供するドイツのルート検索プラットフォーム |
| 提供する価値 | 自動車・自転車・徒歩の高速な経路探索や配送ルート最適化 (VRP)、ジオコーディングを、Apache-2.0 の OSS セルフホストまたはクラウド API で利用できる |
| 想定する利用者 | 物流・配送事業者、モビリティアプリ開発者、アウトドア・地図アプリ開発者、経路最適化を組み込む企業 |
| 商用か非商用か | 商用 (OSS 版は Apache-2.0 で商用利用含め無料。クラウドの GraphHopper Directions API は非商用向けの無料枠あり、商用利用は月額プランの有料契約が必要) |
| 推定の売上 | 推測: 年数億円規模 (ドイツの GraphHopper GmbH がクラウド API、エンタープライズサポート、カスタム開発で収益化。非上場のため公式売上は非公開) |
| 運営 | 企業 (GraphHopper GmbH、ドイツ) |
| 推定の運用費 | 推測: 月数百万円規模。全世界の OSM 道路グラフと GTFS・標高データの高速更新パイプライン、クラウド API 群を維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | OpenLayers (ウェブ地図 `graphhopper.com/maps` の現行フロントエンドは React + OpenLayers。モバイル向けにオフライン・オンライン連携も可能) |
| フレームワーク | 公式サイト (`www.graphhopper.com`) は WordPress (`PHP/8.3.36`・`wp-content` を確認)。地図フロントエンド (`graphhopper-maps`) は React |
| 背景の地図とタイル | OpenStreetMap ベースの背景タイル |
| 投稿やデータの保存先 | 自前ルーティンググラフ (OSM `.osm.pbf` や SRTM 標高、GTFS から Java エンジンで高速構築) |
| 配信 | nginx (`server: nginx`、`x-powered-by: PHP/8.3.36` を応答ヘッダーで確認) |

メモ:

- 一般消費者向けの公式 iOS / Android アプリはないが、Java 製エンジンのため Android やオフライン環境への組み込み実績があり、MapLibre 等と組み合わせてモバイルアプリに利用される。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 道路ネットワーク | OpenStreetMap contributors (ODbL) | GitHub・公式サイト |
| 標高・公共交通 | SRTM 等の標高データ、GTFS 公共交通フィード | GitHub・公式サイト |
