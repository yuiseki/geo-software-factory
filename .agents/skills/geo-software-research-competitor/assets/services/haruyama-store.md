---
financial: commercial
organization: corp-ent
---

# はるやま 店舗検索

- URL: https://haruyama.jp/cojp/shop_info/list
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、スーツ、紳士服、はるやま、P.S.FA、フォーエル、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 西日本を中心に展開する紳士服「はるやま」の店舗を一覧から探し、各店舗の地図や営業時間を確認できる公式店舗一覧・詳細サイト |
| 提供する価値 | 一覧ページから各店舗の住所・電話番号・Google マップリンクを確認でき、詳細ページでは埋め込み地図で所在地を把握できる |
| 想定する利用者 | スーツや礼服、ワイシャツ等の購入ではるやま店舗へ来店する一般客 |
| 商用か非商用か | 商用 (実店舗への来店送客および公式通販サイトとの連携として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗売上への送客に貢献する集客基盤 |
| 運営 | 企業 (はるやま商事株式会社 / 株式会社はるやまホールディングス) |
| 推定の運用費 | 推測: 月数万〜十数万円。Web サーバー運用費および Google Maps JavaScript API の利用料がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API および Google Maps 埋め込み `iframe` (店舗詳細ページ `/cojp/shop_info/detail/0252` 等にて `https://maps.googleapis.com/maps/api/js?key=...&callback=initMap` と `https://maps.google.co.jp/maps?output=embed&q=...` の両方を確認) |
| フレームワーク | jQuery 3.5.1 (`jquery-3.5.1.min.js`)、jQuery UI、jquery.cookie.js |
| 背景の地図とタイル | Google Maps (Maps JavaScript API および `output=embed` iframe 経由) |
| 投稿やデータの保存先 | 自社管理の店舗情報基盤 (`haruyama.jp/cojp/shop_info/list` および `/cojp/shop_info/detail/<店舗コード>`) |
| 配信 | Apache (`server: Apache`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、一覧ページ (`/cojp/shop_info/list`) には `http://maps.google.com/maps?q=...` の外部リンクのみが掲載されている一方、個別の店舗詳細ページ (`/cojp/shop_info/detail/0252` 等) には Google Maps の埋め込み地図が存在することを確認した (参考の事前調査では一覧ページベースで「埋め込み地図なし」と判定されていたと推測される)

データの出どころ (2026-11-17):

- 店舗データ: はるやま商事株式会社自社管理の店舗情報
- 背景地図: Google Maps Platform (Maps JavaScript API / Google Maps Embed)
