---
financial: commercial
organization: corp-ent
first_seen: 2023-03-08
first_seen_by: wayback
---

# サンドラッグ 店舗検索 (所在地を探す)

- URL: https://sundrug-online.com/tools/locations
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ドラッグストア、サンドラッグ、SUNDRUG、調剤薬局、Mapbox、Shopify、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のサンドラッグ店舗を地図・現在地・地名検索から探し、店舗ごとの所在地や距離を確認できる公式オンラインストア内の店舗検索ページ |
| 提供する価値 | Shopify 上のオンラインストアと統合された地図画面から、現在地周辺や指定エリア内のサンドラッグ店舗を直感的に探せる |
| 想定する利用者 | サンドラッグの実店舗を探している一般客、処方箋受付や日用品購入のため最寄り店舗を探している利用者 |
| 商用か非商用か | 商用 (実店舗および公式オンラインストアへの送客として提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗および EC サイト (`sundrug-online.com`) の売上に貢献する集客基盤 |
| 運営 | 企業 (株式会社サンドラッグ) |
| 推定の運用費 | 推測: 月数万円。Shopify ストアアプリの利用料および Mapbox GL JS / Mapbox Geocoder の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Mapbox GL JS (`mapbox-gl-CN72erkz.js`、`mapbox-gl-language/v1.0.0`、`mapbox-gl-rtl-text/v0.2.3`、`.mapboxgl-map`、`.mapboxgl-ctrl-geocoder`) |
| フレームワーク | Shopify Storefront (`cdn.shopify.com`、`prod-sundrug.myshopify.com`) + jQuery 3.5.0 + Pagination.js |
| 背景の地図とタイル | Mapbox (`mapbox://styles/mapbox/streets-v11`、`defaultLanguage: 'ja'`) |
| 投稿やデータの保存先 | Shopify App Proxy (`/tools/locations`) 経由の店舗ロケーションデータ (`window.baseVariables.map_settings` に設定を埋め込み) |
| 配信 | Cloudflare (`server: cloudflare`、`cf-ray: ...-NRT`) |

メモ:

- 2026-11-17 の HTTP 観測では、HTML 内の `dns-prefetch` に `maps.googleapis.com` も記載されているが、実際の地図ウィジェットは Mapbox GL JS と `mapbox://styles/mapbox/streets-v11` スタイルで構成されていることを確認した
- 日本語表示のために `mapbox-gl-language` プラグイン (`defaultLanguage: 'ja'`) と `mapbox-gl-rtl-text` を読み込んでいる

データの出どころ (2026-11-17):

- 店舗データ: 株式会社サンドラッグ
- 背景地図・ジオコーディング: Mapbox (Mapbox GL JS)
