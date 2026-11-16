# ブックオフ 店舗検索

- URL: https://www.bookoff.co.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ブックオフ、BOOKOFF、古本、買取、中古、店舗一覧、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の BOOKOFF (ブックオフ) 店舗を地域や取扱商品から検索し、各店舗の地図や買取・販売情報を確認できる公式店舗検索ページ |
| 提供する価値 | 最寄りの店舗の住所、営業時間、駐車場の有無、取扱商材、店舗詳細ページ上の案内地図とルート検索リンクをまとめて確認できる |
| 想定する利用者 | 古本、ゲーム、CD、家電、トレカなどの購入や店頭買取を希望する一般客 |
| 商用か非商用か | 商用 (実店舗への来店および買取送客のためにブックオフグループが提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の買取・販売売上および店頭受取サービスに貢献する集客基盤 |
| 運営 | 企業 (ブックオフコーポレーション株式会社 / ブックオフグループホールディングス株式会社) |
| 推定の運用費 | 推測: 月数万円〜十数万円。Amazon CloudFront による配信費および店舗詳細ページでの Google Maps Embed API 利用に伴う運用費がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 店舗詳細ページにて iframe 埋め込み (`https://www.google.com/maps/embed/v1/place?key=...`) および `maps.google.com/maps?daddr=...` への外部ルート検索リンク |
| フレームワーク | jQuery (`jquery-1.7.1.min.js`)、独自検索スクリプト (`/shop/js/shop.js`、`jquery.searchshop-common.js`) |
| 背景の地図とタイル | Google Maps (Maps Embed API) |
| 投稿やデータの保存先 | 自社管理の店舗情報基盤 (API 詳細は未確認) |
| 配信 | Amazon CloudFront + Apache (`server: Apache`、`via: ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で `https://www.bookoff.co.jp/shop/` はステータス 200 を返し、個別店舗ページ (`https://www.bookoff.co.jp/shop/shop20500.html`) に Google Maps Embed API の iframe と Google マップのルート検索リンクが埋め込まれていることを確認した

データの出どころ (2026-11-17):

- 店舗データ: ブックオフコーポレーション株式会社自社管理の店舗情報
- 背景地図: Google Maps (Maps Embed API)
