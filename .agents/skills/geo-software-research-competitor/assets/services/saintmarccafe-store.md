---
financial: commercial
organization: corp-ent
first_seen: 2022-12-26
first_seen_by: wayback
---

# サンマルクカフェ 店舗検索

- URL: https://www.saint-marc-hd.com/saintmarccafe/search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、カフェ、ベーカリーカフェ、サンマルクカフェ、チョコクロ、営業時間、Wi-Fi、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | ベーカリーカフェ「サンマルクカフェ」の店舗を地図や条件・地域から検索できる公式店舗検索サイト |
| 提供する価値 | 地図上のピンやクラスタ、エリア・条件絞り込みで近くのサンマルクカフェを探し、営業時間や設備を確認してルート案内へ進める |
| 想定する利用者 | サンマルクカフェへ来店したい一般客、Wi-Fi や喫煙席など条件に合うカフェを探す利用者 |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客導線 |
| 運営 | 企業 (株式会社サンマルクカフェ / 株式会社サンマルクホールディングス) |
| 推定の運用費 | 推測: 月数万〜十数万円。CloudFront + Apache の運用費に加え、Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`react-google-maps`、`markerclusterer` を `search.bundle.js` 内にバンドル) |
| フレームワーク | React 17.0.2 (`react.production.min.js`、`react-dom.production.min.js`、`search.bundle.js`) |
| 背景の地図とタイル | Google Maps (`https://maps.googleapis.com/maps/api/js`) |
| 投稿やデータの保存先 | サンマルクホールディングス管理の店舗情報データ |
| 配信 | Apache + Amazon CloudFront (`server: Apache`, `via: CloudFront`, `x-cache: Hit from cloudfront`) |

メモ:

- 店舗数は全国約 285〜290 店舗
- Google マップアプリ連携用の外部リンク (`https://www.google.com/maps/search/?api=1&query=...`) もバンドル内に含まれている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社サンマルクホールディングス
- 背景地図: Google Maps Platform
