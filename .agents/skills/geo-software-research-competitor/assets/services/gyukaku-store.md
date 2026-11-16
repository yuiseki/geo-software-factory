# 牛角 店舗検索

- URL: https://map.reins.co.jp/gyukaku
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、焼肉、牛角、レインズインターナショナル、営業時間、食べ放題、予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の焼肉「牛角」店舗を、エリア・駅・現在地・条件から検索できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の営業時間、メニュー・食べ放題プラン、店舗位置を確認し、来店や席予約へ進める |
| 想定する利用者 | 牛角を利用したい一般客、友人や家族との外食先を探す人 |
| 商用か非商用か | 商用 (実店舗への来店送客および予約導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社レインズインターナショナル / コロワイドグループ) |
| 推定の運用費 | 推測: 月数万円〜十数万円。Apache + CloudFront の運用費および Google Maps API 利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps (HTML 内に `maps.googleapis.com` への参照を確認。事前調査: Google Maps) |
| フレームワーク | jQuery (`/js/gyu/app.js`, `/js/gyu/pages/search_top.js`) |
| 背景の地図とタイル | Google マップ |
| 投稿やデータの保存先 | 自社店舗検索システム (`map.reins.co.jp`、詳細は未確認) |
| 配信 | Apache + Amazon CloudFront (`server: Apache`、`via: 1.1 ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://map.reins.co.jp/gyukaku` は Apache + CloudFront から配信され、jQuery ベースのフロントエンド (`/js/gyu/app.js`) と `maps.googleapis.com` への参照を含むことを確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社レインズインターナショナル
- 背景地図: Google (事前調査および `maps.googleapis.com` 参照の観測による)
