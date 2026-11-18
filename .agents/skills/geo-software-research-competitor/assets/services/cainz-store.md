---
financial: commercial
organization: corp-ent
---

# カインズ 店舗検索

- URL: https://map.cainz.com/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ホームセンター、カインズ、CAINZ、資材館、ペット、ドッグラン、工作室、店舗受取、営業時間、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のカインズ店舗を現在地・エリア・サービス設備（資材館・ドッグラン・工作室など）から検索し、地図上で位置や店舗詳細を確認できる公式店舗検索サイト |
| 提供する価値 | 店舗ごとの位置、営業時間、資材館やドッグラン・リフォームセンターなどの併設設備を確認でき、目的に合った店舗選びと来店・店舗受取に繋げられる |
| 想定する利用者 | カインズの利用客、DIY 資材や日用品の購入・店舗受取・施設利用のため最寄り店を探している利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客およびオンラインショップの店舗受取・サービス予約への導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および EC 店舗受取の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社カインズ) |
| 推定の運用費 | 推測: 月数万〜数十万円。Google Maps Platform の利用料、CloudFront + Next.js の運用費、店舗情報管理基盤 (Canly 等) の利用料がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (ブラウザ観測で確認。一次 HTTP 取得でも `has_gmaps: true` および `has_leaflet: true` を検出) |
| フレームワーク | Next.js (`x-powered-by: Next.js`、`/_next/static/chunks/...`)、Canly 関連記述あり |
| 背景の地図とタイル | Google マップ (Google Maps Platform) |
| 投稿やデータの保存先 | 自社管理または Canly 連携の店舗データベース (API 詳細は未確認) |
| 配信 | Amazon CloudFront (`via: ...cloudfront.net (CloudFront)`、`x-powered-by: Next.js`) |

メモ:

- 2026-11-16 のブラウザ観測で Google Maps を用いた地図表示を確認した
- 一次 HTTP 取得 (`https://map.cainz.com/`) では `x-powered-by: Next.js` と CloudFront 配信、`has_gmaps: true`・`has_leaflet: true`、および HTML 内の `canly` への言及が確認された
- 公式スマートフォンアプリとして「カインズアプリ」（会員証・店舗在庫確認・店内商品マップ・ポケットレジ・各種予約等）が提供されている

データの出どころ (2026-11-16):

- 店舗データ: 株式会社カインズ
- 背景地図: Google (Google Maps Platform)
