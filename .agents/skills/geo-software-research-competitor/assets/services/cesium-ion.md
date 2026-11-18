---
financial: commercial
organization: corp-ent
---

# Cesium ion

- URL: https://ion.cesium.com
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: Cesium ion、Cesium、3D Tiles、Bentley Systems、デジタルツイン、点群、PLATEAU、WebGL、CesiumJS

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 大容量の 3D 地理空間データ（点群、BIM/CAD、フォトグラメトリ、地形）を 3D Tiles に変換して高速ストリーミング配信する SaaS プラットフォーム |
| 提供する価値 | ブラウザやゲームエンジン上で地球規模の 3D 空間や都市デジタルツインを滑らかに描画するためのデータ最適化・ホスティング・配信基盤を提供する |
| 想定する利用者 | 都市デジタルツイン開発者、建設・インフラ企業、航空宇宙・防衛分野、3D 地図アプリ開発者、研究者 |
| 商用か非商用か | 商用 (個人・非商用・評価向けの Community 無料プランあり。商用個人プランは月額約 $149 から、チーム・エンタープライズ・オンプレミス契約あり) |
| 推定の売上 | 推測: 年数十億円規模 (2024 年にインフラソフトウェア大手 Bentley Systems に買収され、Bentley iTwin Platform と統合されている。単体売上は非公開) |
| 運営 | 企業 (Cesium、米国。親会社は Bentley Systems, Incorporated) |
| 推定の運用費 | 推測: 月数千万円規模。3D Tiles の大容量変換パイプライン、AWS S3 + CloudFront によるグローバル 3D データストリーミングを維持している |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | CesiumJS (応答 HTML 内に `ThirdParty/cesium/Cesium.js` および `IonSdkGeometry.js` 等の読み込みを確認) |
| フレームワーク | 独自構成 (`main.js`、`dashboard-esm.js` による SPA 構成) |
| 背景の地図とタイル | Cesium World Terrain、Bing Maps 航空写真、Cesium OSM Buildings、Google Photorealistic 3D Tiles 連携 (`dev.virtualearth.net` を CSP ヘッダーで確認) |
| 投稿やデータの保存先 | Amazon S3 (`assets.ion.cesium.com` 等の S3 バケットへユーザーアップロードデータを変換・格納) |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net` を応答ヘッダーで確認) |

メモ:

- 一般消費者向けの単体モバイルアプリはないが、開発者向けにゲームエンジン経由で iOS / Android ネイティブアプリへ 3D Tiles を配信できる `Cesium for Unreal` / `Cesium for Unity` を提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 全球地形・3D 建物 | Cesium World Terrain、OpenStreetMap (Cesium OSM Buildings) | Cesium 公式サイト |
| 衛星・3D 都市モデル | Bing Maps、Google Maps Platform (Photorealistic 3D Tiles)、ユーザー投稿の点群・BIM・航空写真 | Cesium 公式サイト |
