# 焼肉きんぐ 店舗検索

- URL: https://www.yakiniku-king.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、焼肉、食べ放題、焼肉きんぐ、物語コーポレーション、営業時間、受付予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の焼肉きんぐ店舗を、エリア・現在地・地図から検索し、店舗情報や順番受付予約へ進める公式店舗検索サイト |
| 提供する価値 | 店舗の営業時間、設備、店舗位置を確認し、混雑回避のための順番受付や席予約へスムーズに進める |
| 想定する利用者 | 焼肉きんぐを利用したい一般客、家族連れやグループ客など |
| 商用か非商用か | 商用 (実店舗への来店送客および予約導線として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社物語コーポレーション) |
| 推定の運用費 | 推測: 月数万円〜十数万円。WordPress + CloudFront + 自社店舗 API サーバーの運用費および Google Maps API 利用料 |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`mcShop.umd.cjs` 内で `google.maps.importLibrary("maps")` および `AdvancedMarkerElement` を利用) |
| フレームワーク | WordPress (`wp-content/themes/king_basic_2024`) + jQuery 3.7.1 + 物語コーポレーション共通店舗検索モジュール (`https://shop.monogatari.co.jp/assets/js/mcShop.umd.cjs`) |
| 背景の地図とタイル | Google マップ |
| 投稿やデータの保存先 | 物語コーポレーション共通店舗 API (`https://local-common.monogatari.co.jp:8443/api/v1`) |
| 配信 | nginx + Amazon CloudFront (`server: nginx`、`via: 1.1 ...cloudfront.net (CloudFront)`) |

メモ:

- 2026-11-17 の一次 HTTP 取得で、`https://www.yakiniku-king.jp/shop/` は WordPress サイト上に共通店舗検索スクリプト `https://shop.monogatari.co.jp/assets/js/mcShop.umd.cjs` を組み込んでいることを確認した
- `mcShop.umd.cjs` の解析により、`google.maps.importLibrary("maps")` と `AdvancedMarkerElement` を用いた Google Maps JavaScript API 実装、および `https://local-common.monogatari.co.jp:8443/api/v1` との連携を確認した

データの出どころ (2026-11-17):

- 店舗データ: 株式会社物語コーポレーション
- 背景地図: Google (Google Maps JavaScript API の実装観測による)
