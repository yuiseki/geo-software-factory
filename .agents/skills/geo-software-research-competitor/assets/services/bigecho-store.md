# ビッグエコー 店舗検索・Web予約

- URL: https://big-echo.jp/shop_search/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、ビッグエコー、BIG ECHO、カラオケ、第一興商、Web予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国のカラオケ ビッグエコー店舗を地図・エリア・設備条件から検索し、Web予約ができる公式店舗検索サービス |
| 提供する価値 | 都道府県や現在地周辺、DAM 機種やパーティールーム等の条件でビッグエコー店舗を探し、そのまま Web 予約や料金確認を行える |
| 想定する利用者 | 友人・職場の二次会や個人練習などでカラオケ店舗を探し、部屋予約を行いたい一般客 |
| 商用か非商用か | 商用 (ビッグエコー各店舗への集客および Web 予約促進のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。カラオケルーム利用料・飲食売上の送客に貢献 |
| 運営 | 企業 (株式会社第一興商) |
| 推定の運用費 | 推測: 月数十万円。GOGA の SaaS 型店舗検索システム「StoreLocator」の利用料と Google Maps JavaScript API の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.google.com/maps/api/js?v=quarterly&callback=onMapLoaded&libraries=places&geometry&region=JP&key=...` を `https://shop.big-echo.jp/` で使用) |
| フレームワーク | GOGA StoreLocator v2 (`https://storage.googleapis.com/storelocator-v2-static/cdn/jquery/...`) + jQuery 1.12.4 / 3.2.1 |
| 背景の地図とタイル | Google マップの地図タイル |
| 投稿やデータの保存先 | GOGA StoreLocator v2 店舗検索基盤 (`https://shop.big-echo.jp/`) |
| 配信 | `big-echo.jp` は Apache (`server: Apache`)、検索本体 `shop.big-echo.jp` は Google Frontend (`server: Google Frontend`) |

メモ:

- `https://big-echo.jp/shop_search/` が店舗検索の入口ページとなっており、都道府県別や地図検索の実体はサブドメイン `https://shop.big-echo.jp/` 側で動作している
- `shop.big-echo.jp` は株式会社ゴーガ (GOGA) の店舗検索 SaaS (`storelocator-v2-static`) 上で構築されており、Google Maps JavaScript API (Places・Geometry ライブラリ含む) を読み込んでいる

データの出どころ (2026-11-17):

- 店舗データ: 株式会社第一興商自社管理の店舗情報 (GOGA StoreLocator v2 経由で配信)
- 背景地図・ジオコーディング: Google Maps Platform
