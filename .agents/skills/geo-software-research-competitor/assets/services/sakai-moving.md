# サカイ引越センター 支社検索

- URL: https://www.hikkoshi-sakai.co.jp/area/all.html
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、支社検索、拠点一覧、引越、引っ越し、サカイ引越センター、パンダ、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のサカイ引越センター支社を都道府県別に一覧表示し、各支社の詳細ページで所在地や地図を確認できる公式拠点検索ページ |
| 提供する価値 | 引越元や引越先の地域を担当する支社の連絡先や所在地を調べ、見積もり依頼や問い合わせにつなげられる |
| 想定する利用者 | 個人または法人の引越しで、地域の担当支社や所在地を確認したい利用者 |
| 商用か非商用か | 商用 (引越見積もり依頼および顧客問い合わせの導線として提供。利用料は無料) |
| 推定の売上 | 推測: 拠点検索単体の売上は 0 円。全国の引越受注および見積もり獲得に貢献する営業基盤 |
| 運営 | 企業 (株式会社サカイ引越センター) |
| 推定の運用費 | 推測: 月数万円程度。Amazon S3 + CloudFront による静的 HTML 配信費のみで、Maps Embed iframe 利用のため地図課金負担は小さい |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (支社詳細 `/area/hokkaido/detail/sapporo.html` にて `google.com/maps/embed?pb=...` の iframe 埋め込みを確認) |
| フレームワーク | 静的 HTML、独自 JS (`/js_v2/env.js`、`/assets_v2/js/common.js`)、MARS FLAG (`mf-search.js`) |
| 背景の地図とタイル | Google Maps (Maps Embed iframe) |
| 投稿やデータの保存先 | 自社静的サイト基盤 (Amazon S3 上の HTML) |
| 配信 | Amazon S3 + Amazon CloudFront (`x-amz-server-side-encryption: AES256`、`Via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 観測では、一覧ページ (`/area/all.html`) には地図がなく、各支社の詳細ページ (`/area/hokkaido/detail/sapporo.html` 等) で Google Maps iframe が埋め込まれていた
- レスポンスヘッダの `x-amz-server-side-encryption: AES256` と `Via: ...cloudfront.net` から、Amazon S3 をオリジンとした CloudFront 静的配信であることが確認できた

データの出どころ (2026-11-17):

- 店舗データ: 株式会社サカイ引越センター自社管理の支社情報
- 背景地図: Google Maps
