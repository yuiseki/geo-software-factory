---
financial: commercial
organization: corp-ent
---

# ニトリ 店舗検索

- URL: https://shop.nitori-net.jp/nitori/
- 観測した日: 2026-11-16
- 概要と収支を確かめた日: 2026-11-16
- 探すときの語: ストアロケーター、店舗検索、ニトリ、家具、インテリア、島忠、ホームズ、デコホーム、駐車場、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のニトリ・デコホーム・島忠ホームズ等の店舗をエリア・地図の中心・条件から検索できる公式店舗検索サイト |
| 提供する価値 | 地図の中心移動や条件絞り込みで近くの店舗を探し、駐車場・授乳室・バリアフリー設備やインテリア相談の対応状況、デジタルチラシまで確認できる |
| 想定する利用者 | 家具や日用品の購入でニトリ店舗へ来店したい一般客、車でのアクセスや駐車場・バリアフリー設備を事前に確認したい家族連れ |
| 商用か非商用か | 商用 (実店舗への来店送客と「ニトリネット」EC サイトとの相互送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および公式通販ニトリネットの売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社ニトリ。店舗検索システムはナビタイムジャパンの NAVITIME Location Cloud を利用) |
| 推定の運用費 | 推測: 月数万〜数十万円。NAVITIME Location Cloud の SaaS 利用料および地図・店舗検索 API の利用料がかかる |

## 技術 (2026-11-16 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | NAVITIME 地図 API (`//pkg.navitime.co.jp/nitori/api/map/tilemap`、`<div class="navitimeMap" id="w_7_detailmap_1_1-map">`) |
| フレームワーク | jQuery 3.7.1、Bootstrap 3.2.0、JsRender 1.0pre35、jQuery UI 1.14.1、Slick |
| 背景の地図とタイル | NAVITIME の地図タイル (`https://alttile.pkg.navitime.co.jp/map/`、`http://mars.navitime.co.jp/mars/tile/` などが `tilemap` スクリプト内に見えた) |
| 投稿やデータの保存先 | NAVITIME Location Cloud (`https://location-cloud.navitime.co.jp/`、フッターに Powered by NAVITIME の導線、`image.pkg.navitime.co.jp/citrus/88/` のアセット) |
| 配信 | Apache (`server: Apache`) |

メモ:

- ナビタイムジャパンの店舗情報プラットフォーム「NAVITIME Location Cloud」(旧称 Citrus 系のアセットパス `citrus/88/` が残る) 上に構築されている
- 地図の中心から検索 (`/nitori/spot/list/map`) や詳細ページで同じ NAVITIME の地図スクリプトを利用している

データの出どころ (2026-11-16):

- 店舗データ・店舗検索システム: 株式会社ニトリ / 株式会社ナビタイムジャパン (NAVITIME Location Cloud)
- 背景地図・タイル: 株式会社ナビタイムジャパン
