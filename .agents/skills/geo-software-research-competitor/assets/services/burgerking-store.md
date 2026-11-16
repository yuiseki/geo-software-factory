# バーガーキング 店舗検索

- URL: https://www.burgerking.co.jp/store
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ハンバーガー、ファストフード、バーガーキング、BURGER KING、営業時間、モバイルオーダー、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のバーガーキング店舗を、地域・条件・地図から検索できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の住所、営業時間、ドライブスルーやモバイルオーダー対応などを確認し、来店や注文へ進める |
| 想定する利用者 | バーガーキングを利用したい一般客、テイクアウトやデリバリーを探す人 |
| 商用か非商用か | 商用 (実店舗への来店送客およびモバイルオーダー導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗およびモバイルオーダーの売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社ビーケージャパンホールディングス) |
| 推定の運用費 | 推測: 月数万円〜十数万円。CloudFront + nginx の運用費および Google Maps API 利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (`/js/app.js` 内に `VUE_APP_GOOGLE_MAP_API_KEY` を保持。事前調査: Google Maps) |
| フレームワーク | Vue.js (`/js/chunk-vendors.js`, `/js/app.js`) + bizMOB (`bizMOB-core.js` 等) |
| 背景の地図とタイル | Google マップ |
| 投稿やデータの保存先 | 自社 API (SPA 構成、詳細は未確認) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: 1.1 ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://www.burgerking.co.jp/store` は CloudFront + nginx から配信される Vue.js + bizMOB の SPA であることを確認した
- `/js/app.js` 内に `VUE_APP_GOOGLE_MAP_API_KEY` が含まれており、Google Maps を利用していることを確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社ビーケージャパンホールディングス
- 背景地図: Google (事前調査および `VUE_APP_GOOGLE_MAP_API_KEY` の観測による)
