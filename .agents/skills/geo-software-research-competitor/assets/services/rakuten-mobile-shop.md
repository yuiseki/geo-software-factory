---
financial: commercial
organization: corp-ent
first_seen: 2020-01-26
first_seen_by: wayback
---

# 楽天モバイルショップ 店舗検索

- URL: https://network.mobile.rakuten.co.jp/shop/
- 観測した日: 2026-11-17
- 概要と収支を確かめた日: 2026-11-17
- 探すときの語: ストアロケーター、店舗検索、楽天モバイル、Rakuten Mobile、携帯電話、来店予約、store locator

## どんなサービスか

| 項目 | 内容 |
|---|---|
| 一行で | 全国の楽天モバイルショップおよび取扱店を地図・現在地・エリアから検索し、店舗情報や来店予約へ進める公式店舗検索ページ |
| 提供する価値 | 地図上のクラスター表示や条件絞り込みにより近くの楽天モバイルショップを素早く見つけ、対応業務やキャンペーン情報を確認して来店予約できる |
| 想定する利用者 | 楽天モバイルの契約相談、SIM 受け取り、端末購入、サポート対応などで実店舗での対面案内を希望する利用者 |
| 商用か非商用か | 商用 (実店舗での契約獲得・来店予約促進のために提供。利用料は無料) |
| 推定の売上 | 推測: 店舗検索単体の売上は 0 円。実店舗での回線契約・端末販売および楽天経済圏への送客に貢献 |
| 運営 | 企業 (楽天モバイル株式会社) |
| 推定の運用費 | 推測: 月数十万〜数百万円。Web 配信・店舗検索基盤の運用費に加え、Google Maps JavaScript API (Places・Geometry ライブラリ含む) の従量課金がかかる |

## 技術 (2026-11-17 の観測)

| 項目 | 観測したもの |
|---|---|
| 描画 | Google Maps JavaScript API (`https://maps.googleapis.com/maps/api/js?key=...&libraries=places,geometry&callback=initMap`) および `markerclustererplus.min.js` |
| フレームワーク | jQuery 3.7.1 + 自社バンドル JS (`shop.index.bundle.js`, `search.common.bundle.js`, `vendor.bundle.js`) |
| 背景の地図とタイル | Google マップの地図タイル |
| 投稿やデータの保存先 | 自社店舗情報基盤 (`network.mobile.rakuten.co.jp/shop/`) |
| 配信 | 未確認 (`HTTP/1.1 200 OK`、`X-Cache-Status: EXPIRED` を確認したがサーバー・CDN 製品名は未出力) |

メモ:

- `/shop/` トップページ自体に Google Maps JavaScript API と `markerclustererplus` が読み込まれており、地図上での店舗ピン表示とクラスタリングを行っている

データの出どころ (2026-11-17):

- 店舗データ: 楽天モバイル株式会社自社管理の店舗情報
- 背景地図・ジオコーディング: Google Maps Platform
