---
financial: commercial
organization: corp-ent
---

# マクドナルド 店舗検索

- URL: https://map.mcdonalds.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、マクドナルド、ファストフード、ドライブスルー、24時間営業、マックカフェ、朝マック、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 日本全国の日本マクドナルド店舗を現在地・キーワード・設備条件から検索し、地図とルート案内を確認できる公式店舗検索サイト |
| 提供する価値 | 24 時間営業、ドライブスルー、マックカフェ、Wi-Fi、駐車場などの条件で絞り込み、最寄り店舗までの経路をその場で確認できる |
| 想定する利用者 | マクドナルドを利用したい一般客、ドライブスルーや深夜営業の店舗を探しているドライバーや歩行者 |
| 商用か非商用か | 商用 (店舗への来店送客とモバイルオーダー等への導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗およびデリバリー・モバイルオーダーの売上に貢献する集客基盤 |
| 運営 | 企業 (日本マクドナルド株式会社) |
| 推定の運用費 | 推測: 月数十万〜数百万円。Google Maps Platform (Dynamic Maps / Geocoding / Directions API) の従量課金と、CloudFront 配信・検索 API のサーバー費がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`//maps.google.com/maps/api/js?v=quarterly&libraries=geometry&key=...&region=JP`、`google.maps.Map`、`Geocoder`、`DirectionsService`、`DirectionsRenderer`) |
| フレームワーク | jQuery 1.9.1、Underscore.js、Backbone.js (`geolocation-marker.js`、`infobox.js` を併用) |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 自社の店舗検索 API (`./api/poi`、`../api/neighborhood/{key}`、`../api/stations/{key}`) |
| 配信 | Amazon CloudFront + nginx (`server: nginx`、`via: ...cloudfront.net`) |

メモ:

- 地図上の店舗検索だけでなく、`Geocoder` や `DirectionsService` / `DirectionsRenderer` を用いたルート検索機能も同一の Google Maps JavaScript API で実装している
- テンプレート描画には Underscore.js のテンプレート (`#infobox-template`、`#map-result-template`) を使用している

データの出どころ (2026-11-16):

- 店舗・最寄駅・周辺情報データ: 日本マクドナルド自社 API (`./api/poi` 等)
- 背景地図・ジオコーディング・ルート検索: Google (Google Maps Platform)
