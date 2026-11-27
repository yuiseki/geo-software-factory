---
financial: public-service
organization: gov-central
first_seen: 2012-03-13
first_seen_by: wayback
---

# USGS Earthquake Map

- URL: https://earthquake.usgs.gov/earthquakes/map/
- ソース: https://github.com/usgs/earthquake-eventpages (関連ウェブアプリのオープンソース公開)
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: USGS、アメリカ地質調査所、地震マップ、Latest Earthquakes、震源、マグニチュード、GeoJSON、MapLibre、Leaflet

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 世界中の最新地震の震源・マグニチュード・深さ・揺れの広がりをリアルタイムで地図表示するアメリカ地質調査所 (USGS) の公式サービス |
| 提供する価値 | 発生直後の地震情報や断層・プレート境界・ShakeMap (揺れの強さ分布) を高精度かつ高速に確認でき、GeoJSON フィードも無償で利用できる |
| 想定する利用者 | 地震学者、防災機関、報道機関、一般市民、地震通知アプリや防災マップの開発者 |
| 商用か非商用か | 非商用 (米国政府機関 USGS による公的サービス。閲覧・GeoJSON API ともに無料、データはパブリックドメイン) |
| 推定の売上 | 0 円 (連邦政府予算による運営であり、商業売上はない) |
| 運営 | 政府機関 (アメリカ地質調査所 USGS / 米国連邦政府内務省 DOI) |
| 推定の運用費 | 推測: 政府予算による運用 (USGS Earthquake Hazards Program の一部として維持されており、単独の運用費は非公開) |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Leaflet / MapLibre / ArcGIS (2026-11-16 の `main-UGTHROUD.js` 解析で `maplibre`、`leaflet`、`arcgis` の参照を検出) |
| フレームワーク | Angular (ビルドされた `polyfills-*.js` と `main-*.js` の構成、および USGS 公式 GitHub の Angular 実装を確認) |
| 背景の地図とタイル | ArcGIS / Esri 系のベースマップおよびプレート境界・断層レイヤー等 (`main-UGTHROUD.js` 内の `arcgis` 参照と整合) |
| 投稿やデータの保存先 | USGS の地震カタログ・GeoJSON フィード基盤 (Did You Feel It? 等の体感報告も収集) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: ... cloudfront.net`、`x-cache: Hit from cloudfront` を応答ヘッダーで確認) |

メモ:

- 公式の専用モバイルアプリは提供していないが、モバイルブラウザ対応の Web アプリと、世界中の開発者が利用する標準 GeoJSON フィードを提供している。

データの出どころ:

| データ | 出どころ | どこに書いてあるか |
|---|---|---|
| 地震・震源・ShakeMap | USGS National Earthquake Information Center (NEIC) および提携地震観測網 | 公式サイトおよび API ドキュメント |
| 体感震度データ | 一般利用者からの「Did You Feel It?」投稿 | 公式サイト |
