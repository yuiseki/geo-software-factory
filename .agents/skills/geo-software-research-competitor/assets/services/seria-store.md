---
financial: commercial
organization: corp-ent
---

# セリア 店舗検索

- URL: https://shop.seria-group.com/seria/top
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、セリア、Seria、100円ショップ、100均、ゼンリン、いつもNAVI、AreaMarker、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の 100円ショップ「Seria (セリア)」の店舗を地図やエリアから検索できる公式店舗検索サイト |
| 提供する価値 | 現在地周辺やエリア指定でセリア店舗を地図上で探し、住所、営業時間、大型店・小型店などの店舗属性を確認できる |
| 想定する利用者 | 日用品や手芸用品、インテリア雑貨などの購入で最寄りのセリア店舗を探す一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客のために株式会社セリアが提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。全国のセリア実店舗での売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社セリア) |
| 推定の運用費 | 推測: 月数万円〜十数万円。ゼンリンデータコムの法人向け店舗検索・地図 API (いつもNAVI API / AreaMarker) の利用料と Amazon S3 + CloudFront の配信費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | ゼンリンいつもNAVI API (`//api.its-mo.com/v3/loader?...&api=zdcmap.js,control.js,search.js,shape.js,userwidget.js,geo.js`) |
| フレームワーク | Angular (`runtime-es2015.js`、`polyfills-es2015.js`、`main-es2015.js`) |
| 背景の地図とタイル | ゼンリン地図 (ゼンリンデータコム いつもNAVI API / AreaMarker) |
| 投稿やデータの保存先 | ゼンリンデータコムの店舗検索 ASP / 自社管理の店舗データ (API 詳細は未確認) |
| 配信 | Amazon S3 + Amazon CloudFront (`server: AmazonS3`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得 (`https://shop.seria-group.com/seria/top`) ではステータス 200 を返し、Angular 製 SPA の HTML 内で `//api.its-mo.com/v3/loader` (`zdcmap.js` 等) を読み込んでいることを確認した
- 参考の事前調査でもゼンリン (AreaMarker) の採用が確認されている

データの出どころ (2026-11-17):

- 店舗データ: 株式会社セリア自社管理の店舗情報 (ゼンリン店舗検索 ASP 経由)
- 背景地図: 株式会社ゼンリン / 株式会社ゼンリンデータコム (いつもNAVI API)
