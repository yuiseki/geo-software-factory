---
financial: non-commercial
organization: individual
---

# OpenRailwayMap

- URL: https://www.openrailwaymap.org
- ソース: https://github.com/OpenRailwayMap/OpenRailwayMap (GPL-3.0)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: OpenRailwayMap、鉄道地図、路線図、信号、最高速度、電化方式、OpenStreetMap、Leaflet、ベクタタイル

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の鉄道インフラ（線路、信号機、最高速度、電化方式、軌間など）を OpenStreetMap データから詳細に可視化する専門地図サービス |
| 提供する価値 | 通常の地図では省略されがちな鉄道の運転保安装置、分岐器、速度制限、電化方式、廃線跡などの専門情報を専用レイヤーを切り替えて確認できる |
| 想定する利用者 | 鉄道ファン、鉄道・交通研究者、OpenStreetMap の鉄道マッパー、交通計画担当者 |
| 商用か非商用か | 非商用 (ボランティアが余暇で維持する非営利プロジェクト。FOSSGIS e.V. 経由の寄付等で運営。公開タイルは小規模・非商用向けの公平利用ポリシー) |
| 推定の売上 | なし (非商用プロジェクト・寄付ベース) |
| 運営 | コミュニティ・非営利支援 (OpenRailwayMap コミュニティ有志、FOSSGIS e.V. による寄付・インフラ支援) |
| 推定の運用費 | 推測: 月数万円〜十数万円規模。OSM 鉄道データの抽出・タイル生成サーバーをコミュニティと FOSSGIS の支援で維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet (および OpenLayers 参照) (応答 HTML 内に `js/leaflet.js`、`js/Leaflet.EditInOSM.js`、`js/L.TileLayer.Grayscale.js` および `openlayers` 文字列を確認) |
| フレームワーク | バニラ JavaScript (`js/search.js`、`js/functions.js`、`js/bitmap-map.js` 等のスクリプト構成) |
| 背景の地図とタイル | 自前の鉄道オーバーレイタイル + グレースケール化した背景地図タイル |
| 投稿やデータの保存先 | 自前 DB なし (OpenStreetMap 本体のデータを参照し、鉄道事業者の補助リストは GitHub 上で管理) |
| 配信 | Apache/2.4.71 (Debian) (`server: Apache/2.4.71 (Debian)` を応答ヘッダーで確認) |

メモ:

- 公式の単体 iOS / Android アプリはないが、OsmAnd 等のサードパーティ地図アプリにオーバーレイタイルとして組み込んで利用できる。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 鉄道インフラ・路線 | OpenStreetMap contributors (ODbL) | 公式サイト・GitHub リポジトリ |
| 鉄道事業者リスト等 | OpenRailwayMap/railway-operators (CC0 1.0) | GitHub リポジトリ |
