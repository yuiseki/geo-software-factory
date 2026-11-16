# 安楽亭 店舗検索

- URL: https://anrakutei.jp/map/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、焼肉、食べ放題、安楽亭、営業時間、駐車場、クーポンの利用、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 首都圏を中心に展開する焼肉レストラン安楽亭の店舗を、エリアや条件から検索できる公式店舗検索サイト |
| 提供する価値 | 最寄り店舗の営業時間、駐車場、宴会や食べ放題の対応状況、店舗位置を確認し、来店や予約へ進める |
| 想定する利用者 | 安楽亭を利用したい一般客、家族連れやドライバーなど |
| 商用か非商用か | 商用 (実店舗への来店送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社安楽亭) |
| 推定の運用費 | 推測: 月数万円。WordPress (Apache / PHP) + CloudFront の運用費および Google Maps API 利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | 未確認 (事前調査: Google Maps。トップページ `/map/` の一次 HTTP 取得では地図ライブラリを直接特定できず) |
| フレームワーク | WordPress (`wp-content/themes/anrakutei`) + jQuery 3.6.1 / jQuery UI 1.12.1 + `asset/js/map.js` |
| 背景の地図とタイル | 未確認 (事前調査では Google Maps) |
| 投稿やデータの保存先 | WordPress データベース (詳細は未確認) |
| 配信 | Apache (`PHP/7.4.30`) + Amazon CloudFront (`via: 1.1 ...cloudfront.net (CloudFront)`、`x-cache: Hit from cloudfront`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://anrakutei.jp/map/` は WordPress (`anrakutei` テーマ) + CloudFront で配信され、jQuery / jQuery UI と `/wp-content/themes/anrakutei/asset/js/map.js` を読み込んでいることを確認した
- トップページの一次 HTTP 取得では Google Maps スクリプトの直接読み込みは観測されず、詳細ページ側での埋め込み方式は未確認

データの出どころ (2026-11-17):

- 店舗データ: 株式会社安楽亭
- 背景地図: Google (事前調査による。一次 HTTP 取得では未確認)
