# スターバックス コーヒー ジャパン 店舗検索

- URL: https://store.starbucks.co.jp/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、カフェ、スターバックス、ドライブスルー、モバイルオーダー、営業時間、最寄駅、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のスターバックス店舗を、現在地・住所・最寄駅・設備条件から検索して地図上に表示する公式店舗検索サイト |
| 提供する価値 | 近くの店舗の位置や営業時間、ドライブスルーや Wi-Fi などの設備条件を素早く確認し、来店前の店舗選びができる |
| 想定する利用者 | スターバックスの店舗を探している一般客、外出先で最寄りの店舗や作業可能な店舗を探している利用者 |
| 商用か非商用か | 商用 (スターバックス店舗への来店送客とモバイルオーダー等への導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上およびモバイルオーダーへの送客に貢献する集客基盤 |
| 運営 | 企業 (スターバックス コーヒー ジャパン 株式会社) |
| 推定の運用費 | 推測: 月数万〜数十万円。CloudFront と AWS API Gateway の通信費に加え、NAVITIME の法人向け地図 API 利用料がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME 地図 API (`navitime.geo.Map`、`//dp.navitime.biz/v1/10354640/mapscript?host=store.starbucks.co.jp&signature=...`) |
| フレームワーク | Vue.js (`vue.develop.js`、`vue-router.js`、`axios.min.js`)、jQuery、Swiper |
| 背景の地図とタイル | NAVITIME の地図タイル (`https://alttile.pkg.navitime.co.jp/map/`、`http://mars.navitime.co.jp/mars/tile/` などが `mapscript` 内に見えた) |
| 投稿やデータの保存先 | 自社の店舗検索 API (`https://hn8madehag.execute-api.ap-northeast-1.amazonaws.com/prd-2019-08-21/storesearch`、Amazon CloudSearch 形式のクエリ構文) |
| 配信 | Amazon CloudFront (`server: CloudFront`) |

メモ:

- 店舗検索ページ上の地図表示には `navitime.geo.Map`、`navitime.geo.overlay.Pin`、`navitime.geo.overlay.InfoWindow` が使われている (`store_vue/js/navitime.js`、`store_vue/js/store.js`)
- 店舗一覧や設備ファセットの取得には AWS API Gateway 経由の検索 API (`index.vue.js`) が使われている

データの出どころ (2026-11-16):

- 店舗データ: スターバックス コーヒー ジャパン自社管理の店舗検索 API (`hn8madehag.execute-api.ap-northeast-1.amazonaws.com`)
- 背景地図・タイル: 株式会社ナビタイムジャパン (NAVITIME 地図 API / タイル配信)
